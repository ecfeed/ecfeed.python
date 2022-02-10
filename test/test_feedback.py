# import sys
# sys.path.append("..")

# from test_config import Config
# import pytest
# import random

# test_provider = Config.get_test_provider()

# # ---------------------------------------------------------

# def validate_f_10_10(a, b, c, d, e, f, g, h, i, j):
#     return not (a == 'a0') and not (b == 'b1') and not (h == 'h6')

# @pytest.mark.parametrize(test_provider.test_header(Config.F_10x10, feedback=True), test_provider.random(method=Config.F_10x10, feedback=True, 
#     length=1, label="Random / Quantity - Single"))
# def test_gen_random_quantity_single_1(a, b, c, d, e, f, g, h, i, j, test_handle):
#     assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_10x10, feedback=True), test_provider.random(method=Config.F_10x10, feedback=True, 
#     length=random.randint(100, 500), label="Random / Quantity - Short"))
# def test_gen_random_quantity_short_1(a, b, c, d, e, f, g, h, i, j, test_handle):
#     assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_10x10, feedback=True), test_provider.random(method=Config.F_10x10, feedback=True, 
#     length=random.randint(1000, 5000), label="Random / Quantity - Long"))
# def test_gen_random_quantity_long_1(a, b, c, d, e, f, g, h, i, j, test_handle):
#     assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_10x10, feedback=True), test_provider.random(method=Config.F_10x10, feedback=True, 
#     length=1, custom={"key1":"value1", "key2":"value2"}, label="Random / Custom"))
# def test_gen_random_quantity_custom_1(a, b, c, d, e, f, g, h, i, j, test_handle):
#     assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_10x10, feedback=True), test_provider.nwise(method=Config.F_10x10, feedback=True, 
#     label="NWise"))
# def test_gen_nwise_1(a, b, c, d, e, f, g, h, i, j, test_handle):
#     assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_10x10, feedback=True), test_provider.nwise(method=Config.F_10x10, feedback=True, 
#     label="NWise / Feedback"))
# def test_gen_nwise_feedback_1(a, b, c, d, e, f, g, h, i, j, test_handle):
#     assert validate_f_10_10(a, b, c, d, e, f, g, h, i, j), test_handle.add_feedback(False, comment="Failed", duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})
#     test_handle.add_feedback(True, comment='OK', duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})

# # ---------------------------------------------------------

# def validate_f_100_2(a, b):
#     return not (a == 'a00') and not (b == 'b00')

# @pytest.mark.parametrize(test_provider.test_header(Config.F_100x2, feedback=True), test_provider.random(method=Config.F_100x2, feedback=True, 
#     length=1, label="Random / Quantity - Single"))
# def test_gen_random_quantity_single_2(a, b, test_handle):
#     assert validate_f_100_2(a, b), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_100x2, feedback=True), test_provider.random(method=Config.F_100x2, feedback=True, 
#     length=random.randint(100, 500), label="Random / Quantity - Short"))
# def test_gen_random_quantity_short_2(a, b, test_handle):
#     assert validate_f_100_2(a, b), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_100x2, feedback=True), test_provider.random(method=Config.F_100x2, feedback=True, 
#     length=random.randint(1000, 5000), label="Random / Quantity - Long"))
# def test_gen_random_quantity_long_2(a, b, test_handle):
#     assert validate_f_100_2(a, b), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_100x2, feedback=True), test_provider.random(method=Config.F_100x2, feedback=True, 
#     length=1, custom={"key1":"value1", "key2":"value2"}, label="Random / Custom"))
# def test_gen_random_quantity_custom_2(a, b, test_handle):
#     assert validate_f_100_2(a, b), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_100x2, feedback=True), test_provider.nwise(method=Config.F_100x2, feedback=True, 
#     label="NWise"))
# def test_gen_nwise(a, b, test_handle):
#     assert validate_f_100_2(a, b), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_100x2, feedback=True), test_provider.nwise(method=Config.F_100x2, feedback=True, 
#     label="NWise / Feedback"))
# def test_gen_nwise_feedback_2(a, b, test_handle):
#     assert validate_f_100_2(a, b), test_handle.add_feedback(False, comment="Failed", duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})
#     test_handle.add_feedback(True, comment='OK', duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})

# # ---------------------------------------------------------

# def validate_f_test(arg1, arg2, arg3):
#     return arg1 < 2

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.random(method=Config.F_TEST, feedback=True, 
#     length=1, label="Random / Quantity - Single"))
# def test_gen_random_quantity_single_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.random(method=Config.F_TEST, feedback=True, 
#     length=random.randint(100, 500), label="Random / Quantity - Short"))
# def test_gen_random_quantity_short_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.random(method=Config.F_TEST, feedback=True, 
#     length=random.randint(1000, 5000), label="Random / Quantity - Long"))
# def test_gen_random_quantity_long_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.random(method=Config.F_TEST, feedback=True, 
#     label="Random"))
# def test_gen_random_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.random(method=Config.F_TEST, feedback=True, 
#     adaptive=False, label="Random - Adaptive"))
# def test_gen_random_adaptive_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.random(method=Config.F_TEST, feedback=True, 
#     duplicates=True, label="Random - Duplicates"))
# def test_gen_random_duplicates_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.nwise(method=Config.F_TEST, feedback=True, 
#     label="NWise"))
# def test_gen_nwise_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.nwise(method=Config.F_TEST, feedback=True, 
#     n=3, label="NWise - N"))
# def test_gen_nwise_n_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.nwise(method=Config.F_TEST, feedback=True, 
#     coverage=50, label="NWise - Coverage"))
# def test_gen_nwise_coverage_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.nwise(method=Config.F_TEST, feedback=True, 
#     constraints="NONE", label="NWise / Constraints - None"))
# def test_gen_nwise_constraints_none_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.nwise(method=Config.F_TEST, feedback=True, 
#     constraints=["constraint1", "constraint2"], label="NWise / Constraints - Selected"))
# def test_gen_nwise_constraints_selected_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.nwise(method=Config.F_TEST, feedback=True, 
#     choices={"arg1":["choice1", "choice2"], "arg2":["choice2", "choice3"]}, label="NWise / Choices - Selected"))
# def test_gen_nwise_choices_selected_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.nwise(method=Config.F_TEST, feedback=True, 
#     custom={"key1":"value1", "key2":"value2"}, label="NWise / Custom"))
# def test_gen_nwise_custom_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.cartesian(method=Config.F_TEST, feedback=True, 
#     label="Cartesian"))
# def test_gen_cartesian_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.static_suite(method=Config.F_TEST, feedback=True, 
#     label="Static"))
# def test_gen_static_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.static_suite(method=Config.F_TEST, feedback=True, 
#     test_suites="ALL", label="Static - All"))
# def test_gen_static_all_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.static_suite(method=Config.F_TEST, feedback=True, 
#     test_suites=["suite1"], label="Static - All"))
# def test_gen_static_selected_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False)
#     test_handle.add_feedback(True)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_TEST, feedback=True), test_provider.nwise(method=Config.F_TEST, feedback=True, 
#     label="NWise / Feedback"))
# def test_gen_nwise_feedback_3(arg1, arg2, arg3, test_handle):
#     assert validate_f_test(arg1, arg2, arg3), test_handle.add_feedback(False, comment="Failed", duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})
#     test_handle.add_feedback(True, comment='OK', duration=random.randint(100, 200), custom={"key1":"value1", "key2":"value2"})