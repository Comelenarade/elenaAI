import discord, asyncio, random, os, datetime
from discord.ext import commands

from helpers import *
from loghelpers import *

from const.TOKEN import TOKEN
from const.TEXT import WELCOME_MESSAGE, CLASS_NAME_RULE, CLASS_END_MESSAGE, MAJOR_END_MESSAGE, ONLINE_MESSAGE, CLASS_DUP_ERROR, REMINDER_HELP

COMMANDMENTS = ""

WELCOME_CHANNEL = 786107233586905128
DEF_ROLE = "comrade"
GULAG_ROLE = 'GULAG'
TYRANT_ROLE  = "Tyrant"
ADMINS_ROLE = "Elena Gubankova"
ELENA_CHANNEL = "elena"

MIN_PEOPLE_CHANNEL = 4

utc_dt = datetime.datetime.now(datetime.timezone.utc)

intents = discord.Intents.all()
intents.members = True
#intents.message_content = True

bot = commands.Bot(command_prefix='?', description="ELENA AI", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    global COMMANDMENTS
    COMMANDMENTS = parse_commandments(os.getcwd(), "commandments")
    checkLogPath()

@bot.event
async def on_member_join(member): #when new person joins, welcome them
    channel = bot.get_channel(WELCOME_CHANNEL)
    await channel.send(WELCOME_MESSAGE)

@bot.command()
async def online(ctx): #check status
    """Sends a message to a chat."""
    await ctx.send(ONLINE_MESSAGE)

@bot.command()
async def allroles(ctx): #stats for all roles
    """Sends a list with all roles statistics"""
    messg = RolesCounterPrepToPrint(RolesCounterAll(ctx))
    for block in messg:
        await ctx.send(block)

@bot.command()
async def classroles(ctx): #stats only for roles
    """Sends a list with class roles statistics."""
    messg = RolesCounterPrepToPrint(RolesCounterClasses(ctx))
    for block in messg:
        await ctx.send(block)

@bot.command()
async def classes(ctx, *classes: str): #Assign classes to person
    """To assign class roles. Classes MUST be 4 letters 4 digits no space! Example: ?classes MATH2100 ELEC2100 ENGR1000"""
    default_role = discord.utils.get(ctx.guild.roles, name=DEF_ROLE)
    await ctx.author.add_roles(default_role) #give comrade role

    classes_assign = [] #list of classes to add to person
    flag_error = True

    for clas in classes: #Check input
        if ClassCheck(str(clas)) == False: #check if matches format
            await ctx.send("{} {} caused this error. No classes assigned/created.".format(CLASS_NAME_RULE, clas))
            flag_error = False
            break
        elif ClassFormat(str(clas)) in classes_assign: #check if repeated
            await ctx.send("{} caused this error. {}".format(clas, CLASS_DUP_ERROR))
        else:
            classes_assign.append(ClassFormat(str(clas))) #if ok, append to list of classes to add to person

    if flag_error == True: #if no errors
        classes_counter = RolesCounterClasses(ctx)

        classes_author = []
        for clas in ctx.author.roles:
            classes_author.append(clas.name)

        for clas in classes_assign:
            if str(clas) in classes_counter: #if such class role already exist
                if str(clas) not in classes_author: # if person does not have such role already
                    role_add = discord.utils.get(ctx.guild.roles, name=str(clas))
                    await ctx.author.add_roles(role_add) #add role to person

                    if classes_counter[clas] == MIN_PEOPLE_CHANNEL: #if enough people for new chanel, create:
                        overwrites = {
                            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                            role_add: discord.PermissionOverwrite(read_messages=True)
                            }
                        categ = await ctx.guild.create_category(clas, overwrites = overwrites) #category, in which:
                        await ctx.guild.create_text_channel("resources", category = categ) #chat for resources
                        await ctx.guild.create_text_channel("general", category = categ) #general chat
                        await ctx.guild.create_voice_channel("voice", category = categ) #voice channel

            else: #if new role, i.e. no such class yet, create it and add to person
                new_role = await ctx.guild.create_role(name = str(clas), permissions = default_role.permissions,
                                                    colour= default_role.colour, mentionable = True)
                await new_role.edit(position=default_role.position-1)
                await ctx.author.add_roles(new_role)

        await ctx.send(CLASS_END_MESSAGE)

    print("done for {}".format(ctx.author.name)) #console log

@bot.command()
async def major(ctx, major: str): #assign major to person, only after classes assigned
    """To assign a major. XX is EE for Electrical engr, CO for Computer engr, OM - for all other majors"""
    limit_to = DEF_ROLE
    flag = CheckPermissionRole(ctx, limit_to)

    if flag:
        if major.upper() == "EE":
            mjr = "Electrical Engr"
        elif major.upper() == "CO" or major.upper() == "CE":
            mjr = "Computer Engr"
        else:
            mjr = "Other Major"

        await ctx.author.add_roles(discord.utils.get(ctx.guild.roles, name=mjr))
        await ctx.send(MAJOR_END_MESSAGE)
    else:
        await ctx.send("You must add classes first, sorry not sorry.")

@bot.command()
async def gulagsmn(ctx): #randomly gulag someone
    """Sends random person to GULAG for 1-48 hours. Can only be used be Tyrant."""
    limit_to = TYRANT_ROLE
    flag = CheckPermissionRole(ctx, limit_to)

    if flag:
        gulag_guy = random.choice(ListRoleMembers(ctx, DEF_ROLE))
        gulag_length = random.randint(1, 48)
        gulag_reason = random.choice(COMMANDMENTS)

        gulag_role = discord.utils.get(ctx.guild.roles, name= GULAG_ROLE)

        await gulag_guy.add_roles(gulag_role)
        await ctx.send(f"{gulag_guy.mention} sent to gulag for {gulag_length} hours. Reason is you are not following the principle of {gulag_reason[0]}: '{gulag_reason[1]}'")

        gulag_follow = random.choice(COMMANDMENTS)
        await asyncio.sleep(gulag_length*60*60)
        await ctx.send(f"{gulag_guy.mention} your gulag sentence ended. stick to the following {gulag_follow[0]} principle: '{gulag_follow[1]}'")
        await gulag_guy.remove_roles(gulag_role)
    else:
        await ctx.send(f"This command can only be used by great {limit_to}. suck some balls hahahahahha")

@bot.command()
async def checkclasses(ctx): #service routine
    """Checks if any role classes with no members are there, because it can mess with Elena. Can only be used be Tyrant."""
    limit_to = TYRANT_ROLE
    flag = CheckPermissionRole(ctx, limit_to)
    if flag:
        r = re.compile('[A-Z]{4}\s[0-9]{4}')
        elenaChnl = discord.utils.get(ctx.guild.text_channels, name= ELENA_CHANNEL)
        all_roles = RolesCounterAllwZero(ctx)

        for role in all_roles:
            if (all_roles.get(role) == 0):
                if r.match(role) is not None:
                    await elenaChnl.send(f"FOUND EMPTY CLASS ROLE {role}. deleting it")
                    empty_role = discord.utils.get(ctx.guild.roles, name= role)
                    await empty_role.delete(reason="no members")
        await elenaChnl.send("done with empty roles check")
    else:
        await ctx.send(f"This command can only be used by great {limit_to}. suck some balls hahahahahha")

@bot.command()
async def logcomrades(ctx): #creates a log file with all comrade role members
    """Updates log json file with all comrades. Can only be used by Tyrant"""
    limit_to = TYRANT_ROLE
    flag = CheckPermissionRole(ctx, limit_to)
    if flag:
        saveComrades(ListRoleMembers(ctx, DEF_ROLE))
        await ctx.send("Comrade role logs are created")
    else:
        await ctx.send(f"This command can only be used by great {limit_to}. suck some balls hahahahahha")

@bot.command()
async def reportcomrades(ctx): #Sends to discord log in friendly format
    """Prints latest log json file with all comrades. Can only be used by Tyrant"""
    limit_to = TYRANT_ROLE
    flag = CheckPermissionRole(ctx, limit_to)
    if flag:
        fileFound = findLatFileBegWith(os.listdir(LOGS_PATH), "comrade")
        if fileFound != "":
            messages_list = getComrades(fileFound)
            for block in MessagesToBlocks(messages_list):
                await ctx.send(block)
        else:
            await ctx.send("No logs for comrades were yet created")
    else:
        await ctx.send(f"This command can only be used by great {limit_to}. suck some balls hahahahahha")

@bot.command()
async def reminder(ctx, *remindAt: str):
    print(remindAt)
    if (remindAt == () or remindAt[0].startswith("-h")):
        await ctx.send(REMINDER_HELP)
    else:
        reminder = {}
        if (remindAt[0].startswith("-at")): # format MM DD YYYY HH MM datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            for _ in remindAt[1:]:

        if (remindAt[0].startswith("-in")):
            pass

bot.run(TOKEN)
