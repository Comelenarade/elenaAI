import discord
from discord.ext import commands

from helpers import *

TOKEN = "OTU5OTMyMTA4MjA4NTAwNzQ2.YkjEcQ.zQoPcgIxn57MoF4AMQouO9MAe-I"
description = "ELENA"

WELCOME_CHANNEL = 786107233586905128

MIN_PEOPLE_CHANNEL = 4

WELCOME_MESSAGE = ("WELCOME TO ELENA COMRADES SERVER! \n"
                    "1) Change your name to the irl one \n"
                    "2) To set the class roles, you need to go to #schedules and drop ur schedule in text format. "
                    "We are using bot to automate role assignment, so u need to follow guidelines: "
                    "In #schedules send something like: '?classes XXXX1111 YYYY2222 ZZZZ3333' \n"
                    "Important! No spaces between the class name and number!! MUST be 4 letters 4 digits!\n"
                    "Example: ?classes MATH2100 ELEC2100 POLS3043 ENGR1000\n"
                    "3) Admins are '@Elena Gubankova', ping if you need help\n"
                    "4) ?????\n"
                    "5) GLORY TO ELENA COMRADES!")

CLASS_NAME_RULE = "Class names should jave 4 letters 4 digits with no space in between, ex: MATH2100."
CLASS_END_MESSAGE = ("All set (hopefully)! Double check your assigned roles, if anything wrong - ping admins (@Elena Gubankova)."
                        " Last, please assign your major. Currently only three options available"
                        " Electrical Engineering, Computer Engineering, and all other majors"
                        " To set major type: ?major XX, where XX is EE or CO or OM. Example: ?major EE ")
MAJOR_END_MESSAGE = ("Congratulations, comrade! You finished registration process! Double check all classes and major assignments."
                        " good luck and always praise Elena")


intents = discord.Intents.all()
intents.members = True
#intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

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
    await ctx.send("Prepare to fight for the cause of the Elena Comrades!")

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
    default_role = discord.utils.get(ctx.guild.roles, name='comrade')
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
                #new_role = discord.utils.get(ctx.guild.roles, name=str(clas))
                await new_role.edit(position=default_role.position-1)
                await ctx.author.add_roles(new_role)

        await ctx.send(CLASS_END_MESSAGE)

    print("done for {}".format(ctx.author.name))

bot.run(TOKEN)
