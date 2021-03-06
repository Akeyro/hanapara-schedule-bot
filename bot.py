import discord
from discord.ext import commands
from datetime import datetime
from time import sleep
import os
import sys
import asyncio
import pprint
from pybooru import Danbooru
from random import randint
import requests

client_api = str(input("Please enter your API Key:"))
pic_api = str(input("Please enter your Danbooru API Key:"))
picbot = Danbooru('danbooru', username='Akeyro', api_key=pic_api)
description = "Sarasa bot for Hanapara, please give me plenty of cake !"
client = commands.Bot(command_prefix='$', description=description, )
bot_dir = "/app/"
os.chdir(bot_dir)

client.pm_help = True

hanapara_server = 0
general_channel = 0

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


@client.event
async def on_ready():
    await client.wait_until_ready()
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='Jed Bullying Simulator'))
    global hanapara_server
    global general_channel
    general_channel = client.get_channel(id='246519048559394817')
    hanapara_server = client.get_server(id='246519048559394817')
    client.loop.create_task(schedule())

@client.command(description="Check if the bot is active")
async def active():
    print("Command received")
    await client.say("Yes Master ? Do you need me ?")

@client.command(description="Shows the strike times schedule")
async def st():
    await client.say('''```Markdown 
Strike times are at :
    JST : 7AM - 8AM // 12PM - 1PM
    PST : 3PM - 4PM // 8PM - 9PM
    DST : 6PM - 7PM // 11PM - 12AM
    UTC : 10PM - 11PM // 4AM - 5AM```''')


@client.command(description="Because Mako rhymes with Full Homo",pass_context=True)
async def bl(ctx):
    msg = "\U0001F440"
    await client.say(msg) 
    await client.send_file(ctx.message.channel, "reactions/homo.gif")

@client.command(description="When the thinking is strong",pass_context=True)
async def rotathinking(ctx):
    msg = "\U0001F914"
    await client.say(msg) 
    await client.send_file(ctx.message.channel, "reactions/tenor.gif")

@client.command(description="Restarts the bot", pass_context=True)
async def restart(ctx):
    if ctx.message.author.id == '90878360053366784':
        print("Restarting the bot")
        msg="Restarting the bot"
        await client.say(msg)
        os.execl(sys.executable, sys.executable, *sys.argv)

    else:
        msg="What are you trying to do ?! Idiot !"
        await client.say(msg)

@client.command(description="Use a reaction pic", pass_context=True)
async def reac(ctx, message : str):
    m_id = str(ctx.message.id)
    m_author = ctx.message.author
    m_author_mention = m_author.mention
    m_channel = ctx.message.channel
    m_del = await client.get_message(m_channel,m_id)
    try:
        picpath = "reactions/" + message + ".png"
        await client.say(m_author_mention)
        await client.send_file(ctx.message.channel, picpath)
        await asyncio.sleep(3)
        await client.delete_message(m_del)
    except FileNotFoundError:
        await client.say("I can't find what you're looking for")

@client.command(description="Lists all the reactions available", pass_context=True)
async def reaclist(ctx):
    m_author = ctx.message.author
    reac_list=[]
    for name in os.listdir("./reactions/"):
        if name.endswith(".png"):
            reac_list.append(os.path.splitext(name)[0])
    sort_list = list(chunks(reac_list, 80))
    for i in range(0,len(sort_list)):
        await client.send_message(m_author, "```{}```".format("\n".join(sort_list[i])))



@client.command(description="Add a role to the user",pass_context=True)
async def addrole(ctx, *, message : str):
    m_author = ctx.message.author
    m_server = ctx.message.server
    roleadd = discord.utils.get(m_server.roles, name=message)
    roleget = str(roleadd)
    await client.say("Trying to add you to the role {}".format(roleadd))
    try :
        if roleget == "Captain" or roleget == "Vice Captain":
            await client.say("No, you can't do that")
        else :
            await client.add_roles(m_author, roleadd)
            await client.say("Successfuly added you to the role {} !".format(roleadd))
    except AttributeError:
        await client.say("There is no such role")
    except :
        await client.say("You don't have the permission to get this role, but you have the permission to give me cake !")

@client.command(description="Remove a role from the user",pass_context=True)
async def remrole(ctx, *, message : str):
    m_author = ctx.message.author
    m_server = ctx.message.server
    rolerem = discord.utils.get(m_server.roles, name=message)
    roleget = str(rolerem)
    await client.say("Trying to remove you from the role {}".format(rolerem))
    try:
        if rolerem == None:
            await client.say("There is no such role")
        else :
            await client.remove_roles(m_author, rolerem)
            await client.say("Successfuly removed you from the role {} !".format(rolerem))
    except AttributeError:
        await client.say("There is no such role")
    except :
        await client.say("You don't have the permission to remove this role")

def is_me(m):
    return m.author == client.user

@client.command(description="Purge all the messages from the bot on the channel", pass_context=True)
async def purge(ctx):
    m_author = ctx.message.author
    m_channel = ctx.message.channel
    deleted = await client.purge_from(m_channel, limit=100, check=is_me)
    await client.send_message(m_channel, 'Deleted {} message(s)'.format(len(deleted)))


@client.command(pass_context=True)
async def safebooru(ctx, message : str):
    m_channel = ctx.message.channel
    path = "./"
    max_limit = 200
    picture = picbot.post_list(tags=message+" rating:safe", limit=max_limit, random=True)
    pic_count = len(picture)
    if pic_count == 0:
        await client.say("There is no picture with this tag")

    else :
        random_pic = randint(0, pic_count - 1)
        picture_link = "https://danbooru.donmai.us/posts/" + str(picture[random_pic]['id'])
        pic_id = str(picture[random_pic]['id'])
        pic_show = picbot.post_show(pic_id)
        pic_url = "https://danbooru.donmai.us" + str(pic_show['file_url'])
        dl = requests.get(pic_url)
        with open(path + "pic_temp.jpg", "wb") as f:
            f.write(dl.content)
        picpath = "./pic_temp.jpg"
        print(picture_link)
        print(pic_url)
        await client.send_file(ctx.message.channel, picpath)

#Scheduler --------------------------------
async def schedule():
    await client.wait_until_login()
    twtr = 19
    st1 = 22
    st2 = 3
    twtr_trigger = 0
    st1_trigger = 0
    st2_trigger = 0
    role = str("Dumb People")
    getrole = discord.utils.get(hanapara_server.roles, name=role)
    role_mention = getrole.mention
    while not client.is_closed:
        now = datetime.now()
        actual_hour = now.hour
        print("[{:02}:{:02}]Checking time".format(now.hour, now.minute))

        if actual_hour == (twtr-1):
            twtr_trigger = 1

        if actual_hour == (st1-1):
            st1_trigger = 1

        if actual_hour == (st2-1):
            st2_trigger = 1

        if actual_hour == st1 and st1_trigger == 1:
            st1_msg = "{} It's strike time, butcher those raids !".format(role_mention)
            await client.send_message(general_channel, st1_msg)
            st1_trigger = 0

        elif actual_hour == st2 and st2_trigger == 1:
            st2_msg = "{} It's strike time, butcher those raids !".format(role_mention)
            await client.send_message(general_channel, st2_msg)
            st2_trigger = 0

        elif actual_hour == twtr and twtr_trigger == 1:
            twtr_msg = "{} Do not forget to use your daily Twitter refresh and to buy your daily thingies ! (And my cake too !!!)".format(role_mention)
            await client.send_message(general_channel, twtr_msg)
            twtr_trigger = 0

        if (now.minute % 5) != 0: #Sync if something happen to the clock
            print("Resyncing the scheduler")
            synctime = (5 - (now.minute%5))*60
            print("Time to wait in order to sync : {}minutes".format(synctime/60))
            await asyncio.sleep(synctime)
            print("Finished syncing!")
        await asyncio.sleep(300) #Check every 5 minutes
#End of scheduler -----------------------------------------------------

client.run(client_api)
