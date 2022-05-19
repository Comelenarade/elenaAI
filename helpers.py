import re

def RolesCounterAll(context):
    all_roles = context.guild.roles
    role_to_count = {}
    for role in all_roles:
        num_ppl = len(role.members)
        if num_ppl > 0 and str(role.name) != "@everyone":
            role_to_count.update({role.name:num_ppl})
    return role_to_count

def RolesCounterPrepToPrint(role_count_dict, block_size = 20):
    counter = 0
    message = ""
    message_blocks = [] #to avoid Discord char limit
    for keey in role_count_dict:
        tmp_mes = "{} - {} members \n".format(str(keey), str(role_count_dict[keey]))
        message += tmp_mes
        counter += 1
        if counter == block_size:
            message_blocks.append(message)
            counter = 0
            message = ""
    if message != "":
        message_blocks.append(message)
    return message_blocks

def RolesCounterClasses(context):
    all_roles_counter = RolesCounterAll(context)
    roles_pop = []
    r = re.compile('[A-Z]{4}\s[0-9]{4}')
    for role in all_roles_counter:
        if r.match(role) is None:
            roles_pop.append(role)
    for role in roles_pop:
        all_roles_counter.pop(role)
    return dict(sorted(all_roles_counter.items(), key=lambda x: x[1]))

def ClassCheck(class_input):
    r = re.compile('[A-zA-Z]{4}[0-9]{4}')
    if r.match(class_input) is not None:
        return True
    else:
        return False

def ClassFormat(class_input):
    class_name = class_input[0:4]
    class_numb = class_input[4:8]
    new_class_name = "{} {}".format(class_name.upper(), class_numb)
    return new_class_name
