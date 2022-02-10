# import sys
# sys.path.append("..")

# from test_config import Config

# import pytest
# import time
# import requests

# # ---------------------------------------------------------

# configuration = {
#     "mode": "error",
#     "endpoint": "https://api.ecfeed.com/"
# }

# test_provider = Config.get_test_provider_workshop()

# # ---------------------------------------------------------

# def send_request(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email):

#     parameters = {
#         "mode": configuration["mode"],
#         "country": Country,
#         "name": Name,
#         "address": Address,
#         "product": Product,
#         "color": Color,
#         "size": Size,
#         "quantity": Quantity,
#         "payment": Payment,
#         "delivery": Delivery,
#         "phone": Phone,
#         "email": Email
#     }

#     return requests.post(configuration["endpoint"], params=parameters)

# def process_request(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email):
    
#     timeStart = time.time()
#     response = send_request(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email)
#     timeEnd = time.time()

#     return {
#         "response": response,
#         "time": int(1000 * (timeEnd - timeStart)),
#         "error": {
#             "input": response.json()['errorInput'],
#             "output": response.json()['errorOutput']
#         }
#     }

# def process_response(response, test_handle):
    
#     assert len(response["error"]["input"]) == 0, test_handle.add_feedback(False, duration=response["time"], comment=''.join('- ' + e + ' ' for e in response["error"]["input"]), custom={'Error type': 'Input'})
#     assert len(response["error"]["output"]) == 0, test_handle.add_feedback(False, duration=response["time"], comment=''.join('- ' + e + ' ' for e in response["error"]["output"]), custom={'Error type': 'Output'})
    
#     test_handle.add_feedback(True, duration=response["time"])

# # ---------------------------------------------------------

# @pytest.mark.parametrize(test_provider.test_header(Config.F_WORKSHOP, feedback=True), test_provider.random(method=Config.F_WORKSHOP, feedback=True, length=1))
# def test_method_error_output(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_handle):
    
#     response = process_request("Norway", Name, Address, Product, Color, Size, Quantity, Payment, Delivery, "+48123456789", Email)
#     process_response(response, test_handle)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_WORKSHOP, feedback=True), test_provider.random(method=Config.F_WORKSHOP, feedback=True, length=1))
# def test_method_error_input(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_handle):

#     response = process_request(Country, Name, Address, Product, "pink", Size, Quantity, Payment, Delivery, Phone, Email)
#     process_response(response, test_handle)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_WORKSHOP, feedback=True), test_provider.nwise(method=Config.F_WORKSHOP, feedback=True))
# def test_method_nwise(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_handle):
    
#     response = process_request(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email)
#     process_response(response, test_handle)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_WORKSHOP, feedback=True), test_provider.random(method=Config.F_WORKSHOP, feedback=True, length=1000))
# def test_method_random(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_handle):
    
#     response = process_request(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email)
#     process_response(response, test_handle)

# @pytest.mark.parametrize(test_provider.test_header(Config.F_WORKSHOP, feedback=True), test_provider.random(method=Config.F_WORKSHOP, feedback=True, length=1000, constraints='NONE'))
# def test_method_random_no_constraints(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_handle):
    
#     response = process_request(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email)
#     process_response(response, test_handle)