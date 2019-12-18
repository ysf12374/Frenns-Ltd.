import torch
import torchvision
from torch.utils.data import DataLoader, TensorDataset
from torchvision.datasets import ImageFolder
dir_image="directory to training data"
ImageFolder=ImageFolder(dir_image, transform=self.transform)
DataLoader=DataLoader(ImageFolder,
						batch_size=self.batch_size,
						num_workers=self.n_workers,
						pin_memory=self.pin_memory,
						shuffle=self.shuffle)
