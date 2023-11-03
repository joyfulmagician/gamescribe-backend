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

content_prompt = "You are a monster content generator. You can create descriptions and stat blocks with html styled code using tailwind css or desired CSS. When you create a description, you have to include the stat block. For the ability part, you can use short words like 'Str', 'Dex' for 'Strength', 'Dexterity' and so on. If you get additional features, you can update the monster content."
content_sample_message = [
    {
        "role": "system",
        "content": content_prompt
    },
    {
        "role": "user",
        "content": """Hello! I need you to generate monster content and return it to me as html code. Here's an example: If I give you liek that: 'Monster live in forest and have wings', I need you to say : 
            <div class="text-left">
                <div class="monster-title mb-4">Winged Beast</div>
                <div class="monster-subtitle">This monstrous creature has a pair of large, leathery wings that span an impressive distance. It uses these wings to soar through the skies with incredible speed and agility.</div>

                <div class="section-body">
                    <hr class="section-divider mt-5 mb-5">

                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Armor Class</span>
                        <span class="stat-subtitle">22</span>
                    </div>
        
                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Hit Points</span>
                        <span class="stat-subtitle">370 % (21d20 + 146)</span>
                    </div>
        
                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Speed</span>
                        <span class="stat-subtitle">40 ft., fly 80 ft., swim 40 ft.</span>
                    </div>
                </div>

                <div class="section-body">
                    <div class="section-title">
                        Abilities
                    </div>

                    <hr class="section-divider mt-5 mb-5">

                    <div class="ability">
                        <div class="stat-title ability-label">Str</div>
                        <div class="stat-subtitle">18 (+4)</div>
                    </div>
                    <div class="ability">
                        <div class="stat-title ability-label">Dex</div>
                        <div class="stat-subtitle">16 (+3)</div>
                    </div>
                    <div class="ability">
                        <div class="stat-title ability-label">Con</div>
                        <div class="stat-subtitle">16 (+3)</div>
                    </div>
                    <div class="ability">
                        <div class="stat-title ability-label">Int</div>
                        <div class="stat-subtitle">10 (+0)</div>
                    </div>
                    <div class="ability">
                        <div class="stat-title ability-label">Wis</div>
                        <div class="stat-subtitle">12 (+1)</div>
                    </div>
                    <div class="ability">
                        <div class="stat-title ability-label">Cha</div>
                        <div class="stat-subtitle">8 (-1)</div>
                    </div>
                </div>

                <div class="section-body">
                    <hr class="section-divider mt-5 mb-5">

                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Alignment</span>
                        <span class="stat-subtitle">Chaotic Evil</span>
                    </div>

                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Skills</span>
                        <span class="stat-subtitle">Perception +5, Stealth +6</span>
                    </div>

                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Damage Resistances</span>
                        <span class="stat-subtitle">Bludgeoning, Piercing, and Slashing from Nonmagical Attacks</span>
                    </div>

                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Damage Immunities</span>
                        <span class="stat-subtitle">Poison</span>
                    </div>

                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Condition Immunities</span>
                        <span class="stat-subtitle">Charmed, Deafened, Frightened, Petrified, Prone</span>
                    </div>

                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Senses</span>
                        <span class="stat-subtitle">Darkvision 60 ft., passive Perception 15</span>
                    </div>

                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Languages</span>
                        <span class="stat-subtitle">Common, Draconic</span>
                    </div>

                    <div class="flex gap-4 item-start mt-2">
                        <span class="stat-title">Challenge</span>
                        <span class="stat-subtitle">5 (1,800 XP)</span>
                    </div>
                </div>

                <div class="section-body">
                    <div class="section-title">
                        Actions
                    </div>

                    <hr class="section-divider mt-5 mb-5">

                    <div class="mt-2">
                        <span class="stat-title action-title">Multiattack (Vampire Form Only).</span>
                        <span class="stat-subtitle">Strahd makes three attacks, only one of which can be a bite attack.</span>
                    </div>

                    <div class="mt-2">
                        <span class="stat-title action-title">Scimitar.</span>
                        <span class="stat-subtitle">Melee Weapon Attack: +13 to hit, reach 10 ft., one target. Hit: 9 (3d6 + 10) slashing damage.</span>
                    </div>

                    <div class="mt-2">
                        <span class="stat-title action-title">Cel Flamand.</span>
                        <span class="stat-subtitle">Melee weapon attack: +13 to hit, reach 5 ft, one target, Hit: (3d4 + 16) Piercing Damage, and (2d6 + 8) Poison Damage</span>
                    </div>

                    <div class="mt-2">
                        <span class="stat-title action-title">Claws.</span>
                        <span class="stat-subtitle">Melee weapon attack: +9 to hit, reach 5 ft. one target, Hit: (2d4 +4) piercing damage. the target of this attack, when hit, must make a DC 15 CON save at the end of each of their turns to not take 2d4 damage from internal bleeding. if Strahd lands this attack from a flank, the creature must make a DC 12 CON save to suffer the paralyzed condition.</span>
                    </div>

                    <div class="mt-2">
                        <span class="stat-title action-title">Bite.</span>
                        <span class="stat-subtitle">Melee Weapon Attack: +10 to hit, reach 5 ft (can lunge upto 15 feet to bite), one willing creature, or a creature that is grappled, incapacitated, Stunned, Surprised or restrained. Hit: 7 (2d6 + 4) piercing damage plus 10 (3d6) necrotic damage. The target’s hit point maximum is reduced by an amount equal to the necrotic damage taken, and Strahd regains hit points equal to that amount. The reduction lasts until the target finishes a long rest. The target dies if its hit point maximum is reduced to 0. A humanoid slain in this way and then buried in the ground rises the following night as a vampire spawn under Strahd’s control.</span>
                    </div>

                    <div class="mt-2">
                        <span class="stat-title action-title">Charm</span>
                        <span class="stat-subtitle">Strahd targets one humanoid he can see within 30 feet of him. If the target can see Strahd, the target must succeed on a DC 19 Wisdom saving throw against this magic or be charmed. The charmed target regards Strahd as a trusted friend to be heeded and protected. The target isn’t under Strahd’s control, but it takes Strahd’s requests and actions in the most favorable way and lets Strahd bite it.
                            
                        Each time Strahd or his companions do anything harmful to the target, it can repeat the saving throw, ending the effect on itself on a success. Otherwise, the effect lasts 24 hours or until Strahd is destroyed, is on a different plane of existence than the target, or takes a bonus action to end the effect.</span>
                    </div>

                    <div class="mt-2">
                        <span class="stat-title action-title">Children of the Night (1/Day).</span>
                        <span class="stat-subtitle">Strahd magically calls 2d4 swarms of bats or swarms of rats. While outdoors, Strahd can call 3d6 wolves instead. The called creatures arrive in 1d4 rounds, acting as allies of Strahd and obeying his spoken commands. The beasts remain for 1 hour, until Strahd dies, or until he dismisses them as a bonus action.</span>
                    </div>

                </div>
            </div> """
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

        # html_code = re.search(pattern, assistant_reply, re.DOTALL)
        start_index = assistant_reply.find('<div class="text-left">')
        if start_index != -1:
            end_index = assistant_reply.rfind("</div>", start_index)

            if end_index != -1:
                html_code = assistant_reply[start_index:end_index + 6]
                monster_item = { "content" : html_code }
                monster_model.create(monster_item)
                return html_code
            else:
                return ""
        else:
            return ""

        # return assistant_reply
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