import json
from scipy import ndimage
from skimage.measure import block_reduce

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import network.mnist_loader as mnl
from network.network2 import Network2
from network.network_function import *
import numpy as np
import math
import random

net = Network2([784, 90, 10])


def index(request):
    return render_to_response('index.html')


def train(request):
    print("begin")
    training_data, validation_data, test_data = mnl.load_data_wrapper()
    print("loaded ... starting training")
    ar,steps = net.SGD(training_data, 5, 10, 3.0, test_data=test_data)
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
        print(n)
        ans = net.feedforward(n)
        print(ans)
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


def function(request):
    return render_to_response('function.html')

@csrf_exempt
def function_go(request):
    data = json.loads(request.body)
    f = lambda x: eval(data['function'])

    def makeNetwork(numInputs, numHiddenLayers, numInEachLayer):
        network = Network()
        inputNodes = [InputNode(i) for i in range(numInputs)]
        outputNode = Node()
        network.outputNode = outputNode
        network.inputNodes.extend(inputNodes)

        layers = [[Node() for _ in range(numInEachLayer)] for _ in range(numHiddenLayers)]

        # weights are all randomized
        for inputNode in inputNodes:
            for node in layers[0]:
                Edge(inputNode, node)

        for layer1, layer2 in [(layers[i], layers[i + 1]) for i in range(numHiddenLayers - 1)]:
            for node1 in layer1:
                for node2 in layer2:
                    Edge(node1, node2)

        for node in layers[-1]:
            Edge(node, outputNode)

        return network

    def makeTrainedNetwork(numLayers, numNodes, nIt, rate):
        domain = lambda: [random.random() * math.pi * 4 for _ in range(100)]

        network = makeNetwork(1, numLayers, numNodes)
        labeledExamples = [((x,), f(x)) for x in domain()]
        network.train(labeledExamples, learningRate=rate, maxIterations=nIt)

        errors = [abs(f(x) - network.evaluate((x,))) for x in domain()]
        print("Avg error: %.4f" % (sum(errors) * 1.0 / len(errors)))

        return network

    trained_network = makeTrainedNetwork(int(data['layers']), int(data['nodes']), int(data['iterations']), float(data['rate']))
    p_sw = []
    p_nsw = []
    p_xaxis = []

    for i in np.arange(0, 6.28, 0.05):
        p_sw.append(f(i))
        y_nsw = trained_network.evaluate((i,))
        p_nsw.append(y_nsw)
        p_xaxis.append(i)

    return JsonResponse({
        'data': p_nsw,
        'target': p_sw,
        'output': p_nsw,
        'xaxis': p_xaxis
    })



