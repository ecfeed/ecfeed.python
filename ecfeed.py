import os
import requests
from OpenSSL import crypto

import json
from enum import Enum

from ecfeed_helper import *

class EcFeedError(Exception):
    pass

class TemplateType(Enum):
    CSV = 1
    XML = 2
    Gherkin = 3
    JSON = 4

class Context:
    def __init__(self, **kwargs):
        keystore_path=kwargs.pop('keystore', '~/.ecfeed/security.p12')
        password=kwargs.pop('password', 'changeit')
        self.genserver=kwargs.pop('genserver', 'develop-gen.ecfeed.com')
        self.model=kwargs.pop('model', None)
        self.package=kwargs.pop('package', '')
        self.classname=kwargs.pop('classname', '')

        filename, extension = os.path.splitext(os.path.basename(keystore_path))
        extension = extension[1:len(extension)]
        self.cert_file_name = '__temp_' + filename + '.cert'
        self.pkey_file_name = '__temp_' + filename + '.pkey'
        self.ca_file_name = '__temp_' + filename + '.ca'

        if os.path.isfile(keystore_path) == False:
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
        if os.path.isfile(self.cert_file_name):
            os.remove(self.cert_file_name)

        if os.path.isfile(self.pkey_file_name):
            os.remove(self.pkey_file_name)

class EcFeed:
    def __init__(self, **kwargs):
        self.context = Context(**kwargs)

    def generate(self, method, data_source, **kwargs):
        request = prepare_request(method=method, data_source=data_source, gen_args=self.__parse_gen_args(**kwargs), **kwargs)
        # response = requests.get(request, verify=self.context.ca_file_name, cert=(self.context.cert_file_name, self.context.pkey_file_name), stream=True)
        response = requests.get(request, verify=False, cert=(self.context.cert_file_name, self.context.pkey_file_name), stream=True)

        args_info = {}
        for line in response.iter_lines(decode_unicode=True):
            line = line.decode('utf-8')
            if 'template' in kwargs:
                yield line
            elif 'raw_output' in kwargs:
                yield line
            else:
                test_data = parse_test_line(line=line)
                if 'method' in test_data:
                    args_info = test_data['method']   
                if 'values' in test_data:
                    yield  [cast(value) for value in list(zip(test_data['values'], [arg[0] for arg in args_info['args']]))]

    def nwise(self, method, n, coverage=100, **kwargs):
        properties={}
        properties['n'] = str(n)
        properties['coverage'] = str(coverage)
        yield from self.generate(method=method, data_source=DataSource.NWISE, properties=properties, **kwargs)

    def pairwise(self, method, coverage=100, **kwargs):
        yield from self.nwise(method, n=2, coverage=coverage, **kwargs)

    def cartesian(self, method, **kwargs):
        yield from self.generate(method=method, data_source=DataSource.CARTESIAN, **kwargs)

    def random(self, method, length, adaptive=True, duplicates=False, **kwargs):
        properties={}
        properties['adaptive'] = str(adaptive).lower()
        properties['duplicates'] = str(duplicates).lower()
        properties['length'] = str(length)
        kwargs['properties'] = properties
        yield from self.generate(method=method, data_source=DataSource.RANDOM, **kwargs)

    def static_suite(self, method, test_suites, **kwargs):
        kwargs['test_suites'] = test_suites
        yield from self.generate(method=method, data_source=DataSource.STATIC_DATA, **kwargs)

    def method_arg_names(self, method_info=None, method_name=None):
        if method_info != None:
            return [i[1] for i in method_info['args']]
        elif method_name != None:
            return self.method_arg_names(self.method_info(method=method_name))

    def method_arg_types(self, method_info=None, method_name=None):
        if method_info != None:
            return [i[0] for i in method_info['args']]
        elif method_name != None:
            return self.method_arg_types(self.method_info(method=method_name))

    def method_info(self, method):
        info={}
        for line in self.random(method=method, length=0, raw_output=True):
            line = line.replace('"{', '{').replace('}"', '}').replace('\'', '"')#fix wrong formatting in some versions of the gen-server
            try:                
                parsed = json.loads(line)
            except ValueError as e:
                print('Unexpected problem when getting method info: ' + str(e))
            if 'info' in parsed :
                method_name = parsed['info']['method']
                info = parse_method_definition(method_name)
        return info


    def __parse_gen_args(self, **kwargs):
        result={}

        model = kwargs.pop('model', None)
        genserver = kwargs.pop('genserver', None)
        package = kwargs.pop('package', None)
        classname = kwargs.pop('classname', None)

        if model == None:
            model = self.context.model
        if genserver == None:
            genserver = self.context.genserver
        if package == None:
            package = self.context.package
        if classname == None:
            classname = self.context.classname

        if model == None:
            raise EcFeedError('model not defined')
        if genserver == None:
            raise EcFeedError('gen server url not defined')

        result['model'] = model
        result['genserver'] = genserver
        result['package'] = package
        result['classname'] = classname

        return result
 
    
