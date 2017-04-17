import discord
from discord.ext import commands
from datetime import datetime
from time import sleep

description = "Schedule bot for Hanapara"
client = commands.Bot(command_prefix='$', description=description)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    
@client.event
async def on_message(message):
    if message.content.startswith('!schedule'):
        msg = "Scheduling launched ! http://danbooru.donmai.us/data/__sarasa_granblue_fantasy_drawn_by_suwi__666d35a4d6579abf0b70cb3928ed9e8d.png"
        await client.send_message(message.channel, msg)
        pre_tr = 0
        pre_st1 = 0
        pre_st2= 0
        while True:
                now = datetime.now()
                actual_time = now.hour
                #Twitter refresh notification
                tweet_refresh = 16
                pre_tr_calc = tweet_refresh - actual_time
                if pre_tr_calc == 1:
                        print("Pre_tr status changed")
                        pre_tr = 1
                if tweet_refresh == actual_time and pre_tr == 1:
                        print("Notification sent !")
                        msg = "@everyone Do not forget to use your Twitter refresh!"
                        await client.send_message(message.channel, msg)
                        pre_tr = 0
                #End of twitter refresh notification
                #Strike time 1 notifications
                striketime_1 = 24
                pre_st1_calc = striketime_1 - actual_time
                if pre_st1_calc == 1:
                        print("Pre_st1 status changed")
                        pre_st1 = 1
                if (striketime_1-24) == actual_time and pre_st1 == 1:
                        print("Notification sent !")
                        msg = "@everyone It's Strike Time!"
                        await client.send_message(message.channel, msg)
                        pre_st1 = 0
                #Strike Time 1 notifications end
                #Strike Time 2 Notifications
                striketime_2 = 5
                pre_st2_calc = striketime_2 - actual_time
                if pre_st2_calc == 1:
                        print("Pre_st2 status changed")
                        pre_st2 = 1
                if striketime_2 == actual_time and pre_st2 == 1:
                        print("Notification sent !")
                        msg = "@everyone It's Strike Time!"
                        await client.send_message(message.channel, msg)
                        pre_st2 = 0
                #Strike Time 2 notifications end
                
                sleep(1)
@client.command()
async def cuck():
    await client.say("Marika is a cuck")


client.run('MzAyMTY3NzUyNjU4MTI0ODAw.C9XVng.LvmGVT9N_i2q5s2LgSquOmBN-JY')



