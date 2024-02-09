from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# Load token
load_dotenv()
TOKEN: Final[str] = os.getenv("DISCORD_TOKEN")

# Setup bot
Intents: Intents = Intents.default()
Intents.message_content = True  # NOQA
client: Client = Client(intents=Intents)


# Message functionality
async def send_message(message: Message, user_message):
    if not user_message:
        print("Message was empty because intents were not enabled probably")
        return

    if is_private := user_message[0] == "?":
        user_message = user_message[1:]

    try:
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)


# Handle the startup
@client.event
async def on_ready():
    print(f"{client.user} is now running!")


# Handle incoming messages
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f"[{channel}] {username}: {user_message}")
    await send_message(message, user_message)


@client.event
async def on_member_join(member, message):
    await message.channel.send(f"Hello, {member}")


# Main entry point
def main():
    client.run(token=TOKEN)


if __name__ == '__main__':
    main()
