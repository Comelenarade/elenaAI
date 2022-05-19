import discord
import asyncio
import random
from discord.ext import commands

from helpers import *

from const.TOKEN import TOKEN
from const.TEXT import WELCOME_MESSAGE, CLASS_NAME_RULE, CLASS_END_MESSAGE, MAJOR_END_MESSAGE, ONLINE_MESSAGE

WELCOME_CHANNEL = 786107233586905128
DEF_ROLE = "comrade"
GULAF_ROLE = 'GULAG'

MIN_PEOPLE_CHANNEL = 4

intents = discord.Intents.all()
intents.members = True
#intents.message_content = True

bot = commands.Bot(command_prefix='?', description="ELENA", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(WELCOME_CHANNEL)
    await channel.send(WELCOME_MESSAGE)

@bot.command()
async def online(ctx):
    await ctx.send(ONLINE_MESSAGE)

@bot.command()
async def allroles(ctx):
    messg = RolesCounterPrepToPrint(RolesCounterAll(ctx))
    for block in messg:
        await ctx.send(block)

@bot.command()
async def classroles(ctx):
    messg = RolesCounterPrepToPrint(RolesCounterClasses(ctx))
    for block in messg:
        await ctx.send(block)

@bot.command()
async def major(ctx, major: str):
    if major.upper() == "EE":
        mjr = "Electrical Engr"
    elif major.upper() == "CO" or major.upper() == "CE":
        mjr = "Computer Engr"
    else:
        mjr = "Other Major"

    await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=mjr))
    await ctx.send(MAJOR_END_MESSAGE)


@bot.command()
async def classes(ctx, *classes: str):
    default_role = discord.utils.get(ctx.guild.roles, name=DEF_ROLE)
    await ctx.author.add_roles(default_role)

    classes_assign = []
    flag_error = True

    for clas in classes:
        if ClassCheck(str(clas)) == False:
            await ctx.send("{} {} caused this error. No classes assigned/created.".format(CLASS_NAME_RULE, clas))
            flag_error = False
            break
        else:
            classes_assign.append(ClassFormat(str(clas)))

    if flag_error == True:
        classes_counter = RolesCounterClasses(ctx)

        classes_author = []
        for clas in ctx.author.roles:
            classes_author.append(clas.name)

        for clas in classes_assign:
            if str(clas) in classes_counter:
                if str(clas) not in classes_author:
                    role_add = discord.utils.get(ctx.guild.roles, name=str(clas))
                    await ctx.author.add_roles(role_add)

                    if classes_counter[clas] == MIN_PEOPLE_CHANNEL:
                        overwrites = {
                            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            role_add: discord.PermissionOverwrite(read_messages=True)
                            }
                        categ = await ctx.guild.create_category(clas, overwrites = overwrites)
                        await ctx.guild.create_text_channel("resources", category = categ)
                        await ctx.guild.create_text_channel("general", category = categ)
                        await ctx.guild.create_voice_channel("voice", category = categ)

            else:
                new_role = await ctx.guild.create_role(name = str(clas), permissions = default_role.permissions,
                                                    colour= default_role.colour, mentionable = True)
                await new_role.edit(position=default_role.position-1)
                await ctx.author.add_roles(new_role)

        await ctx.send(CLASS_END_MESSAGE)

    print("done for {}".format(ctx.author.name))

@bot.command()
async def gulagsmn(ctx):
    limit_to = "Tyrant"
    flag = CheckPermissionRole(ctx, limit_to)

    if flag:
        gulag_guy = random.choice(ListRoleMembers(bot, DEF_ROLE))
        gulag_length = random.randint(1, 48)

        gulag_role = discord.utils.get(ctx.guild.roles, name= GULAF_ROLE)
        await gulag_guy.add_roles(gulag_role)

        await ctx.send(f"{gulag_guy.mention} sent to gulag for {gulag_length} hours")

        await asyncio.sleep(gulag_length*60*60)
        await ctx.send(f"{gulag_guy.mention} your gulag sentence ended. be luckier next time")
        await gulag_guy.remove_roles(gulag_role)
    else:
        await ctx.send(f"This command can only be used by great {limit_to}. suck some balls hahahahahha")

bot.run(TOKEN)
