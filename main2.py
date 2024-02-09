import os
from dotenv import load_dotenv
from discord import Intents, Client, Message
import discord
from discord.ext import commands
from discord.ui import Button, View
from random import randint
from random import choice

# TO-DO: Change channel ID in KICK statement, uncomment kick command
# Don't forget to change admin role
# pip install PyNaCl

# Load token
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")


# Customize !help command
help_command = commands.DefaultHelpCommand(
    no_category="Commands for use <3"
)


user_timer = {}


# Setup bot
Intents: Intents = Intents.default()
Intents.message_content = True  # NOQA
# client = Client(intents=Intents)
bot = commands.Bot(intents=Intents, command_prefix="!", help_command=help_command)

# Set channel for logs:
log_channel_id = 1205262797517094952
welcome_channel_id = 1205284046515609710
monitoring_channel_id = 1205150098435080215
voice_category_id = 1205150098435080213
user_dict = {}
temporary_channels = []
temporary_categories = []


@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    possible_channel_name = f"{member.display_name}'s area"
    if after.channel is not None:
        if after.channel.name == "temp":
            temp_channel = await after.channel.clone(name=possible_channel_name)
            await member.move_to(temp_channel)
            temporary_channels.append(temp_channel.id)
        if after.channel.name == "teams":
            temp_category = await after.channel.guild.create_category(name=possible_channel_name)
            temp_channel = await temp_category.create_voice_channel(name="voice")
            await member.move_to(temp_channel)
            temporary_categories.append(temp_channel.id)
            await temp_category.create_text_channel(name="text")

    if before.channel:
        if before.channel.id in temporary_channels:
            if len(before.channel.members) == 0:
                await before.channel.delete()
        if before.channel.id in temporary_categories:
            if len(before.channel.members) == 0:
                for channel in before.channel.category.channels:
                    await channel.delete()
                await before.channel.category.delete()


@bot.command(name="roll-dice", help="Just will give you a random number from 1 to 6, kinda useless")
async def roll_dice(ctx):
    await ctx.send(str(randint(1, 6)))


@bot.command(name='create-channel', help="Was created for creating :P another channel")
@commands.has_role('Admin')
async def create_channel(ctx, channel_name='empty'):
    guild = ctx.message.guild
    print(ctx.message.content)
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Trying to create a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
        await ctx.send(f"Successfully created a {channel_name} channel")
    if existing_channel:
        await ctx.send("Cannot create a new channel, already exists")


@bot.command(name="delete-channel", help=".delete-channel channelname")
@commands.has_role('Admin')
async def deleter_channel(ctx, channel_name="empty"):
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if existing_channel:
        print(f"trying to delete {channel_name}")
        await channel_name.delete()
        await guild.delete_text_channel(1205508580925640774)
        await ctx.delete_text_channel(channel_name)
        await ctx.delete_channel(channel_name)
    else:
        await ctx.send(f"Channel {channel_name} doesn't exists")


@bot.command(name="ping", help="pong?")
async def pong(ctx):
    await ctx.send("pong")


@bot.command(name="kick", help="Probably just kicks someone", pass_context=True)
# @commands.has_permissions(kick_members=True)
@commands.has_role('Admin')
async def kick(ctx, *, user: discord.Member):
    reason = None
    await user.kick(reason=None)
    kick_embed = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
    await bot.get_channel(log_channel_id).send(embed=kick_embed)


@bot.command(name="Himari", help="Who is Himari")
async def himari_about(ctx):
    await ctx.send("Himari was created specifically for <3\nAnd cannot be used for other servers. :pink_heart:")


@bot.command(name="create-voice", help="Creates a new voice channel")
async def create_voice(ctx, member: discord.Member):
    print("ENTRY")


# Bot Events


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):  # If user don't have a permission to do that, then:
        await ctx.send("Sorry, you don't have permission to do that :broken_heart: ")


@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")


@bot.event
async def on_member_join(member):
    await bot.get_channel(welcome_channel_id).send(f"Greetings, <@{member.id}>!")
    button = Button(label=f"Kick {member.display_name}", style=discord.ButtonStyle.red)
    view = View()
    view.add_item(button)
    embed_message = discord.Embed(title=f"**{member.display_name}** just connected!", description="Kick them?")
    embed_message.set_author(name="New user", icon_url=member.avatar.url)
    await bot.get_channel(log_channel_id).send(embed=embed_message, view=view)


@bot.event
async def on_message(message):
    await bot.process_commands(message)  # Important not to delete!! Will break event and command

    if message.author == bot.user:
        return

    if message.content.lower() == "hello, himari!":
        await message.channel.send(choice([
            "Hello :P",
            "Hiiii!!"
            "<3"
        ]))

    if message.content.lower() == "!":
        await message.channel.send("Sorry?")


if __name__ == '__main__':
    bot.run(TOKEN)