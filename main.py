import discord
import os
#import pynacl
#import dnspython
import server
from discord.ext import commands
from discord.utils import get
from utils.config import HOST_CHANNEL, ROLES
from utils.utils import should_ignore
from utils.roles import add_role, get_role_from_reaction, remove_role, remove_all_roles
from utils.emojis import get_emoji_from_reaction, is_clearing_emoji, is_listed_emoji

from utils.config import EMBEDS
from discord.ext.commands import HelpFormatter
from utils.utils import is_mod_or_admin
dow = 1
import datetime
import time
import requests
import json
from itertools import islice
client = commands.Bot(command_prefix='&')
client2 = discord.Client()
memberlist = []
updatefunc = False
from getpass import getpass
listen = False

if server.result != "":
	print(server.result)
	
@client.command(pass_conetext=True)
async def say(ctx, *, messages):
	await ctx.send(messages)
	await ctx.message.delete()
def isPower (x, y):
     
    # The only power of 1
    # is 1 itself
    if (x == 1):
        return (y == 1)
         
    # Repeatedly compute
    # power of x
    pow = 1
    while (pow < y):
        pow = pow * x
 
    # Check if power of x
    # becomes y
    return (pow == y)
def listToString(s): 
    
    # initialize an empty string
    str1 = "" 
    
    # traverse in the string  
    for ele in s: 
        str1 += ele  
    
    # return string  
    return str1 
@client.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    await run_cleanup()

@client.event
async def on_member_join(member):
  sender_id = str(ctx.author)
  	#db[sender_id] = 0
  member = ctx.author
  role_members = discord.utils.get(ctx.guild.roles, name='Level 1')
  await update_data(users, member)
  


async def help_cmd(client, ctx, *args):
    formatter = HelpFormatter()

    if len(args) == 0:
        pages = client.formatter.format_help_for(ctx, bot)
    else:
        cmd_str = args[0][0]
        command = client.commands.get(cmd_str)

        if command is None:
            emb = discord.Embed(title='Command: {}'.format(cmd_str), type='rich',
                                description='Invalid command entered', color=0xff0000)
            await client.send_message(ctx.message.channel, embed=emb)
            return
        else:
            pages = client.formatter.format_help_for(ctx, command)
    for page in pages:
        await client.send_message(ctx.message.channel, page)


async def init(client, channel, user):
    if dow == 42:
        await client.send_message(channel, "Must be mod or admin to initiate")
    else:
        await client.send_message(channel, "Initiating...")

        for i in range(len(EMBEDS)):
            title, message = 0, 1
            init_embed = discord.Embed(title=EMBEDS[i][title], type='rich',
                                       description=EMBEDS[i][message], color=0xffffff)
            init_message = await client.send_message(channel, embed=init_embed)

            role_group = sorted(ROLES.keys())[i]
            curr_roles = ROLES[role_group]
            for r, emoji in curr_roles.items():
                reaction = get(client.get_all_emojis(), name=emoji)
                # if reaction is not a default Discord reaction
                if reaction is None:
                    reaction = emoji
                await client.add_reaction(init_message, reaction)
@client.event
async def on_reaction_add(reaction, user):
    """ When reaction is added, dispatch correct action """

    if not should_ignore(client, reaction.message.channel, user):
        emoji = get_emoji_from_reaction(reaction)

        # if a clearing emoji was clicked, remove all roles
        if is_clearing_emoji(emoji):
            await remove_all_roles(client, user)

        # if emoji was not already listed, remove
        elif not is_listed_emoji(emoji):
            await client.remove_reaction(reaction.message, reaction.emoji, user)

        else:
            role = get_role_from_reaction(reaction)
            await add_role(client, user, role)

async def run_cleanup():
    """ Removes all bot messages from HOST_CHANNEL and re-initiates """

    print("Started cleanup")
    channel = get(client.get_all_channels(), name=HOST_CHANNEL)
    if channel is None:
        print("Could not locate channel: {}".format(HOST_CHANNEL))
        return
    else:
        author = None
        async for message in client.logs_from(channel):
            if message.author.id == client.user.id:
                author = message.author
                await client.delete_message(message)

        if author is None:
            print("Could not re-add reaction messages. Admin must manually run >init")
        else:
            await commands.init(client, channel, author)
    print("Finished cleaning up {} channel".format(HOST_CHANNEL))

@client.event
async def on_reaction_remove(reaction, user):
    """ When user removes reaction, remove role from user """

    if not should_ignore(client, reaction.message.channel, user):
        role = get_role_from_reaction(reaction)
        await remove_role(client, user, role)



@client.command()
async def suggest(ctx, *, message):
	guild1 = str(ctx.guild.id)
	if guild1 == 742960432225976342:
		channel = client.get_channel(839252569260032011)
		await channel.send(message)
	elif guild1 == 745189311770656808:
		channel = client.get_channel(845770429469294632)
		await channel.send(message)
	elif guild1 == 780893031149731842:
		channel1 = client.get_channel(817250080142655489)
		await channel.send(message)
	
  
@client.command(pass_context=True, help="enable afk role")
async def afk_on(ctx):
  	author = ctx.author
  	role = discord.utils.get(ctx.guild.roles, name='AFK')
  	await author.add_roles(role)
  	await ctx.send("You are now labeled as AFK. To disable it type afk_off")

	
	
@client.command(pass_context=True, help="disable afk role")
async def afk_off(ctx):
  member = ctx.author
  role_members = discord.utils.get(ctx.guild.roles, name='Members')
  role_muted = discord.utils.get(ctx.guild.roles, name='AFK')
  await member.remove_roles(role_muted)
  await member.add_roles(role_members)
  await ctx.send("You are not afk anymore!")
  
@client.command(pass_context = True)
async def add_role(ctx, *, role_add):
  user = ctx.author
  if "[!]" in role_add:
    embed = discord.Embed(title="Permission Denied.", description="You can't add an administrator role to yourself", color=0xff00f6) 
    await ctx.send(embed=embed)
  else:
    try:
      role_get = discord.utils.get(ctx.guild.roles, name=str(role_add))
      await user.add_roles(role_get)
      await ctx.send(f"Role added to {user}")
    except AttributeError:
      await ctx.send("That role doesn't exist!")

@client.command()
async def commands(ctx):
  	member_command_list = "add_role (role), afk_off, afk_on, say [](make the bot say something), suggest [](server suggestion here)"
  	admin_command_list = "mute [@user], unmute[@user], deletechannel [channel name], warn [@user] [message to send], clearwarnings[@user], checkwarnings[@user], ban[@user], kick[@user]"
  	embed = discord.Embed(title="Info", description="Note if a word is in brackets you don't have to write the brackets in the command", color=0xff00f6) 
  	await ctx.send(embed=embed)
  	embed = discord.Embed(title="Member Commands", description=member_command_list, color=0xff00f6) 
  	await ctx.send(embed=embed)
  	embed = discord.Embed(title="Admin Commands", description=admin_command_list, color=0xff00f6) 
  	await ctx.send(embed=embed)
  

@client.command(pass_context=True, help="mute a server member so they can't send messages")
async def mute(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    role_members = discord.utils.get(ctx.guild.roles, name='Members')
    role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role_members)
    await member.add_roles(role_muted)
    await ctx.send("User Was Muted")
    print(f'{member} was muted')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)

@client.command(name='deletechannel', help='delete a channel with the specified name')
async def deletechannel(ctx, channel_name):
   # check if the channel exists
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
   # if the channel exists
    if existing_channel is not None:
      await existing_channel.delete()
   # if the channel does not exist, inform the user
    else:
      await ctx.send(f'No channel named, "{channel_name}", was found')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)

@client.command(pass_context=True)
async def unmute(ctx, member: discord.Member):
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    role_members = discord.utils.get(ctx.guild.roles, name='Members')
    role_muted = discord.utils.get(ctx.guild.roles, name='Muted')
    await member.remove_roles(role_muted)
    await member.add_roles(role_members)
    await ctx.send("User Was Unmuted")
    print(f'{member} was unmuted')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)

@client.command()
async def warn(ctx, member: discord.Member, *, reason):
	role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
	if role in ctx.author.roles:
		response = requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'warnings','function': 'add_warnings', 'author': str(member), 'reason':str(reason)})
		json_response = response.json()
		print(json_response)
		await member.create_dm()
		await member.dm_channel.send(f'This is a warning for {reason} sent by {ctx.author}')
		await ctx.send("Warning sent!")
	else:
		embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
		await ctx.send(embed=embed)
		


@client.command()
async def clearwarnings(ctx, member: discord.Member):
  auth = str(ctx.author)
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'warnings','function': 'clearwarnings', 'author': str(member)})
    await member.create_dm()
    await member.dm_channel.send('Your warnings have been cleared!')
    await ctx.send(f'Warnings cleared for {auth}')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)
		


@client.command()
async def checkwarnings(ctx, member: discord.Member):
  auth = str(ctx.author)
  mem = str(member)
  response = requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'warnings','function': 'checkwarnings', 'author': str(member)})
  json_response = response.json()
  print(json_response)
  warningsnum = json_response['number']
  reasons_list = json_response['reasons']
  embed = discord.Embed(description=f'This member has {warningsnum} warnings for {reasons_list}',color = 0xf54242)
  await ctx.send(embed=embed)
	
@client.command(pass_context=True)
async def ban(ctx, member: discord.Member, *,reason=None, membertoban):
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    await ban(membertoban)
    await ctx.send(f'User {membertoban} has been banned')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)
    
@client.command(pass_context=True)
async def kick(ctx, member: discord.Member, *, reason=None):
  role = discord.utils.get(ctx.guild.roles, name='[!]STAFF TEAM')
  if role in ctx.author.roles:
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked.')
  else:
    embed = discord.Embed(title="Permission Denied.", description="You don't have permission to use this command.", color=0xff00f6) 
    await ctx.send(embed=embed)



#----------------------------------EVENTS----------------------------------
@client.event
async def on_member_join(member: discord.Member):
  role = discord.utils.get(member.guild.roles, name="Level 1")
  guild1 = str(message.guild.name)
  if guild1 == "Catgalactic Hangout/Support Server":
    spam_chat = client.get_channel(838864866876850228)
  elif guild1 == "sʞɹoMʎɯnᗡɓıᙠ⚠":
    spam_chat = client.get_channel(842544786506121247)
    await spam_chat.send(f'{member} welcome')
    with open('users.json', 'r') as f:
      users = json.load(f)
      await update_data(users, member)
      with open('users.json', 'w') as f:
        json.dump(users, f)
        await member.add_roles(role)


@client.event
async def on_message(message):
	listen = True
	member = message.author
	auth = str(message.author)
	if auth not in memberlist:
		memberlist.append(auth)
  		#db[auth] = 0
	mescon = str(message.content)
	mescon = mescon.lower()
	data = [mescon]
  	
	bad_words = ["cunt", "bloody hell", "crikey", "choad", "wanker", "twat", "pussy", "nigga"]
	res = [ele for ele in bad_words if(ele in mescon)]
	result = bool(res)
	if result == True:
		await message.channel.send("You have said a swear word. It will now be deleted") 
		await message.delete()
		print(message.content)
	if message.author.bot == False:
		if isinstance(message.channel,discord.channel.DMChannel):
			return
		else:
			guild1 = str(message.guild.name)
			if guild1 == "Catgalactic Hangout":
				requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'users','function': 'update_data', 'author': auth})
				await add_experience(auth)
				await level_up(message, auth)
							
							
							
			elif guild1 == "Chill Dimension":
				requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'users2','function': 'update_data', 'author': auth})
				await add_experience(auth)
				await level_up(member, auth)
			elif guild1 == "Amadden's Hangout Server":
				requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'users3','function': 'update_data', 'author': auth})
				await add_experience(auth)
				await level_up(member, auth)
			elif guild1 == "ℳᎽ𝒯ℋℂℛᎯℱ𝒯":
				requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'users4','function': 'update_data', 'author': auth})
				await add_experience(auth)
				await level_up(member, auth)
	if listen == True:
		await client.process_commands(message)


@client.event
async def on_member_remove(member: discord.Member):
  print(f'{member} has left a server.')

async def update_data(users, user):
	requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'users','update_warnings': 'add_experience', 'author': user})
	requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'users','update_data': 'add_experience', 'author': user})

async def add_experience(user):
	requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'users','function': 'add_experience', 'author': user})


async def level_up(user, username):
	user = message.author
	user_id = user.id
	guild_id = message.guild.id
	response = requests.get('https://Test-1.loganpollack.repl.co', params={'file': 'users','function': 'level_up', 'author': username})
	output = response.json()
	lvl_end = int(output['end'])
	lvl_start = int(output['start'])
	if lvl_start < lvl_end:
		await user.create_dm()
		await user.dm_channel.send(f'You are now level {lvl_end}!')
		if lvl_end == 1:
			role = discord.utils.get(user.guild.roles, name="Level 1")
			user = message.author
			user_id = user.id
			guild_id = message.guild.id
			await member.add_roles(guild_id, user_id, 838847628053708850, reason=None)
		elif lvl_end == 2:
			previous = discord.utils.get(user.guild.roles, name="Level 1")
			role = discord.utils.get(user.guild.roles, name="Level 2")
			user = message.author
			user_id = user.id
			guild_id = message.guild.id
			
			await member.add_roles(guild_id, user_id, 838847846361858058, reason=None)
		elif lvl_end == 3:
			previous = discord.utils.get(user.guild.roles, name="Level 2")
			role = discord.utils.get(user.guild.roles, name="Level 3")
			user = message.author
			user_id = user.id
			guild_id = message.guild.id
			
			await member.add_roles(guild_id, user_id, 838847888116940871, reason=None)
		elif lvl_end == 4:
			previous = discord.utils.get(user.guild.roles, name="Level 3")
			role = discord.utils.get(user.guild.roles, name="Level 4")
			user = message.author
			await user.remove_roles(previous)
			await user.add_roles(role)
		elif lvl_end == 5:
			previous = discord.utils.get(user.guild.roles, name="Level 4")
			role = discord.utils.get(user.guild.roles, name="Level 5")
			user = message.author
			await user.remove_roles(previous)
			await user.add_roles(role)
		elif lvl_end == 6:
			previous = discord.utils.get(user.guild.roles, name="Level 5")
			role = discord.utils.get(user.guild.roles, name="Level 6")
			user = message.author
			await user.remove_roles(previous)
			await user.add_roles(role)
		elif lvl_end == 7:
			previous = discord.utils.get(user.guild.roles, name="Level 6")
			role = discord.utils.get(user.guild.roles, name="Level 7")
			user = message.author
			await user.remove_roles(previous)
			await user.add_roles(role)
		elif lvl_end == 8:
			previous = discord.utils.get(user.guild.roles, name="Level 7")
			role = discord.utils.get(user.guild.roles, name="Level 8")
			user = message.author
			await user.remove_roles(previous)
			await user.add_roles(role)
		elif lvl_end == 9:
			previous = discord.utils.get(user.guild.roles, name="Level 8")
			role = discord.utils.get(user.guild.roles, name="Level 9")
			user = message.author
			await user.remove_roles(previous)
			await user.add_roles(role)



TOKEN = os.getenv("DISCORD_TOKEN")
server.server()
client.run(TOKEN)
