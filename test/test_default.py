import sys
sys.path.append("..")

from test_config import Config
import pytest

test_provider = Config.get_test_provider()

@pytest.mark.parametrize(test_provider.test_header(Config.F_LOAN_2), test_provider.generate_nwise(method=Config.F_LOAN_2))
def test_provider_nwise(familyName, firstName, gender, age, documentSerialNumber, documentType):
    print("\n" + "familyName = " + familyName + ", firstName = " + firstName + ", gender = " + str(gender) + ", age = " + str(age) + ", id = " + documentSerialNumber + ", type = " + str(documentType))