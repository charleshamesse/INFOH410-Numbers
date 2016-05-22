from django.http import HttpResponse
from django.template import loader
import os.path
from network import network  as nn
from network import mnist_loader
from django.contrib.staticfiles.templatetags.staticfiles import static
from network.network import Network, load_data_shared
from network.layers.cp import ConvPoolLayer
from network.layers.fc import FullyConnectedLayer
from network.layers.sm import SoftmaxLayer

path = os.getcwd() + "/static/mnist.pkl.gz"
print  path
training_data, validation_data, test_data = load_data_shared(static(path))
mini_batch_size = 10

def index(request):
    template = loader.get_template('index.html')
    basic_conv(3, 1)
    context = {
        'test': 'wassup'
    };
    return HttpResponse(template.render(context, request))


def basic_conv(n=3, epochs=60):
    for j in range(n):
        print "Conv + FC architecture"
        net = Network([
            ConvPoolLayer(image_shape=(mini_batch_size, 1, 28, 28),
                          filter_shape=(20, 1, 5, 5),
                          poolsize=(2, 2)),
            FullyConnectedLayer(n_in=20 * 12 * 12, n_out=100),
            SoftmaxLayer(n_in=100, n_out=10)], mini_batch_size)
        net.SGD(training_data, epochs, mini_batch_size, 0.1, validation_data, test_data)
    return net
