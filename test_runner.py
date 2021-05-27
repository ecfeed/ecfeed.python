import ecfeed
from ecfeed import TestProvider
import pytest
import random

# ---------------------------------------------------------

ecfeed = TestProvider(model='IMHL-K0DU-2U0I-J532-25J9')

method_10_10 = 'com.example.test.Playground.size_10x10'
method_100_2 = 'com.example.test.Playground.size_100x2'
method_test = 'QuickStart.test'

def validate_f_10_10(a, b, c, d, e, f, g, h, i, j):
    return not (a == 'a0') and not (b == 'b1') and not (h == 'h6')

@pytest.mark.parametrize(ecfeed.test_header(method_10_10, feedback=True), ecfeed.random(method=method_10_10, feedback=True, 
    length=1, label="Random / Quantity - Single"))
def test_gen_random_quantity_single_1(a, b, c, d, e, f, g, h, i, j, test_handle):
    assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_10_10, feedback=True), ecfeed.random(method=method_10_10, feedback=True, 
    length=random.randint(100, 500), label="Random / Quantity - Short"))
def test_gen_random_quantity_short_1(a, b, c, d, e, f, g, h, i, j, test_handle):
    assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_10_10, feedback=True), ecfeed.random(method=method_10_10, feedback=True, 
    length=random.randint(1000, 5000), label="Random / Quantity - Long"))
def test_gen_random_quantity_long_1(a, b, c, d, e, f, g, h, i, j, test_handle):
    assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_10_10, feedback=True), ecfeed.random(method=method_10_10, feedback=True, 
    length=1, custom={"key1":"value1", "key2":"value2"}, label="Random / Custom"))
def test_gen_random_quantity_custom_1(a, b, c, d, e, f, g, h, i, j, test_handle):
    assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_10_10, feedback=True), ecfeed.nwise(method=method_10_10, feedback=True, 
    label="NWise"))
def test_gen_nwise_1(a, b, c, d, e, f, g, h, i, j, test_handle):
    assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_10_10, feedback=True), ecfeed.nwise(method=method_10_10, feedback=True, 
    label="NWise / Feedback"))
def test_gen_nwise_feedback_1(a, b, c, d, e, f, g, h, i, j, test_handle):
    assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False, comment="Failed", duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})
    test_handle.add_feedback(True, comment='OK', duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})

# ---------------------------------------------------------

def validate_f_100_2(a, b):
    return not (a == 'a00') and not (b == 'b00')

@pytest.mark.parametrize(ecfeed.test_header(method_100_2, feedback=True), ecfeed.random(method=method_100_2, feedback=True, 
    length=1, label="Random / Quantity - Single"))
def test_gen_random_quantity_single_2(a, b, test_handle):
    assert validate_f_100_2(a, b), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_100_2, feedback=True), ecfeed.random(method=method_100_2, feedback=True, 
    length=random.randint(100, 500), label="Random / Quantity - Short"))
def test_gen_random_quantity_short_2(a, b, test_handle):
    assert validate_f_100_2(a, b), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_100_2, feedback=True), ecfeed.random(method=method_100_2, feedback=True, 
    length=random.randint(1000, 5000), label="Random / Quantity - Long"))
def test_gen_random_quantity_long_2(a, b, test_handle):
    assert validate_f_100_2(a, b), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_100_2, feedback=True), ecfeed.random(method=method_100_2, feedback=True, 
    length=1, custom={"key1":"value1", "key2":"value2"}, label="Random / Custom"))
def test_gen_random_quantity_custom_2(a, b, test_handle):
    assert validate_f_100_2(a, b), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_100_2, feedback=True), ecfeed.nwise(method=method_100_2, feedback=True, 
    label="NWise"))
def test_gen_nwise(a, b, test_handle):
    assert validate_f_100_2(a, b), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_100_2, feedback=True), ecfeed.nwise(method=method_100_2, feedback=True, 
    label="NWise / Feedback"))
def test_gen_nwise_feedback_2(a, b, test_handle):
    assert validate_f_100_2(a, b), test_handle.add_feedback(False, comment="Failed", duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})
    test_handle.add_feedback(True, comment='OK', duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})

# ---------------------------------------------------------

def validate_f_test(arg1, arg2, arg3):
    return arg1 < 2

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.random(method=method_test, feedback=True, 
    length=1, label="Random / Quantity - Single"))
def test_gen_random_quantity_single_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.random(method=method_test, feedback=True, 
    length=random.randint(100, 500), label="Random / Quantity - Short"))
def test_gen_random_quantity_short_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.random(method=method_test, feedback=True, 
    length=random.randint(1000, 5000), label="Random / Quantity - Long"))
def test_gen_random_quantity_long_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.random(method=method_test, feedback=True, 
    label="Random"))
def test_gen_random_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.random(method=method_test, feedback=True, 
    adaptive=False, label="Random - Adaptive"))
def test_gen_random_adaptive_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.random(method=method_test, feedback=True, 
    duplicates=True, label="Random - Duplicates"))
def test_gen_random_duplicates_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.nwise(method=method_test, feedback=True, 
    label="NWise"))
def test_gen_nwise_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.nwise(method=method_test, feedback=True, 
    n=3, label="NWise - N"))
def test_gen_nwise_n_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.nwise(method=method_test, feedback=True, 
    coverage=50, label="NWise - Coverage"))
def test_gen_nwise_coverage_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.nwise(method=method_test, feedback=True, 
    constraints="NONE", label="NWise / Constraints - None"))
def test_gen_nwise_constraints_none_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.nwise(method=method_test, feedback=True, 
    constraints=["constraint1", "constraint2"], label="NWise / Constraints - Selected"))
def test_gen_nwise_constraints_selected_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.nwise(method=method_test, feedback=True, 
    choices={"arg1":["choice1", "choice2"], "arg2":["choice2", "choice3"]}, label="NWise / Choices - Selected"))
def test_gen_nwise_choices_selected_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.nwise(method=method_test, feedback=True, 
    custom={"key1":"value1", "key2":"value2"}, label="NWise / Custom"))
def test_gen_nwise_custom_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.cartesian(method=method_test, feedback=True, 
    label="Cartesian"))
def test_gen_cartesian_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.static_suite(method=method_test, feedback=True, 
    label="Static"))
def test_gen_static_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.static_suite(method=method_test, feedback=True, 
    test_suites="ALL", label="Static - All"))
def test_gen_static_all_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.static_suite(method=method_test, feedback=True, 
    test_suites=["suite1"], label="Static - All"))
def test_gen_static_selected_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
    test_handle.add_feedback(True)

@pytest.mark.parametrize(ecfeed.test_header(method_test, feedback=True), ecfeed.nwise(method=method_test, feedback=True, 
    label="NWise / Feedback"))
def test_gen_nwise_feedback_3(arg1, arg2, arg3, test_handle):
    assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False, comment="Failed", duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})
    test_handle.add_feedback(True, comment='OK', duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})