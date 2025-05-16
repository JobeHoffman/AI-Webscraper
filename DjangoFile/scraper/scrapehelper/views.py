from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

# import LLM api here

# Create your views here.
def home(request):
    testVar = getData()
    return HttpResponse(testVar)

def getData():
    return "test test"

@csrf_exempt
def get_data_json(request):
    # use POST to retrieve data
    parsedData = json.loads(request.body)
    text = parsedData.get('scrapedText')
    images = parsedData.get('scrapedImages')
    
    # PUT PYTHON CODE HERE
    
    
    return JsonResponse([text, images], safe=False)
