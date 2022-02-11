import csv
import requests
from bs4 import BeautifulSoup
import time
import os

def get_lat_lng(address):
  url = 'http://www.geocoding.jp/api/'
  latlngs = []
  payload = {'q': address}
  r = requests.get(url, params=payload)
  ret = BeautifulSoup(r.content, 'lxml')
  try:
    x = ret.find('lat').string
    y = ret.find('lng').string
    return x, y
  except:
    print('error')
    return 0, 0

output_file_list = ['center.csv']
for output_file in output_file_list:
  input_path = 'data/{}'.format(output_file)
  output_file = '{}'.format(output_file)
  data_dir = 'zahyo'

  if not os.path.exists(data_dir):
    os.mkdir(data_dir)
  
  f1 = open(input_path)
  reader = csv.reader(f1)

  f2 = open('{}/{}'.format(data_dir, output_file), 'w')
  writer = csv.writer(f2)

  zahyo_d = {}
  for (num, row) in enumerate(reader):
    address = row[1]
    if address in zahyo_d:
      print('skip')
      x = zahyo_d[address][0]
      y = zahyo_d[address][1]
    else:
      print('get zahyo...')
      x, y = get_lat_lng(address)
      time.sleep(5)
      if x==0 and y==0:
        continue
      zahyo_d[address] = [x, y]
    row.append(x)
    row.append(y)
    writer.writerow(row)
  f1.close()
  f2.close()
