import ecfeed
from ecfeed import TestProvider, DataSource, TemplateType
import pytest
import sys
import os
import json
import random
import time

# ---------------------------------------------------------

ecfeed = TestProvider(model='7LAP-M2H5-DCN6-YAKW-UKBU') #LRYK-Z4RF-W7AU-EF0Q-MYUF/7LAP-M2H5-DCN6-YAKW-UKBU
method = 'QuickStart.test'

@pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_10x10', feedback=True), ecfeed.nwise(method='com.example.test.Playground.size_10x10', feedback=True))
def test_method_1a(a, b, c, d, e, f, g, h, i, j, test_id):
    assert not (a == 'a0') and not(b == 'b1') and not (h == 'h6'), ecfeed.feedback(test_id, False, duration=int(time.time())+2000)
    ecfeed.feedback(test_id, True, comment='Works')

@pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_10x10 ', feedback=True), ecfeed.random(method='com.example.test.Playground.size_10x10', feedback=True, length=200))
def test_method_2a(a, b, c, d, e, f, g, h, i, j, test_id):
    assert not (a == 'a0') and not(b == 'b1') and not (h == 'h6'), ecfeed.feedback(test_id, False, duration=int(time.time())+2000)
    ecfeed.feedback(test_id, True, comment='Works')

@pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_10x10 ', feedback=True), ecfeed.random(method='com.example.test.Playground.size_10x10', feedback=True, length=50, adaptive=False))
def test_method_3a(a, b, c, d, e, f, g, h, i, j, test_id):
    assert not (a == 'a0') and not(b == 'b1') and not (h == 'h6'), ecfeed.feedback(test_id, False, duration=int(time.time())+2000)
    ecfeed.feedback(test_id, True, comment='Works')

@pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_10x10 ', feedback=True), ecfeed.random(method='com.example.test.Playground.size_10x10', feedback=True, length=50, adaptive=True, duplicates=True))
def test_method_4a(a, b, c, d, e, f, g, h, i, j, test_id):
    assert not (a == 'a0') and not(b == 'b1') and not (h == 'h6'), ecfeed.feedback(test_id, False, duration=int(time.time())+2000)
    ecfeed.feedback(test_id, True, comment='Works')

@pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.random(method='QuickStart.test', length=20, feedback=True))
def test_method_1b(arg1, arg2, arg3, test_id):
    assert arg1 < 2, ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.cartesian(method='QuickStart.test', feedback=True))
def test_method_2b(arg1, arg2, arg3, test_id):
    assert arg1 < 2, ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.nwise(method='QuickStart.test', feedback=True))
def test_method_3b(arg1, arg2, arg3, test_id):
    assert arg1 < 2, ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.nwise(method='QuickStart.test', feedback=True,
label='Test session label', constraints='ALL', choices='ALL', custom={'first':'uno', 'second':'dos'}))
def test_method_4b(arg1, arg2, arg3, test_id):
    assert arg1 < 2, ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.nwise(method='QuickStart.test', feedback=True,
label='Test session label', constraints=['constraint1','constraint2'], choices={'arg1':['choice1','choice2'], 'arg2':['choice1','choice2','choice3']}, custom={'first':'uno', 'second':'dos'}))
def test_method_5b(arg1, arg2, arg3, test_id):
    assert arg1 < 2, ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.static_suite(method='QuickStart.test', feedback=True,
test_suites='ALL'))
def test_method_6b(arg1, arg2, arg3, test_id):
    assert arg1 < 2, ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.static_suite(method='QuickStart.test', feedback=True,
test_suites=['suite1']))
def test_method_7b(arg1, arg2, arg3, test_id):
    assert arg1 < 2, ecfeed.feedback(test_id, False, duration=int(time.time())+2000)
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.nwise(method='QuickStart.test', feedback=True,
label='Lorem ipsum dolor sit amet.'))
def test_method_8b(arg1, arg2, arg3, test_id):
    assert arg1 < 2, ecfeed.feedback(test_id, False, comment='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.', custom={'first':'uno', 'second':'dos'})
    ecfeed.feedback(test_id, True)

@pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_10x10 ', feedback=True), ecfeed.random(method='com.example.test.Playground.size_10x10', feedback=True,
length=2500))
def test_method_9b(a, b, c, d, e, f, g, h, i, j, test_id):
    assert not (a == 'a0') and not(b == 'b1') and not (h == 'h6'), ecfeed.feedback(test_id, False)
    ecfeed.feedback(test_id, True, comment='Size test')

@pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_100x2', feedback=True), ecfeed.nwise(method='com.example.test.Playground.size_100x2', feedback=True))
def test_method_1c(a, b, test_id):
    assert not (a == 'a00') and not(b == 'b00'), ecfeed.feedback(test_id, False, duration=int(time.time()))
    ecfeed.feedback(test_id, True, comment='Works')

@pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_100x2', feedback=True), ecfeed.random(method='com.example.test.Playground.size_100x2', feedback=True, length=random.randint(1000, 10000)))
def test_method_2c(a, b, test_id):
    assert not (a == 'a00') and not(b == 'b00'), ecfeed.feedback(test_id, False, duration=int(time.time()))
    ecfeed.feedback(test_id, True, comment='Works')

@pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_100x2', feedback=True), ecfeed.random(method='com.example.test.Playground.size_100x2', feedback=True, length=100))
def test_method_1d(a, b, test_id):
    assert not (a == 'a00') and not(b == 'b00'), ecfeed.feedback(test_id, False, duration=int(time.time()))
    ecfeed.feedback(test_id, True, comment='Works')

