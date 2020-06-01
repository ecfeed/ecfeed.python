import ecfeed
from ecfeed import TestProvider, DataSource, TemplateType
import pytest
import sys
import os
import json

ecfeed = TestProvider(model='U6C5-Q7VP-VAS3-5HW3-QG2Z', genserver='develop-gen.ecfeed.com')    

@pytest.mark.parametrize(ecfeed.method_arg_names(method_name='com.example.test.TestClass2.testMethod2'), ecfeed.generate_random(method='com.example.test.TestClass2.testMethod2', length=5))
def test_method_1(arg0, arg1, arg2, arg3, arg4, arg5):
    print('method(' + str(arg0) + ', ' + str(arg1) + ', ' + str(arg2) + ', ' + str(arg3) + ', ' + str(arg4) + ', ' + str(arg5) + ')')

def main():

    for line in ecfeed.method_arg_names(method_name='com.example.test.TestClass2.testMethod2'):
        print(line)

    for line in ecfeed.method_arg_types(method_name='com.example.test.TestClass2.testMethod2'):
        print(line)

    for line in ecfeed.export_nwise(method='com.example.test.TestClass2.testMethod2', n='2', template='XML'):
        print(line)

    for line in ecfeed.generate_nwise(method='com.example.test.TestClass2.testMethod2', n='2'):
        print(line)

    for line in ecfeed.export_pairwise(method='com.example.test.TestClass2.testMethod2', template='XML'):
        print(line)

    for line in ecfeed.generate_pairwise(method='com.example.test.TestClass2.testMethod2'):
        print(line)

    for line in ecfeed.export_cartesian(method='com.example.test.TestClass2.testMethod2', template='XML' ):
        print(line)

    for line in ecfeed.generate_cartesian(method='com.example.test.TestClass2.testMethod2'):
        print(line)

    for line in ecfeed.export_random(method='com.example.test.TestClass2.testMethod2', length='2', adaptive='false', duplicates='false', template='XML'):
        print(line)

    for line in ecfeed.generate_random(method='com.example.test.TestClass2.testMethod2', length='2', adaptive='false', duplicates='false', template='XML'):
        print(line)

    for line in ecfeed.export_static_suite(method='com.example.test.TestClass2.testMethod2', test_suites=['default'], template='XML'):
        print(line)

    for line in ecfeed.generate_static_suite(method='com.example.test.TestClass2.testMethod2', test_suites=['default'], template='XML'):
        print(line)
   

if __name__ == "__main__":
    main()

# python3 ecfeed_cli.py --model="U6C5-Q7VP-VAS3-5HW3-QG2Z" --method="com.example.test.TestClass2.testMethod2" --generate_pairwise --genserver="develop-gen.ecfeed.com" --template="JSON"