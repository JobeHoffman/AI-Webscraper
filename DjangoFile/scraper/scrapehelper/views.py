from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI

# import LLM api here

def callDeepSeek(prompt, text, images):

    client = OpenAI(apiKey="<DeepSeek API Key>", baseUrl="https://api.deepseek.com")
    message = prompt + ':' + text + images
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": f'{message}'},
        ],
        stream=False
    )

    print(response.choices[0].message.content)

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
