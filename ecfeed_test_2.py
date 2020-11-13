import ecfeed
from ecfeed import TestProvider, DataSource, TemplateType
import pytest
import sys
import os
import json
import random

ecfeed = TestProvider(model='2057-8093-8471-3697-1154')
method = 'com.example.test.TestClass2.testMethod2'

@pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.generate_random(method=method, length=25))
def test_method_1(arg0, arg1, arg2, arg3, arg4, arg5, test_id):
    assert random.random() < 0.5, ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

# def main():

    # for line in ecfeed.method_arg_names(method_name='com.example.test.TestClass2.testMethod2'):
    #     print(line)

    # for line in ecfeed.method_arg_types(method_name='com.example.test.TestClass2.testMethod2'):
    #     print(line)

    # for line in ecfeed.export_nwise(method='com.example.test.TestClass2.testMethod2', n='2', template='XML'):
    #     print(line)

    # for line in ecfeed.generate_nwise(method='com.example.test.TestClass2.testMethod2', n='2'):
    #     print(line)

    # for line in ecfeed.export_pairwise(method='com.example.test.TestClass2.testMethod2', template='XML'):
    #     print(line)

    # for line in ecfeed.generate_pairwise(method='com.example.test.TestClass2.testMethod2'):
    #     print(line)

    # for line in ecfeed.export_cartesian(method='com.example.test.TestClass2.testMethod2', template='XML' ):
    #     print(line)

    # for line in ecfeed.generate_cartesian(method='com.example.test.TestClass2.testMethod2'):
    #     print(line)

    # for line in ecfeed.export_random(method='com.example.test.TestClass2.testMethod2', length='2', adaptive='false', duplicates='false', template='XML'):
    #     print(line)

    # for line in ecfeed.generate_random(method='com.example.test.TestClass2.testMethod2', length='2', adaptive='false', duplicates='false'):
    #     print(line)

    # for line in ecfeed.export_static_suite(method='com.example.test.TestClass2.testMethod2', test_suites=['default'], template='XML'):
    #     print(line)

    # for line in ecfeed.generate_static_suite(method='com.example.test.TestClass2.testMethod2', test_suites=['default']):
    #     print(line)
   

# if __name__ == "__main__":
#     main()

# python3 ecfeed_cli.py --model="2057-8093-8471-3697-1154" --method="com.example.test.TestClass2.testMethod2" --generate_pairwise --template="JSON"