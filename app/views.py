import gzip
import json
import os
import random
from scipy import ndimage
from skimage.measure import block_reduce

import sys

import cPickle

import scipy
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import network.mnist_loader as mnl
from network.network2 import Network2

net = Network2([784, 100, 30, 10])


def index(request):
    return render_to_response('index.html')


def train(request):
    print("begin")
    training_data, validation_data, test_data = mnl.load_data_wrapper()
    print("loaded ... starting training")
    ar,steps = net.SGD(training_data, 30, 10, 3.0, test_data=test_data)
    data = {'error':ar,'batch':steps}
    return JsonResponse(data)


@csrf_exempt
def recognize(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        a = np.array(data['img'])
        s = a.reshape((280,280))
        n = block_mean(s, 10)
        n /= float(255)
        n = np.ndarray((28*28,1),buffer=np.array(n))
        ans = net.feedforward(n)
        return JsonResponse({'ans':np.argmax(ans),'x':range(0,9),'ansL':ans.tolist()})
    return HttpResponse("Error")


def recognizeMNist(request):
    path = os.getcwd() + "/app/static/mnist.pkl.gz"
    f = gzip.open(path, 'rb')
    data_x,data_y, yolo = cPickle.load(f)
    d_x, d_y = data_x
    f.close()
    rand = random.randint(0,len(d_x))
    ans = net.feedforward(d_x[rand].reshape((784,1)))
    img = d_x[rand].reshape(28,28)*255
    img = scipy.ndimage.zoom(img, 10, order=0)
    img = img.reshape((78400,1)).tolist()
    return JsonResponse({'ans':np.argmax(ans),'img':img})


def block_mean(ar, fact):
    assert isinstance(fact, int), type(fact)
    sx, sy = ar.shape
    X, Y = np.ogrid[0:sx, 0:sy]
    regions = sy/fact * (X/fact) + Y/fact
    res = ndimage.mean(ar, labels=regions, index=np.arange(regions.max() + 1))
    res.shape = (sx/fact, sy/fact)
    return res


@csrf_exempt
def saveNet(request):
    net.save("configNeuralNetwork")
    return HttpResponse("good")

@csrf_exempt
def loadNet(request):
    net.load("configNeuralNetwork")
    return HttpResponse("good")