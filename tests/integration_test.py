import os
import unittest
import ocrize.ocrlib
import cv2
import numpy as np 

class Helper:
    @staticmethod
    def generate_rotated_images(document_path:str) -> None:
        # load the image
        img = cv2.imread(document_path)
        
        # grab the dimensions of the image and calculate the center of the image
        (h, w) = img.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        
        name, ext = os.path.splitext(document_path)

        # rotate image for angle [0,360[ degrees around the center of the image
        for angle in range(360):
            file_name = name + "_" + str(angle) + "_degree" + ext
            if os.path.exists(file_name):
                continue
            
            # grab the rotation matrix 
            M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
            
            # compute the new bounding dimensions of the image
            cos = np.abs(M[0, 0])
            sin = np.abs(M[0, 1])
            nW = int((h * sin) + (w * cos))
            nH = int((h * cos) + (w * sin))
            
            # adjust the rotation matrix to take into account translation
            M[0, 2] += (nW / 2) - cX
            M[1, 2] += (nH / 2) - cY
    
            img_rotated = cv2.warpAffine(img, M, (nW, nH))
            cv2.imwrite(file_name, img_rotated)

class IntegrationTests(unittest.TestCase):

    def test_success_on_dataset(self):
        # first dataset
        data_directory_1= "/workspaces/ocr-engine-python/tests/data/2022-04-01-testing-data/insurance-card/"
        data_directory_2= "/workspaces/ocr-engine-python/tests/data/2022-04-06-testing-data/insurance-card/"
        data_directory_3= "/workspaces/ocr-engine-python/tests/data/2022-04-07-testing-data/insurance-card/"
        
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
    
    def test_success_on_rotated_images(self):
        image_path = "/workspaces/ocr-engine-python/tests/data/2022-04-01-testing-data/insurance-card-rotated/PastedGraphic-2.png"
        
        # generate rotated image
        Helper.generate_rotated_images(image_path)
        
        # expected insurance card number
        expected_result = "80756009940015401778"
        
        name, ext = os.path.splitext(image_path)

        # rotate image for angle [0,360[ degrees around the center of the image
        for angle in [0, 90, 180, 270]:#range(360):
            file_name = name + "_" + str(angle) + "_degree" + ext
            #img = cv2.imread(file_name)
            #if osd["rotate"] != 0 and osd["orientation_conf"] > 3:
            #osd = pytesseract.image_to_osd(img, output_type=pytesseract.Output.DICT)
            #with open('result.txt', 'a') as f:
            #    f.write(str(angle) + ": " + str(osd) + '\n')
            #    f.write('angle {angle}: {result}\n'.format(angle=angle, result=(ocr_result == expected_result)))

            status, ocr_result = ocrize.ocrlib.Ocrizer.process(file_name,ocrize.ocrlib.DocType.CARD)
            self.assertTrue(status == ocrize.ocrlib.ProcessingStatus.SUCCESS)
            self.assertTrue(ocr_result == expected_result)
        
        
            
        

   