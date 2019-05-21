from wordcloud import WordCloud
import json
import time

start = time.time()
ID = list()
Name = list()
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
            Name.append(business['name'].encode('utf8').decode('unicode_escape').encode('utf8'))
    except AttributeError:
        pass
f.close()

f = open('yelp_dataset/review.json','r')
# review_list = [list() for i in range(len(ID))]
# print len(review_list)
lines = f.readlines()
f.close()

for line in lines:
    review = json.loads(line)

    if review['business_id'].encode('utf8').decode('unicode_escape').encode('utf8') in ID:
        index = ID.index(review['business_id'].encode('utf8').decode('unicode_escape').encode('utf8'))
        text_name = 'picture/'+ Name[index] + '.txt'
        # print text_name
        input_text = open(text_name,'a+')
        try:
            input_text.write(review['text'].encode('utf8').decode('unicode_escape').encode('utf8')+'\n')
        except UnicodeDecodeError:
            pass
        input_text.close()
        # text += review['text']



for i in range(len(Name)):
    filename = 'picture/' + Name[i] + '.txt'
    output_text = open(filename,'r')
    text = output_text.readlines()
    output_text.close()
    img = WordCloud().generate(text)
    filename = 'picture/' + Name[i] + '.png'
    img.to_file(filename)

end = time.time()
print 'time:{}'.format(end - start)
