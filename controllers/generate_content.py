import os
from os import environ
from urllib.parse import urlparse
from dotenv import dotenv_values

import re
import json
import openai

env_vars = dotenv_values('.env')
openai.api_key = env_vars["OPENAI_API_KEY"]
        
content_prompt = f"You are a monster content generator. You can create descriptions and stat blocks. When you create a description, you have to include the stat block. If the user message is not related with monster specialist you answer only 'Introducing a monster...' or blank message."

key_array = ["Environment", "Size", "Appearance", "Attack Mode", "Movement Speed"]
key_array = [str(item) for item in key_array]
key_string = ", ".join(key_array)
question_prompt = f"You are a helpful AI assistant that makes the questions for monster content and stat. You can create questions for generating monster content. {key_string}. They are keys that help create the monster's content. If you can know about the key from user's message, you have to ask other keys. And if you know about all keys from user's messages, you don't ask anymore and answer only 'Thanks'."


quiz_sample_message = [
    {
        "role": "system",
        "content": question_prompt
    },
    {
        "role": "user",
        "content": "Hi"
    },
    {
        "role": "assistant",
        "content": "Hello! How can I assist you today?"
    },
    {
        "role": "user",
        "content": "I wanna build a monster content."
    },
    {
        "role": "assistant",
        "content": "That's great! I can help you with that. To get started, could you please provide me with some information about the monster you would like to create? Specifically, I need to know about the monster's environment, size, and appearance."
    },
    {
        "role": "user",
        "content": "Live in forest and have wings"
    },
    {
        "role": "assistant",
        "content": "Great! We have the environment and appearance covered. Now, could you please let me know the size of the monster? Is it small, medium, or large?"
    },
    {
        "role": "user",
        "content": "I'm not sure"
    },
    {
        "role": "assistant",
        "content": "No problem! I can help you determine the size of the monster based on its environment and appearance. Since it lives in the forest and has wings, it could be a medium-sized creature that is agile and capable of flying through the trees. Does that sound suitable for your monster?"
    },
    {
        "role": "user",
        "content": "Sure!"
    },
    {
        "role": "assistant",
        "content": "Thanks!"
    }
]

content_sample_message = [
            {
                "role": "system",
                "content": content_prompt
            },
            {
                "role": "user",
                "content": "It should be large, have wings, and be similar to a dragon."
            },
            {
                "role": "assistant",
                "content": """
                    Description:
                    The Draconian Monarch is a colossal creature that strikes fear into the hearts of all who lay eyes upon it. Standing at a towering height of 30 feet, this majestic beast possesses a muscular and serpentine body covered in shimmering scales that glisten in the sunlight. Its wings, spanning an impressive 50 feet, are adorned with intricate patterns resembling stained glass, giving it an ethereal and otherworldly appearance. The Draconian Monarch's head features a pair of piercing, intelligent eyes that glow with an intense, fiery hue, and its mouth is filled with rows of razor-sharp teeth capable of rending even the toughest armor.

                    Stat Block:
                    - Size: Large
                    - Hit Points: 300
                    - Armor Class: 18
                    - Speed: 40 feet, fly 80 feet
                    - Strength: 22 (+6)
                    - Dexterity: 14 (+2)
                    - Constitution: 20 (+5)
                    - Intelligence: 16 (+3)
                    - Wisdom: 14 (+2)
                    - Charisma: 18 (+4)

                    Abilities:
                    - Fire Breath: The Draconian Monarch can unleash a devastating cone of fire, dealing 6d10 fire damage to all creatures within a 60-foot cone. Targets must make a Dexterity saving throw (DC 17) to halve the damage.
                    - Wing Buffet: With a mighty flap of its wings, the Draconian Monarch creates a powerful gust of wind, forcing all creatures within a 20-foot radius to make a Strength saving throw (DC 18) or be knocked prone.
                    - Frightful Presence: Any creature within 120 feet of the Draconian Monarch must succeed on a Wisdom saving throw (DC 16) or become frightened for 1 minute.
                    - Legendary Resistance (3/Day): If the Draconian Monarch fails a saving throw, it can choose to succeed instead.
                    - Multiattack: The Draconian Monarch can make three attacks per round, choosing from its bite, claw, and tail attacks.
                    - Bite: Melee Weapon Attack, +10 to hit, reach 10 ft., one target. Hit: 2d10 + 6 piercing damage.
                    - Claw: Melee Weapon Attack, +10 to hit, reach 10 ft., one target. Hit: 2d6 + 6 slashing
                """
            },
            {
                "role": "user",
                "content": "Hi"
            },
            {
                "role": "assistant",
                "content": "Introducing a monster..."
            },
            {
                "role": "user",
                "content": "I wanna build a monster content"
            },
            {
                "role": "assistant",
                "content": "Introducing a monster..."
            }
        ]

def generate_content(user_input):

    content_sample_message.append({
        "role": "user",
        "content": user_input
    })

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = content_sample_message
    )

    if response and response.choices:
        assistant_reply = response.choices[0].message["content"]

        content_sample_message.append({
            "role": "assistant",
            "content": assistant_reply
        })

        return assistant_reply
    else:
        return "Error"

def generate_question(user_input):
    
    quiz_sample_message.append({
        "role": "user",
        "content": user_input
    })

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = quiz_sample_message
    )

    if response and response.choices:
        assistant_reply = response.choices[0].message["content"]

        quiz_sample_message.append({
            "role": "assistant",
            "content": assistant_reply
        })

        return assistant_reply
    else:
        return "Error"

    pass