import pytest
from ecfeed import EcFeed, TemplateType, DataSource

ecfeed = EcFeed(keystore_path='./security.p12', model='0168-4412-8644-9433-6380')

#### access to generators in python code
#### NWISE ####
# for line in ecfeed.nwise('TestClass.method', n=3, template=TemplateType.Gherkin):
#     print(line)

#### PAIRWISE ####
# for line in ecfeed.pairwise('TestClass.method', template=TemplateType.XML, coverage=30):
#     print(line)

#### CARTESIAN ####
# for line in ecfeed.cartesian('TestClass.method', choices={'arg1':['choice1'], 'arg3':['choice2', 'choice4']}): #No template!
#     print(line)

#### RANDOM ####
# for line in ecfeed.random('TestClass.method', length=5, duplicates=True, adaptive=True, template=TemplateType.JSON):
#     print(line)

#### STATIC ####
# for line in ecfeed.static_suite('TestClass.method', test_suites=['suite1', 'suite2'], template=TemplateType.XML): 
#     print(line)
# for line in ecfeed.static_suite('TestClass.method', template=TemplateType.JSON): #All suites by default
#     print(line)

class TestedClass:
    @pytest.mark.parametrize(ecfeed.method_arg_names(method_name='TestClass.method'), ecfeed.random(method='TestClass.method', length=5))
    def test_method_1(self, arg1, arg2, arg3, arg4, arg5):
        print('method(' + str(arg1) + ', ' + str(arg2) + ', ' + str(arg3) + ', ' + str(arg4) + ', ' + str(arg5) + ')')

