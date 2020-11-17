from os import path, remove

import requests
from OpenSSL import crypto
import tempfile

import json
from enum import Enum
import sys
import time

import importlib

def __default_keystore_path():
    keystore_paths = [path.expanduser('~/.ecfeed/security.p12'), path.expanduser('~/ecfeed/security.p12')]
    for keystore_path in keystore_paths:
        if path.exists(keystore_path):
            return keystore_path
    return keystore_path

DEFAULT_GENSERVER = 'gen.ecfeed.com'
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

    def __init__(self, genserver = DEFAULT_GENSERVER, 
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
        self.creation_timestamp = time.time()
        self.execution_data = {}

        self.remove_passed_tests = True
        self.keep_test_data = True

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

        feedback = kwargs.pop('feedback', False)
        feedback_label = kwargs.pop('feedback_label', str(time.time()) if feedback else '')

        raw_output = False
        if 'raw_output' in kwargs or template == TemplateType.RAW:
            raw_output = True
        if template == TemplateType.RAW: 
            template = None

        request = self.__prepare_request(genserver=self.genserver, 
                            model=model, method=method, 
                            data_source=data_source, template=template, 
                            **kwargs)

        # print(f'request:{request}')
        if(kwargs.pop('url', None)):
            yield request
            return

        with open(self.keystore_path, 'rb') as keystore_file:
            keystore = crypto.load_pkcs12(keystore_file.read(), self.password.encode('utf8'))

        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, keystore.get_privatekey())      
        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, keystore.get_certificate())
        ca = crypto.dump_certificate(crypto.FILETYPE_PEM, keystore.get_ca_certificates()[0])

        with tempfile.NamedTemporaryFile(delete=False) as temp_cert_file: 
            temp_cert_file.write(cert)
        with tempfile.NamedTemporaryFile(delete=False) as temp_pkey_file: 
            temp_pkey_file.write(key)
        with tempfile.NamedTemporaryFile(delete=False) as temp_ca_file:
            temp_ca_file.write(ca)

        try:
            response = requests.get(request, verify=temp_ca_file.name, cert=(temp_cert_file.name, temp_pkey_file.name), stream=True)
            if(response.status_code != 200):
                print('Error: ' + str(response.status_code))
                raise EcFeedError(json.loads(response.content.decode('utf-8'))['error'])
            else:
                args_info = {}

                self._add_feedback(feedback, feedback_label, method)

                index_local = 0

                for line in response.iter_lines(decode_unicode=True):
                    line = line.decode('utf-8')
                    if template != None:
                        yield line
                    elif raw_output:
                        yield line
                    else:
                        test_data = self.__parse_test_line(line=line)
                        if 'method' in test_data:
                            args_info = test_data['method']
                        if 'values' in test_data:
                            test_case = [self.__cast(value) for value in list(zip(test_data['values'], [arg[0] for arg in args_info['args']]))]

                            self._build_feedback(feedback, [feedback_label, "execution", index_local, "data"], test_case.copy(), condition=self.keep_test_data)
                            self._build_feedback(feedback, [feedback_label, "execution", index_local, "time"], time.time())

                            test_case.append({"label" : feedback_label, "id" : index_local })

                            index_local += 1

                            print("yield")
                            time.sleep(1)
                            yield  test_case

                self._build_feedback(feedback, [feedback_label, "size_total"], index_local)
                self._build_feedback(feedback, [feedback_label, "status"], "completed")

        finally:
            remove(temp_cert_file.name)
            remove(temp_pkey_file.name)
            remove(temp_ca_file.name)

    def _add_feedback(self, feedback, feedback_label, method):

        if not feedback:
            return
        
        if feedback_label in self.execution_data:
            raise NameError('The generation ID already exists')

        self.execution_data[feedback_label] = {}
        self.execution_data[feedback_label]["execution"] = {}
        self.execution_data[feedback_label]["test_provider_id"] = self.creation_timestamp
        self.execution_data[feedback_label]["method"] = method
        self.execution_data[feedback_label]["status"] = "pending"
        self.execution_data[feedback_label]["size_total"] = 0
        self.execution_data[feedback_label]["size_processed"] = 0
        self.execution_data[feedback_label]["size_passed"] = 0

    def _build_feedback(self, feedback, path, element, condition=True):

        if (not feedback) and (not condition):
            return

        index = self.execution_data

        for i in range(len(path) - 1):
            if path[i] not in index:
                index[path[i]] = {}
            index = index[path[i]]

        index[path[-1]] = element

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

    def feedback(self, test_id, status, comment=None):     

        print("feedback")
        
        if test_id["label"] not in self.execution_data:
            return

        test_suite = self.execution_data[test_id["label"]]

        if test_id["id"] not in test_suite["execution"]:
            return comment

        test = test_suite["execution"][test_id["id"]]

        if "passed" in test:
            return comment

        if status and self.remove_passed_tests:
            del test_suite["execution"][test_id["id"]]
        else:
            test["passed"] = status
            test["time"] = time.time() - test["time"]
            if comment:
                test["comment"] = comment
        
        if status:
            test_suite["size_passed"] += 1

        test_suite["size_processed"] += 1

        if (test_suite["status"] == "completed") and (test_suite["size_total"] == test_suite["size_processed"]):
            self.__process_test_suite_results(test_id["label"])

        return comment

    def __process_test_suite_results(self, feedback_label):
        self.__process_test_suite_results_cleanup(feedback_label)
        
        print(self.execution_data[feedback_label])            # Do some stuff...
        
        del self.execution_data[feedback_label]

    def __process_test_suite_results_cleanup(self, feedback_label):
        test_suite = self.execution_data[feedback_label]

        del test_suite["status"]
        del test_suite["size_processed"]

        # for test in test_suite["execution"]:
        #     del test_suite["execution"][test]["passed"]

    def __prepare_request(self, method, data_source, 
                          genserver=None, 
                          model=None,
                          template=None, **user_data) -> str:
                          
        if genserver == None:
            genserver = self.genserver
        if model == None:
            model = self.model

        generate_params={}
        generate_params['method'] = ''
        generate_params['method'] += method
        generate_params['model'] = model
        generate_params['userData'] = self.__serialize_user_data(data_source=data_source, **user_data)
        
        request_type='requestData'
        if template != None:
            generate_params['template'] = str(template)
            request_type='requestExport'

        request = 'https://' + genserver + '/testCaseService?requestType=' + request_type + '&client=python' + '&request='
        request += json.dumps(generate_params).replace(' ', '')
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
                result['method'] = self.__parse_method_definition(json.loads(info)['method'])
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
            




