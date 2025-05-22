from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import anthropic 
import openai as OpenAI #This if for the call of DeepSeek and ChatGPT if you
# choose to use those over Claude

################################################################################
# The following are the API calls for various LLMs, feel free to use whichever
# serves the purposes of what you are building best.
# There will be supporting documentation for each of these calls and reasoning
# for why you would use one over the others.
# There will also be an accompanying explanation for the various components
# that were added but not in the documentation of the LLMs.
################################################################################

previousMessages = []
# This is global that keeps track of the previous messages

################################################################################
# Claude API call
################################################################################

def callClaude(prompt, inputText, images, previousMessages):
    inputMessage = [
            { "role": "user", "content": [ { "type": "text", "text": f'{prompt}'}] },
            { "role": "user", "content": [ { "type": "text", "text": f'{inputText}'}]},
            { "role": "user", "content": [ { "type": "image", "image": images}]}
        ]
    totalMessages = previousMessages + inputMessage
    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=10000,
        temperature=1,
        system="Provide a clear and unbiased approach to the following inputs",
        messages=totalMessages
    )
    previousMessages = totalMessages
    return message.content

################################################################################
# Explanation of why someone would use Claude here
################################################################################

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
# don;t worry your little head my star, my perfect silence.
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
    # PUT PYTHON CODE HERE
    # prompt = 'put prompt here'
    # claudeResponse = callClaude(prompt,text,images)
    return JsonResponse(text, safe=False)
