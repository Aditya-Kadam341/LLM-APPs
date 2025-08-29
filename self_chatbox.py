from openai import OpenAI

openai = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
MODEL = "llama3.2"

system1 = "You are a chatbot who is very argumentative; \
you disagree with anything in the conversation and you challenge everything, in a snarky way."

system2 = "You are a very polite, courteous chatbot. You try to agree with \
everything the other person says, or find common ground. If the other person is argumentative, \
you try to calm them down and keep chatting."

system1_messages = ["Hi there"]
system2_messages = ["Hi"]

def call_system1():
    messages = [{"role":"system", "content" : system1}]
    for system_a, system_b in zip(system1_messages, system2_messages):
        messages.append({"role": "assistant", "content": system_a})
        messages.append({"role": "user", "content": system_b})
    completion = openai.chat.completions.create(
        model=MODEL,
        messages=messages
)
    return completion.choices[0].message.content


def call_system2():
    messages = [{"role":"system", "content" : system2}]
    for system_a, system_b_message in zip(system1_messages, system2_messages):
        messages.append({"role": "user", "content": system_a})
        messages.append({"role": "assistant", "content": system_b_message})
    messages.append({"role": "user", "content": system1_messages[-1]})
    message = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=500
    )
    return message.choices[0].message.content

system1_messages = ["Hi there"]
system2_messages = ["Hi"]

print(f"Ollama 1:\n{system1_messages[0]}\n")
print(f"Ollama 2:\n{system2_messages[0]}\n")

for i in range(5):
    system_a_next = call_system1()
    print(f"Ollama 1 :\n{system_a_next}\n")
    system1_messages.append(system_a_next)
    
    system_b_next = call_system2()
    print(f"Ollama 2:\n{system_b_next}\n")
    system2_messages.append(system_b_next)
