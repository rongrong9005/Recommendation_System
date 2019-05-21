import json
import difflib
import numpy as np


def cluster_name(dish_list):
    filenames = list()
    for i in range(7):
        filename = 'cluster/cluster-'+str(i)+'.txt'
        with open(filename,'r') as f:
            lines = f.readlines()
        f.close()
        lines = [line.strip().strip('\"').strip('\r\n').lower() for line in lines]
        # print str(i)+':',lines
        for item in dish_list:
            if item in lines:
                filenames.append(filename)
    return filenames


def load2dict(fn):
    '''
    load reviews to dictionay
    '''
    fl = open(fn).readlines()
    res = {}
    for ith, item in enumerate(fl):
        dict_item = json.loads(item)
        resid = list(dict_item.keys())[0]
        # import pdb; pdb.set_trace()
        res[resid] = {}
        res[resid]['info'] = dict_item[resid]
        if 'reviews' in res:
            res[resid]['reviews'].append(dict_item[resid]['review'])
        else:
            res[resid]['reviews'] = [dict_item[resid]['review']]

def load_dishes(fn):
    '''
    Given the file name of dish, return a list of the dishes
    '''
    dish = open(fn).readlines()
    dishes = [e.strip() for e in dish]
    return dishes

def load_resturant(fn):
    fl = open(fn).readlines()
    resturants = {}
    for item in fl:
        resturants.update(json.loads(item))
    return resturants

def matches(large_string, query_string, threshold=0.6):
    '''
    Given a query_string, extract the confident it is include in large_string
    '''
    # words = large_string.split()
    # for word in words:
    #     s = difflib.SequenceMatcher(None, word, query_string)
    #     match = ''.join(word[i:i+n] for i, j, n in s.get_matching_blocks() if n)
          # if len(match) / float(len(query_string)) >= threshold:
          #     yield match
    s = difflib.SequenceMatcher(None, large_string.lower(), query_string.lower())
    conf = sum(n for i,j,n in s.get_matching_blocks())/float(len(query_string))
    # if conf > threshold:
    #     return True, conf
    # else:
    #     return False, conf
    return conf

def matchW(a, b):
    '''
    word match, check if a and b matches
    '''
    return difflib.SequenceMatcher(None, a, b).ratio()


def match_Dish(dishList, dish):
    '''
    return the most likely dish confident and id in dishList
    '''
    conf_max = 0
    conf_max_ith = 0
    # import pdb; pdb.set_trace()
    for ith, item in enumerate(dishList):
        # if ith==31:
        #     import pdb; pdb.set_trace()
        conf = matchW(item, dish)
        if conf > conf_max:
            conf_max = conf
            conf_max_ith = ith
        # print('conf{}:{} {}th'.format(conf, item, ith))
    return [conf_max, conf_max_ith]



def recommend_res(dish_matrix, topK=3, rec_type='mix'):
    '''
    Given a list matrix of dishes in matrix, we could
    Input:
        dish_matrix: #dish * # resturant
        type = [max, median, mix]
    '''
    res_score_max = dish_matrix.sum(axis=0)
    res_score_median = np.median(dish_matrix, axis=0)
    if rec_type == 'max':
        res_score = res_score_max
    elif rec_type == 'median':
        res_score = res_score_median
    elif rec_type == 'mix':
        res_score = (res_score_max*res_score_median)/(res_score_max + res_score_median)*2

    sort_ind = np.argsort(res_score)
    return sort_ind[-topK:], np.sort(res_score)[-topK:]


def recommend_print(resturantList, ind, score):
    print('#\tBased on your input dishes we suggest the following resturant for you:\n')
    print('\t\t{}\t{}'.format('Name', 'Score'))
    for ith, s in zip(ind, score):
        print('\t\t{}\t{:.2f}'.format(resturantList[ith], s))




if __name__ == '__main__':
    # load Yelp dataset
    resturant = load_resturant('info.txt')
    # import pdb; pdb.set_trace()

    # load dish List
    dishList = load_dishes('dishes.txt')


    # update dishes score according to Yelp dataset
    # dish_res
    dish_res = np.load('matrix.npy')

    # load resturant
    resturantList = [list(json.loads(open('RestaurantName_ID.txt').readlines()[i]).keys()) for i in range(500)]

    while(1):
        print('\n\n' + '#'*30 + '\n')
        print('Dishes you can choose:\n\n{}\n'.format(dishList))
        print('\n' + '-'*30 + '\n')
        input_dish = raw_input('#\tDishes I want to eat(seperate by comma):\n\t\t')
        # input_dish  = input()
        reserve_time = raw_input('#\tTime I want to eat:\n\t\t')
        dist = raw_input('#\tDistance I can accept(mi):')
        # import pdb; pdb.set_trace()

        # match use input dishes with the dishList
        threshold_find_dish = 0.6
        dish_match_score = [match_Dish(dishList, item.strip()) for item in input_dish.split(',')]
        dish_not_exist = [ dishList[item[1]] for item in dish_match_score if item[0] < threshold_find_dish]

        dish_find = [ item[1] for item in dish_match_score if item[0] > threshold_find_dish]


        # print '*'*50,dish_find
        # print '*'*50,dish_not_exist


        if len(dish_not_exist) < 1:
            print('#\tWe are looking for the dishes and best resturant for you...')
            # import pdb; pdb.set_trace()
            dish_matrix = dish_res[tuple(dish_find),:]
            rec_ind, rec_score = recommend_res(dish_matrix, topK=3, rec_type='mix')
            recommend_print(resturantList, rec_ind, rec_score)

        elif len(dish_not_exist) >0 :
            dishList = [text.strip().strip('\"').strip('\r\n').lower() for text in dishList]
            dish_not_exist = [text.lower() for text in dish_not_exist]
            filenames = cluster_name(dish_not_exist)
            # print '*'*50,filenames
            recomend_dish_ith = list()
            restaurant_index_list = list()
            for filename in filenames:
                with open(filename,'r') as f:
                    lines = f.readlines()
                f.close()
                    # lines = [line.strip().strip('\"').strip('\r\n') for line in lines]
                    # recomend_dish_ith.append(dishList.index(lines[0].strip().strip('\"').strip('\r\n')))
                for line in lines:
                    index = dishList.index(line.strip().strip('\"').strip('\r\n').lower())
                    recomend_dish_ith.append(index)
            # print 'recomend_dish: ',recomend_dish_ith

            if len(dish_find) == 0:
                ith_list = list()
                for dish in dish_not_exist:
                    ith = dishList.index(dish)
                    ith_list.append(ith)

                    # index = np.where(np.max(dish_res[ith,:]))

                    # print('\t\t{}\t'.format(resturantList[index]))
                # print '~'*50,ith_list
                dish_matrix = dish_res[tuple(ith_list),:]
                rec_ind, rec_score = recommend_res(dish_matrix, topK=3, rec_type='mix')
                recommend_print(resturantList, rec_ind, rec_score)
            else:
                dish_matrix = dish_res[tuple(dish_find),:]
                rec_ind, rec_score = recommend_res(dish_matrix, topK=3, rec_type='mix')

                count = list()
                for ith in rec_ind:
                    temp = 0
                    for j in recomend_dish_ith:
                        if dish_res[j,ith] > 0:
                            temp += 1
                    count.append(temp)
                index = count.index(max(count))
                rec_ind = np.append(rec_ind,rec_ind[index])
                rec_score = np.append(rec_score,rec_score[index])
                recommend_print(resturantList, rec_ind, rec_score)
            # for index in recomend_dish:
            #     dish_matrix = dish_res[:,index]
            #     restaurant_index_list.append(np.where(np.max(dish_matrix,axis=1)))
            # print('#\tBased on your input dishes we suggest the following resturant for you:\n')
            # print('\t\t{}'.format('Name'))
            # print restaurant_index_list[0][0]
            # for item in restaurant_index_list:
            #     print('\t\t{}'.format(resturantList[item[0][0]]))
            # dish_matrix = dish_res[set(dish_find),:]
            # rec_ind, rec_score = recommend_res(dish_matrix, topK=3, rec_type='mix')
            # recommend_print(resturantList, rec_ind, rec_score)

        else:
            print('#\tYour dish query can not be found, would you try any other dishes?\n')
        print('\n'+ '#'*30 + '\n')
