import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI

print("Hello Aditya")

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
# MODEL = "llama3.2"
# response = openai.chat.completions.create(
#  model=MODEL,
#  messages=[{"role": "user", "content": "What is 2 + 2?"}]
# )

# message = "Hello, GPT! This is my first ever message to you! Hi!. What are you called ?"
# response = openai.chat.completions.create(model="llama3.2", messages=[{"role":"user", "content":message}])
# print(response.choices[0].message.content)



headers = {
 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

class Website:
    def __init__(self,url):
        self.url = url
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")
        self.title = soup.title.string if soup.title else "no title found"
        for irrelevant in soup.body(["script","style", "img", "input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n",strip=True)
ed = Website("https://edwarddonner.com")
# print(ed.title)
# print(ed.text)


# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."

system_prompt = "You are an assistant that analyzes the contents of a website \
and provides a short summary, ignoring text that might be navigation related. \
Respond in markdown in Spanish."


# A function that writes a User Prompt that asks for summaries of websites:

def user_prompt_for(website):
    user_prompt = f"You are looking at a website titled {website.title}"
    user_prompt += "\nThe contents of this website is as follows; \
                    please provide a short summary of this website in markdown. \
                    If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt

# print(user_prompt_for(ed))


messages = [
    {"role": "system", "content": "You are a snarky assistant"},
    {"role": "user", "content": "What is 2 + 2?"}
]
response = openai.chat.completions.create(model="llama3.2",messages=messages)
# print(response.choices[0].message.content)

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for(website)}
    ]

# print(messages_for(ed))


def summarize(url):
    website = Website(url)
    response= openai.chat.completions.create(model="llama3.2", messages=messages_for(website))
    return response.choices[0].message.content

# summarize("https://edwarddonner.com")


########################################## OR ##########################################


import ollama
response = ollama.chat(model = "llama3.2",messages=messages)
# print(response['message']['content'])



########################################## Same for summarization ##########################################


import ollama
url = "https://edwarddonner.com"
website = Website(url)
response = ollama.chat(model = "llama3.2",messages=messages_for(website))
print(response['message']['content'])
