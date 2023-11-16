import os
from os import environ
from urllib.parse import urlparse
from dotenv import dotenv_values
from models.monsters import Monsters

import re
import json
import openai

env_vars = dotenv_values('.env')
openai.api_key = env_vars["OPENAI_API_KEY"]

monster_model = Monsters()
        
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
        "content": """Hello! I need you to generate questions for monster content and stat. Here's an example: If I give you liek that: 'Monster live in forest and have wings', I need you to say : 'Great! We have the environment and appearance covered. Now, could you please let me know the size of the monster? Is it small, medium, or large?'"""
    },
    {
        "role": "assistant",
        "content": "Sure thing!"
    },
]

content_prompt = "You are a monster content generator. You can create descriptions and stat blocks. When you create a description, you have to include the stat and ability block. Also you should include the 'Action', 'Legendary Actions' section. For the ability part, you can use short words like 'Str', 'Dex' for 'Strength', 'Dexterity' and so on. If you get additional features, you can update the monster content. You have to format the monster content in a homebrewery markdown. If you can't generate the monster content, answer is empty string."

markdown_sample = """
## Forest Guardian

*Large fey, neutral*

---

###

- **Armor Class** 17 (natural armor)
- **Hit Points** 136 (13d10 + 65)
- **Speed** 40 ft.

---

###

|STR|DEX|CON|INT|WIS|CHA|
|-|-|-|-|-|-|
|20 (+5)|16 (+3)|20 (+5)|14 (+2)|18 (+4)|16 (+3)|

---

###

- **Skills** Perception +8, Stealth +6
- **Damage Resistances** bludgeoning, piercing, and slashing damage from nonmagical attacks
- **Damage Immunities** poison
- **Condition Immunities** poisoned
- **Senses** darkvision 60 ft., passive Perception 18
- **Languages** Sylvan, Elvish
- **Challenge** 9 (5,000 XP)

---

###

***Innate Spellcasting.*** The forest guardian's innate spellcasting ability is Wisdom (spell save DC 16). It can innately cast the following spells, requiring no material components:

- At will: *druidcraft, entangle, pass without trace*
- 3/day each: *call lightning, barkskin*
- 1/day: *plant growth*

***Tree Stride.*** Once on its turn, the forest guardian can use 10 feet of its movement to step magically into one living tree within its reach and emerge from a second living tree within 60 feet of the first tree, appearing in an unoccupied space within 5 feet of the second tree. Both trees must be Large or bigger.

***Regeneration.*** The forest guardian regains 10 hit points at the start of its turn if it has at least 1 hit point.

***Spellbreaker.*** The forest guardian has advantage on saving throws against spells and other magical effects.

---

### Actions

***Multiattack.*** The forest guardian makes two attacks: one with its *wooden club* and one with its *thorny vine whip*.

***Wooden Club.*** *Melee Weapon Attack:* +9 to hit, reach 10 ft., one target. *Hit:* 14 (2d8 + 5) bludgeoning damage.

***Thorny Vine Whip.*** *Melee Weapon Attack:* +9 to hit, reach 15 ft., one target. *Hit:* 14 (2d8 + 5) slashing damage plus 7 (2d6) poison damage, and the target must succeed on a DC 16 Constitution saving throw or become poisoned for 1 minute. The target can repeat the saving throw at the end of each of its turns, ending the effect on itself on a success.

---

### Legendary Actions

The forest guardian can take 3 legendary actions, choosing from the options below. Only one legendary action option can be used at a time and only at the end of another creature's turn. The forest guardian regains spent legendary actions at the start of its turn.

***Wooden Club.*** The forest guardian makes a wooden club attack.

***Entwining Roots (Costs 2 Actions).*** The forest guardian magically causes grass and vines to grow rapidly from the ground in a 20-foot radius centered on itself. The area becomes difficult terrain, and any creature that starts its turn in the area must succeed on a DC 16 Strength saving throw or have its speed reduced to 0 until the start of its next turn.

***Healing Surge (Costs 3 Actions).*** The forest guardian regains 30 hit points.
"""

content_sample_message = [
    {
        "role": "system",
        "content": content_prompt
    },
    {
        "role": "user",
        "content": f"Hello! I need you to generate monster content and return it to me as homebrewery markdown content. The homebrewery markdown content must start with &&& and end with &&&. Here's an example: If I give you like that: 'Monster live in forest', I need you to say like that: '&&&{markdown_sample}&&&'"
    },
    {
        "role": "assistant",
        "content": "Sure thing!"
    }
]

def generate_content(message_list, last_content):
    messages = content_sample_message + message_list

    if last_content != "":
        messages[-1]["content"] += "This is last generated monster content : " + last_content

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = messages
    )

    if response and response.choices:
        assistant_reply = response.choices[0].message["content"]

        print(f"=============Assistant reply: {assistant_reply}")

        pattern = r'&&&(.*?)&&&'
        result = re.search(pattern, assistant_reply, re.DOTALL)
        if result:
            monster_item = { "content": result.group(1), "prompt": message_list }
            monster_model.create(monster_item)
            print(f"----------------------Generated monster content: {result.group(1)}")
            return result.group(1)
        else:
            return ""
    else:
        return "Error"

def generate_question(message_list):
    messages = quiz_sample_message + message_list

    response = openai.ChatCompletion.create(
        model = "gpt-3.5-turbo-16k",
        messages = messages
    )

    if response and response.choices:
        assistant_reply = response.choices[0].message["content"]

        return assistant_reply
    else:
        return "Error"

    pass