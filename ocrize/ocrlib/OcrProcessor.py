from . import Types
from . import OcrImplementations

class Ocrizer:
    @staticmethod
    def process(document_path:str, document_type:Types.DocType) -> list[Types.ProcessingStatus, str]:
        match document_type:
            case Types.DocType.INSURANCE_CARD:
                return OcrImplementations.insurance_card_file_ocr(document_path)
            case Types.DocType.PDF_UNILABS:
                return OcrImplementations.unilab_pdf_file_ocr(document_path)
            case Types.DocType.PDF_DIANALABS:
                return OcrImplementations.dianalab_pdf_file_ocr(document_path)
            case _:
                return [Types.ProcessingStatus.FAILED, None]
