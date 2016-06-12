import json
from scipy import ndimage
from skimage.measure import block_reduce

import sys
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
        return JsonResponse({'ans':np.argmax(ans)})
    return HttpResponse("Error")


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
    net.save("yolo")
    return HttpResponse("good")

@csrf_exempt
def loadNet(request):
    net.load("yolo")
    return HttpResponse("good")