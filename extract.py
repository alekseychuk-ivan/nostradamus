import torch
import torchvision
from torchvision.models import vgg16_bn, resnet18, shufflenet_v2_x2_0, squeezenet1_1
from torchvision.transforms import transforms
from PIL import Image
from pathlib import Path
import os

path = Path('data/images/0a836e4128143f881710ae8701b0aea3.jpg')

transform = transforms.Compose([transforms.Resize((224, 224)),
                                 transforms.ToTensor(),
                                 transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

model = resnet18()
img = Image.open(path)
img = transform(img).unsqueeze(dim=0)
print(img.shape)
print(model(img).shape)


class Img2VecResnet18:
    def __init__(self):
        self.device = torch.device("cpu")
        self.numberFeatures = 512
        self.modelName = "resnet-18"
        self.model, self.featureLayer = self.getFeatureLayer()
        self.model = self.model.to(self.device)
        self.model.eval()
        self.toTensor = transforms.ToTensor()

        # normalize the resized images as expected by resnet18
        # [0.485, 0.456, 0.406] --> normalized mean value of ImageNet, [0.229, 0.224, 0.225] std of ImageNet
        self.normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

    def getVec(self, img):
        image = self.normalize(self.toTensor(img)).unsqueeze(0).to(self.device)
        embedding = torch.zeros(1, self.numberFeatures, 1, 1)

        def copyData(m, i, o): embedding.copy_(o.data)

        h = self.featureLayer.register_forward_hook(copyData)
        self.model(image)
        h.remove()

        return embedding.numpy()[0, :, 0, 0]

    def getFeatureLayer(self):
        cnnModel = resnet18(pretrained=True)
        layer = cnnModel._modules.get('avgpool')
        self.layer_output_size = 512

        return cnnModel, layer


# generate vectors for all the images in the set
img2vec = Img2VecResnet18()

allVectors = {}
print("Converting images to feature vectors:")
for image in os.listdir(Path('data/images')):
    I = Image.open(path)
    vec = img2vec.getVec(I)
    allVectors[image] = vec
    I.close()
    break
