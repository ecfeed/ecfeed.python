from os import path, remove

import requests
from OpenSSL import crypto
import tempfile

import json
from enum import Enum

import importlib

LOCALHOST = False

def __default_keystore_path():
    keystore_paths = \
        [path.expanduser('~/.ecfeed/localhost.p12'), path.expanduser('~/ecfeed/localhost.p12')] if LOCALHOST else \
        [path.expanduser('~/.ecfeed/security.p12'), path.expanduser('~/ecfeed/security.p12')]    
    for keystore_path in keystore_paths:
        if path.exists(keystore_path):
            return keystore_path
    return keystore_path

DEFAULT_GENSERVER = 'https://localhost:8090' if LOCALHOST else 'https://gen.ecfeed.com'
DEFAULT_KEYSTORE_PATH = __default_keystore_path()
DEFAULT_KEYSTORE_PASSWORD = 'changeit'

class EcFeedError(Exception): pass

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

    @staticmethod
    def parse_template(template):
        if template == str(TemplateType.CSV): return TemplateType.CSV
        elif template == str(TemplateType.JSON): return TemplateType.JSON
        elif template == str(TemplateType.Gherkin): return TemplateType.Gherkin
        elif template == str(TemplateType.XML): return TemplateType.XML
        elif template == str(TemplateType.RAW): return TemplateType.RAW
        return None

DEFAULT_TEMPLATE = TemplateType.CSV
DEFAULT_N = 2
DEFAULT_COVERAGE = 100
DEFAULT_ADAPTIVE = True
DEFAULT_DUPLICATES = False
DEFAULT_LENGTH = 1

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

    def get_model(self): return self.model
    
    def get_genserver(self): return self.genserver
    
    def get_keystore_password(self): return self.password
    
    def get_keystore_path(self): return self.keystore_path
    
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
        
        config = self.__configuration_init(**kwargs)
        
        if (config['config']['url']):
            yield config['config']['request']
            return
        
        config = self.__configuration_update(config, **kwargs)
        
        try:
            response = RequestHelper.process_request_data(config)
            
            for line in response.iter_lines(decode_unicode=True):
                
                line = line.decode('utf-8')
                
                test_case = None
                raw_type = ((config['template'] is not None) and (config['template'] is not TemplateType.RAW)) or config['config']['rawOutput']
                
                if raw_type and (config['testSessionId'] is None):
                    yield line
                elif raw_type:
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
            RequestHelper.certificate_remove(config)

    def validate(self):
         
        config = self.__configuration_init_validation()
        
        try:
            response = RequestHelper.process_request_validation(config)
            
            for line in response.iter_lines(decode_unicode=True):
               print(line)

        except:
            RequestHelper.certificate_remove(config)
            
    def __configuration_init(self, **kwargs):

        config = {
            'config' : {
                'genServer' : self.genserver,
                'rawOutput' : kwargs.pop('raw_output', None),
                'url' : kwargs.pop('url', None)
            },
            'properties' : kwargs.pop('properties', None),
            'dataSource' : self.__configuration_get_data_source(**kwargs),
            'template' : kwargs.pop('template', None),
            'model' : self.__configuration_get_model(**kwargs),
            'method' : self.__configuration_get_method(**kwargs),
            'testSuites' : kwargs.pop('test_suites', None),
            'constraints' : kwargs.pop('constraints', None),
            'choices' : kwargs.pop('choices', None),
        }

        config['config']['request'] = RequestHelper.prepare_request_data(config)

        return config

    def __configuration_init_validation(self):
        
        config = {
            'config' : {
                'genServer' : self.genserver,
                'certificate' : RequestHelper.certificate_load(self.keystore_path, self.password)
            },
            'framework' : 'Python',
            'timestamp' : None
        }

        config['config']['request'] = RequestHelper.prepare_request_validation(config)

        return config
    
    def __configuration_update(self, config, **kwargs):

        update = {
            'config' : {
                'testCurrent' : 0,
                'testTotal' : 0,
                'certificate' : RequestHelper.certificate_load(self.keystore_path, self.password),
                'feedback' : kwargs.pop('feedback', False),
                'args' : {}
            },
            'testSessionId' : None,
            'framework' : 'Python',
            'timestamp' : None,
            'testSessionLabel' : kwargs.pop('label', None),
            'custom' : kwargs.pop('custom', None),
            'testResults' : {}
        }

        update['config'].update(config['config'])
        config.update(update)

        return config

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

    def __configuration_append(self, config, path, element, condition=True):

        if not condition:
            return

        for i in range(len(path) - 1):
            if path[i] not in config:
                config[path[i]] = {}
            config = config[path[i]]

        config[path[-1]] = element

    def __response_parse_test_session_id(self, config, test_data):
        
        if 'test_session_id' in test_data:
            if config['config']['feedback'] is True: 
                self.__configuration_append(config, ['testSessionId'], test_data['test_session_id'])

    def __response_parse_timestamp(self, config, test_data):
        
        if 'timestamp' in test_data:
            self.__configuration_append(config, ['timestamp'], test_data['timestamp'])

    def __response_parse_method_info(self, config, test_data):
       
        if 'method_info' in test_data:
            self.__configuration_append(config, ['method'], test_data['method_info'])

    def __response_parse_method(self, config, test_data):
        
        if 'method' in test_data:
            config['config']['args'] = test_data['method']
    
    def __response_parse_values(self, config, test_data):
        
        if 'values' in test_data:
            return [self.__cast(value) for value in list(zip(test_data['values'], [arg[0] for arg in config['config']['args']['args']]))]
        else:
            return None

    def __response_parse_test_case(self, line, config, test_case):
       
        self.__configuration_append(config, ['testResults', ('0:' + str(config['config']['testTotal'])), 'data'], line)

        if (config['testSessionId'] is not None):
            test_handle = TestHandle('0:' + str(config['config']['testTotal']), config) 
            test_case.append(test_handle)

        config['config']['testTotal'] += 1

        return test_case

    def generate_nwise(self, **kwargs): return self.nwise(template=None, **kwargs)

    def export_nwise(self, **kwargs): return self.nwise(template=kwargs.pop('template', DEFAULT_TEMPLATE), **kwargs)

    def generate_pairwise(self, **kwargs): return self.nwise(n=kwargs.pop('n', DEFAULT_N), template=None, **kwargs)

    def export_pairwise(self, **kwargs): return self.nwise(n=kwargs.pop('n', DEFAULT_N), template=kwargs.pop('template', DEFAULT_TEMPLATE), **kwargs)

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
        properties['n'] = str(kwargs.pop('n', DEFAULT_N))
        properties['coverage'] = str(kwargs.pop('coverage', DEFAULT_COVERAGE))
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
        properties['coverage'] = str(kwargs.pop('coverage', DEFAULT_COVERAGE))

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
        properties['adaptive'] = str(kwargs.pop('adaptive', DEFAULT_ADAPTIVE)).lower()
        properties['duplicates'] = str(kwargs.pop('duplicates', DEFAULT_DUPLICATES)).lower()
        properties['length'] = str(kwargs.pop('length', DEFAULT_LENGTH))

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
            header.append("test_handle")
        
        return header

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

        if typename in ['byte', 'short', 'int', 'long']:
            return int(value)
        elif typename in ['float', 'double']:
            return float(value)
        elif typename in ['String', 'char']:
            return value
        elif typename in ['boolean']:
            return value.lower in ['true', '1']
        else:
            i = typename.rfind('.')
            module_name = typename[:i]
            type_name = typename[i+1:]
            if i != -1 and module_name != '':
                module = importlib.import_module(module_name)
                enum_type = getattr(module, type_name)
                return enum_type[value]

class TestHandle:

    def __init__(self, id, config):
        self.config = config      
        self.id = id  

    def add_feedback(self, status, duration=None, comment=None, custom=None):
        test_case = self.config["testResults"][self.id]

        if "status" in test_case:
            return comment

        test_case["status"] = "P" if status else "F"
        
        if duration:
            test_case["duration"] = duration
        if comment:
            test_case["comment"] = comment
        if custom:
            test_case["custom"] = custom

        self.config['config']['testCurrent'] += 1

        if (self.config['config']['testCurrent'] == self.config['config']['testTotal']):
            RequestHelper.process_request_feedback(self.config)

        return comment

class RequestHelper:

    @staticmethod
    def process_request_data(config):
        
        return RequestHelper.process_request(config['config']['request'], config)

    @staticmethod
    def process_request_feedback(config):
        status = RequestHelper.process_request(RequestHelper.prepare_feedback_address(config), config, RequestHelper.prepare_feedback_body(config))
        RequestHelper.certificate_remove(config)

        return status

    @staticmethod
    def process_request_validation(config):
        
        return RequestHelper.process_request(RequestHelper.prepare_request_validation(config), config)
    
    @staticmethod
    def process_request(request, config, body=''):
        response = ''

        if not request.startswith('https://'):
            print('The address should always start with https://.')
            raise EcFeedError('The address should always start with https://.')

        try:
            certificate = config['config']['certificate']
            response = requests.get(request, verify=certificate["server"], cert=(certificate["client"], certificate["key"]), data=body, stream=True)
        except requests.exceptions.RequestException as e:
            print('The generated request is erroneous: ' + e.request.__dict__)
            raise EcFeedError('The generated request is erroneous: ' + e.request.url)
        except Exception:
            print('The server could not process the request. Check if the package/class/method is correct and you have required privileges.')
            raise EcFeedError('The server could not process the request.')

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
    def certificate_remove(config):

        certificate = config['config']['certificate']
        
        if not isinstance(certificate["server"], bool):
            remove(certificate["server"])
        if not isinstance(certificate["client"], bool):
            remove(certificate["client"])
        if not isinstance(certificate["key"], bool):
            remove(certificate["key"])
    
    @staticmethod
    def prepare_request_data(config) -> str:
        user_data={}
        
        user_data['dataSource'] = repr(config['dataSource'])
        user_data['testSuites'] = config['testSuites']
        user_data['properties'] = config['properties']
        user_data['constraints'] = config['constraints']
        user_data['choices'] = config['choices']
        
        user_data = {k: v for k, v in user_data.items() if v is not None}
        
        params = {}

        params['method'] = config['method']
        params['model'] = config['model']
        params['userData'] = json.dumps(user_data).replace(' ', '').replace('"', '\'')
        
        if (config['template'] is not None) and (config['template'] is not TemplateType.RAW):
            params['template'] = str(config['template'])
            request_type='requestExport'
        else:
            request_type='requestData'
        
        request = config['config']['genServer'] + '/testCaseService?'
        
        request += 'requestType=' + request_type 
        request += '&client=python'
        request += '&request='
        request += json.dumps(params).replace(' ', '')
        
        return request

    @staticmethod
    def prepare_request_validation(config) -> str:
        request = config['config']['genServer'] + '/genServiceVersion?'
        
        request += '&client=python'
        
        return request
    
    @staticmethod
    def prepare_feedback_address(config) -> str:

        return config['config']['genServer'] + '/streamFeedback?client=python'

    @staticmethod
    def prepare_feedback_body(config) -> str:
        body = {}

        body['modelId'] = config['model']
        body['methodInfo'] = config['method']
        body['generatorType'] = config['dataSource'].to_feedback_param()
        body['testSuites'] = config['testSuites']
        body['constraints'] = config['constraints']
        body['choices'] = config['choices']
        body['testSessionId'] = config['testSessionId']
        body['framework'] = config['framework']
        body['timestamp'] = config['timestamp']
        body['generatorOptions'] = RequestHelper.parse_dictionary(config['properties'])
        body['testSessionLabel'] = config['testSessionLabel']
        body['custom'] = config['custom']
        body['testResults'] = config['testResults']

        body = {k: v for k, v in body.items() if v is not None}

        return json.dumps(body)

    @staticmethod    
    def parse_dictionary(dictionary):

        if dictionary == None:
            return None

        parsed = ''

        for key in dictionary:
            parsed += key + '=' + dictionary[key] + ', '

        parsed = parsed[:-2]

        return parsed