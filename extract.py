import torch
import torch.nn as nn
import torchvision
from torchvision.models import vgg16_bn, resnet18, shufflenet_v2_x2_0, squeezenet1_1
from torchvision.transforms import transforms
from PIL import Image
from pathlib import Path
import os


class Img2VecResnet18:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
        self.modelName = "resnet-18"
        self.model = nn.Sequential(*list(resnet18(weights=True).children())[:-1])
        self.model = self.model.to(self.device)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

    def getVec(self, img):
        img = self.transform(img).unsqueeze(dim=0)
        image = self.model(img).flatten()

        return (image / torch.linalg.norm(image)).detach().numpy()



# generate vectors for all the images in the set
img2vec = Img2VecResnet18()

since = time.time()
allVectors = {}
print("Converting images to feature vectors:")
for image in os.listdir(Path('data/images')):
    I = Image.open(os.path.join('data/images', image))
    vec = img2vec.getVec(I)
    allVectors[image] = vec
    I.close()
