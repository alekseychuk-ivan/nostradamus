from torchvision.models import vgg16_bn, resnet18, shufflenet_v2_x2_0, squeezenet1_1
import torch
from torchvision.transforms import transforms
import torch.nn as nn


class Img2VecResnet18:
    def __init__(self, device=None):
        self.device = torch.device('cuda' if torch.cuda.is_available() else "cpu")
        self.modelName = "resnet-18"
        self.model = nn.Sequential(*list(resnet18(weights="ResNet18_Weights.DEFAULT").children())[:-1])
        self.model = self.model.to(self.device)
        self.model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
        if device is not None:
            self.device = device

    def getVec(self, img):
        img = self.transform(img).unsqueeze(dim=0).to(self.device)
        image = self.model(img).flatten().to('cpu')

        return (image / torch.linalg.norm(image)).detach()


def recommend(vec, feature_list, device='cpu'):
    vec = vec.unsqueeze(dim=0).to(device)
    cos = nn.CosineSimilarity(dim=1, eps=1e-6)
    dist = cos(feature_list, vec)
    pdist, idx = torch.sort(dist, descending=True)

    return idx
