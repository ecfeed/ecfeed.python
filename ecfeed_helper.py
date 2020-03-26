import json
from enum import Enum

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

def prepare_request(genserver, model, method, data_source, template=None, **user_data):
    generate_params={}
    generate_params['method'] = ''
    generate_params['method'] += method
    generate_params['model'] = model
    generate_params['userData'] = serialize_user_data(data_source=data_source, **user_data)
    
    request_type='requestData'
    if template != None:
        generate_params['template'] = str(template)
        request_type='requestExport'

    request = 'https://' + genserver + '/testCaseService?requestType=' + request_type + '&request='
    request += json.dumps(generate_params).replace(' ', '')
    return request

def serialize_user_data(data_source, **kwargs):
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

def parse_method_definition(method_info_line):
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

def cast(arg_info):
    value = arg_info[0]
    typename = arg_info[1]

    if typename in ['byte, short', 'int', 'long']:
        return int(value)
    elif typename in ['float', 'double']:
        return float(value)
    elif typename in ['String', 'char']:
        return value
    elif typename in ['booolean']:
        return value in ['True', 'TRUE', 'true', '1']

