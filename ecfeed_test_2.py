import ecfeed
from ecfeed import TestProvider, DataSource, TemplateType
import pytest
import sys
import os
import json
import random
import time

# ecfeed = TestProvider(model='2057-8093-8471-3697-1154')
# method = 'com.example.test.TestClass2.testMethod2'

# @pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.generate_random(method=method, length=25, feedback=True))
# def test_method_1(arg0, arg1, arg2, arg3, arg4, arg5, test_id):
#     assert random.random() < 0.5, ecfeed.feedback(test_id, False)
#     ecfeed.feedback(test_id, True)


# ---------------------------------------------------------

ecfeed = TestProvider(model='YVJ1-N3H8-MHI4-1TZG-DJIY')
generator = ecfeed.generate_random(method='QuickStart.test', length=5, feedback=True)

@pytest.mark.parametrize('index', range(20))
def test_one(index):
    test = ecfeed.next(generator)
    # time.sleep(1)
    assert random.random() < 1, ecfeed.feedback(test, False)
    ecfeed.feedback(test, True)

# ---------------------------------------------------------

# python3 ecfeed_cli.py --model="2057-8093-8471-3697-1154" --method="com.example.test.TestClass2.testMethod2" --generate_pairwise --template="JSON"