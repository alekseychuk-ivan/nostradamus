import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json

dct = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36 '
}

url = 'https://www.arteks.ooo/catalog/'
pagenurl = 'https://www.arteks.ooo/catalog/?PAGEN_1='

result = requests.get(url=url, verify=False)
soup = BeautifulSoup(result.text, 'lxml')
# all_products = soup.find_all('a', class_='catalog-item')
all_products_dict = dict()
cnt_page = int(soup.find_all('a', class_='pagination__pages-link')[-1].get_text('\n', strip=True))
for page in range(1, cnt_page + 1):
    result = requests.get(url=f'{pagenurl}{page}', verify=False)
    soup = BeautifulSoup(result.text, 'lxml')
    all_products = soup.find_all('a', class_='catalog-item')
    for product in all_products:
        model = product.find(class_='catalog-item__collection').get_text('\n', strip=True)
        model = re.sub(r'[\n\s]', '_', model)
        link = 'https://www.arteks.ooo' + product.get('href')
        all_products_dict[model] = link
        newresult = requests.get(link, verify=False)
        newsoup = BeautifulSoup(newresult.text, 'lxml')
        all_image = newsoup.find_all('a', class_='product-card__textures-img')
        for image in all_image:
            print(image)
            img = 'https://www.arteks.ooo' + image.get('href')
            img1 = image.get('src')
            print(img)
            # print(img1)

        break
    break

with open('data/catalog_arteks.json', 'w', encoding='utf-8') as file:
    json.dump(all_products_dict, file, ensure_ascii=False, indent=4)
