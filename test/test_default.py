# import sys
# sys.path.append("..")

# from test_config import Config
# from ecfeed import TestProvider
# from ecfeed import TemplateType
# import pytest

# test_provider = Config.get_test_provider()

# @pytest.mark.generate
# @pytest.mark.parametrize(test_provider.test_header(Config.F_LOAN_2), test_provider.generate_nwise(method=Config.F_LOAN_2))
# def test_provider_nwise(familyName, firstName, gender, age, documentSerialNumber, documentType):
#     print("\n" + "familyName = " + familyName + ", firstName = " + firstName + ", gender = " + str(gender) + ", age = " + str(age) + ", id = " + documentSerialNumber + ", type = " + str(documentType))
    
# @pytest.mark.generate    
# @pytest.mark.parametrize(test_provider.test_header(Config.F_LOAN_2), test_provider.generate_pairwise(method=Config.F_LOAN_2))
# def test_provider_pairwise(familyName, firstName, gender, age, documentSerialNumber, documentType):
#     print("\n" + "familyName = " + familyName + ", firstName = " + firstName + ", gender = " + str(gender) + ", age = " + str(age) + ", id = " + documentSerialNumber + ", type = " + str(documentType))
    
# @pytest.mark.generate    
# @pytest.mark.parametrize(test_provider.test_header(Config.F_LOAN_2), test_provider.generate_cartesian(method=Config.F_LOAN_2))
# def test_provider_cartesian(familyName, firstName, gender, age, documentSerialNumber, documentType):
#     print("\n" + "familyName = " + familyName + ", firstName = " + firstName + ", gender = " + str(gender) + ", age = " + str(age) + ", id = " + documentSerialNumber + ", type = " + str(documentType))

# @pytest.mark.generate    
# @pytest.mark.parametrize(test_provider.test_header(Config.F_LOAN_2), test_provider.generate_random(method=Config.F_LOAN_2))
# def test_provider_random(familyName, firstName, gender, age, documentSerialNumber, documentType):
#     print("\n" + "familyName = " + familyName + ", firstName = " + firstName + ", gender = " + str(gender) + ", age = " + str(age) + ", id = " + documentSerialNumber + ", type = " + str(documentType))
    
# @pytest.mark.generate    
# @pytest.mark.parametrize(test_provider.test_header(Config.F_LOAN_2), test_provider.generate_static_suite(method=Config.F_LOAN_2))
# def test_provider_static(familyName, firstName, gender, age, documentSerialNumber, documentType):
#     print("\n" + "familyName = " + familyName + ", firstName = " + firstName + ", gender = " + str(gender) + ", age = " + str(age) + ", id = " + documentSerialNumber + ", type = " + str(documentType))
    
# @pytest.mark.generate    
# @pytest.mark.parametrize(test_provider.test_header(Config.F_LOAN_2, feedback=True), test_provider.generate_nwise(method=Config.F_LOAN_2, feedback=True, label="Test - Default"))
# def test_provider_nwise_feedback(familyName, firstName, gender, age, documentSerialNumber, documentType, test_handle):
#     print("\n" + "familyName = " + familyName + ", firstName = " + firstName + ", gender = " + str(gender) + ", age = " + str(age) + ", id = " + documentSerialNumber + ", type = " + str(documentType))
#     test_handle.add_feedback(True)

# @pytest.mark.export
# def test_export_type_raw():
#     for line in test_provider.export_nwise(method=Config.F_LOAN_2, template=TemplateType.RAW):
#         print(line)
    
# @pytest.mark.export
# def test_export_type_xml():
#     for line in test_provider.export_nwise(method=Config.F_LOAN_2, template=TemplateType.XML):
#         print(line)
        
# @pytest.mark.export
# def test_export_type_json():
#     for line in test_provider.export_nwise(method=Config.F_LOAN_2, template=TemplateType.JSON):
#         print(line)
        
# @pytest.mark.export
# def test_export_type_csv():
#     for line in test_provider.export_nwise(method=Config.F_LOAN_2, template=TemplateType.CSV):
#         print(line)
        
# @pytest.mark.export
# def test_export_type_gherkin():
#     for line in test_provider.export_nwise(method=Config.F_LOAN_2, template=TemplateType.Gherkin):
#         print(line)

# @pytest.mark.options
# def test_nwise_options():
#     for line in test_provider.generate_nwise(method=Config.F_LOAN_2, constraints=['gender'], choices={'firstName':['male:short']}, coverage=100, n=3):
#         print(line)
#     for line in test_provider.export_nwise(method=Config.F_LOAN_2, constraints=['gender'], choices={'firstName':['male:short']}, coverage=100, n=3, template=TemplateType.CSV):
#         print(line)
        
# @pytest.mark.options
# def test_pairwise_options():
#     for line in test_provider.generate_pairwise(method=Config.F_LOAN_2, constraints=['gender'], choices={'firstName':['male:short']}, coverage=100):
#         print(line)
#     for line in test_provider.export_pairwise(method=Config.F_LOAN_2, constraints=['gender'], choices={'firstName':['male:short']}, coverage=100, template=TemplateType.CSV):
#         print(line)
        
# @pytest.mark.options
# def test_cartesian_options():
#     for line in test_provider.generate_cartesian(method=Config.F_LOAN_2, constraints=['gender'], choices={'firstName':['male:short']}):
#         print(line)
#     for line in test_provider.export_cartesian(method=Config.F_LOAN_2, constraints=['gender'], choices={'firstName':['male:short']}, template=TemplateType.CSV):
#         print(line)
        
# @pytest.mark.options
# def test_random_options():
#     for line in test_provider.generate_random(method=Config.F_LOAN_2, constraints=['gender'], choices={'firstName':['male:short']}, length=25, adaptive=True, duplicates=True):
#         print(line)
#     for line in test_provider.export_random(method=Config.F_LOAN_2, constraints=['gender'], choices={'firstName':['male:short']}, length=25, adaptive=True, duplicates=True, template=TemplateType.CSV):
#         print(line)
        
# @pytest.mark.options
# def test_static_options():
#     for line in test_provider.generate_static_suite(method=Config.F_LOAN_2, test_suites=["default suite"]):
#         print(line)
#     for line in test_provider.export_static_suite(method=Config.F_LOAN_2, test_suites=["default suite"], template=TemplateType.CSV):
#         print(line)

# @pytest.mark.options
# def test_get_method_types():
#     print(test_provider.method_arg_types(method_name=Config.F_LOAN_2))
    
# @pytest.mark.options
# def test_get_method_names():
#     print(test_provider.method_arg_names(method_name=Config.F_LOAN_2))
    
# @pytest.mark.options
# def test_validate():
#     print(test_provider.validate())
    
# @pytest.mark.options
# def test_get_model():
#     print(test_provider.get_model())
#     assert test_provider.get_model() == Config.MODEL_DEVELOP or test_provider.get_model() == Config.MODEL_PROD
    
# @pytest.mark.options
# def test_get_model_custom():
#     test_provider_custom = TestProvider(model='testModel')
    
#     assert test_provider_custom.get_model() == 'testModel'
    
# @pytest.mark.options
# def test_get_generator_address():
#     print(test_provider.get_genserver())

# @pytest.mark.options
# def test_get_generator_custom():
#     test_provider_custom = TestProvider(genserver='testGenServer')
    
#     assert test_provider_custom.get_genserver() == 'testGenServer'
    
# @pytest.mark.options
# def test_get_keystore_password():
#     print(test_provider.get_keystore_password())    
    
# @pytest.mark.options
# def test_get_keystore_password_custom():
#     test_provider_custom = TestProvider(password='testPassword')
    
#     assert test_provider_custom.get_keystore_password() == 'testPassword'
    
# @pytest.mark.options
# def test_get_keystore_path():
#     print(test_provider.get_keystore_path())    
    
# @pytest.mark.options
# def test_get_keystore_path_custom():
#     test_provider_custom = TestProvider(keystore_path='testKeystorePath')
    
#     assert test_provider_custom.get_keystore_path() == 'testKeystorePath'
    
# @pytest.mark.options
# def test_error_model_name():
#     test_provider_custom = TestProvider(model='testModel')
    
#     for line in test_provider_custom.export_nwise(method=Config.F_LOAN_2, template=TemplateType.CSV):
#         print(line)
        
# @pytest.mark.options
# def test_error_method_name():
    
#     for line in test_provider.export_nwise(method='testMethod', template=TemplateType.CSV):
#         print(line)