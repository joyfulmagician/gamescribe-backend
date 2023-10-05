import os
from os import environ
from urllib.parse import urlparse
from dotenv import dotenv_values

import re
import json
import openai

env_vars = dotenv_values('.env')
openai.api_key = env_vars["OPENAI_API_KEY"]

current_directory = os.getcwd()
file_path = os.path.join(current_directory, "data/data.json")

with open(file_path, 'r') as dataFile:
    data = json.load(dataFile)

text = ""
for item in data:
    text += "{"
    for key, value in item.items():
        text += f"Monster { key } : { value }" + "\n"
    text += "}\n\n"
        
dataFile.close()
prompt = f"Monster Data: \n{text}\n\nPlease provide a human readable content of this data. Should be understandable to 18 year old. You must reference this data for generating content. There are lots of monsters information and you can generate the monster description based on this data. The data consists of objects of many monsters, and there are many different monsters in the data. Therefore, based on the user's message, you find a suitable monster in the data and write a description of that monster based on that monster's information. Please don't make unreal data. You have to make the content from data. It allows users to feel a sense of life and vividly describes the characteristics of the monster.\n\n"

sample_message = [
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": "It should be large, have wings, and be similar to a dradon."
            },
            {
                "role": "assistant",
                "content": """
                    Introducing the Draegonspire, a fearsome and majestic creature that prowls the shadowed realms of your game's world. Standing at a towering height with scales as dark as midnight, the Draegonspire commands both awe and terror. Its eyes, blazing orbs of molten gold, possess an uncanny intelligence that pierces through the deepest corners of your soul.

                    With wings that stretch wide and powerful, the Draegonspire dominates the skies, casting an ominous silhouette as it soars. Its talons, sharp as obsidian blades, can tear through even the hardiest of defenses, making it a formidable adversary. Yet, it's not just its physical prowess that makes the Draegonspire a creature to be reckoned with. Legends speak of its ability to manipulate the very elements, conjuring storms that darken the sun and crack the earth.

                    But within this terrifying exterior lies a complexity that challenges expectations. Whispers carried by the wind claim that the Draegonspire is a guardian of forgotten knowledge, a sentinel of ancient secrets buried deep within the heart of the world. Some say it can be appeased with offerings of precious gems and rare herbs, and in return, it imparts hidden wisdom to those who prove themselves worthy.

                    Venture forth, for encountering the Draegonspire will test your courage, wit, and strategy. Will you face it as an adversary, driven by the desire to conquer, or will you seek to unravel the enigma it embodies and uncover the truths that lie beneath its majestic exterior? The choice is yours, as you navigate the uncharted territories where legends and reality intertwine.
                """
            }
        ]

def generate_content(user_input):

    print(prompt)

    sample_message.append({
        "role": "user",
        "content": user_input
    })

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = sample_message
    )

    if response and response.choices:
        assistant_reply = response.choices[0].message["content"]

        sample_message.append({
            "role": "assistant",
            "content": assistant_reply
        })

        return assistant_reply
    else:
        return "Error"

def generate_question():
    pass