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

    with open(Path('catalog/catalog.json'), 'r', encoding='utf-8') as file:
        data = json.load(file)

    allVectors = []
    print("Converting images to feature vectors:")
    for d in tqdm.tqdm(data):
        for image in d:
            I = Image.open(os.path.join('data/images', image))
            vec = img2vec.getVec(I)
            allVectors.append(vec)
            I.close()

    tensor = torch.stack(allVectors).to(device)
    with open(Path('catalog/allvectors.pt'), 'wb', ) as file:
        torch.save(tensor.to('cpu'), file)
