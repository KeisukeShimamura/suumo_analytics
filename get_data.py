from bs4 import BeautifulSoup
import requests
import time
import csv
import os

url_list = ['https://suumo.jp/jj/chintai/ichiran/FR301FC001/?ar=010&bs=040&fw2=&pc=50&po1=25&po2=99&ta=01&sc=01101&md=07&cb=0.0&ct=10.0&et=10&mb=45&mt=9999999&cn=15&co=1&tc=0400101&tc=0400502&tc=0400301&tc=0400905&tc=0400912&tc=0400405&shkr1=03&shkr2=03&shkr3=03&shkr4=03']
save_dir = 'data'
output_path_list = ['center.csv']
num_pages = 2

os.mkdir(save_dir)
for (url, output_path) in zip(url_list, output_path_list):
  urls = []
  for page in range(1, num_pages + 1):
    url_page = url + '&page={}'.format(page)
    urls.append(url_page)
  print('number of urls is {}'.format(len(urls)))

  f = open('{}/{}'.format(save_dir, output_path), 'a')
  for url in urls:
    print('get data of url({})'.format(url))
    new_list = []
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c, "html.parser")
    summary = soup.find("div", {'id': 'js-bukkenList'})
    apartments = summary.find_all("div", {'class': 'cassetteitem'})
    for apart in apartments:
      room_number = len(apart.find_all('tbody'))
      name = apart.find("div",{'class':'cassetteitem_content-title'}).text
      address = apart.find("li", {'class':"cassetteitem_detail-col1"}).text
      age_and_height = apart.find('li', class_='cassetteitem_detail-col3')
      age = age_and_height('div')[0].text
      height = age_and_height('div')[1].text
      money = apart.find_all("span", {'class':"cassetteitem_other-emphasis ui-text--bold"})
      kanri = apart.find_all("span", {'class':"cassetteitem_price cassetteitem_price--administration"})
      sikikin = apart.find_all("span", {'class':"cassetteitem_price cassetteitem_price--deposit"})
      reikin = apart.find_all("span", {'class':"cassetteitem_price cassetteitem_price--gratuity"})
      madori = apart.find_all("span", {'class':"cassetteitem_madori"})
      menseki = apart.find_all("span", {'class':"cassetteitem_menseki"})
      floor = apart.find_all("td")

      for i in range(room_number):
        write_list = [name, address, age, money[i].text, kanri[i].text, sikikin[i].text, reikin[i].text, madori[i].text, menseki[i].text, floor[2+i*9].text.replace('\t', '').replace('\r','').replace('\n', '')]
        writer = csv.writer(f)
        writer.writerow(write_list)
    time.sleep(10)
