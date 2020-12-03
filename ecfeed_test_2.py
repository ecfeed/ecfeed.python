import ecfeed
from ecfeed import TestProvider, DataSource, TemplateType
import pytest
import sys
import os
import json
import random
import time

# ---------------------------------------------------------

ecfeed = TestProvider(model='TestUuid11')
method = 'QuickStart.test'

# @pytest.mark.parametrize(ecfeed.test_header(method), ecfeed.generate_random(method=method, length=5))
# def test_method_1(arg1, arg2, arg3):
#     assert random.random() < 0.5

# @pytest.mark.parametrize("data", ecfeed.generate_random(method=method, length=5))
# def test_method_2(data):
#     print(data)

# Unfortunately we have to use the 'feedback' flag twice. Those are two unrelated methods... The first one defines argument names, the second one provides values.
@pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.generate_random(method=method, length=5, feedback=True, label="test"))
def test_method_3(arg1, arg2, arg3, test_id):
    assert random.random() < 0.5, ecfeed.feedback(test_id, False, "bad")
    ecfeed.feedback(test_id, True, "good")

# @pytest.mark.parametrize(["data", "test_id"], ecfeed.export_random(method=method, length=5, template=TemplateType.JSON, feedback=True))
# def test_method_4(data, test_id):
#     print(data)
#     ecfeed.feedback(test_id, True)

# ---------------------------------------------------------