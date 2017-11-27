import discord, logging, json
from discord.ext import commands
import asyncio

description = '''Bot description here'''
bot = commands.Bot(command_prefix='~', description=description)

print('Starting Bot...')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name="with your waifu!"))

@bot.listen()
async def on_member_join(member):
	is_verified = False
	for role in member.roles:
		if role.name == "Verified":
			is_verified = True
			break
	if is_verified == False:
		await bot.send_message(member,"Please message the bot with the command ~verify to get normal permissions")

#########Bot Commands############

@bot.command(pass_context=True)
async def verify(context):
	"""Basic command to give user basic permissions"""
	for server in bot.servers:
		roles = server.roles
		members = server.members
		member = None
		for mem in members:
			if mem.id == context.message.author.id:
				member = mem
				break
		for role in roles:
			if role.name == "Verified":
				await bot.add_roles(member, role)
				await bot.send_message(member,"Thank you for your cooperation!")
				break

@bot.command(pass_context=True)
async def purge(context, number : int):
	"""Clear a specified number of messages in the chat"""
	deleted = await bot.purge_from(context.message.channel, limit=number)
	await bot.send_message(context.message.channel, 'Deleted {} message(s)'.format(len(deleted)))

@bot.command(pass_context = True)
async def kick(ctx, userName: discord.User):
    await bot.kick(userName)

@bot.command(pass_context = True)
async def ban(ctx, userName: discord.User):
    await bot.ban(userName)



## Bot Token ##
bot.run('')


