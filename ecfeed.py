from os import path, remove

import requests
from OpenSSL import crypto
import tempfile

import json
from enum import Enum
import sys
import time
import uuid

import importlib

def __default_keystore_path():
    keystore_paths = [path.expanduser('~/.ecfeed/security.p12'), path.expanduser('~/ecfeed/security.p12')]
    for keystore_path in keystore_paths:
        if path.exists(keystore_path):
            return keystore_path
    return keystore_path

DEFAULT_GENSERVER = 'https://localhost:8090' # gen.ecfeed.com
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
        self.creation_timestamp = int(time.time() * 1000000)        
        self.execution_data = {}

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
        
        try:
            method = kwargs.pop('method')
            data_source = kwargs.pop('data_source')
        except KeyError as e:
            raise EcFeedError(f"missing required argument: {e}.")

        model = kwargs.pop('model', self.model)
        template = kwargs.pop('template', None)

        feedback_flag = kwargs.pop('feedback', False)
        feedback_id = int(time.time() * 1000000) if feedback_flag == True else None

        raw_output = False
        if 'raw_output' in kwargs or template == TemplateType.RAW:
            raw_output = True
        if template == TemplateType.RAW: 
            template = None

        request = self.__prepare_request(model=model, method=method, feedback_id=feedback_id, data_source=data_source, template=template, **kwargs)

        if(kwargs.pop('url', None)):
            yield request
            return

        config = {
            'generator_options' : self.__parse_dictionary(kwargs.pop('properties', None)),
            'generator_type' : data_source.to_feedback_param(),
            'test_session_label' : kwargs.pop('label', None),
            'constraints' : kwargs.pop('constraints', None),
            'test_suites' : kwargs.pop('test_suites', None),
            'choices' : kwargs.pop('choices', 'ALL'),
            'custom' : kwargs.pop('custom', None)
        }

        cert = self.__certificate_load()

        try:
            response = self.__process_request(request, cert)

            self.__feedback_set_up(feedback_id, model, method, config, cert)
            
            args_info = {}
            test_index = 0
                
            for line in response.iter_lines(decode_unicode=True):
                line = line.decode('utf-8')
                test_case = None

                if ((template != None) or raw_output) and (feedback_id is None):
                    yield line
                elif ((template != None) or raw_output):
                    test_case = [str(line)]
                else:
                    test_data = self.__parse_test_line(line=line) 
                        
                    if 'timestamp' in test_data:
                        self.__feedback_append(feedback_id, ["timestamp"], test_data['timestamp'])
                    if 'test_session_id' in test_data:
                        self.__feedback_append(feedback_id, ["testSessionId"], test_data['test_session_id'])
                    if 'method_info' in test_data:
                        self.__feedback_append(feedback_id, ["methodInfo"], test_data['method_info'])
                    if 'method' in test_data:
                        args_info = test_data['method']
                    if 'values' in test_data:
                        test_case = [self.__cast(value) for value in list(zip(test_data['values'], [arg[0] for arg in args_info['args']]))]
                
                if test_case is not None:
                    self.__feedback_append(feedback_id, ["testResults", ("0:" + str(test_index)), "data"], line)

                    if (feedback_id is not None):
                        test_case.append({"label" : feedback_id, "id" : ("0:" + str(test_index)) })

                    test_index += 1

                    yield test_case
                            
            self.__feedback_append(feedback_id, ["summaryTotal"], test_index)

        except:
            self.__certificate_remove(cert)
            

    def __parse_dictionary(self, dictionary):

        if dictionary == None:
            return None

        parsed = ''

        for key in dictionary:
            parsed += key + '=' + dictionary[key] + ', '

        parsed = parsed[:-2]

        return parsed

    def __certificate_load(self):
        with open(self.keystore_path, 'rb') as keystore_file:
            keystore = crypto.load_pkcs12(keystore_file.read(), self.password.encode('utf8'))

        server = crypto.dump_certificate(crypto.FILETYPE_PEM, keystore.get_ca_certificates()[0])
        client = crypto.dump_certificate(crypto.FILETYPE_PEM, keystore.get_certificate())
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, keystore.get_privatekey())      

        with tempfile.NamedTemporaryFile(delete=False) as temp_server_file:
            temp_server_file.write(server)
        with tempfile.NamedTemporaryFile(delete=False) as temp_client_file: 
            temp_client_file.write(client)
        with tempfile.NamedTemporaryFile(delete=False) as temp_key_file: 
            temp_key_file.write(key)
        
        # The generator on localhost is not associated with the *.ecfeed.com domain, it cannot the checked (that's why it is set to False).
        return { "server" : False, "client" : temp_client_file.name, "key" : temp_key_file.name }   

    def __certificate_remove(self, cert):

        if not isinstance(cert["server"], bool):
            remove(cert["server"])
        if not isinstance(cert["client"], bool):
            remove(cert["client"])
        if not isinstance(cert["key"], bool):
            remove(cert["key"])

    def __process_request(self, request, cert, body=''):
        response = requests.get(request, verify=cert["server"], cert=(cert["client"], cert["key"]), data=body, stream=True)
        
        if(response.status_code != 200):
            print('Error: ' + str(response.status_code))
            raise EcFeedError(json.loads(response.content.decode('utf-8'))['error'])
        
        return response
        
    def __feedback_set_up(self, feedback_id, model, method, config, cert):

        if feedback_id is None:
            return

        if feedback_id in self.execution_data:
            raise NameError('The feedback ID already exists')
        
        self.execution_data[feedback_id] = {}
        # Required fields.
        self.execution_data[feedback_id]["testSessionId"] = 0
        self.execution_data[feedback_id]["modelId"] = model
        self.execution_data[feedback_id]["methodInfo"] = method
        self.execution_data[feedback_id]["testResults"] = {}
        # Optional fields, but the client is nice enough to send them.
        self.execution_data[feedback_id]["framework"] = 'Python'
        self.execution_data[feedback_id]["timestamp"] = feedback_id
        self.execution_data[feedback_id]["generatorType"] = config['generator_type']
        # Optional fields.
        if config['generator_options']:
            self.execution_data[feedback_id]["generatorOptions"] = config['generator_options']
        if config['test_session_label']:
            self.execution_data[feedback_id]["testSessionLabel"] = config['test_session_label']
        if config['constraints']:
            self.execution_data[feedback_id]["constraints"] = config['constraints']
        if config['choices']:
            self.execution_data[feedback_id]["choices"] = config['choices']
        if config['custom']:
            self.execution_data[feedback_id]["custom"] = config['custom']
        if config['test_suites']:
            self.execution_data[feedback_id]["testSuites"] = config['test_suites']
        # Technical fields, removed before sending the feedback.
        self.execution_data[feedback_id]["summaryTotal"] = 0
        self.execution_data[feedback_id]["summaryCurrent"] = 0
        self.execution_data[feedback_id]["certificate"] = cert
        
    def __feedback_append(self, feedback_id, path, element, condition=True):

        if not condition or (feedback_id is None):
            return

        index = self.execution_data[feedback_id]

        for i in range(len(path) - 1):
            if path[i] not in index:
                index[path[i]] = {}
            index = index[path[i]]

        index[path[-1]] = element

    def __feedback_process(self, feedback_id):

        feedback_data = self.execution_data[feedback_id].copy()
        cert = feedback_data["certificate"].copy()

        del feedback_data["summaryCurrent"]
        del feedback_data["summaryTotal"]   
        del feedback_data["certificate"]
        
        del self.execution_data[feedback_id]

        request = self.__prepare_request_feedback(feedback_id=feedback_data['testSessionId'])

        self.__process_request(request, cert, json.dumps(feedback_data))
        self.__certificate_remove(cert)

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
        
        if (test_id["label"] not in self.execution_data) or (test_id["label"] == ""):
            return
        
        test_suite = self.execution_data[test_id["label"]]
        test_case = test_suite["testResults"][test_id["id"]]

        if "status" in test_case:
            return comment

        test_case["status"] = "passed" if status else "failed"
        
        if duration:
            test_case["duration"] = duration
        if comment:
            test_case["comment"] = comment
        if custom:
            test_case["custom"] = custom

        test_suite["summaryCurrent"] += 1

        if (test_suite["summaryCurrent"] == test_suite["summaryTotal"]):
            self.__feedback_process(test_id["label"])

        return comment

    def __prepare_request(self, method, data_source,
                          type = "requestData",
                          model=None,
                          template=None,
                          feedback_id=None,
                          feedback=None, 
                          **user_data) -> str:
                          
        if model == None:
            model = self.model

        generate_params={}
        generate_params['method'] = ''
        generate_params['method'] += method
        generate_params['model'] = model
        generate_params['userData'] = self.__serialize_user_data(data_source=data_source, **user_data)
        
        request_type=type
        if template != None:
            generate_params['template'] = str(template)
            request_type='requestExport'
        
        request = self.genserver + '/testCaseService?requestType=' + request_type + '&client=python'
        
        if feedback_id is not None:
            request += '&generationID=' + str(feedback_id)

        if feedback is not None:
            request += '&feedback=' + str(feedback)
        
        request += '&request='
        request += json.dumps(generate_params).replace(' ', '')

        return request

    def __prepare_request_feedback(self, feedback_id=None) -> str:
        
        request = self.genserver + '/streamFeedback?client=python'
        request += '&generationID=' + str(feedback_id)

        return request

    def __parse_test_line(self, line):
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
                result['test_session_id'] = json_parsed['id']
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

    def __serialize_user_data(self, data_source, **kwargs):
        user_data={}
        user_data['dataSource']=repr(data_source)
        test_suites=kwargs.pop('test_suites', None)
        properties=kwargs.pop('properties', None)
        constraints=kwargs.pop('constraints', None)
        choices=kwargs.pop('choices', None)
        if test_suites != None:
            user_data['testSuites']=test_suites
        if properties != None:
            user_data['properties']=properties
        if constraints != None:
            user_data['constraints']=constraints
        if choices != None:
            user_data['choices']=choices
        return json.dumps(user_data).replace(' ', '').replace('"', '\'')

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
            




