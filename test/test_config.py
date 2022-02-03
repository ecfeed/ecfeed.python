import sys
sys.path.append("..")

from ecfeed import TestProvider

class Config:
    KEYSTORE_PROD = "/home/krzysztof/.ecfeed/security_prod.p12"
    GENERATOR_DEVELOP = "https://develop-gen.ecfeed.com"
    MODEL_DEVELOP = "QERK-K7BW-ME4G-W3TT-NT32"
    MODEL_PROD = "IMHL-K0DU-2U0I-J532-25J9"
    MODEL_WORKSHOP = '6EG2-YL4S-LMAK-Y5VW-VPV9'
    MODEL_DUMMY = "XXXX-XXXX-XXXX-XXXX-XXXX"
    
    @staticmethod
    def get_test_provider(prod = False):
        return Config.get_test_provider_prod() if prod else Config.get_test_provider_develop()
        
    @staticmethod
    def get_test_provider_prod():
        return TestProvider(model=Config.MODEL_PROD, keystore_path=Config.KEYSTORE_PROD)
    
    @staticmethod
    def get_test_provider_develop():
        return TestProvider(model=Config.MODEL_DEVELOP, genserver=Config.GENERATOR_DEVELOP)
    
    @staticmethod
    def get_test_provider_workshop():
        return TestProvider(model=Config.MODEL_WORKSHOP, keystore_path=Config.KEYSTORE_PROD)
    
    F_TEST = "QuickStart.test"
    F_10x10 = "com.example.test.Playground.size_10x10"
    F_100x2 = "com.example.test.Playground.size_100x2"
    F_LOAN_2 = "com.example.test.LoanDecisionTest2.generateCustomerData"
    F_WORKSHOP = 'com.example.test.Demo.typeString'