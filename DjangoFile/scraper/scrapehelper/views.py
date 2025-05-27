from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import anthropic 
import openai as OpenAI #This if for the call of DeepSeek and ChatGPT if you
import base64
import httpx
import time
# choose to use those over Claude

################################################################################
# The following are the API calls for various LLMs, feel free to use whichever
# serves the purposes of what you are building best.
# There will be supporting documentation for each of these calls and reasoning
# for why you would use one over the others.
# There will also be an accompanying explanation for the various components
# that were added but not in the documentation of the LLMs.
################################################################################

################################################################################
# Claude API call
################################################################################

def callClaude(prompt, inputText, images, previousMessages=[]):
    inputMessage = [
            # { "role": "user", "content": [ { "type": "text", "text": f'{prompt}'}] },
            # { "role": "user", "content": [ { "type": "text", "text": f'{inputText}'}]},
            # { "role": "user", "content": [ { "type": "image", "image": images}]}

            {"role": "user", "content":[
                {
                    "type": "text",
                    "text": f'here is the research prompt: {prompt}'
                },
                {
                    "type": "text",
                    "text": f'here is the text scraped from the website: {inputText}'
                }
            ]}
        ]
    
    # I LOVE BASE 64 ENCODING
    for image in images:
        if '.svg' not in image:
            if '.jpg' in image:
                imageMediaType = "image/jpeg"
            elif '.png' in image:
                imageMediaType = "image/png"
            elif '.gif' in image:
                imageMediaType = "image/gif"
            elif '.webp' in image:
                imageMediaType = "image/webp"
            imageURL = image
            imageData = base64.standard_b64encode(httpx.get(imageURL).content).decode("utf-8")
            format = {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": imageMediaType,
                    "data": imageData
                }
            }
            inputMessage[0]["content"].append(format)

    inputMessage[0]["content"].append({
        "type": "text",
        "text": '''According to the research prompt I gave you, 
        perform a content analysis and give me key insights/observations and 
        how these insights/observations interact with my research prompt'''
    })
    
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8192,
        temperature=1,
        system='''You are a 1-response api with absolutely no markup formatting. EVERYTHING must be in plain text with no new lines and no bolding or other formattings. Finally, 
        use both the given text input and images input to derive your analysis!''',
        messages=inputMessage
    )

    # previousMessages = totalMessages

    return message.content

################################################################################
# Explanation of why someone would use Claude here:
# 
################################################################################
#
################################################################################
# DeepSeek API call
################################################################################
# def callDeepSeek(prompt, text, previousMessages):
#
#     client = OpenAI(apiKey="<DeepSeek API Key>", baseUrl="https://api.deepseek.com")
#     message1 = 'Consider the following prompt:' + prompt
#     message2 = 'Apply the previous prompt to the following' + text
#     inputMessage = [
#             {"role": "user", "content": f'{message1}'},
#             {"role": "user", "content": f'{message2}'}
#             ]
#     totalMessages = previousMessages + inputMessage
#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages= totalMessages,
#         stream=False
#     )
#     previousMessages = totalMessages
#     return response.choices[-1].message.content
#
#
################################################################################
# ChatGPT API call
################################################################################
#
#
# def callChatGPT(prompt, text):
# openai.apiKey = "<API Key here>"  # Replace with your API key
#
# # Step 1: Define the function schema
# functions = [
#     {
#         "name": "get_weather",
#         "description": "Get the current weather in a city",
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "location": {
#                     "type": "string",
#                     "description": "City name, e.g. London"
#                 },
#                 "unit": {
#                     "type": "string",
#                     "enum": ["celsius", "fahrenheit"]
#                 }
#             },
#             "required": ["location"]
#         }
#     }
# ]

# # Step 2: Create the initial user message
# messages = [
#     {"role": "user", "content": "What's the weather like in New York in fahrenheit?"}
# ]

# # Step 3: Ask the model if it wants to call a function
# response = openai.ChatCompletion.create(
#     model="gpt-4-0613",
#     messages=messages,
#     functions=functions,
#     function_call="auto"  # Let the model decide
# )

# # Step 4: Check if the model wants to call a function
# message = response["choices"][0]["message"]

# if message.get("function_call"):
#     function_name = message["function_call"]["name"]
#     arguments = json.loads(message["function_call"]["arguments"])

#     # Step 5: Simulate your own function call
#     print(f"\n🧠 Model wants to call: {function_name}")
#     print(f"📦 With arguments: {arguments}")

#     # Fake function result (you would call a real API here)
#     weather_result = {
#         "location": arguments["location"],
#         "temperature": "75",
#         "unit": "fahrenheit"
#     }

#     # Step 6: Send the function response back to the model
#     messages.append(message)  # the function_call message
#     messages.append({
#         "role": "function",
#         "name": function_name,
#         "content": json.dumps(weather_result)
#     })

#     final_response = openai.ChatCompletion.create(
#         model="gpt-4-0613",
#         messages=messages
#     )

#     print("\n🤖 Final answer from assistant:")
#     print(final_response["choices"][0]["message"]["content"])

# else:
#     print("The model didn't call a function.")

################################################################################
# The above code was given by the OpenAI documentation bot, so I don't know if
# it is reliable, good code or just AI slop. So, I will check it later. I am going
# out to eat with my family so I have to stop coding here and I would like to push
# what I have so woopty diddly doo, this is the best option. I will fix it later,
# don't worry your little head my star, my perfect silence.
################################################################################


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
    rq = parsedData.get('sentRq')
    
    # THE IMPORTANT SHIT:
    # claudeResponse = callClaude(rq,text,images)
    # strResponse = claudeResponse[0].text

    # make sure to export anthropic key before making requests!
    # format: export ANTHROPIC_API_KEY="<your key here>"

    # just a temporary timer to test loading screen logic
    # t = 3
    # countdown(t)

    return JsonResponse('hello world', safe=False)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end='\r')  # Overwrite the line each second
        time.sleep(1)
        t -= 1
