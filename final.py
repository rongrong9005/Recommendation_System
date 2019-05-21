import numpy as np
import difflib
import json
from tqdm import tqdm

def matches(large_string, query_string):
    '''
    Given a query_string, extract the confident it is include in large_string
    '''
    words = large_string.split()
    # for word in words:
    #     s = difflib.SequenceMatcher(None, word, query_string)
    #     match = ''.join(word[i:i+n] for i, j, n in s.get_matching_blocks() if n)
        # if len(match) / float(len(query_string)) >= threshold:
        #     yield match
    s = difflib.SequenceMatcher(None, large_string, query_string)
    conf = sum(n for i,j,n in s.get_matching_blocks())/float(len(query_string))
    # if conf > threshold:
    #     return True, conf
    # else:
    #     return False, conf
    return conf


matrix = np.zeros((100,500))
dish = []
with open('dishes.txt','r') as f1:
    for line in f1.readlines():
        line=line.strip('\n')
        dish.append(line)

# print len(dish)

dict_info = dict()
list_id = []
with open('info.txt','r') as f2:
    for l in f2.readlines():
        l = l.strip('\n')
        str = eval(l)
        # print str
        dict_info.update(str)
        list_id.append(str.keys()[0])


match_conf=0.6
import pdb;pdb.set_trace()

for ith, d in enumerate(dish):
    for k in tqdm(range(0,len(list_id))):
        rate1 = 0
        m = 0
        for txt in dict_info[list_id[k]]['review']:
            result = matches(txt['text'],d)
            if result > match_conf:
                rate1 += txt['rate']
                m+=1

        if rate1 > 0:
            rate1 = rate1/m
        else:
            rate1 = 0
        matrix[ith, k] = rate1

print matrix
np.save('matrix.npy',matrix)





# with open('restaurant_id.txt','w') as w1:
#     for i in list_id:
#         # i=json.dumps(i)
#         w1.writelines(i)
#         w1.writelines('\n')


# match_conf=0.6
# import pdb;pdb.set_trace()
# import time

# def dis_rate(dish):
# for ith, d in enumerate(dish):
#     for jth, res_id in tqdm(enumerate(list_id)):
#         rate = 0
#         m = 0
#         # tic0 = time.time()
#         for txt in dict_info[res_id]['review']:
#             # print txt['text']
#             # tic = time.time()
#             result = matches(txt['text'],d)
#             # toc = time.time()
#
#             if result > match_conf:
#                 rate += txt['rate']
#                 m+=1
#             # toc1 = time.time()
#
#             # print('match speed:{}\t rate:{}'.format(1/(toc-tic), 1/(toc1-toc+0.00000000000001)))
#         # toc2 = time.time()
#         # print('dish-res item time:{}'.format(1/(toc2-tic0)))
#         if rate > 0:
#             rate = rate/m
#         else:
#             rate = 0
#         matrix[ith, jth] = rate
#
# print matrix
# np.save('matrix.npy',matrix)

