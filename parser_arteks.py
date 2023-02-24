import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import json

requests.packages.urllib3.disable_warnings()
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,/;q=0.8,'
              'application/signed-exchange;v=b3;q=0.7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36 '
}

url = 'https://www.arteks.ooo/catalog/'
pagenurl = 'https://www.arteks.ooo/catalog/?PAGEN_1='

#read catalog page
result = requests.get(url=url, verify=False, headers=headers)
soup = BeautifulSoup(result.text, 'lxml')

# find count of page
cnt_page = int(soup.find_all('a', class_='pagination__pages-link')[-1].get_text('\n', strip=True))
catalog_dct = json.loads("{}")
image_dct = []

# read all page
for page in range(1, cnt_page + 1):
    print(f'{page} страница каталога из {cnt_page} страниц.')
    result = requests.get(url=f'{pagenurl}{page}', verify=False)
    soup = BeautifulSoup(result.text, 'lxml')

    # find all collection and download images for collection
    all_products = soup.find_all('a', class_='catalog-item')
    print(f'Найдено {len(all_products)} коллекций.')
    for product in all_products:
        collection = product.find(class_='catalog-item__collection').get_text('\n', strip=True)
        collection = re.sub(r'[\n\s]', '_', collection)
        print(f'Загружается коллекция {collection}.')

        # request page of product
        # create new link
        link = 'https://www.arteks.ooo' + product.get('href')
        result = requests.get(link, verify=False, headers=headers)
        soup = BeautifulSoup(result.text, 'lxml')

        # find section <script> var productObject </script> and get data
        all_image = soup.find_all(['script', ], )[-1].get_text('\n', strip=True).split('=')[-1]
        temp_json = json.loads(all_image[:-1])
        catalog_dct.update(temp_json)

        #get data from json
        for model in temp_json:
            mod = temp_json[model]
            textures = mod['textures']

            # download and save images
            for texture in textures:
                path = texture['mini']
                name = path.split('/')[-1]
                image_dct.append({name: model})
                imgurl = 'https://www.arteks.ooo' + path
                res = requests.get(url=imgurl, headers=headers, verify=False)
                content = res.content
                with open(Path(f'data/images/{collection}_{name}'), 'wb') as file:
                    file.write(content)
            break

with open(Path('data/catalog_arteks.json'), 'w', encoding='utf-8') as file:
    json.dump(catalog_dct, file, indent=4, ensure_ascii=False)

with open(Path('data/catalog.json'), 'w', encoding='utf-8') as file:
    json.dump(image_dct, file, indent=4, ensure_ascii=False)
