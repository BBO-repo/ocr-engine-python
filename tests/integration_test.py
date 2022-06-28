import os
import unittest
import ocrize.ocrlib
import cv2
import numpy as np 
import requests
import json 

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

    def test_success_on_insurance_card_dataset(self):
        # datasets directories
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
    
    # processing rotated images has been disabled in computation
    @unittest.SkipTest
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
    
    def test_success_on_unilab_pdf(self):
        data_directory_1= "/workspaces/ocr-engine-python/tests/data/2022-04-06-testing-data/unilabs/"
        data_directory_2= "/workspaces/ocr-engine-python/tests/data/2022-06-20-testing-data/unilabs/"
        pdfs_unilab = [
            (data_directory_1+"0 OM labo urine 17.12.21.pdf","SHRESTHA Rajani"),
            (data_directory_1+"8402 OM labo urine 10.1.22.pdf","GUTIERREZ MOLET Maria Alicia"),
            (data_directory_1+"labo du 18.12.2021.pdf","SHRESTHA Rajani"),
            (data_directory_1+"serologie COVID du 28.09.2021.pdf","DESTINOBLES VAILLANT Violette"),
            (data_directory_2+"0 h.pylori.pdf","RAUDALES FUNEZ Beyra Lizeth"),
            (data_directory_2+"0 labo sang 28.3.22.pdf","D'ABRUZZO Michele"),
            (data_directory_2+"0 OM.pdf","DESTINOBLES VAILLANT Violette"),
            (data_directory_2+"0 OM frottis nasal covid.pdf","MOLINA ECHEVERRIA Karen"),
            (data_directory_2+"0 OM frottis nasal covid 2.pdf","MOLINA MONTERO Roider"),
            (data_directory_2+"0 OM labo 2014.pdf","RODRIGUEZ BRUNO Carla"),
            (data_directory_2+"0 OM labo sang.pdf","PINTO Paulo Jorge"),
            (data_directory_2+"0 OM labo sang 2.pdf","ALVAREZ PALLEJA Vanessa"),
            (data_directory_2+"0 OM labo sang 3.pdf","MARTINEZ BARREIRO Vanessa Evelin"),
            (data_directory_2+"0 OM labo sang 4.pdf","CIUCIU Amalia-Evelyne"),
            (data_directory_2+"0 OM labo sang 8.2.22.pdf","GARCIA GOICOECHEA ALARCIA Maria"),
            (data_directory_2+"0 OM labo sang 8.4.22.pdf","RADWAN Anna Maria"),
            ##(data_directory_2+"0 OM labo sang 13.6.21.pdf","SURDO Maria Assunta"),
            (data_directory_2+"0 OM labo sang 22.3.21.pdf","RADWAN Anna Maria"),
            (data_directory_2+"0 OM labo sang 29.4.21.pdf","KRISTIANSSON Charlotte Marie"),
            (data_directory_2+"0 OM labo urine 17.12.21.pdf","SHRESTHA Rajani"),
            (data_directory_2+"5 lab 9.7.21.pdf","DESTINOBLES VAILLANT Violette"),
            (data_directory_2+"5 OM labo sang 3.5.21.pdf","DESTINOBLES Violette"),
            (data_directory_2+"5 OM labo sang 15.6.21.pdf","DESTINOBLES Violette"),
            (data_directory_2+"23 OM labo sang 15.2.22.pdf","QUIRY Anne Claude"),
            (data_directory_2+"3586 OM sang 6.5.22.pdf","ODIER Alexandre"),            
            (data_directory_2+"3586 urine 6.5.22.pdf","ODIER Alexandre"),
            (data_directory_2+"132201622020191111163426476__20191111163134_1900606373_20191111_ODIER_19640220__16220.pdf","ODIER Alexandre"),
            (data_directory_2+"_A4VERT__1900254982_465613.pdf","GUIDINI JOUBERT César"),
            (data_directory_2+"_A4VERT__1900260135.pdf","FERNANDEZ Juan-José"),
            (data_directory_2+"_A4VERT__1900261465.pdf","NAVAS Francisco"),
            (data_directory_2+"_A4VERT__1900261469.pdf","NAVAS Josefa"),
            (data_directory_2+"_A4VERT__1900264682_465613.pdf","CHAPEL Anastasia"),
            (data_directory_2+"_A4VERT__1900296680_465613.pdf","FRASCA Carmen"),
            (data_directory_2+"_A4VERT__1900329248.pdf","MAZZOLINI Giordano"),
            (data_directory_2+"FERREIRA-DIAS_Joaquim_19510910_20201221_Unilabs_132201759120201222123500489.pdf","FERREIRA DIAS Joaquim"),
        ]
        
        for i, val in enumerate(pdfs_unilab):
            status, ocr_result = ocrize.ocrlib.Ocrizer.process(val[0],ocrize.ocrlib.DocType.PDF_UNILAB)
            self.assertTrue(status == ocrize.ocrlib.ProcessingStatus.SUCCESS)
            self.assertTrue(ocr_result == val[1])
    
    def test_success_on_dianalab_pdf(self):
        data_directory_1= "/workspaces/ocr-engine-python/tests/data/2022-04-06-testing-data/dianalabs/"
        data_directory_2= "/workspaces/ocr-engine-python/tests/data/2022-06-20-testing-data/dianalabs/"
        pdfs_dianalab = [
            (data_directory_1+"8405 labo 17.12.2021.pdf","GLAVAS Milan"),
            (data_directory_1+"8411 labo du 27.12.2021.pdf","PEDRAZZOLI Debora"),
            (data_directory_1+"8411 sed urinaire 27.12.2021.pdf","PEDRAZZOLI Debora"),
            (data_directory_1+"8412 sed urinaire 27.12.2021.pdf","REY Severine"),
            (data_directory_1+"8412labo du 27.12.2021.pdf","REY Severine"), 
            (data_directory_2+"5 OM labo sang 10.5.21.pdf","DESTINOBLES Violette"), 
            (data_directory_2+"5 OM labo sang 21.4.21.pdf","DESTINOBLES Violette"), 
            (data_directory_2+"5 OM labo sang 21.4.21 bis.pdf","DESTINOBLES Violette"), 
            (data_directory_2+"5 OM labo urinaire 21.4.21.pdf","DESTINOBLES Violette"), 
            (data_directory_2+"19 labo du 28.09.2021.pdf","STUTZMANN Jean Marie"), 
            (data_directory_2+"23 OM labo urine 5.5.21.pdf","QUIRY Anne Claude"),             
            (data_directory_2+"23 OM labo urine 5.5.21.pdf","QUIRY Anne Claude"), 
            (data_directory_2+"23 OM labo urine 18.1.22.pdf","QUIRY Anne Claude"), 
            (data_directory_2+"23 res urine du 07.02.2022.pdf","QUIRY Anne Claude"), 
            (data_directory_2+"23 res urine du 28.03.2022.pdf","QUIRY Anne Claude"), 
            (data_directory_2+"42 OM labo urine 7.12.21.pdf","LESTON Jesus"), 
            (data_directory_2+"23 OM labo urine 18.1.22.pdf","QUIRY Anne Claude"), 
            (data_directory_2+"23 res urine du 07.02.2022.pdf","QUIRY Anne Claude"), 
            (data_directory_2+"23 res urine du 28.03.2022.pdf","QUIRY Anne Claude"), 
            (data_directory_2+"42 OM labo urine 7.12.21.pdf","LESTON Jesus"), 
            (data_directory_2+"132- Urines Dianalabs.pdf","SPIRIG Friedrich"), 
            (data_directory_2+"1737dianalabs.pdf","SANCHEZ Maria-Olga"), 
            (data_directory_2+"2672 OM labo sang 15.2.22.pdf","CRUZ Antonio José"), 
            (data_directory_2+"2701 labo.pdf","FERNANDEZ Gerardo"), 
            (data_directory_2+"2701 OM.pdf","FERNANDEZ Gerardo"), 
            (data_directory_2+"2701 OM labo.pdf","FERNANDEZ Gerardo"), 
            (data_directory_2+"2701 OM sang 2.6.22.pdf","FERNANDEZ Gerardo"), 
            (data_directory_2+"2701 urine 2.6.22.pdf","FERNANDEZ Gerardo"), 
            (data_directory_2+"2718 OM labo sang 7.6.21.pdf","MARGIOTTA Patrick"), 
            (data_directory_2+"2718 OM labo urine 7.6.21.pdf","MARGIOTTA Patrick"), 
            (data_directory_2+"3175 OM labo sang 18.3.21.pdf","CASTAGNOLO ANTONINO"), 
            (data_directory_2+"3175 OM labo sang 20.9.21.pdf","CASTAGNOLO Antonino"), 
            (data_directory_2+"3175 OM labo urine 18.3.21.pdf","CASTAGNOLO ANTONINO"), 
            (data_directory_2+"3440 Examens complementaires hospitalisation 7.12.21.pdf","CUESTA SYLVIA SANCHEZ"), 
            (data_directory_2+"4096Dianalabs.pdf","Laghzaoui Mohamed"), 
            (data_directory_2+"6802dianalabs.pdf","VENA SEVERICH Tatiana Helga"), 
            (data_directory_2+"6859 Dianalabs.pdf","ANTONIJEVIC Milenko"), 
            (data_directory_2+"7192- rapport partiel Dianalabs.pdf","SUAREZ VILCA Lucas Alexandre"), 
            (data_directory_2+"144781622020190117143630213__20190117143159_0113525335M_20190117_STUTZMANN_19631208_19_16220.pdf","STUTZMANN Jean Marie"), 
            (data_directory_2+"144781933320200827115539721__20200827115236_0113897489M_20200824_DALLA-MUTTA-HOMBERGER_19690210__19333.pdf","DALLA MUTTA HOMBERGER Brigitte"), 
            (data_directory_2+"144781933320200918165538967_3767332_20200918165236_0113919308S_20200918_HOMBERGER_19690210_3869_19333.pdf","HOMBERGER Brigitte"), 
            (data_directory_2+"144781933320200921080233363_3767332_20200921080131_0113919308M_20200918_HOMBERGER_19690210_3869_19333.pdf","HOMBERGER Brigitte"), 
            (data_directory_2+"144781933320200923085546598__20200923085326_0113922898S_20200922_HOMBERGER_19690210__19333.pdf","HOMBERGER Brigitte"), 
            (data_directory_2+"144781933320200924141046139_3767332_20200924140631_0113924386S_20200924_HOMBERGER_19690210__19333.pdf","HOMBERGER Brigitte"), 
            (data_directory_2+"144781933320200926095640237_3767332_20200926095104_0113924386M_20200924_HOMBERGER_19690210__19333.pdf","HOMBERGER Brigitte"), 
            (data_directory_2+"Test COVID- du 04.11.20.pdf","CHOITEL Julien"), 
        ]
            
        for i, val in enumerate(pdfs_dianalab):
            status, ocr_result = ocrize.ocrlib.Ocrizer.process(val[0],ocrize.ocrlib.DocType.PDF_DIANALAB)
            self.assertTrue(status == ocrize.ocrlib.ProcessingStatus.SUCCESS)
            self.assertTrue(ocr_result == val[1])
    
    # disable by default since requires running webapp
    def test_success_on_webapp(self):
        # before running the test make sure webapp is running and url is correct
        url = "http://127.0.0.1:5000/ocr/insurance-card"
        file = open("/workspaces/ocr-engine-python/tests/data/2022-04-01-testing-data/insurance-card/PastedGraphic-1.png", 'rb')
        # test with a valid image
        response = requests.post(url, files = {"document": file})
        result=response.json()
        self.assertTrue(response.status_code == 200)
        self.assertTrue(result["status"] == "ProcessingStatus.SUCCESS")
        file.close()
        
        # test without image
        response = requests.post(url, files = {})
        result=response.json()
        self.assertTrue(response.status_code == 400)
        self.assertTrue(result["status"] == "ProcessingStatus.FAIL")
        
        # test with a non valid image
        response = requests.post(url, files = {"document": None})
        result=response.json()
        self.assertTrue(response.status_code == 400)
        self.assertTrue(result["status"] == "ProcessingStatus.FAIL")
        
        url = "http://127.0.0.1:5000/ocr/pdf/unilab"
        file = open("/workspaces/ocr-engine-python/tests/data/2022-04-06-testing-data/unilabs/0 OM labo urine 17.12.21.pdf", 'rb')
        # test with a valid image
        response = requests.post(url, files = {"document": file})
        result=response.json()
        self.assertTrue(response.status_code == 200)
        self.assertTrue(result["status"] == "ProcessingStatus.SUCCESS")
        file.close()
        
        # test without document
        response = requests.post(url, files = {})
        result=response.json()
        self.assertTrue(response.status_code == 400)
        self.assertTrue(result["status"] == "ProcessingStatus.FAIL")
        
        # test with a non valid document
        response = requests.post(url, files = {"document": None})
        result=response.json()
        self.assertTrue(response.status_code == 400)
        self.assertTrue(result["status"] == "ProcessingStatus.FAIL")
        
        url = "http://127.0.0.1:5000/ocr/pdf/dianalab"
        file = open("/workspaces/ocr-engine-python/tests/data/2022-04-06-testing-data/dianalabs/8405 labo 17.12.2021.pdf", 'rb')
        # test with a valid image
        response = requests.post(url, files = {"document": file})
        result=response.json()
        self.assertTrue(response.status_code == 200)
        self.assertTrue(result["status"] == "ProcessingStatus.SUCCESS")
        file.close()
        
        # test without document
        response = requests.post(url, files = {})
        result=response.json()
        self.assertTrue(response.status_code == 400)
        self.assertTrue(result["status"] == "ProcessingStatus.FAIL")
        
        # test with a non valid document
        response = requests.post(url, files = {"document": None})
        result=response.json()
        self.assertTrue(response.status_code == 400)
        self.assertTrue(result["status"] == "ProcessingStatus.FAIL")
        
            
        

   