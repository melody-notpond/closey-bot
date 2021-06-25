import os
import discord
from dotenv import load_dotenv
import subprocess

load_dotenv()
my_secret = os.getenv("TOKEN")


TOKEN = os.environ['TOKEN']

replies: dict[int, discord.Message] = {}

CLOSEY_MODE_EXEC = 0
CLOSEY_MODE_CORRECTNESS = 1
CLOSEY_MODE_IR = 2
CLOSEY_MODE_CODEGEN = 3


class Client(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if (message.content.startswith('!closey')):
            args: list[str] = message.content.split('\n')[0].split(' ')
            mode = 'exec'
            if len(args) > 1:
                mode = args[1]

            async with message.channel.typing():
                output = subprocess.run(['./bin/closeyc', 'exec', '\n'.join(message.content.split('```')[1:][::2]), mode], capture_output=True)
                stdout,stderr = output.stdout.decode('utf-8'), output.stderr.decode('utf-8')

                if not stderr:
                    embed=discord.Embed(title="Success", description='```' + stdout + '```', color=0x00ff00)
                    response = await message.reply(embed=embed)
                else:
                    embed=discord.Embed(title="Error", description='```' + stderr + '```', color=0xff0000)
                    response = await message.reply(embed=embed)
                replies[message.id] = response


    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.id in replies:
            await replies[before.id].delete()
            del replies[before.id]
        await self.on_message(after)


client = Client()
client.run(TOKEN)
