import json

ID = list()
Name = list()
city = list()
state = list()
adr = list()
categories = list()
hours = list()
rate = list()
postal_code = list()
f = open('yelp_dataset/business.json','r')
lines = f.readlines()
for line in lines:
    business = json.loads(line)
    try:
        if business['state'].decode('utf-8') == 'NV' \
                and business['city'].decode('utf-8') == 'Las Vegas' \
                and 'Chinese' in business['categories'].decode('utf-8'):
            # print business['business_id'], business['city'], business['state'],business['categories']
            ID.append(business['business_id'])
            Name.append(business['name'])
            adr.append(business['address'])
            city.append(business['city'])
            state.append(business['state'])
            categories.append(business['categories'])
            temp = business['hours']

            if temp:
                t = list()
                day = list()
                for key,value in temp.items():
                    time = value.encode('utf8').decode('unicode_escape').encode('utf8')
                    time = time.split('-')
                    right = time[0].split(':')
                    left = time[1].split(':')
                    time = (right[0]+'.'+str(int(float(right[1])/60*100)),left[0]+'.'+str(int(float(left[1])/60*100)))
                    t.append(time)
                    day.append(key.encode('utf8').decode('unicode_escape').encode('utf8'))

                D = {day[i]:t[i] for i in range(len(day))}
                print 'D:'
                print D
                hours.append(D)
            else:
                hours.append(None)
            rate.append(business['stars'])
            postal_code.append(business['postal_code'])
            # print  type(business['hours'])

    except AttributeError:
        pass
f.close()



f = open('yelp_dataset/review.json','r')
review_list = [list() for i in xrange(len(ID))]
print len(review_list)
lines = f.readlines()
for line in lines:
    review = json.loads(line)
    if review['business_id'] in ID:
        index = ID.index(review['business_id'])
        temp = {'user_id':review['user_id'],
                'rate':review['stars'],
                'text': review['text']
                }
        review_list[index].append(temp)
# print review_list[0]
for i in range(len(ID)):
    final_dict = {ID[i]:{}}
    inside = {
            'name':Name[index],
            'rate': rate[index],
            # 'user_id':review['user_id'],
            'address':adr[index],
            'city':city[index],
            'state':state[index],
            'zip_code':postal_code[index],
            'review':review_list[i],
            'hours': hours[i]
            # 'rate':review['stars'],
            # 'review':review['text']
            }
    final_dict[ID[i]] = inside
    # print final_dict
    output = open('InfoWithHour.txt','a+')
    output.write(json.dumps(final_dict)+'\n')
    output.close()
f.close()

# for i in range(len(ID)):
#     f = open('RestaurantName_ID.txt','a+')
#     temp = {Name[i]:ID[i]}
#     f.write(json.dumps(temp) + '\n')
#     f.close()
