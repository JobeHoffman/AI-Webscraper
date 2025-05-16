from openai import OpenAI



client = OpenAI(apiKey="<DeepSeek API Key>", baseUrl="https://api.deepseek.com")

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "user", "content": f'{prompt}'},
    ],
    stream=False
)

print(response.choices[0].message.content)

# we need to put this in views.py later