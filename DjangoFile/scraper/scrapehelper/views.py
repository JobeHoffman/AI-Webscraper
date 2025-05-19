from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import anthropic

# import LLM api here
def callClaude(prompt, inputText, images):

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=1000,
        temperature=1,
        system="You are a data scientist who",
        messages=[
            { "role": "user", "content": [ { "type": "text", "text": f'{prompt}'}] },
            { "role": "user", "content": [ { "type": "text", "text": f'{inputText}'}]},
            { "role": "user", "content": [ { "type": "image", "image": images}]}
        ]
    )
    return message.content

# def callDeepSeek(prompt, text, images):

#     client = OpenAI(apiKey="<DeepSeek API Key>", baseUrl="https://api.deepseek.com")
#     message1 = 'Consider the following prompt:' + prompt
#     message2 = 'Apply the previous prompt to the following' + text + images
#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=[
#             {"role": "user", "content": f'{message1}'},
#             {"role": "user", "content": f'{message2}'}
#         ],
#         stream=False
#     )

#     print(response.choices[1].message.content)

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
