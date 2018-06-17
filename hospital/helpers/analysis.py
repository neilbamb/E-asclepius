import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import math

sid = SentimentIntensityAnalyzer()
def live_review(hotel_rev):
    sum=[0,0,0,0]
    l=len(hotel_rev)
    print(l)
    for sentence in hotel_rev:
        #print(sentence)
        ss = sid.polarity_scores(sentence)
        print (ss)
        sum[0]=sum[0]+(ss["compound"])
        sum[1] = sum[1] + (ss["neg"])
        sum[2] = sum[2] + (ss["pos"])
        sum[3] = sum[3] + (ss["neu"])
        i=0
    for b in sum:
        sum[i]=sum[i]/l
        i=i+1
    return sum