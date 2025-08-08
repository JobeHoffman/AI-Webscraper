from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
import json
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import anthropic 
import openai as OpenAI #This if for the call of DeepSeek and ChatGPT if you
import base64
import httpx
from openai import OpenAI

# agentic AI setup
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor

# tools import
from langchain.tools import Tool
from .tools import *

# ToDos: agentic ai integration
load_dotenv()
# choose to use those over Claude

################################################################################
# The following are the API calls for various LLMs, feel free to use whichever
# serves the purposes of what you are building best.
# There will be supporting documentation for each of these calls and reasoning
# for why you would use one over the others.
# There will also be an accompanying explanation for the various components
# that were added but not in the documentation of the LLMs.
# The calls now are made as if the AI were used for social media research.
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
        "text": '''According to the research question I gave you, 
        perform a content analysis. Give me key insights/observations keeping in mind 
        how these insights/observations interact with my research question'''
    })
    
    client = anthropic.Anthropic() # API key goes here
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8192,
        temperature=1,
        system='''You are a 1-response api with absolutely no markup formatting. 
        EVERYTHING must be in plain text with no new lines and no bolding or other formattings. 
        Finally, use both the given text input and images input to derive your analysis!''',
        messages=inputMessage
    )

    # previousMessages = totalMessages

    return message.content

################################################################################
# Explanation of why someone would use Claude here:
# Claude is the most expensive in terms of API key pricing, but in every other
# regard it is one of the best LLMs on the market.
################################################################################
#
################################################################################
# DeepSeek API call
################################################################################
#
# def callDeepSeek(prompt, text, previousMessages = []):
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
################################################################################
# Explanation of why someone would use DeepSeek here:
# DeepSeek is the least expensive on the market and gives very good results, 
# in many cases comparable to Claude and Chat-GPT. However, it is unable to
# take images as inputs which can become a problem for the specific use case
# the project is tuned to now (social media research).
################################################################################
#
################################################################################
# ChatGPT API call
################################################################################

def callOpenAI(rq, inputText, images):
    client = OpenAI()
    input=[{   
            "role": "user",
            "content": [
                {
                    "type": "input_text", 
                    "text": f"What are some key details in the images provided in relation to the rq?: {rq}"
                }
            ]
        }
    ]

    # this is an expansive list
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
                "type": "input_image",
                "image_url": f"data:image/jpeg;base64,{imageData}"
            }
            input[0]["content"].append(format)
    
    imageAnalysis = client.responses.create(
        model="gpt-4o-mini-2024-07-18",
        input=input
    )

    print(imageAnalysis.output_text)

    class responseFormat(BaseModel):
        overview_of_content: str
        perspectives_within_content: str
        overall_rhetorical_analysis: str
        overall_usefulness_to_users_research_question: str

    parser = PydanticOutputParser(pydantic_object = responseFormat)

    prompt1 = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are a research tool helping students extract meaningful insight from different sources.
                Since you are capable of analyzing images, you must analyze the images
                You must refrain from using markup-formatting and follow this format when wrapping your output:
                {format_instructions}
                """
            ),
            ("placeholder", "{agent_scratchpad}"),
            (
                "human", "{rq} {text} {image_analysis}"
            ),
        ]
    ).partial(format_instructions = parser.get_format_instructions())

    # instantiate tools here
    tools = [
        websearch
    ]

    agent1 = create_tool_calling_agent(
        llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18"),
        prompt = prompt1,
        tools = tools
    )
    

    executor1 = AgentExecutor(agent = agent1, tools = tools, verbose = True)


    response1 = executor1.invoke(
        {
            "rq":rq,
            "text": inputText,
            "image_analysis":imageAnalysis.output_text
,
        }
    )
    query = f"analyse this image based on this RQ: {rq}"

    print(response1.get('output'))

    return response1.get('output')




################################################################################
# Explanation of why someone would use ChatGPT here:
# ChatGPT allows for images to be inputs and is less expensive than Claude.
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
    
    # THE IMPORTANT  (I commented ts out cus too expensive):
    openAiResponse = callOpenAI(rq,text,images)
    # strResponse = claudeResponse[0].text

    # make sure to export anthropic key before making requests!
    # format: export ANTHROPIC_API_KEY="<your key here>"
    # for server hosting websites like render, API key is stored as env

    # temporary = rq + text + str(images)

    return JsonResponse(openAiResponse, safe=False)

