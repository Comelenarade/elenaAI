import re, os, discord

MAX_STRING_CHAR = 2000

def parse_commandments(path, folder): #make tuple with all commandments
    path_princ = os.path.join(path, folder)
    all_tuple = ()
    for file in os.listdir(path_princ):
        with open(os.path.join(path_princ, file)) as f:
            lines = f.readlines()
            for line in lines:
                new_tuple = (file.split(".")[0],line.strip())
                all_tuple = (new_tuple, ) + all_tuple
    return all_tuple

def RolesCounterAllwZero(context): #make dictionary {with role_name : num_of_people_with_this_role} including roles with no members
    all_roles = context.guild.roles
    role_to_count = {}
    for role in all_roles:
        role_to_count.update({role.name:len(role.members)})
    return role_to_count

def RolesCounterAll(context): #make dictionary {with role_name : num_of_people_with_this_role}, only >0 people
    all_roles = RolesCounterAllwZero(context)

    flagDeleteItem = 1 ##Deleting all roles with zero members
    while (flagDeleteItem):
        for role in all_roles:
            if (all_roles.get(role) == 0):
                flagDeleteItem = 0
                break
        if (not flagDeleteItem):
            all_roles.pop(role)
            flagDeleteItem = 1
        else:
            flagDeleteItem = 0

    all_roles.update({"@ everyone":all_roles.pop("@everyone")}) #add everyone without tagging
    return dict(reversed(list(all_roles.items())))

def RolesCounterPrepToPrint(role_count_dict): #Creates messages to output number of people in each role
    all_messages = []
    for keey in role_count_dict:
        tmp_mes = "{} - {} members \n".format(str(keey), str(role_count_dict[keey]))
        all_messages.append(tmp_mes)
    return MessagesToBlocks(all_messages)

def MessagesToBlocks(list_of_messages): #makes blocks of messages
    counter = 0
    message = ""
    message_blocks = [] #to avoid Discord char limit
    for _ in list_of_messages:
        if (counter + len(_)) < MAX_STRING_CHAR:
            message += _
            counter = counter + len(_)
        else:
            message_blocks.append(message)
            message = _
            counter = len(_)
    if message != "":
        message_blocks.append(message)
    return message_blocks

def RolesCounterClasses(context): #stats for people taking classes
    all_roles_counter = RolesCounterAll(context) #take in stats for all roles
    roles_pop = []
    r = re.compile('[A-Z]{4}\s[0-9]{4}')
    for role in all_roles_counter:
        if r.match(role) is None:
            roles_pop.append(role)
    for role in roles_pop:
        all_roles_counter.pop(role)
    if all_roles_counter == {}:
        all_roles_counter = {"no classroles":"no"}
    return dict(sorted(all_roles_counter.items(), key=lambda x: x[1])) #sort

def ClassCheck(class_input): #Check if input (ex. MATH2100) class matches format
    r = re.compile('[A-zA-Z]{4}[0-9]{4}')
    if r.match(class_input) is not None:
        return True
    else:
        return False

def ClassFormat(class_input): #convert input into class name (ex. MATH2100 into Math 2100)
    class_name = class_input[0:4]
    class_numb = class_input[4:8]
    new_class_name = "{} {}".format(class_name.upper(), class_numb)
    return new_class_name

def CheckPermissionRole(context, role_check): #checks if person has needed permission, role (string)
    #works woth message too, message.author.roles; abused used for gulag
    for role in context.author.roles:
        if role.name == role_check:
            return True
    return False

def ListRoleMembers(context, role_check): #return list of everyone with role, list of objects
    role_add = discord.utils.get(context.guild.roles, name=role_check)
    return role_add.members

def CheckValue(valueCheck, valueRe, valueOutputs):
    r = re.compile('[A-zA-Z]{4}[0-9]{4}')
    if valueRe.match(class_input) is not None:
        return True
    else:
        return False

def checkCategoryClass(categorie):
    ALL_OTHER_CHANNELS = "All Other Classes"
    _catSplit = categorie.split(" ")
    if ((len(_catSplit) >= 2) or categorie == ALL_OTHER_CHANNELS):
        if (ClassCheck(f"{_catSplit[0]}{_catSplit[1]}") or categorie == ALL_OTHER_CHANNELS):
            return True
    return False
