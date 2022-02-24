import requests
import re
import pprint
import pandas
from urllib.parse import urlencode

from time import sleep
from bs4 import BeautifulSoup


'''
Extract data from yad 2
'''
basic_url = 'https://www.yad2.co.il/realestate/rent?topArea=43&area=22&city=9000&page='
r = requests.get('https://www.yad2.co.il/realestate/rent?topArea=43&area=22&city=9000',
                  headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c = r.content
soup = BeautifulSoup(c, 'html.parser')
#last_page = int(soup.find_all('button', {'class': 'page-num'})[0].string)

# scrapping data - yad 2
lst = []
for pages_numb in range(0, 10): # iterate pages
    sleep(1)
    a = requests.get(basic_url + str(pages_numb),
                     headers={
                         'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
    c = a.content
    soup = BeautifulSoup(c, 'html.parser')
    all = soup.find_all('div', {'class', 'feeditem table'})
    i = 0
    for item in all: # iterate needed items and get the  data.

        dic = {}
        # Address
        address = item.find_all('span', {"class": "title"})[0].string
        address = address.strip()
        if  'שכונה' in address:
            address=address.replace('שכונה','')
        if "'" in address:
            address=address.replace(",",'')
        dic['Address'] = address

        # nigbrhood
        zone = item.find_all('span', {"class": "subtitle"})[0].string
        dic['Zone'] = (zone.split(',')[1])

        # prices
        try:
            price = item.find_all('div', {'class': 'price'})[0].string.replace("\n", "").replace(" ", '')
            dic['Price'] = price[:-1]
        except:
            dic['Price'] = "no price"

        # rooms

        rooms = item.find_all('span', {'class': 'val'})[0].string
        dic['Rooms'] = rooms

        # Floor
        floor = item.find_all('span', {'class': 'val'})[1].string
        dic['Floor'] = floor

        # Link
        m = re.search('item-id="(.+?)"><div', str(item))
        if m:
            found = m.group(1)
            item_num = found
        else:
            item_num = 0
        item_url = 'https://www.yad2.co.il/item/' + str(item_num)
        i += 1

        dic['Link'] = item_url

        lst.append(dic)
df = pandas.DataFrame(lst)
print(df)
#df = pandas.read_csv("SampleData.csv", encoding="utf-8")
# createing cordinate column


'''
Get coordinate for each address and calculate distance from university using google maps
'''

api_key = 'AIzaSyDE8u4h8zyVjm_pj-B9XkRshHNvGF4e-WE'
data_type = 'json'


def extract_lat_lng(address_or_postalcode):
    endpoint = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {"address": address_or_postalcode, "key": api_key}
    url_params = urlencode(params)
    url = f"{endpoint}?{url_params}"
    r = requests.get(url)

    return r.json()
    if r.status_code not in range(200, 299):
        return {}
    latlng = {}
    try:
        latlng = r.json()['results'][0]['geometry']['location']
    except:
        pass
    return latlng.get("lat"), latlng.get("lng")

def duration_time(origin_cordi):
    url1 = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins='
    url2 = "&destinations="
    url3 = '&mode=walking&key='
    destintion = '31.264041,34.799129'

    origin = origin_cordi
    urlfull = url1 + origin + url2 + destintion + url3 + api_key
    output = requests.get(urlfull).json()
    return (output['rows'][0]['elements'][0]['duration']['text'])


# df = pandas.read_csv('first.csv')

cordinates = []
address_list = (df['Address'])
mystr = " באר שבע,".join(address_list)
# pprint.pprint(extract_lat_lng(mystr))
cordi_dic = extract_lat_lng(mystr)
# ['results'][1]['geometry']['location']
for i in range(df.shape[0]):
    currnt_cordi = (cordi_dic['results'][i]['geometry']['location'])
    x_crodi = currnt_cordi['lat']
    y_crodi = currnt_cordi['lng']
    final_cordi = str(x_crodi) +','+ str(y_crodi)
    print(final_cordi)
    #print(duration_time(final_cordi))




#
# for address in address_list:
#     print(address)
#     currnt_cordi = extract_lat_lng(address + "באר שבע ")


cordinates.append(str(currnt_cordi[0]) + "," + str(currnt_cordi[1]))
print(cordinates)
df['Cordinates'] = cordinates


# time from university
# print(duration_time('31.256407,34.783234'))
cordinates_list = df['Cordinates']
duration_list = []

for cord in cordinates_list:
    x_cordi = ((cord).split(',')[0])
    y_cordi = ((cord).split(',')[1])
    duration_list.append(duration_time((x_cordi + ',' + y_cordi)))

print(duration_list)
df['Time from universty'] = duration_list
df.to_csv("seceond_update.csv", encoding='utf-8-sig')

# # export to csv
df.to_csv('SampleData.csv', encoding='utf-8-sig')
print('fin')
