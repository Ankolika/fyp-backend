#https://medium.com/@marioruizgonzalez.mx/how-install-tesseract-orc-and-pytesseract-on-windows-68f011ad8b9b
#https://github.com/UB-Mannheim/tesseract/wiki
#install tesseract
#install pytesseract

from operator import index
import pytesseract
import os
import cv2
import pandas as pd

def extract_text_images(poet_name):
    

    images_parent_dir = './final_dataset/images'
    # pytesseract.pytesseract.tesseract_cmd =r'C:\Users\ankolikde2\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tesseract_cmd = '/app/.apt/usr/bin/tesseract'
    #navyanth's system
    # pytesseract.pytesseract.tesseract_cmd =r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    #get images and store in list
    texts = {}

    for file in os.listdir(os.path.join(images_parent_dir,poet_name)):
        # print(file)
        img = cv2.imread(os.path.join(images_parent_dir,poet_name,file))
        # try: 
        text = pytesseract.image_to_string(img)
        # except: 
        #     print(e)
        #     print(file)
        text = text.replace('\n',' ')

        count_underscore = file.count('_')

        if count_underscore == 1:
            filename = file.split('.')[0]
            texts[filename] = text

        else:
            temp1, temp2, temp3 = file.split('_')

            try:
                #if string already exists
                texts[temp1 + "_" + temp2] += text
            except:
                #if string is new file
                texts[temp1 + "_" + temp2] = text

    
    return texts



if __name__ == '__main__':

    #extract texts and save it to the csv file
    texts = extract_text_images('atticus')
    df = pd.DataFrame(texts,index = [0])
    df.to_csv('texts_from_images/atticus.csv', index=False)
    
