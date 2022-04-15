import pandas as pd 
import nltk
import os
nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def extract_comments(poet_name):
    comments_obj = {}

    comments_parent_dir = './final_dataset/comments'

    #get images and store in list

    analyzer = SentimentIntensityAnalyzer()

    for file in os.listdir(os.path.join(comments_parent_dir,poet_name)):

        df = pd.read_csv(os.path.join(comments_parent_dir,poet_name,file))

        comments = list(df['="Comment Text"'].values)

        polarity_scores = [float(analyzer.polarity_scores(comment)['compound']) for comment in comments]

        #to remove neutral comments
        polarity_scores = [score for score in polarity_scores if score]
        
        avg_score = sum(polarity_scores)/len(polarity_scores)

        filename = file.split('.')[0]

        comments_obj[filename] = (avg_score)
    
    return comments_obj
