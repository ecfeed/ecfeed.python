import ecfeed
from ecfeed import TestProvider, DataSource, TemplateType
import pytest
import sys
import os
import json
import random
import time

# ---------------------------------------------------------

ecfeed = TestProvider(model='BL2H-B2FZ-JTEL-TB4O-YS1U')
method = 'QuickStart.test'

# @pytest.mark.parametrize(ecfeed.test_header(method), ecfeed.generate_random(method=method, length=5))
# def test_method_1(arg1, arg2, arg3):
#     assert random.random() < 0.5

# @pytest.mark.parametrize("data", ecfeed.generate_random(method=method, length=5))
# def test_method_2(data):
#     print(data)

# Unfortunately we have to use the 'feedback' flag twice. Those are two unrelated methods... The first one defines argument names, the second one provides values.
# @pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.generate_cartesian(method=method, choices={'arg1' : ['choice1', 'choice2'], 'arg2' : ['choice2', 'choice3']}, feedback=True))
# def test_method_3(arg1, arg2, arg3, test_id):
#     assert random.random() < 0.5, ecfeed.feedback(test_id, False, "bad")
#     ecfeed.feedback(test_id, True, "good")

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.random(method='QuickStart.test', length=10, feedback=True))
# def test_method_4(arg1, arg2, arg3, test_id):
#     assert random.random() < 0.5, ecfeed.feedback(test_id, False)
#     ecfeed.feedback(test_id, True)

# @pytest.mark.parametrize(["data", "test_id"], ecfeed.export_random(method=method, length=5, template=TemplateType.JSON, feedback=True))
# def test_method_4(data, test_id):
#     print(data)
#     ecfeed.feedback(test_id, True)

# ---------------------------------------------------------

@pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_10x10 ', feedback=True), ecfeed.nwise(method='com.example.test.Playground.size_10x10', feedback=True))
def test_method_4(a, b, c, d, e, f, g, h, i, j, test_id):
    print()
    assert not (a == 'a0') and not(b == 'b1') and not (h == 'h6'), ecfeed.feedback(test_id, False, duration=int(time.time())+2000)
    ecfeed.feedback(test_id, True, comment='Works')