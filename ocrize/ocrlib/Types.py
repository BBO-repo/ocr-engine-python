from enum import Enum, unique

@unique
class DocType(Enum):
    UNKNOWN = 0
    INSURANCE_CARD = 1
    PDF_UNILABS = 2
    PDF_DIANALABS = 3
    
    # remove prefix DocType when enum gets converted to string
    def __str__(self):
        return self.name

@unique
class ProcessingStatus(Enum):
    NONE = 0,
    SUCCESS = 1,
    WARNING = 2,
    FAILED = 3,
    WRONG_FILE = 4
    
    # remove prefix ProcessingStatus when enum gets converted to string
    def __str__(self):
        return self.name