import json
from enum import Enum

class DataSource(Enum):
    STATIC_DATA = 0
    NWISE = 1
    CARTESIAN = 2
    RANDOM = 3

    def to_url_param(self):
        if self == DataSource.STATIC_DATA:
            return 'static'
        if self == DataSource.NWISE:
            return 'genNWise'
        if self == DataSource.CARTESIAN:
            return 'genCartesian'
        if self == DataSource.RANDOM:
            return 'genRandom'

def prepare_request(method, data_source, gen_args, **kwargs):
    generate_params={}
    generate_params['method'] = ''
    if gen_args['package'] != None:
        generate_params['method'] += gen_args['package'] + '.'
    if gen_args['classname'] != None:
        generate_params['method'] += gen_args['classname'] + '.' 
    generate_params['method'] += method
    generate_params['model'] = gen_args['model']
    generate_params['userData'] = serialize_user_data(data_source=data_source, **kwargs)
    template=kwargs.pop('template', None)
    
    request_type='requestData'
    if template != None:
        generate_params['template'] = str(template)
        request_type='requestExport'

    request = 'https://' + gen_args['genserver'] + '/testCaseService?requestType=' + request_type + '&request='
    request += json.dumps(generate_params).replace(' ', '')
    return request

def serialize_user_data(data_source, **kwargs):
    user_data={}
    user_data['dataSource']=data_source.to_url_param()
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

def parse_test_line(line):
    result = {}
    try:
        parsed_line = json.loads(line)
    except ValueError as e:
        print('Unexpected error while parsing line: "' + line + '": ' + str(e))
    if 'info'  in parsed_line:
        info = parsed_line['info'].replace('\'', '"')
        try:
            result['method'] = parse_method_definition(json.loads(info)['method'])
        except (ValueError, KeyError) as e:
            pass
    elif 'testCase' in parsed_line:
        try:
            result['values'] = [arg['value'] for arg in parsed_line['testCase']]
        except ValueError as e:
            print('Unexpected error when parsing test case line: "' + line + '": ' + str(e))

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

