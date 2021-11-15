import pytest
from ecfeed import TestProvider, TemplateType, DataSource
from enum import Enum

ecfeed = TestProvider(model='2057-8093-8471-3697-1154')

#################### access to generators in python code #####################
#### NWISE ####
for line in ecfeed.generate_nwise(method='com.example.test.TestClass2.testMethod2', n=3, coverage=40):
    print(line)
for line in ecfeed.export_nwise(method='com.example.test.TestClass2.testMethod2', n=3, coverage=40):
    print(line)

#### PAIRWISE ####
# for line in ecfeed.generate_pairwise(method='TestClass.method', coverage=10, constraints='NONE'):
#     print(line)
# for line in ecfeed.export_pairwise(method='TestClass.method', template=TemplateType.XML, coverage=10):
#     print(line)

#### CARTESIAN ####
# for line in ecfeed.generate_cartesian(method='TestClass.method', coverage=40, choices={'arg1':['choice1'], 'arg3':['choice2', 'choice4']}): 
#     print(line)
# for line in ecfeed.export_cartesian(method='TestClass.method', coverage=40, choices={'arg1':['choice1'], 'arg3':['choice2', 'choice4']}): #No template!
#     print(line)

#### RANDOM ####
# for line in ecfeed.generate_random(method='TestClass.method', length=5, duplicates=True, adaptive=True, constrains=['force_arg1']):
#     print(line)
# for line in ecfeed.export_random(method='TestClass.method', length=5, duplicates=True, adaptive=True, constrains=['force_arg1'], template=TemplateType.CSV):
#     print(line)

#### STATIC ####
# for line in ecfeed.generate_static_suite(method='TestClass.method', test_suites=['suite1']): 
#     print(line)
# for line in ecfeed.export_static_suite(method='TestClass.method', test_suites=['suite1'], template=TemplateType.JSON): #All suites by default
#     print(line)


################################## PYTEST #####################################
# class TestedClass:
#     @pytest.mark.parametrize(ecfeed.method_arg_names(method_name='TestClass.method'), 
#                              ecfeed.generate_random(method='TestClass.method', length=5))
#     def test_method_1(self, arg1, arg2, arg3, arg4, arg5):
#         print('method(' + str(arg1) + ', ' + str(arg2) + ', ' + str(arg3) + ', ' + str(arg4) + ', ' + str(arg5) + ')')

# ############TEST ENUM##############
# class MyEnum(Enum):
#     VALUE0 = 0
#     VALUE1 = 1
#     VALUE2 = 2
#     VALUE3 = 3
#     VALUE4 = 4

# class TestedClassWithEnum:
#    @pytest.mark.parametrize(ecfeed.method_arg_names(method_name='TestClass.testEnum'), 
#                             ecfeed.generate_random(method='TestClass.testEnum', length=5))
#    def test_method_1(self, arg1, arg2, arg3, arg4):
#        print('method(' + str(arg1) + ', ' + str(arg2) + ', ' + str(arg3) + ', ' + str(arg4) + ')')

#################### Example calls for the cli tool #####################
#### NWISE ####
#python3 ./ecfeed_cli.py --model 2037-6847-2110-8251-1296 --method TestClass.method --nwise -n 3 --template XML

#### PAIRWISE ####
#python3 ./ecfeed_cli.py --model 2037-6847-2110-8251-1296 --method TestClass.method --pairwise 

#### CARTESIAN ####
#python3 ./ecfeed_cli.py --model 2037-6847-2110-8251-1296 --method TestClass.method --cartesian --template JSON --choices "{'arg1':['choice1', 'choice2'], 'arg2':['choice3', 'abs:choice4']}"

#### RANDOM ####
#python3 ./ecfeed_cli.py --model 2037-6847-2110-8251-1296 --method TestClass.method --random --keystore ~/ecfeed/security.p12 --template RAW  --length 10 --adaptive --constraints "['force_arg1', 'constraint']"

#### STATIC ####
#python3 ./ecfeed_cli.py --model 2037-6847-2110-8251-1296 --method TestClass.method --static --suites "[suite2]" --template XML
