'''
!trivia 

'''
import json
import os
import random
import re

import wikipedia
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from dotenv import load_dotenv
import discord
intents = discord.Intents.default()
intents.members = True

from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = int(os.getenv('DISCORD_CHANNEL'))

bot = commands.Bot(command_prefix='!', intents=intents)

# with open('questions.json') as file:
#     questions = json.load(file)


def get_question():
    question = ''

    while True:
        while True:
            try:
                title = wikipedia.random(1)
                page = wikipedia.page(title=title)
                categories = page.categories
                question += '__**Categories:**__\n' + ', '.join(categories) + '\n'
                summary = wikipedia.summary(title)
                summary = re.sub(r'([A-Za-z0-9]\.)([A-Za-z])', r'\1 \2', summary)
                break
            except:
                continue

        sentence = sent_tokenize(summary)[0]
        words = nltk.pos_tag(word_tokenize(sentence))
        print('DEBUG: words', words, '\n')

        if len(words) > 50:
            print('DEBUG: Sentence truncated\n')
            words = words[:50]
            words.append(('...', 'ELLIPSES'))

        noun = [i for i in words if i[1] in ['NN']] # ['NN', 'NNP']
        if noun:
            break

    question += '__**Question:**__\n'

    answer_written = False
    for word in words:
        if word[1] in ['NN'] and not answer_written:
            answer = word[0]
            question += f'||{answer}|| '
            answer_written = True
        else:
            question += word[0] + ' '

    question += '\n__**Want a new question? Use the !trivia command!**__\n'

    return question


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='trivia', help='')
async def trivia(ctx, *args):
    await ctx.send(get_question())


# @bot.command(name='trivia', help='')
# async def trivia(ctx, goal: int, player_1: discord.Member, player_2: discord.Member):
#     # playing = True
#     # while playing:

#     question = random.choice(questions)

#     player = '@' + str(player_1)
#     response = '\nCategory: ' + question['category'] + '\nSubcategory: ' + question['subcategory'] + '\nQuestion: ' + question['question']
#     await ctx.send(player)
#     await ctx.send(response)


    # players = [player_1, player_2]
    # guild = discord.utils.get(bot.guilds, name=GUILD)
    # member_ids = {}
    # for member in guild.members:
    #     member_ids[member.name] = member.id
    # print(member_ids)

    # response = f'A new trivia game has started with {num_players} players!'
    # print(args)
    # for member in args:
    #     print(type(member), member)
    # guild = discord.utils.get(bot.guilds, name=GUILD)

    # print(player_1, player_2)
    # await ctx.send(player_1)
    # await ctx.send(player_1)


bot.run(TOKEN)
