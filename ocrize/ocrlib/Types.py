from enum import Enum, unique

@unique
class DocType(Enum):
    UNKNOWN = 0
    CARD = 1
    PDF_UNILAB = 2
    PDF_DIANALAB = 3

@unique
class ProcessingStatus(Enum):
    SUCCESS = 0
    FAIL = 1