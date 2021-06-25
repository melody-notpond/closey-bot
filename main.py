import os
import discord
from dotenv import load_dotenv

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
            mode = CLOSEY_MODE_EXEC
            if len(args) > 1:
                if args[1] == 'exec':
                    mode = CLOSEY_MODE_EXEC
                elif args[1] == 'analyse' or args[1] == 'analyze':
                    mode = CLOSEY_MODE_CORRECTNESS
                elif args[1] == 'ir':
                    mode = CLOSEY_MODE_IR
                elif args[1] == 'codegen':
                    mode = CLOSEY_MODE_CODEGEN
                else:
                    response = await message.reply("Invalid option! Please use one of exec, analyse, ir, or codegen.")
                    replies[message.id] = response
                    return

            async with message.channel.typing():
                response = await message.reply("mode: %i" % mode)
                replies[message.id] = response


    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.id in replies:
            await replies[before.id].delete()
            del replies[before.id]
        await self.on_message(after)


client = Client()
client.run(TOKEN)
