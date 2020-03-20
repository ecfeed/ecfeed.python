import pytest

from ecfeed import EcFeed

ecfeed = EcFeed(keystore='./security.p12', model='0168-4412-8644-9433-6380', 
                package='com.example.test', classname='TestClass1')



class TestEcFeed:

    @pytest.mark.parametrize(ecfeed.method_arg_names(method_name='testMethod1(int,int,int)'), ecfeed.random('testMethod1(int,int,int)', length=5))
    def test_args(self, arg1, arg2, arg3):
        print('test_args(' + str(arg1) + ' ' + str(arg2) + ' ' + str(arg3) + ')')


# try:
# context = Context(keystore='./security.p12')
# ecfeed=EcFeed(keystore='./security1.p12', model='0168-4412-8644-9433-6380', 
#                   package='com.example.test', classname='TestClass1')

# for line in ecfeed.random(method='testMethod1(int,int,int)', length=4, adaptive=True, duplicates=True):
#     print(line)
# for line in ecfeed.static_suite(method='testMethod1(int,int,int)', test_suites=['default', 'cycki'], template=TemplateType.CSV):
#     print(line)

# method_info = ecfeed.method_info(method='testMethod1(int,int,int)')
# print(str(method_info))
# print(str(ecfeed.method_arg_names(method_info)))
# print(str(ecfeed.method_arg_types(method_info)))

# ecfeed_gen.nwise(N=2, method='testMethod1')
# ecfeed.nwise(N=1, method='testMethod1(int,int,int)')
# ecfeed.pairwise(method='testMethod1(int,int,int)')
# ecfeed.nwise(N=2, method = 'testMethod1(int,int,int,int,int,int,int,int,int,int,int)')
# ecfeed.cartesian(method='testMethod1(int,int,int)')
# ecfeed.random(method='testMethod1(int,int,int)', length=10, adaptive=True, duplicates=True, template=TemplateType.XML)

# class EcFeed:
#     def __init__(self, **kwargs):
#         self.generator = EcFeedGenerator(**kwargs)  

#     def generate_args(self, generator, method):
#         method_info = self.method_info(method=method)
#         types_info = self.method_arg_types(method_info=method_info)
#         for line in generator:
#             parsed_line = json.loads(line)
#             if 'testCase' in line:
#                 args_strings = [arg['value'] for arg in parsed_line['testCase']]
#                 result = [self.__cast(val) for val in list(zip(args_strings, types_info))]
#                 yield result

#     def nwise(self, method, n, coverage=100, **kwargs):
#         yield from self.generate_args(self.generator.nwise(method=method, n=n, coverage=coverage, **kwargs), method=method)

#     def pairwise(self, method, coverage=100, **kwargs):
#         yield from self.generate_args(self.generator.pairwise(method=method, coverage=coverage, **kwargs), method=method)

#     def cartesian(self, method, **kwargs):
#         yield from self.generate_args(self.generator.cartesian(method=method, **kwargs), method=method)

#     def random(self, method, length, adaptive=True, duplicates=False, **kwargs):
#         yield from self.generate_args(self.generator.random(method=method, length=length, adaptive=adaptive, duplicates=duplicates, **kwargs), method=method)

#     def method_arg_names(self, method_info):
#         return [i[1] for i in method_info['args']]

#     def method_arg_types(self, method_info):
#         return [i[0] for i in method_info['args']]

#     def method_info(self, method):
#         for line in self.generator.random(method=method, length=0):
#             line = line.replace('"{', '{').replace('}"', '}').replace('\'', '"')#fix wrong formatting in some versions of the gen-server
#             parsed = json.loads(line)
#             if 'info' in parsed :
#                 method_name = parsed['info']['method']
#                 method_info = self.__parse_method_info_line(method_name)
#         return method_info

#     def __parse_method_info_line(self, method_info_line):
#         result={}
#         full_method_name = method_info_line[0:method_info_line.find('(')]
#         method_args = method_info_line[method_info_line.find('(')+1:-1]
#         full_class_name = full_method_name[0:full_method_name.rfind('.')]
#         result['package_name'] = full_class_name[0:full_class_name.rfind('.')]
#         result['class_name'] = full_class_name[full_class_name.rfind('.')+1:-1]
#         result['method_name'] = full_method_name[full_method_name.rfind('.')+1:-1]
#         args=[]
#         for arg in method_args.split(','):
#             args.append(arg.strip().split(' '))
#         result['args'] = args
#         return result



   
# ecfeed = EcFeed(keystore='./security.p12', model='0168-4412-8644-9433-6380', 
#                 package='com.example.test', classname='TestClass1')


# for line in ecfeed.random('testMethod1(int,int,int)', length=10):
#     print(str(line))

