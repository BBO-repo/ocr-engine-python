from . import Types
from . import OcrImplementations

class Ocrizer:
    @staticmethod
    def process(document_path:str, document_type:Types.DocType) -> list[Types.ProcessingStatus, str]:
        match document_type:
            case Types.DocType.CARD:
                return OcrImplementations.insurance_card_ocr(document_path)
            case Types.DocType.PDF_DIANALAB:
                return OcrImplementations.pdf_unilabs_ocr(document_path)
            case Types.DocType.PDF_DIANALAB:
                return OcrImplementations.pdf_dianalabs_ocr(document_path)
            case _:
                return [Types.ProcessingStatus.FAIL, None]
