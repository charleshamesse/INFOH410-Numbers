import json
from django.http import HttpResponse, JsonResponse
import os.path
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from network.network import Network, load_data_shared
from network.layers.cp import ConvPoolLayer
from network.layers.fc import FullyConnectedLayer
from network.layers.sm import SoftmaxLayer
from Numbers.settings import BASE_DIR
import numpy as np

path = os.getcwd() + "/app/static/mnist.pkl.gz"
print path
training_data, validation_data, test_data = load_data_shared(static(path))
mini_batch_size = 10
net = Network([
    ConvPoolLayer(image_shape=(mini_batch_size, 1, 28, 28),
                  filter_shape=(20, 1, 5, 5),
                  poolsize=(2, 2)),
    FullyConnectedLayer(n_in=20 * 12 * 12, n_out=100),
    SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)


def index(request):
    return render_to_response('index.html')


def train(request):
    ar,steps = basic_conv(1, 1)
    data = {'error':ar,'batch':steps}
    return JsonResponse(data)

def basic_conv(n=3, epochs=60):
    ar = net.SGD(training_data, epochs, mini_batch_size, 0.1, validation_data, test_data)
    return ar


@csrf_exempt
def recognize(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        a = np.array(data['img'])
        n = a.reshape(-1,100).max(axis=-1) #downsampling

        return HttpResponse("OK")
    return HttpResponse("Error")