import ecfeed
from ecfeed import TestProvider, DataSource, TemplateType
import pytest
import sys
import os
import json
import random
import time

# ---------------------------------------------------------

ecfeed = TestProvider(model='IMHL-K0DU-2U0I-J532-25J9')
method = 'QuickStart.test'

# ---------------------------------------------------------

method1 = 'com.example.test.Playground.size_10x10'

def condition_1(a, b, c, d, e, f, g, h, i, j):
    return not (a == 'a0') and not(b == 'b1') and not (h == 'h6')

@pytest.mark.parametrize(ecfeed.test_header(method1, feedback=True), ecfeed.nwise(method=method1, feedback=True))
def test_method_1a(a, b, c, d, e, f, g, h, i, j, test_id):
    assert condition_1(a, b, c, d, e, f, g, h, i, j), ecfeed.feedback(test_id, False, duration=random.randint(10, 990))
    ecfeed.feedback(test_id, True, comment='OK')

@pytest.mark.parametrize(ecfeed.test_header(method1, feedback=True), ecfeed.random(method=method1, feedback=True, length=random.randint(100, 500)))
def test_method_2a(a, b, c, d, e, f, g, h, i, j, test_id):
    assert condition_1(a, b, c, d, e, f, g, h, i, j), ecfeed.feedback(test_id, False, duration=random.randint(10, 990))
    ecfeed.feedback(test_id, True, comment='OK')

@pytest.mark.parametrize(ecfeed.test_header(method1, feedback=True), ecfeed.random(method=method1, feedback=True, length=random.randint(50, 100), adaptive=False))
def test_method_3a(a, b, c, d, e, f, g, h, i, j, test_id):
    assert condition_1(a, b, c, d, e, f, g, h, i, j), ecfeed.feedback(test_id, False, duration=random.randint(10, 990))
    ecfeed.feedback(test_id, True, comment='OK')

@pytest.mark.parametrize(ecfeed.test_header(method1, feedback=True), ecfeed.random(method=method1, feedback=True, length=random.randint(50, 100), adaptive=True, duplicates=True))
def test_method_4a(a, b, c, d, e, f, g, h, i, j, test_id):
    assert condition_1(a, b, c, d, e, f, g, h, i, j), ecfeed.feedback(test_id, False, duration=random.randint(10, 990))
    ecfeed.feedback(test_id, True, comment='OK')

@pytest.mark.parametrize(ecfeed.test_header(method1, feedback=True), ecfeed.random(method=method1, feedback=True, length=random.randint(2000, 5000)))
def test_method_5a(a, b, c, d, e, f, g, h, i, j, test_id):
    assert condition_1(a, b, c, d, e, f, g, h, i, j), ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True, comment='OK')

# ---------------------------------------------------------

method2 = 'QuickStart.test'

def condition_2(arg1, arg2, arg3):
    return arg1 < 2

@pytest.mark.parametrize(ecfeed.test_header(method2, feedback=True), ecfeed.random(method=method2, length=20, feedback=True))
def test_method_1b(arg1, arg2, arg3, test_id):
    assert condition_2(arg1, arg2, arg3), ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header(method2, feedback=True), ecfeed.cartesian(method=method2, feedback=True))
def test_method_2b(arg1, arg2, arg3, test_id):
    assert condition_2(arg1, arg2, arg3), ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header(method2, feedback=True), ecfeed.nwise(method=method2, feedback=True))
def test_method_3b(arg1, arg2, arg3, test_id):
    assert condition_2(arg1, arg2, arg3), ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header(method2, feedback=True), ecfeed.nwise(method=method2, feedback=True, label='Test session label', constraints='ALL', choices='ALL', custom={'first':'uno', 'second':'dos'}))
def test_method_4b(arg1, arg2, arg3, test_id):
    assert condition_2(arg1, arg2, arg3), ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header(method2, feedback=True), ecfeed.nwise(method=method2, feedback=True, constraints=['constraint1','constraint2'], choices={'arg1':['choice1','choice2'], 'arg2':['choice1','choice2','choice3']}, custom={'first':'uno', 'second':'dos'}))
def test_method_5b(arg1, arg2, arg3, test_id):
    assert condition_2(arg1, arg2, arg3), ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header(method2, feedback=True), ecfeed.static_suite(method=method2, feedback=True, test_suites='ALL'))
def test_method_6b(arg1, arg2, arg3, test_id):
    assert condition_2(arg1, arg2, arg3), ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header(method2, feedback=True), ecfeed.static_suite(method=method2, feedback=True, test_suites=['suite1']))
def test_method_7b(arg1, arg2, arg3, test_id):
    assert condition_2(arg1, arg2, arg3), ecfeed.feedback(test_id, False, duration=random.randint(10, 990))
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header(method2, feedback=True), ecfeed.nwise(method=method2, feedback=True, label='Lorem ipsum dolor sit amet.'))
def test_method_8b(arg1, arg2, arg3, test_id):
    assert condition_2(arg1, arg2, arg3), ecfeed.feedback(test_id, False, comment='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', custom={'first':'uno', 'second':'dos'})
    ecfeed.feedback(test_id, True)

# ---------------------------------------------------------

method3 = 'com.example.test.Playground.size_100x2'

def condition_3(a, b):
    return not (a == 'a00') and not (b == 'b00')

@pytest.mark.parametrize(ecfeed.test_header(method3, feedback=True), ecfeed.nwise(method=method3, feedback=True))
def test_method_1c(a, b, test_id):
    assert condition_3(a, b), ecfeed.feedback(test_id, False, duration=random.randint(10, 990))
    ecfeed.feedback(test_id, True, comment='OK')

@pytest.mark.parametrize(ecfeed.test_header(method3, feedback=True), ecfeed.random(method=method3, feedback=True, length=random.randint(1000, 10000)))
def test_method_2c(a, b, test_id):
    assert condition_3(a, b), ecfeed.feedback(test_id, False, duration=random.randint(10, 990))
    ecfeed.feedback(test_id, True, comment='OK')

@pytest.mark.parametrize(ecfeed.test_header(method3, feedback=True), ecfeed.random(method=method3, feedback=True, length=100))
def test_method_3c(a, b, test_id):
    assert condition_3(a, b), ecfeed.feedback(test_id, False, duration=random.randint(10, 990))
    ecfeed.feedback(test_id, True, comment='OK')

