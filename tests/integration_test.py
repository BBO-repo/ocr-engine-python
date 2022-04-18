import unittest
from xmlrpc.client import FastMarshaller
import ocrize.ocrlib

class IntegrationTests(unittest.TestCase):

    def test_success_on_dataset(self):
        # first dataset
        data_directory_1 = "/workspaces/ocr-engine-python/tests/data/2022-04-01-testing-data/insurance-card/"
        data_directory_2 = "/workspaces/ocr-engine-python/tests/data/2022-04-06-testing-data/insurance-card/"
        data_directory_3 = "/workspaces/ocr-engine-python/tests/data/2022-04-07-testing-data/insurance-card/"
        
        image_insurance_number = [
            (data_directory_1+"PastedGraphic-1.png", "80756000620054622611"),
            (data_directory_1+"PastedGraphic-2.png", "80756009940015401778"),
            (data_directory_2+"carete gm.png", "80756014790032134492"),
            (data_directory_2+"carte assure sanacur.png", "80756015620245213019"),
            (data_directory_2+"carte atupri.png", "80756003120013488843"),
            (data_directory_2+"carte concordia.png", "80756002900033507014"),
            (data_directory_2+"carte egk.png", "80756008810012828799"),
            (data_directory_2+"carte kpt.png", "80756003760245213019"),
            (data_directory_2+"carte okk.png", "80756004550011767393"),
            (data_directory_2+"carte rhenusana.png", "80756014010001260791"),
            (data_directory_2+"carte sanacur.png", "80756012340245213019"),
            (data_directory_2+"carte sanitas.png", "80756015090033592708"),
            (data_directory_2+"carte swica.png", "80756013840045400466"),
            (data_directory_2+"carte sympany.png", "80756000570001200409"),  
            (data_directory_2+"carte visana.png", "80756015550031576925"),
            (data_directory_3+"carte assura.png","80756015620245213019"),
            (data_directory_3+"carte assura 2.png","80756015620245213019"),
            (data_directory_3+"carte concordia 2.png","80756002901234567890"),
            (data_directory_3+"carte kpt 2.png","80756003760245213019"),
            (data_directory_3+"carte kpt 3.png","80756003760245213019"),
            (data_directory_3+"carte swica 2.png","80756013841234567890"),
            (data_directory_3+"carte swica angle 1.png","80756013841234567890"),
            (data_directory_3+"carte swica angle 2.png","80756013841234567890"),
        ]
        
        for i, val in enumerate(image_insurance_number):
            status, ocr_result = ocrize.ocrlib.Ocrizer.process(val[0],ocrize.ocrlib.DocType.CARD)
            self.assertTrue(status == ocrize.ocrlib.ProcessingStatus.SUCCESS)
            self.assertTrue(ocr_result == val[1])
            
        

   