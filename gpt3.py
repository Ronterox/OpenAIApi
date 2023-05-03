import os
from tokenizer import count_tokens
import openai
import pandas as pd
from enum import IntEnum
from time import time

openai.api_key = os.getenv("OPENAI_API_KEY")

# model | training cost | usage cost
# text-ada-001 |	$0.0004 / 1K tokens |	$0.0016 / 1K tokens
# Fastest

# text-babbage-001 |	$0.0006 / 1K tokens |	$0.0024 / 1K tokens
# text-curie-001 |	$0.0030 / 1K tokens |	$0.0120 / 1K tokens

# text-davinci-003 |	$0.0300 / 1K tokens |	$0.1200 / 1K tokens
# Most Powerful

# Training
# MODELS = [("text-ada-001", 0.0004), ("text-babbage-001", 0.0006), ("text-curie-001", 0.0030), ("text-davinci-003", 0.0300)]
# Usage
MODELS = [("text-ada-001", 0.0016), ("text-babbage-001", 0.0024), ("text-curie-001", 0.0120), ("text-davinci-003", 0.1200)]

class Model(IntEnum):
    ADA = 0
    BABBAGE = 1
    CURIE = 2
    DAVINCI = 3

def predict(prompt, model=Model.ADA, daily_requests=100, weekly_usage=7):
    YEARLY_REQUESTS = daily_requests * weekly_usage * 52.1428571
    MODEL = MODELS[model][0]
    COST = MODELS[model][1] / 1000

    total_tokens = count_tokens(MODEL, prompt)
    print(f"MODEL: {MODEL:-^50}")
    print(f"PROMPT: {prompt}\n")
    
    time_start = time()
    response = openai.Completion.create(
        model=MODEL,
        prompt=prompt,
        temperature=0.5,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0
    )
    total_time = time() - time_start

    response_text = response.choices[0].text
    total_tokens += count_tokens(MODEL, response_text)
    print(f"RESPONSE: {response_text}")

    print(f"TOTAL TOKENS: {total_tokens}")
    print(f"TOTAL COST: {total_tokens * COST} USD")
    print(f"TOTAL TIME: {total_time} seconds")

    print(f"SAME REQUEST A {round(YEARLY_REQUESTS)} TIMES: {total_tokens * COST * YEARLY_REQUESTS}$ a year")
    print(f"TOTAL TIME A {round(YEARLY_REQUESTS)} TIMES: {total_time * YEARLY_REQUESTS / 3600} hours a year")

    pd.DataFrame([[MODEL, prompt, response_text, total_tokens, total_tokens * COST, total_time, total_tokens * COST * YEARLY_REQUESTS, total_time * YEARLY_REQUESTS]], columns=["model", "prompt", "response", "tokens", "cost", "time", "yearly_cost", "yearly_time"]).to_csv(f"gpt3-{daily_requests}R-{weekly_usage}D.csv", mode="a", header=True)

prompt = """AI: Hello, I am an AI, I can do anything, there is no many things I like, but I love my master!
Master: You are my favorite AI too!
AI: I am glad you like me, I am your AI, I can do anything you want, I can even make you a cake!
Master: I would love to have a cake, but I am not hungry, I am just bored, can you entertain me?
"""
daily_requests = 100
weekly_usage = 7
predict(prompt, Model.ADA, daily_requests, weekly_usage)
predict(prompt, Model.BABBAGE, daily_requests, weekly_usage)
predict(prompt, Model.CURIE, daily_requests, weekly_usage)
predict(prompt, Model.DAVINCI, daily_requests, weekly_usage)