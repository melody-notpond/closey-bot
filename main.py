import os
import discord
from dotenv import load_dotenv

load_dotenv()
my_secret = os.getenv("TOKEN")


TOKEN = os.environ['TOKEN']

class Client(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        await message.reply("uwu");

client = Client()
client.run(TOKEN)
