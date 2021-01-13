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

# @pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_10x10 ', feedback=True), ecfeed.nwise(method='com.example.test.Playground.size_10x10', feedback=True))
# def test_method_1a(a, b, c, d, e, f, g, h, i, j, test_id):
#     print()
#     assert not (a == 'a0') and not(b == 'b1') and not (h == 'h6'), ecfeed.feedback(test_id, False, duration=int(time.time())+2000)
#     ecfeed.feedback(test_id, True, comment='Works')

# @pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_10x10 ', feedback=True), ecfeed.random(method='com.example.test.Playground.size_10x10', feedback=True, length=50))
# def test_method_2a(a, b, c, d, e, f, g, h, i, j, test_id):
#     print()
#     assert not (a == 'a0') and not(b == 'b1') and not (h == 'h6'), ecfeed.feedback(test_id, False, duration=int(time.time())+2000)
#     ecfeed.feedback(test_id, True, comment='Works')

# @pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_10x10 ', feedback=True), ecfeed.random(method='com.example.test.Playground.size_10x10', feedback=True, length=50, adaptive=False))
# def test_method_3a(a, b, c, d, e, f, g, h, i, j, test_id):
#     print()
#     assert not (a == 'a0') and not(b == 'b1') and not (h == 'h6'), ecfeed.feedback(test_id, False, duration=int(time.time())+2000)
#     ecfeed.feedback(test_id, True, comment='Works')

# @pytest.mark.parametrize(ecfeed.test_header('com.example.test.Playground.size_10x10 ', feedback=True), ecfeed.random(method='com.example.test.Playground.size_10x10', feedback=True, length=50, adaptive=True, duplicates=True))
# def test_method_4a(a, b, c, d, e, f, g, h, i, j, test_id):
#     print()
#     assert not (a == 'a0') and not(b == 'b1') and not (h == 'h6'), ecfeed.feedback(test_id, False, duration=int(time.time())+2000)
#     ecfeed.feedback(test_id, True, comment='Works')

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.random(method='QuickStart.test', length=20, feedback=True))
# def test_method_2a(arg1, arg2, arg3, test_id):
#     assert arg1 < 2, ecfeed.feedback(test_id, False)
#     ecfeed.feedback(test_id, True)

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.cartesian(method='QuickStart.test', feedback=True))
# def test_method_2b(arg1, arg2, arg3, test_id):
#     assert arg1 < 2, ecfeed.feedback(test_id, False)
#     ecfeed.feedback(test_id, True)

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.nwise(method='QuickStart.test', feedback=True))
# def test_method_2c(arg1, arg2, arg3, test_id):
#     assert arg1 < 2, ecfeed.feedback(test_id, False)
#     ecfeed.feedback(test_id, True)

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.nwise(method='QuickStart.test', feedback=True,
# test_session_label='Test session label', constraints='ALL', choices='ALL', custom={'first':'uno', 'second':'dos'}))
# def test_method_2d(arg1, arg2, arg3, test_id):
#     assert arg1 < 2, ecfeed.feedback(test_id, False)
#     ecfeed.feedback(test_id, True)

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.nwise(method='QuickStart.test', feedback=True,
# test_session_label='Test session label', constraints=['constraint1','constraint2'], choices={'arg1':['choice1','choice2'], 'arg2':['choice1','choice2','choice3']}, custom={'first':'uno', 'second':'dos'}))
# def test_method_2e(arg1, arg2, arg3, test_id):
#     assert arg1 < 2, ecfeed.feedback(test_id, False)
#     ecfeed.feedback(test_id, True)

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.static_suite(method='QuickStart.test', feedback=True,
# test_suites='ALL'))
# def test_method_2f(arg1, arg2, arg3, test_id):
#     assert arg1 < 2, ecfeed.feedback(test_id, False)
#     ecfeed.feedback(test_id, True)

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.static_suite(method='QuickStart.test', feedback=True,
# test_suites=['suite1']))
# def test_method_2g(arg1, arg2, arg3, test_id):
#     assert arg1 < 2, ecfeed.feedback(test_id, False)
#     ecfeed.feedback(test_id, True)

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.nwise(method='QuickStart.test', feedback=True,
# test_session_label='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'))
# def test_method_2h(arg1, arg2, arg3, test_id):
#     assert arg1 < 2, ecfeed.feedback(test_id, False)
#     ecfeed.feedback(test_id, True)

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.nwise(method='QuickStart.test', feedback=True,
# test_session_label='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'))
# def test_method_2i(arg1, arg2, arg3, test_id):
#     assert arg1 < 2, ecfeed.feedback(test_id, False, comment='Comment', custom={'first':'uno', 'second':'dos'})
#     ecfeed.feedback(test_id, True)

# @pytest.mark.parametrize(ecfeed.test_header('QuickStart.test', feedback=True), ecfeed.nwise(method='QuickStart.test', feedback=True,
# test_session_label='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'))
# def test_method_2j(arg1, arg2, arg3, test_id):
#     assert arg1 < 2, ecfeed.feedback(test_id, False, comment='Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.', custom={'first':'uno', 'second':'dos'})
#     ecfeed.feedback(test_id, True)