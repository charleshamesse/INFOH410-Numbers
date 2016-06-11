import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import network.mnist_loader as mnl
from network.network2 import Network2

net = Network2([784, 100, 10])


def index(request):
    return render_to_response('index.html')


def train(request):
    print("begin")
    training_data, validation_data, test_data = mnl.load_data_wrapper()
    print("loaded ... starting training")
    ar,steps = net.SGD(training_data, 2, 10, 3.0, test_data=test_data)
    data = {'error':ar,'batch':steps}
    return JsonResponse(data)


@csrf_exempt
def recognize(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        a = np.array(data['img'])
        n = a.reshape(-1,100).max(axis=-1) #downsampling
        n = np.ndarray((28*28,1),buffer=np.array(n))
        ans = net.feedforward(n)
        return JsonResponse({'ans':np.argmax(ans)})
    return HttpResponse("Error")