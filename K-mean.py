import numpy as np
import difflib
from tqdm import tqdm
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import json


def matches(large_string, query_string):
    '''
    Given a query_string, extract the confident it is include in large_string
    '''
    # words = large_string.split()
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


MainRecipe = list()
with open('MainRecipe.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        temp = line.strip()
        MainRecipe.append(temp)
print MainRecipe
print len(MainRecipe)

SideRecipe = list()
with open('SideRecipe.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        temp = line.strip()
        SideRecipe.append(temp)
print SideRecipe
print len(SideRecipe)

dish =list()
with open('dishes.txt','r') as f1:
    lines = f1.readlines()
    for line in lines:
        temp = line.strip()
        dish.append(temp)
print dish
print len(dish)


matrix = np.zeros((len(dish), len(MainRecipe)+len(SideRecipe)))
match_conf = 0.3
count = [0]*(len(MainRecipe)+len(SideRecipe))
for index in tqdm(range(100)):
    filename = 'recipe/' + str(index) +'.txt'
    f = open(filename,'r')
    lines = f.readlines()
    text = ''
    for line in lines:
        text += line.strip()
    print text
    for i in range(len(MainRecipe)):
        result = matches(dish[index],MainRecipe[i])
        # print result
        if result>0.6:
            matrix[index,i] = 1

        else:
            matrix[index,i] = 0
    for k in range(len(SideRecipe)):
        if SideRecipe[k] in text:
            matrix[index,len(MainRecipe)+k] = 1
        else:
            matrix[index,len(MainRecipe)+k] = 0

# print matrix
# np.savetxt('recipe_matrix.txt',matrix)


# np.savetxt('xxx.txt',matrix)
ran = []
for k in range(2,15):
    km = KMeans(n_clusters=k)
    km.fit(matrix)
    ran.append(sum(np.min(cdist(matrix,km.cluster_centers_,'euclidean'),axis=1))/np.shape(matrix[0]))

plt.plot(range(2,15),ran,'*')
plt.xlabel('k')
plt.ylabel('Distortion')
plt.title('Optimal k')
plt.show()
# print m
# km = KMeans(n_clusters = 7, n_init = 1000) # try 100 different initial centroids
# km.fit(matrix)
# cluster = []
# cluster_stat = dict()
#
# print km.labels_
# for idx, cls in enumerate(km.labels_):
#     if cluster_stat.has_key(cls):
#         cluster_stat[cls] += 1
#     else:
#         cluster_stat[cls] = 1
#     open('cluster-{0}.txt'.format(cls), 'a').write(json.dumps(dish[idx]) + '\r\n')

