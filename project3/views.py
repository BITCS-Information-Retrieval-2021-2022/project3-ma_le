# Create your views here.
import json

from django.http import HttpResponse
from project3 import function as F


def search(request):
    value = json.loads(request.body)['value']
    obj_return = {}
    res, sorted_res = F.fuzz_search(value)

    if len(res) == 0:
        obj_return['status'] = 201  # not find
    else:
        obj_return['status'] = 200  # find
        for d in res:
            del d['inCitations']
            del d['outCitations']
        obj_return['data'] = res
        obj_return['sorted_data'] = sorted_res
    return HttpResponse(json.dumps(obj_return))


def draw(request):
    value = json.loads(request.body)['value']

    obj_return = F.draw(value)

    return HttpResponse(json.dumps(obj_return))
