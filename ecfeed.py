from os import path, remove
import requests
from OpenSSL import crypto

import json
from enum import Enum

class EcFeedError(Exception):
    pass

class TemplateType(Enum):
    """Built-in export templates
    """

    CSV = 1
    XML = 2
    Gherkin = 3
    JSON = 4

    def __str__(self):
        return self.name

class DataSource(Enum):
    STATIC_DATA = 0
    NWISE = 1
    CARTESIAN = 2
    RANDOM = 3

    def __repr__(self):
        return self.to_url_param()

    def to_url_param(self):
        if self == DataSource.STATIC_DATA:
            return 'static'
        if self == DataSource.NWISE:
            return 'genNWise'
        if self == DataSource.CARTESIAN:
            return 'genCartesian'
        if self == DataSource.RANDOM:
            return 'genRandom'


class Context:
    """Contains parameters constant during lifetime of EcFeed class objects.

    ...

    Attributes
    ----------
    genserver : str
        url of the ecFeed generator service

    cert_file_name : str
        path to created user certificate file 

    pkey_file_name : str
        path to created user private key file 

    ca_file_name : str
        path to created server certificate file 
    """

    def __init__(self, genserver, keystore_path, password):
        """
        Parameters
        ----------
        genserver : str
            url to ecFeed generator service (default is 'develop-gen.ecfeed.com')

        keystore_path : str
            path to keystore file with user and server certificates (default is '~/.ecfeed.security.p12')

        password : str
            password to keystore (default is 'changeit')

        Raises
        ------
        EcFeedError
            If a problem occured during opening the keystore
        """

        self.genserver = genserver
        filename, extension = path.splitext(path.basename(keystore_path))
        extension = extension[1:len(extension)]
        self.cert_file_name = '__temp_' + filename + '.cert'
        self.pkey_file_name = '__temp_' + filename + '.pkey'
        self.ca_file_name = '__temp_' + filename + '.ca'

        if path.isfile(keystore_path) == False:
            raise EcFeedError('keystore file ' + keystore_path + ' does not exist')

        keystore = crypto.load_pkcs12(open(keystore_path, 'rb').read(), password.encode('utf8'))
        key = crypto.dump_privatekey(crypto.FILETYPE_PEM, keystore.get_privatekey())      
        cert = crypto.dump_certificate(crypto.FILETYPE_PEM, keystore.get_certificate())
        ca = crypto.dump_certificate(crypto.FILETYPE_PEM, keystore.get_ca_certificates()[0])

        with open('./' + self.pkey_file_name, 'wb') as pkeystream:
            pkeystream.write(key)
            pkeystream.close()

        with open('./' + self.cert_file_name, 'wb') as certstream:
            certstream.write(cert)
            certstream.close()

        with open('./' + self.ca_file_name, 'wb') as castream:
            castream.write(ca)
            castream.close()

    def __del__(self):
        """Remove all temporary files derived from the keystore
        """
        try:
            remove(self.cert_file_name)
        except OSError:
            pass
        try:
            remove(self.pkey_file_name)
        except OSError:
            pass
        try:
            remove(self.ca_file_name)
        except OSError:
            pass

class EcFeed:
    '''Access provider to ecFeed remote generator services

    ...
    Attributes
    ----------
    model : str
        Id of the accessed model. Must be accessible for user 
        owning the keystore file.        
    '''

    model = ''

    def __init__(self, genserver = 'develop-gen.ecfeed.com', 
                 keystore_path='~/.ecfeed/security.p12', password='changeit',
                 model=None):
        '''
        Parameters
        ----------
        genserver : str
            url to ecFeed generator service (default is 'develop-gen.ecfeed.com')

        keystore_path : str
            path to keystore file with user and server certificates (default is '~/.ecfeed.security.p12')

        password : str
            password to keystore (default is 'changeit')

        model : str
            id of the default model used by generators

        '''
        
        self.model = model
        self.__context = Context(genserver=genserver, keystore_path=keystore_path, password=password)

    def generate(self, method, data_source, model=None, template=None, request_only=False, **user_data):
        """Generic call to ecfeed generator service

        Parameters
        ----------
        method : str
            full name (including full class path) of the method that 
            will be used for generation. 

            Method parameters are not required. If parameters are not
            provided, the generator will generate data from the first 
            method it finds with that name

        data_source : str 
            the way how generator service will obtain the data. In general
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
            will be used

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

        if model == None:
            model = self.model

        request = self.__prepare_request(genserver=self.__context.genserver, 
                            model=model, method=method, 
                            data_source=data_source, template=template, 
                            **user_data)
        response = requests.get(request, verify=self.__context.ca_file_name, cert=(self.__context.cert_file_name, self.__context.pkey_file_name), stream=True)
        # response = requests.get(request, verify=False, cert=(self.__context.cert_file_name, self.__context.pkey_file_name), stream=True)

        if(response.status_code != 200):
            print('Error: ' + str(response.status_code))
            raise EcFeedError(json.loads(response.content.decode('utf-8'))['error'])
        else:
            args_info = {}
            for line in response.iter_lines(decode_unicode=True):
                line = line.decode('utf-8')
                if template != None:
                    yield line
                elif 'raw_output' in user_data and user_data['raw_output'] == True:
                    yield line
                else:
                    test_data = self.__parse_test_line(line=line)
                    if 'method' in test_data:
                        args_info = test_data['method']
                    if 'values' in test_data:
                        yield  [self.__cast(value) for value in list(zip(test_data['values'], [arg[0] for arg in args_info['args']]))]

    def nwise(self, method, n, coverage=100, template=None, **user_data):
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
        properties['n'] = str(n)
        properties['coverage'] = str(coverage)
        yield from self.generate(method=method, data_source=DataSource.NWISE, 
                                 properties=properties, template=template, **user_data)

    def pairwise(self, method, coverage=100, template=None, **user_data):
        """Calls nwise with n=2

        Parameters
        ----------
        method : str
            See 'generate'
            
        coverage : int
            See 'nwise' 

        template : str
            See 'generate'            

        choices : dictionary
            See 'generate' 

        constraints : dictionary
            See 'generate' 

        model : str
            See 'generate'                         
        """

        yield from self.nwise(method, n=2, coverage=coverage, template=template, **user_data)

    def cartesian(self, method, template=None, **user_data):
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

        yield from self.generate(method=method, data_source=DataSource.CARTESIAN, template=template, **user_data)

    def random(self, method, length, adaptive=True, duplicates=False, template=None, **user_data):
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
        properties['adaptive'] = str(adaptive).lower()
        properties['duplicates'] = str(duplicates).lower()
        properties['length'] = str(length)
        user_data['properties'] = properties
        yield from self.generate(method=method, data_source=DataSource.RANDOM, template=template, **user_data)

    def static_suite(self, method, test_suites=None, template=None, **user_data):
        """Calls generator service for pre-generated data from test suites

        Parameters
        ----------
        method : str
            See 'generate'        

        test_suites : list
            A list of test suites that shall be requested

        model : str
            See 'generate'                         

        """

        user_data['test_suites'] = test_suites
        yield from self.generate(method=method, data_source=DataSource.STATIC_DATA, template=template, **user_data)

    def method_info(self, method, model=None):
        """Queries generator service for information about the method

        Parameters
        ----------
        method : str
            Querried method        

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
        for line in self.random(method=method, length=0, raw_output=True, model=model):
            line = line.replace('"{', '{').replace('}"', '}').replace('\'', '"')#fix wrong formatting in some versions of the gen-server
            try:                
                parsed = json.loads(line)
            except ValueError as e:
                print('Unexpected problem when getting method info: ' + str(e))
            if 'info' in parsed :
                method_name = parsed['info']['method']
                info = self.__parse_method_definition(method_name)
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

    def __prepare_request(self, method, data_source, 
                          genserver=None, 
                          model=None,
                          template=None, **user_data) -> str:
                          
        if genserver == None:
            genserver = self.__context.genserver
        if model == None:
            model = self.__context.model

        generate_params={}
        generate_params['method'] = ''
        generate_params['method'] += method
        generate_params['model'] = model
        generate_params['userData'] = self.__serialize_user_data(data_source=data_source, **user_data)
        
        request_type='requestData'
        if template != None:
            generate_params['template'] = str(template)
            request_type='requestExport'

        request = 'https://' + genserver + '/testCaseService?requestType=' + request_type + '&request='
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




