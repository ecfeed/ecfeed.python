from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.select import Select

import sys
sys.path.append("..")

from test_config import Config

import pytest
import time

# The driver should be placed in the '/usr/bin/' directory.

# ---------------------------------------------------------

endpoint = "http://www.workshop-2021-december.ecfeed.com?mode=error"

form = {
    "execute": ["submit"],
    "output": ["status", "response"],
    "input": [["name", "address", "quantity", "phone", "email"], ["country", "product", "color", "size", "payment", "delivery"]]
}

test_provider = Config.get_test_provider_workshop()

driver = webdriver.Firefox()

# ---------------------------------------------------------

def set_form(values):
    validate_values(form["input"], values)

    set_form_text(values[0])
    set_form_combo(values[1])

def validate_values(reference, values):

    if len(values) != 2:
        raise Exception("The dimension of the input array is incorrect.")
        
    if len(reference[0]) != len(values[0]): 
        raise Exception("The number of the input text fields is incorrect.")
        
    if len(reference[1]) != len(values[1]):
        raise Exception("The number of the input select fields is incorrect.")

def set_form_text(values):
    for i in range(len(form["input"][0])):
        element = driver.find_element_by_id(form["input"][0][i])
        element.clear()
        element.send_keys(values[i])
        
def set_form_combo(values):
    for i in range(len(form["input"][1])):
        Select(driver.find_element_by_id(form["input"][1][i])).select_by_visible_text(values[i])

def execute():
    for element in form["execute"]:
        driver.find_element_by_id(element).click()

def get_response():
    response = []

    for i in range(len(form["output"])):
        response.append(driver.find_element_by_id(form["output"][i]).get_attribute("value"))

    return response
    
# ---------------------------------------------------------

def set_selenium_form(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_handle):
    timeStart = time.time()

    try:
        set_form([[Name, Address, Quantity, Phone, Email], [Country, Product, Color, Size, Payment, Delivery]])
        execute()
    except NoSuchElementException as err:
        assert False, test_handle.add_feedback(False, comment=err.msg, custom={'Error type': 'Input'})
    
    timeEnd = time.time()

    return {
        "response": get_response(),
        "time": int(1000 * (timeEnd - timeStart))
    }

def process_selenium_results(response, test_handle):
    
    assert response["response"][0] == " Request accepted", test_handle.add_feedback(False, duration=response["time"], comment=''.join(e + ' ' for e in response["response"]), custom={'Error type': 'Output'})
    
    test_handle.add_feedback(True, duration=response["time"])

# ---------------------------------------------------------

@pytest.fixture(scope='session', autouse=True)
def setup():
    driver.get(endpoint) 
    yield driver
    driver.close()

@pytest.mark.parametrize(test_provider.test_header(Config.F_WORKSHOP, feedback=True), test_provider.nwise(method=Config.F_WORKSHOP, feedback=True))
def test_method_random(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_handle):

    response = set_selenium_form(Country, Name, Address, Product, Color, Size, Quantity, Payment, Delivery, Phone, Email, test_handle)
    time.sleep(1)
    process_selenium_results(response, test_handle)

    
    