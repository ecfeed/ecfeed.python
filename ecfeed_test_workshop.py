import ecfeed
from ecfeed import TestProvider, DataSource, TemplateType
import pytest
import time
import json
import requests

# ---------------------------------------------------------

ecfeed = TestProvider(model='LANG-A4RD-MZ18-0G7M-KXXT')
method = 'com.example.test.Demo.typeString'
endpoint = 'https://api.ecfeed.com/'

# @pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.random(method=method, feedback=True, length=1))
# def test_method_error_output(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_id):
    
#     parameters = {
#         "mode": 'error',
#         "country": 'Norway',
#         "name": Name,
#         "address": Address,
#         "product": Product,
#         "color": Color,
#         "size": Size,
#         "quantity": '0',
#         "payment": Payment,
#         "delivery": Delivery,
#         "phone": '+48123456789',
#         "email": Email
#     }

#     timeStart = time.time()
#     response = requests.post(endpoint, params=parameters)
#     timeEnd = time.time()

#     timeTotal = int(1000 * (timeEnd - timeStart))

#     errorInput = response.json()['errorInput']
#     errorOutput = response.json()['errorOutput']

#     assert len(errorInput) == 0, ecfeed.feedback(test_id, False, duration=timeTotal, comment=''.join('- ' + e + ' ' for e in errorInput), custom={'Error type': 'Input'})
#     assert len(errorOutput) == 0, ecfeed.feedback(test_id, False, duration=timeTotal, comment=''.join('- ' + e + ' ' for e in errorOutput), custom={'Error type': 'Output'})

#     ecfeed.feedback(test_id, True, duration=timeTotal)

# @pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.random(method=method, feedback=True, length=1))
# def test_method_error_input(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_id):
    
#     parameters = {
#         "mode": 'error',
#         "country": Country,
#         "name": Name,
#         "address": Address,
#         "product": Product,
#         "color": 'pink',
#         "size": Size,
#         "quantity": Quantity,
#         "payment": Payment,
#         "delivery": Delivery,
#         "phone": Phone,
#         "email": Email
#     }

#     timeStart = time.time()
#     response = requests.post(endpoint, params=parameters)
#     timeEnd = time.time()

#     timeTotal = int(1000 * (timeEnd - timeStart))

#     errorInput = response.json()['errorInput']
#     errorOutput = response.json()['errorOutput']

#     assert len(errorInput) == 0, ecfeed.feedback(test_id, False, duration=timeTotal, comment=''.join('- ' + e + ' ' for e in errorInput), custom={'Error type': 'Input'})
#     assert len(errorOutput) == 0, ecfeed.feedback(test_id, False, duration=timeTotal, comment=''.join('- ' + e + ' ' for e in errorOutput), custom={'Error type': 'Output'})

#     ecfeed.feedback(test_id, True, duration=timeTotal)

@pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.nwise(method=method, feedback=True))
def test_method_nwise(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_id):
    
    parameters = {
        "mode": 'error',
        "country": Country,
        "name": Name,
        "address": Address,
        "product": Product,
        "color": Color,
        "size": Size,
        "quantity": Quantity,
        "payment": Payment,
        "delivery": Delivery,
        "phone": Phone,
        "email": Email
    }

    timeStart = time.time()
    response = requests.post(endpoint, params=parameters)
    timeEnd = time.time()

    timeTotal = int(1000 * (timeEnd - timeStart))

    errorInput = response.json()['errorInput']
    errorOutput = response.json()['errorOutput']

    assert len(errorInput) == 0, ecfeed.feedback(test_id, False, duration=timeTotal, comment=''.join('- ' + e + ' ' for e in errorInput), custom={'Error type': 'Input'})
    assert len(errorOutput) == 0, ecfeed.feedback(test_id, False, duration=timeTotal, comment=''.join('- ' + e + ' ' for e in errorOutput), custom={'Error type': 'Output'})

    ecfeed.feedback(test_id, True, duration=timeTotal)

# @pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.random(method=method, feedback=True, length=1000))
# def test_method_random(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_id):
    
#     parameters = {
#         "mode": 'error',
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

#     timeStart = time.time()
#     response = requests.post(endpoint, params=parameters)
#     timeEnd = time.time()

#     timeTotal = int(1000 * (timeEnd - timeStart))

#     errorInput = response.json()['errorInput']
#     errorOutput = response.json()['errorOutput']

#     assert len(errorInput) == 0, ecfeed.feedback(test_id, False, duration=timeTotal, comment=''.join('- ' + e + ' ' for e in errorInput), custom={'Error type': 'Input'})
#     assert len(errorOutput) == 0, ecfeed.feedback(test_id, False, duration=timeTotal, comment=''.join('- ' + e + ' ' for e in errorOutput), custom={'Error type': 'Output'})

#     ecfeed.feedback(test_id, True, duration=timeTotal)

# @pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.random(method=method, feedback=True, length=1000, constraints='NONE'))
# def test_method_random_no_constraints(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_id):
    
#     parameters = {
#         "mode": 'error',
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

#     timeStart = time.time()
#     response = requests.post(endpoint, params=parameters)
#     timeEnd = time.time()

#     timeTotal = int(1000 * (timeEnd - timeStart))

#     errorInput = response.json()['errorInput']
#     errorOutput = response.json()['errorOutput']

#     assert len(errorInput) == 0, ecfeed.feedback(test_id, False, duration=timeTotal, comment=''.join('- ' + e + ' ' for e in errorInput), custom={'Error type': 'Input'})
#     assert len(errorOutput) == 0, ecfeed.feedback(test_id, False, duration=timeTotal, comment=''.join('- ' + e + ' ' for e in errorOutput), custom={'Error type': 'Output'})

#     ecfeed.feedback(test_id, True, duration=timeTotal)