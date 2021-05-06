from os import path, remove

import requests
from OpenSSL import crypto
import tempfile

import json
from enum import Enum
import sys
import time

import importlib

LOCALHOST = True

def __default_keystore_path():
    keystore_paths = \
        [path.expanduser('~/.ecfeed/localhost.p12'), path.expanduser('~/ecfeed/localhost.p12')] if LOCALHOST else \
        [path.expanduser('~/.ecfeed/security.p12'), path.expanduser('~/ecfeed/security.p12')]    
    for keystore_path in keystore_paths:
        if path.exists(keystore_path):
            return keystore_path
    return keystore_path

DEFAULT_GENSERVER = 'https://localhost:8090' if LOCALHOST else 'https://develop-gen.ecfeed.com'
DEFAULT_KEYSTORE_PATH = __default_keystore_path()
DEFAULT_KEYSTORE_PASSWORD = 'changeit'

class EcFeedError(Exception):
    pass

class TemplateType(Enum):
    """Built-in export templates
    """

    CSV = 1
    XML = 2
    Gherkin = 3
    JSON = 4
    RAW = 99

    def __str__(self):
        return self.name

def parse_template(template):
    if template == str(TemplateType.CSV): return TemplateType.CSV
    elif template == str(TemplateType.JSON): return TemplateType.JSON
    elif template == str(TemplateType.Gherkin): return TemplateType.Gherkin
    elif template == str(TemplateType.XML): return TemplateType.XML
    elif template == str(TemplateType.RAW): return TemplateType.RAW
    return None

DEFAULT_TEMPLATE = TemplateType.CSV

class DataSource(Enum):
    STATIC_DATA = 0
    NWISE = 1
    PAIRWISE = 2
    CARTESIAN = 3
    RANDOM = 4

    def __repr__(self):
        return self.to_url_param()

    def to_url_param(self):
        if self == DataSource.STATIC_DATA:
            return 'static'
        if ((self == DataSource.NWISE) or \
            (self == DataSource.PAIRWISE)):
            return 'genNWise'
        if self == DataSource.CARTESIAN:
            return 'genCartesian'
        if self == DataSource.RANDOM:
            return 'genRandom'

    def to_feedback_param(self):
        if self == DataSource.STATIC_DATA:
            return 'Static'
        if ((self == DataSource.NWISE) or \
            (self == DataSource.PAIRWISE)):
            return 'NWise'
        if self == DataSource.CARTESIAN:
            return 'Cartesian'
        if self == DataSource.RANDOM:
            return 'Random'

class TestProvider:
    '''Access provider to ecFeed remote generator services

    ...
    Attributes
    ----------
    model : str
        Id of the accessed model. Must be accessible for user 
        owning the keystore file.        
    '''

    model = ''

    def __init__(self, genserver=DEFAULT_GENSERVER, 
                 keystore_path=DEFAULT_KEYSTORE_PATH, 
                 password=DEFAULT_KEYSTORE_PASSWORD,
                 model=None):
        '''
        Parameters
        ----------
        genserver : str
            url to ecFeed generator service (default is 'gen.ecfeed.com')

        keystore_path : str
            path to keystore file with user and server certificates 
            (default is '~/.ecfeed.security.p12' on windows and 
            '~/.ecfeed.security.p12' otherwise)

        password : str
            password to keystore (default is 'changeit')

        model : str
            id of the default model used by generators

        '''
        self.genserver = genserver      
        self.model = model
        self.keystore_path = path.expanduser(keystore_path)
        self.password = password    

    def generate(self, **kwargs):
        """Generic call to ecfeed generator service

        Parameters
        ----------
        method : str, required
            Full name (including full class path) of the method that 
            will be used for generation. 

            Method parameters are not required. If parameters are not
            provided, the generator will generate data from the first 
            method it finds with that name

        data_source : str, required
            The way how generator service will obtain the data. In general
            it may define the generator type (nwise, random, etc.) or pre-generated
            test suite.

            For convenience, the enum DataSource may be used, For other generators,
            added to generator service after this code was written, a string with 
            generator name may be used. Always up-to-date documentation can be found
            at www.ecfeed.com

        model : str
            Id of the model that will be used for generation. If not provided, 
            the model defined in class constructor will be used

        properties : dictionary
            A dictionary defining the parameters of the generation. The content 
            depends of the data_source used (see documentation at www.ecfeed.com). 
            
        choices : dictionary
            The keys in the dictionary are names of method parameters. The values define
            list of choices that will be used for these parameters in the generation. 
            If an argument is skipped in the dictionary, all defined choices will be used
            For example: choices={'arg1' : [choice1, choice2], 'arg2' : [choice3]}

        constraints : list
            List of constraints used for the generation. If not provided, all constraints 
            will be used, to ignore all constraints set the value to 'NONE'

        template : TemplateType
            Template to be used when exporting data to text. If set to None
            data will be casted to argument type

        raw_output : if set to True works the same as template = None

        Yields
        -------
            If a template was not provided, the function yields tuples of values casted
            to types defined by the signature of the function used for the generation. 
            If a template was provided, the function yields lines of the exported data
            according to the template 

        Raises
        ------
        EcFeedError
            If the generator service resposes with error
        """
        
        config = self.__configuration_init()

        self.__configuration_update_main(config, **kwargs)

        request = RequestHelper.prepare_request_data(self.genserver, config)
        
        if (kwargs.pop('url', None)):
            yield request
            return

        self.__configuration_update_additional(config, **kwargs)

        try:
            response = RequestHelper.process_request(request, config['config']['certificate'])

            for line in response.iter_lines(decode_unicode=True):
                line = line.decode('utf-8')

                test_case = None

                if ((config['config']['template'] != None) or config['config']['rawOutput']) and (config['testSessionId'] is None):
                    yield line
                elif ((config['config']['template'] != None) or config['config']['rawOutput']):
                    test_case = [str(line)]
                else:
                    test_data = self.__response_parse_line(line=line) 
                    self.__response_parse_test_session_id(config, test_data)
                    self.__response_parse_timestamp(config, test_data)
                    self.__response_parse_method_info(config, test_data)
                    self.__response_parse_method(config, test_data)
                    test_case = self.__response_parse_values(config, test_data)
                
                if test_case is not None:
                    yield self.__response_parse_test_case(line, config, test_case)

        except:
            RequestHelper.certificate_remove(config['config']['certificate'])
            
    def __configuration_init(self):

        return {
            'config' : {}
        }

    def __configuration_update_main(self, config, **kwargs):

        update = self.__configuration_init()

        data_source = self.__configuration_get_data_source(**kwargs)
        raw_output = self.__configuration_get_raw_output(**kwargs)
        template = self.__configuration_get_template(**kwargs)

        update = {
            'config' : {
                'template' : template,
                'rawOutput' : raw_output,
                'dataSource' : data_source,
                'properties' : kwargs.pop('properties', None)
            },
            'modelId' : self.__configuration_get_model(**kwargs),
            'methodInfo' : self.__configuration_get_method(**kwargs),
            'generatorType' : data_source.to_feedback_param(),
            'testSuites' : kwargs.pop('test_suites', None),
            'constraints' : kwargs.pop('constraints', None),
            'choices' : kwargs.pop('choices', None),
        }

        update['config'].update(config['config'])
        config.update(update)

    def __configuration_update_additional(self, config, **kwargs):
        
        update = self.__configuration_init()

        update = {
            'config' : {
                'summaryCurrent' : 0,
                'testIndex' : 0,
                'certificate' : RequestHelper.certificate_load(self.keystore_path, self.password),
                'feedbackFlag' : kwargs.pop('feedback', False),
                'argsInfo' : {}
            },
            'testSessionId' : None,
            'framework' : 'Python',
            'timestamp' : None,
            'generatorOptions' : self.__parse_dictionary(kwargs.pop('properties', None)),
            'testSessionLabel' : kwargs.pop('label', None),
            'custom' : kwargs.pop('custom', None),
            'testResults' : {}
        }

        update['config'].update(config['config'])
        config.update(update)

    def __configuration_get_model(self, **kwargs):

        model = kwargs.pop('model', None)

        if (model == None):
            model = self.model

        return model

    def __configuration_get_method(self, **kwargs):
        
        try:
            return kwargs.pop('method')
        except KeyError:
            raise EcFeedError("The 'method' argument is not defined.")

    def __configuration_get_data_source(self, **kwargs):

        try:
            return kwargs.pop('data_source')
        except KeyError:
            raise EcFeedError(f"The 'data_source' argument is not defined.")

    def __configuration_get_raw_output(self, **kwargs):

        return True if ('raw_output' in kwargs or kwargs.get('template', None) == TemplateType.RAW) else False

    def __configuration_get_template(self, **kwargs):
        template = kwargs.pop('template', None)

        if template == TemplateType.RAW: 
            template = None

        return template

    def __response_parse_test_session_id(self, config, test_data):
        if 'test_session_id' in test_data:
            if config['config']['feedbackFlag'] is True: 
                self.__feedback_append(config, ['testSessionId'], test_data['test_session_id'])

    def __response_parse_timestamp(self, config, test_data):
        if 'timestamp' in test_data:
            self.__feedback_append(config, ['timestamp'], test_data['timestamp'])

    def __response_parse_method_info(self, config, test_data):
        if 'method_info' in test_data:
            self.__feedback_append(config, ['methodInfo'], test_data['method_info'])

    def __response_parse_method(self, config, test_data):
        if 'method' in test_data:
            config['config']['argsInfo'] = test_data['method']
    
    def __response_parse_values(self, config, test_data):
        if 'values' in test_data:
            return [self.__cast(value) for value in list(zip(test_data['values'], [arg[0] for arg in config['config']['argsInfo']['args']]))]
        else:
            return None

    def __response_parse_test_case(self, line, config, test_case):
        self.__feedback_append(config, ['testResults', ('0:' + str(config['config']['testIndex'])), 'data'], line)

        if (config['testSessionId'] is not None):
            test_case.append({'config' : config, 'id' : ('0:' + str(config['config']['testIndex'])) })

        config['config']['testIndex'] += 1

        return test_case
    
    def __parse_dictionary(self, dictionary):

        if dictionary == None:
            return None

        parsed = ''

        for key in dictionary:
            parsed += key + '=' + dictionary[key] + ', '

        parsed = parsed[:-2]

        return parsed
        
    def __feedback_append(self, config, path, element, condition=True):

        if not condition:
            return

        for i in range(len(path) - 1):
            if path[i] not in config:
                config[path[i]] = {}
            config = config[path[i]]

        config[path[-1]] = element

    def __feedback_process(self, config):

        cert = config['config']["certificate"].copy()

        del config['config']

        config = {k: v for k, v in config.items() if v is not None}

        RequestHelper.process_request(RequestHelper.prepare_request_feedback(self.genserver), cert, json.dumps(config))
        RequestHelper.certificate_remove(cert)

    def generate_nwise(self, **kwargs): 
        return self.nwise(template=None, **kwargs)

    def export_nwise(self, **kwargs): 
        return self.nwise(template=kwargs.pop('template', DEFAULT_TEMPLATE), **kwargs)

    def generate_pairwise(self, **kwargs): 
        return self.nwise(n=kwargs.pop('n', 2), template=None, **kwargs)

    def export_pairwise(self, **kwargs): 
        return self.nwise(n=kwargs.pop('n', 2), template=kwargs.pop('template', DEFAULT_TEMPLATE), **kwargs)

    def nwise(self, **kwargs):
        """A convenient way to call nwise generator. 

        Parameters
        ----------
        method : str
            See 'generate'

        n : int
            The 'N' in NWise

        coverage : int
            The percent of N-tuples that the generator will try to cover. 

        template : str
            See 'generate'            

        choices : dictionary
            See 'generate'                         

        constraints : dictionary
            See 'generate'                         

        model : str
            See 'generate'                         

        """

        properties={}
        properties['n'] = str(kwargs.pop('n', 2))
        properties['coverage'] = str(kwargs.pop('coverage', 100))
        kwargs['properties'] = properties

        yield from self.generate(data_source=DataSource.NWISE, **kwargs)

    def generate_cartesian(self, **kwargs): return self.cartesian(template=None, **kwargs)

    def export_cartesian(self, **kwargs): return self.cartesian(template=kwargs.pop('template', DEFAULT_TEMPLATE), **kwargs)

    def cartesian(self, **kwargs):
        """Calls cartesian generator

        Parameters
        ----------
        method : str
            See 'generate'

        template : str
            See 'generate'            

        choices : dictionary
            See 'generate' 

        constraints : dictionary
            See 'generate' 

        model : str
            See 'generate'                         

        """

        properties={}
        properties['coverage'] = str(kwargs.pop('coverage', 100))

        yield from self.generate(data_source=DataSource.CARTESIAN, **kwargs)

    def generate_random(self, **kwargs): return self.random(template=None, **kwargs)

    def export_random(self, **kwargs): return self.random(template=kwargs.pop('template', DEFAULT_TEMPLATE), **kwargs)

    def random(self, **kwargs):
        """Calls random generator

        Parameters
        ----------
        method : str
            See 'generate'        

        length : int
            Number of test cases to generate

        adaptive : boolean
            If set to True, the generator will try to maximize the Hamming distance
            of each generate test case from already generated tests

        template : str
            See 'generate'            

        choices : dictionary
            See 'generate' 

        constraints : dictionary
            See 'generate' 

        model : str
            See 'generate'                         
        """

        properties={}
        properties['adaptive'] = str(kwargs.pop('adaptive', True)).lower()
        properties['duplicates'] = str(kwargs.pop('duplicates', False)).lower()
        properties['length'] = str(kwargs.pop('length', 1))

        yield from self.generate(data_source=DataSource.RANDOM, properties=properties, **kwargs)

    def generate_static_suite(self, **kwargs): return self.static_suite(template=None, **kwargs)

    def export_static_suite(self, **kwargs): return self.static_suite(template=kwargs.pop('template', DEFAULT_TEMPLATE), **kwargs)

    def static_suite(self, **kwargs):
        """Calls generator service for pre-generated data from test suites

        Parameters
        ----------
        method : str
            See 'generate'        

        template : str
            See 'generate'           

        test_suites : list
            A list of test suites that shall be requested

        model : str
            See 'generate'                         

        """

        yield from self.generate(data_source=DataSource.STATIC_DATA, **kwargs)

    def method_info(self, method, model=None):
        """Queries generator service for information about the method

        Parameters
        ----------
        method : str
            Queried method        

        model : str
            Model id of the model where the method is defined

        Returns
        -------
        A dictionary with following entries:
            package_name: the package of the method, eg. com.example
            class_name: full name of the class, where the method is defined, e.g com.example.TestClass
            method_name: full name of the method. Repeated from the argument
            args: list of tuples containing type and name of arguments, eg. [[int, arg1], [String, arg2]]                           
        """

        info={}
        for line in self.generate_random(method=method, length=0, raw_output=True, model=model, feedback=False):
            line = line.replace('"{', '{').replace('}"', '}').replace('\'', '"')#fix wrong formatting in some versions of the gen-server

            try:                
                parsed = json.loads(line)
            except ValueError as e:
                print('Unexpected problem when getting method info: ' + str(e))
            if 'info' in parsed :
                try:
                    method_name = parsed['info']['method']
                    info = self.__parse_method_definition(method_name)
                except TypeError as e:
                    pass
        return info
 
    def method_arg_names(self, method_info=None, method_name=None):
        """Returns list of argument names of the method

        Parameters
        ----------
        method_info : dict
            If provided, the method parses this dictionary for names of the methid arguments

        method_name : str
            If method_info not provided, this function first calls method_info(method_name), 
            and then recursively calls itself with the result

        Returns
        -------
        List of method argument names
        """

        if method_info != None:
            return [i[1] for i in method_info['args']]
        elif method_name != None:
            return self.method_arg_names(self.method_info(method=method_name))

    def method_arg_types(self, method_info=None, method_name=None):
        """Returns list of argument types of the method

        Parameters
        ----------
        method_info : dict
            If provided, the method parses this dictionary for names of the methid arguments

        method_name : str
            If method_info not provided, this function first calls method_info(method_name), 
            and then recursively calls itself with the result

        Returns
        -------
        List of method argument types
        """
        
        if method_info != None:
            return [i[0] for i in method_info['args']]
        elif method_name != None:
            return self.method_arg_types(self.method_info(method=method_name))

    def test_header(self, method_name, feedback=False):
        header = self.method_arg_names(method_name=method_name)

        if feedback:
            header.append("test_id")
        
        return header

    def feedback(self, test_id, status, duration=None, comment=None, custom=None):     
        
        test_suite = test_id["config"]
        test_case = test_suite["testResults"][test_id["id"]]

        if "status" in test_case:
            return comment

        test_case["status"] = "P" if status else "F"
        
        if duration:
            test_case["duration"] = duration
        if comment:
            test_case["comment"] = comment
        if custom:
            test_case["custom"] = custom

        test_suite['config']["summaryCurrent"] += 1

        if (test_suite['config']["summaryCurrent"] == test_suite['config']["testIndex"]):
            self.__feedback_process(test_suite)

        return comment

    def __response_parse_line(self, line):
        result = {}

        try:
            parsed_line = json.loads(line)
        except ValueError as e:
            print('Unexpected error while parsing line: "' + line + '": ' + str(e))
        
        if 'info'  in parsed_line:
            info = parsed_line['info'].replace('\'', '"')
            try:
                json_parsed = json.loads(info)
                result['timestamp'] = int(json_parsed['timestamp'])
                result['test_session_id'] = json_parsed['testSessionId']
                result['method_info'] = json_parsed['method']
                result['method'] = self.__parse_method_definition(result['method_info'])
            except (ValueError, KeyError) as e:
                pass
        elif 'testCase' in parsed_line:
            try:
                result['values'] = [arg['value'] for arg in parsed_line['testCase']]
            except ValueError as e:
                print('Unexpected error when parsing test case line: "' + line + '": ' + str(e))

        return result

    def __parse_method_definition(self, method_info_line):
        result={}
        full_method_name = method_info_line[0:method_info_line.find('(')]
        method_args = method_info_line[method_info_line.find('(')+1:-1]
        full_class_name = full_method_name[0:full_method_name.rfind('.')]
        result['package_name'] = full_class_name[0:full_class_name.rfind('.')]
        result['class_name'] = full_class_name[full_class_name.rfind('.')+1:-1]
        result['method_name'] = full_method_name[full_method_name.rfind('.')+1:-1]
        args=[]
        for arg in method_args.split(','):
            args.append(arg.strip().split(' '))
        result['args'] = args
        return result

    def __cast(self, arg_info):
        value = arg_info[0]
        typename = arg_info[1]

        if typename in ['byte, short', 'int', 'long']:
            return int(value)
        elif typename in ['float', 'double']:
            return float(value)
        elif typename in ['String', 'char']:
            return value
        elif typename in ['booolean']:
            return value.lower in ['true', '1']
        else:
            i = typename.rfind('.')
            module_name = typename[:i]
            type_name = typename[i+1:]
            if i != -1 and module_name != '':
                module = importlib.import_module(module_name)
                enum_type = getattr(module, type_name)
                return enum_type[value]

class RequestHelper:

    @staticmethod
    def process_request(request, cert, body=''):
        response = ''

        if not request.startswith('https://'):
            print('The address should always start with https')
            raise EcFeedError('The address should always start with https')

        try:
            response = requests.get(request, verify=cert["server"], cert=(cert["client"], cert["key"]), data=body, stream=True)
        except requests.exceptions.RequestException as e:
            print('The generated request is erroneous: ' + e.request.__dict__)
            raise EcFeedError('The generated request is erroneous: ' + e.request.url)

        if (response.status_code != 200):
            print('Error: ' + str(response.status_code))
            for line in response.iter_lines(decode_unicode=True):
                print(line)
            raise EcFeedError(json.loads(response.content.decode('utf-8'))['error'])

        return response

    @staticmethod
    def certificate_load(keystore_path, keystore_password):

        with open(keystore_path, 'rb') as keystore_file:
            keystore = crypto.load_pkcs12(keystore_file.read(), keystore_password.encode('utf8'))

        server = crypto.dump_certificate(crypto.FILETYPE_PEM, keystore.get_ca_certificates()[0])
        client = crypto.dump_certificate(crypto.FILETYPE_PEM, keystore.get_certificate())
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, keystore.get_privatekey())      

        with tempfile.NamedTemporaryFile(delete=False) as temp_server_file:
            temp_server_file.write(server)
        with tempfile.NamedTemporaryFile(delete=False) as temp_client_file: 
            temp_client_file.write(client)
        with tempfile.NamedTemporaryFile(delete=False) as temp_key_file: 
            temp_key_file.write(key)
        
        return { "server" : False if LOCALHOST else temp_server_file.name, "client" : temp_client_file.name, "key" : temp_key_file.name }   

    @staticmethod
    def certificate_remove(certificate):

        if not isinstance(certificate["server"], bool):
            remove(certificate["server"])
        if not isinstance(certificate["client"], bool):
            remove(certificate["client"])
        if not isinstance(certificate["key"], bool):
            remove(certificate["key"])

    @staticmethod
    def prepare_request_data(genserver, config) -> str:
        
        params={}
        params['method'] = config['methodInfo']
        params['model'] = config['modelId']
        params['userData'] = RequestHelper.serialize_user_data(config)
        
        if config['config']['template'] != None:
            params['template'] = str(config['config']['template'])
            request_type='requestExport'
        else:
            request_type='requestData'
        
        request = genserver + '/testCaseService?requestType=' + request_type + '&client=python'
        
        request += '&request='
        request += json.dumps(params).replace(' ', '')
        
        return request

    @staticmethod
    def prepare_request_feedback(genserver):
        return genserver + '/streamFeedback?client=python'

    @staticmethod
    def serialize_user_data(config):
        user_data={}
        user_data['dataSource']=repr(config['config']['dataSource'])

        test_suites=config['testSuites']
        properties=config['config']['properties']
        constraints=config['constraints']
        choices=config['choices']
        
        if test_suites != None:
            user_data['testSuites']=test_suites
        if properties != None:
            user_data['properties']=properties
        if constraints != None:
            user_data['constraints']=constraints
        if choices != None:
            user_data['choices']=choices
        
        return json.dumps(user_data).replace(' ', '').replace('"', '\'')