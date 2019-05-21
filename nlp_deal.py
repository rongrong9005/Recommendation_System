import numpy as np
import difflib
import json
from tqdm import tqdm
import nltk

nltk.downloader.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

matrix = np.zeros((100, 500))
dish = []
with open('dishes.txt', 'r') as f1:
    for line in f1.readlines():
        line = line.strip('\n')
        dish.append(line)

# print len(dish)

dict_info = dict()
list_id = []
with open('info.txt', 'r') as f2:
    for l in f2.readlines():
        l = l.strip('\n')
        str = eval(l)
        # print str
        dict_info.update(str)
        list_id.append(str.keys()[0])

match_conf = 0.6

# for ith, d in enumerate(dish):
for k in tqdm(range(0, len(dict_info))):
    rate1 = 0
    m = 0
    test_data_x = []
    # get every restaurant review and calculate the rate
    for jth, txt in enumerate(dict_info[list_id[k]]['review']):

        view = [txt['text']]
        sid = SentimentIntensityAnalyzer()
        list_nlp = []
        for sen in view:
            ss = sid.polarity_scores(sen)
            list_nlp.append(ss['neg'])
            list_nlp.append(ss['neu'])
            list_nlp.append(ss['pos'])
            list_nlp.append(ss['compound'])
            rate1 -= ss['neg']
            rate1 += ss['pos']
            m += 1
        dict_info[list_id[k]]['review'][jth]['nlp_rate'] = list_nlp
    rate1 = rate1 / m
    dict_info[list_id[k]]['restaurant_rate'] = rate1
# print dict_info
with open('info_nlp.txt', 'w') as file:
    file.write(json.dumps(dict_info))
# # print ss
# if ss['neg'] > ss['pos']:
#     rate1 -= 1
# else:
#     rate1 += 1
# print ith, k
# print rate1
# matrix[ith, k] = rate1

# print matrix
# np.save('matrix.npy', matrix)
