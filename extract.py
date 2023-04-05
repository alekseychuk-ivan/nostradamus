import torch
from PIL import Image
from pathlib import Path
import os
import json
import tqdm
from utils.Img2vec import Img2VecResnet18

if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
    # generate vectors for all the images in the set
    img2vec = Img2VecResnet18()
    allCatalog = []
    allVectors = []
    files = ['catalog.json', 'allvectors.pt']

    for file in files:
        if os.path.exists(Path(f'catalog/{file}')):
            os.remove(Path(f'catalog/{file}'))

    for catalog in os.listdir('catalog'):
        with open(Path(f'catalog/{catalog}'), 'r', encoding='utf-8') as file:
            data = json.load(file)

        print(f"Converting images from {catalog.split('.')[0]} to feature vectors:")
        for d in tqdm.tqdm(data):
            for image in d:
                try:
                    I = Image.open(Path(os.path.join('data/images', image)))
                    vec = img2vec.getVec(I)
                    allVectors.append(vec)
                    allCatalog.append(d)
                    I.close()
                except:
                    continue

        tensor = torch.stack(allVectors).to(device)
    with open(Path('catalog/allvectors.pt'), 'wb', ) as file:
        torch.save(tensor.to('cpu'), file)
    with open(Path('catalog/catalog.json'), 'w', encoding='utf-8') as file:
        json.dump(allCatalog, file, indent=4, ensure_ascii=False)
