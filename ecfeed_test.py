import pytest
from ecfeed import TestProvider, TemplateType, DataSource
from enum import Enum

ecfeed = TestProvider(model='2037-6847-2110-8251-1296')

#### access to generators in python code
#### NWISE ####
# for line in ecfeed.nwise(method='TestClass.method', n=3, template=TemplateType.Gherkin, coverage=40):
#     print(line)

#### PAIRWISE ####
# for line in ecfeed.pairwise(method='TestClass.method', template=TemplateType.XML, coverage=10):
#     print(line)

#### CARTESIAN ####
# for line in ecfeed.cartesian(method='TestClass.method', coverage=40, choices={'arg1':['choice1'], 'arg3':['choice2', 'choice4']}): #No template!
#     print(line)

#### RANDOM ####
for line in ecfeed.export_random(method='TestClass.method', length=5, duplicates=True, adaptive=True, template=TemplateType.CSV):
    print(line)

#### STATIC ####
# for line in ecfeed.static_suite(method='TestClass.method', test_suites=['suite1'], template=TemplateType.XML): 
#     print(line)
# for line in ecfeed.static_suite('TestClass.method', template=TemplateType.JSON): #All suites by default
#     print(line)

# class TestedClass:
#     @pytest.mark.parametrize(ecfeed.method_arg_names(method_name='TestClass.method'), ecfeed.random(method='TestClass.method', length=5))
#     def test_method_1(self, arg1, arg2, arg3, arg4, arg5):
#         print('method(' + str(arg1) + ', ' + str(arg2) + ', ' + str(arg3) + ', ' + str(arg4) + ', ' + str(arg5) + ')')

############TEST ENUM##############
class MyEnum(Enum):
    VALUE0 = 0
    VALUE1 = 1
    VALUE2 = 2
    VALUE3 = 3
    VALUE4 = 4


# for line in ecfeed.cartesian(method='TestClass.testEnum', coverage=4, choices={'arg1':['choice1'], 'arg3':['choice2', 'choice4']}): #No template!
#     print(line)

# for line in ecfeed.random(method='TestClass.testEnum', length=5, duplicates=True, adaptive=True, template=TemplateType.CSV):
#     print(line)

#class TestedClassWithEnum:
#    @pytest.mark.parametrize(ecfeed.method_arg_names(method_name='TestClass.testEnum'), ecfeed.random(method='TestClass.testEnum', length=5))
#    def test_method_1(self, arg1, arg2, arg3, arg4):
#        print('method(' + str(arg1) + ', ' + str(arg2) + ', ' + str(arg3) + ', ' + str(arg4) + ')')
