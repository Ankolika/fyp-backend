from cgi import test
from extract_comments import extract_comments
from find_similarity import find_similarity
from flask import Flask, request,jsonify
from flask_cors import CORS, cross_origin
from datetime import date, timedelta
import pandas as pd
import numpy as np
import json
import ast
import math
# from flask import current_app
# current_app.config['SERVER_NAME'] = 'localhost'   
# with current_app.test_request_context():
#      url = url_for('index', _external=True)

today = date.today()
app = Flask(__name__)
Cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/getInfo", methods=["POST"])
# @cross_origin()
def onSubmit():
    # print('hi')

    if request.method == "POST":
        #get arguments from request url https://stackabuse.com/get-request-query-parameters-with-flask/
        form_data = request.data
        data =  form_data.decode("UTF-8")
        data_dict = ast.literal_eval(data)
        poet_names = data_dict['poet_names']
        test_string= data_dict['input_string']
        print("Poet: ", poet_names)
        print("Input: ", test_string)


    all_poets = ['atticus', 'rupi_kaur','najwa','nikita_gill','rmdrk']
    texts = {}
    comments_obj = {}
    print(poet_names)
    print(type(poet_names))
    for poet_name in poet_names:
        print("Extracting text")
        # poet_texts = extract_text_images(poet_name)
        df = pd.read_csv(f'texts_from_images/{poet_name}.csv')
        dic = df.to_dict()
        texts.update(dic)
               
        print("Extracting Comments")
        poet_comments_obj = extract_comments(poet_name)
        comments_obj.update(poet_comments_obj)

    print("Finding Similarity")
    similarity_score = find_similarity(test_string, texts)

    weighted_avg = {}

    print("Getting Weighted Average")
    for key,value in similarity_score.items():
        avg = 0.6*value + (0.4*comments_obj[key])
        weighted_avg[key] = avg

    sorted_avg = dict(sorted(weighted_avg.items(), key=lambda item: item[1], reverse= True))

    file_name = list(sorted_avg.keys())[0]

    response_obj = {}
    response_obj['filename'] = file_name
    response_obj['text'] = texts[file_name][0]
    
    # response_obj['poet'] = poet_name

    #recommendation part
    #remove the poets selected
    texts = {}
    comments_obj = {}
    remaining_poets = list(set(all_poets) - set(poet_names))
    print(remaining_poets)
    if(remaining_poets):
        for poet_name in remaining_poets:
            print("Extracting text")

            # poet_texts = extract_text_images(poet_name)
            df = pd.read_csv(f'texts_from_images/{poet_name}.csv')
            dic = df.to_dict()
            texts.update(dic)
                
            print("Extracting Comments")
            poet_comments_obj = extract_comments(poet_name)
            comments_obj.update(poet_comments_obj)

        print("Finding Similarity")
        similarity_score = find_similarity(test_string, texts)

        weighted_avg = {}

        print("Getting Weighted Average")
        for key,value in similarity_score.items():
            avg = 0.6*value + (0.4*comments_obj[key])
            weighted_avg[key] = avg

        sorted_avg = dict(sorted(weighted_avg.items(), key=lambda item: item[1], reverse= True))

        file_name = list(sorted_avg.keys())[:5]
        rec_text = []
        for fname in file_name:
            # if(fname=='nikitagill_2'):
            #     print(texts[fname][0])
            #     print(type(texts[fname][0]))
            temp_obj = {}
            temp_obj['image'] = fname
            
            if(type(texts[fname][0]) != float):
                temp_obj['text'] = texts[fname][0]
                
            else:
                temp_obj['text'] = ""
                

            rec_text.append(temp_obj)

        # response_obj['recommended_filename'] = file_name
        response_obj['recommended_files'] = rec_text
        # print(json.dumps(response_obj)[860:920])
        return response_obj

    else:
        return response_obj


if __name__ == '__main__':
    app.run(debug=True)