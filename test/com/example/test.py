from enum import Enum

class Gender(Enum):
    MALE = 1
    FEMALE = 2
    
class DocumentType(Enum):
    PASSPORT = 1
    DRIVERS_LICENSE = 2
    PERSONAL_ID = 3