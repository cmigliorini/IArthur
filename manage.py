#!/usr/bin/env python
import os
import sys
import torch.nn as nn
import torch

class Net(nn.Module):
    def __init__(self, cuda = True):
        super(Net, self).__init__()
        self.couche1 = nn.Linear(6*7, 30, bias = False)
        self.couche2 = nn.Linear(30, 10, bias = False)
        self.couche3 = nn.Linear(10, 1, bias = False)
        self.sigmoid = torch.sigmoid
        if cuda:
            self.couche1 = self.couche1.cuda()
            self.couche2 = self.couche2.cuda()
            self.couche3 = self.couche3.cuda()
        

    def forward(self, x):
        x = self.sigmoid(self.couche1(x))
        x = self.sigmoid(self.couche2(x))
        x = self.couche3(x)
        return x

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IArthur.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
