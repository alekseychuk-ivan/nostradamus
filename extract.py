import torch
import torchvision
from torchvision.models import vgg16_bn, resnet18, shufflenet_v2_x2_0, squeezenet1_1
from torchvision.transforms import transforms
from PIL import Image
from pathlib import Path

path = Path('data/images/0a836e4128143f881710ae8701b0aea3.jpg')

transform = transforms.Compose([transforms.Resize((224, 224)),
                                 transforms.ToTensor(),
                                 transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])

model = resnet18()
img = Image.open(path)
img = transform(img).unsqueeze(dim=0)
print(img.shape)
print(model(img).shape)
