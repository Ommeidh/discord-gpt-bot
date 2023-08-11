import os
import discord
from discord.ext import tasks
import openai
from dotenv import load_dotenv
from queue import Queue

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY
model_engine = "text-davinci-003"

intents = discord.Intents().all()
client = discord.Client(intents=intents)

status_queue = Queue()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    status_queue.put(True)

async def on_message(message):
    print('Message received:', message.content)
    # rest of the code

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    print(message.content)

    if message.content.startswith('%'):
        response = generate_response(message.content[1:])
        await message.channel.send(response)

async def start_bot():
    await client.start(TOKEN)

def start_bot_task():
    tasks.loop(seconds=0)(start_bot).start()

def generate_response(message):
    print("Generating response for message:", message)
    prompt = f"{message.strip()}"
    print("Prompt:", prompt)
    response = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = response.choices[0].text.strip()
    print("Generated response:", message)
    return message

client.run(TOKEN)