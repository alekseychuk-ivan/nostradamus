import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36 '
}

url = 'https://www.arteks.ooo/catalog/'
pagenurl = 'https://www.arteks.ooo/catalog/?PAGEN_1='

#read catalog page
result = requests.get(url=url, verify=False)
soup = BeautifulSoup(result.text, 'lxml')
with open(Path('data/catalog_arteks.json'), 'a', encoding='utf-8') as file:
    empty_json = dict()
    json.dumps(empty_json,)

# find count of page
cnt_page = int(soup.find_all('a', class_='pagination__pages-link')[-1].get_text('\n', strip=True))
# read all page
for page in range(1, cnt_page + 1):
    result = requests.get(url=f'{pagenurl}{page}', verify=False)
    soup = BeautifulSoup(result.text, 'lxml')

    # find all collection and download images for collection
    all_products = soup.find_all('a', class_='catalog-item')
    for product in all_products:
        model = product.find(class_='catalog-item__collection').get_text('\n', strip=True)
        model = re.sub(r'[\n\s]', '_', model)

        # request page of product
        # create new link
        link = 'https://www.arteks.ooo' + product.get('href')
        result = requests.get(link, verify=False)
        soup = BeautifulSoup(result.text, 'lxml')

        # find section <script> var productObject </script> and get data
        all_image = soup.find_all(['script', ], )[-1].get_text('\n', strip=True).split('=')[-1]
        temp_json = json.loads(all_image[:-1])
        with open('data/temp.json', 'w', encoding='utf-8') as file:
            json.dump(temp_json, file, ensure_ascii=False, indent=4)
        for image in all_image:
            print(image)
            img = 'https://www.arteks.ooo' + image.get('href')
            img1 = image.get('src')
            print(img)
            # print(img1)

        break
    break
