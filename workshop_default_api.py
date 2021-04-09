import ecfeed
from ecfeed import TestProvider, DataSource, TemplateType
import pytest
import time
import json
import requests

# ---------------------------------------------------------

configuration = {
    "mode": "error",
    "endpoint": "https://api.ecfeed.com/"
}

ecfeed = TestProvider(model='6EG2-YL4S-LMAK-Y5VW-VPV9')
method = 'com.example.test.Demo.typeString'

# ---------------------------------------------------------

def send_request(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email):

    parameters = {
        "mode": configuration["mode"],
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

    return requests.post(configuration["endpoint"], params=parameters)

def process_request(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email):
    
    timeStart = time.time()
    response = send_request(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email)
    timeEnd = time.time()

    return {
        "response": response,
        "time": int(1000 * (timeEnd - timeStart)),
        "error": {
            "input": response.json()['errorInput'],
            "output": response.json()['errorOutput']
        }
    }

def process_response(response, test_id):
    
    assert len(response["error"]["input"]) == 0, ecfeed.feedback(test_id, False, duration=response["time"], comment=''.join('- ' + e + ' ' for e in response["error"]["input"]), custom={'Error type': 'Input'})
    assert len(response["error"]["output"]) == 0, ecfeed.feedback(test_id, False, duration=response["time"], comment=''.join('- ' + e + ' ' for e in response["error"]["output"]), custom={'Error type': 'Output'})
    
    ecfeed.feedback(test_id, True, duration=response["time"])

# ---------------------------------------------------------

@pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.nwise(method=method, feedback=True))
def test_method_nwise(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_id):

    response = process_request(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email)
    process_response(response, test_id)

    