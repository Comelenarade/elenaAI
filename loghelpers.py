import json, datetime, os

cwd = os.getcwd()
LOGS_PATH = os.path.join(cwd, "logs")
COMRADE_FILE = "comrade_"
TODO_JSON = "todo.json"

def checkLogPath():
    if not os.path.exists(LOGS_PATH):
        os.makedirs(LOGS_PATH)

def saveComrades(allComrades): # saves comrades in json log file
    datetimenow = datetime.datetime.now().strftime("%Y_%m_%d_id%S")
    with open(LOGS_PATH+os.sep+f"{COMRADE_FILE}{datetimenow}.json", "w") as write_file:
        data = {}
        for _ in allComrades:
            data[_.id] = {"name":_.name, "nick":_.nick, "discriminator":_.discriminator, "roles":[_a.name for _a in _.roles]}
        json.dump(data, write_file)

def getComrades(fileName): #returns info from comrades logs in human friendly way
    with open(LOGS_PATH+os.sep+fileName) as read_file:
        dataComrades = json.load(read_file)
    message=""
    allMessages = []
    for _ in dataComrades:
        message += (f"User ID {str(_)}:\n")
        for _a in dataComrades[_]:
            if _a == "roles":
                dataComrades[_][_a] = [_aa for _aa in dataComrades[_][_a] if _aa != "@everyone"]
            message += (f"\t\t{_a}: {dataComrades[_][_a]}\n")
        message += "\n \u200b"
        allMessages.append(message)
        message=""
    return allMessages

def findLatFileBegWith(files_list, begWith): #return latest created file in the list
    compare_time = 0
    fileRet = ""
    for _ in files_list:
        if _.startswith(begWith):
            fileCreaTime = os.path.getmtime(LOGS_PATH+os.sep+_)
            if compare_time == 0:
                compare_time = fileCreaTime
                fileRet = _
            else:
                if compare_time < fileCreaTime:
                    compare_time = fileCreaTime
                    fileRet = _
    return fileRet

def todo_file():
    with open(TODO_JSON) as read_file:
        todo_tasks = json.load(read_file)
    message=""
    allMessages = []
    for _ in todo_tasks:
        message += (f"Task {str(_)}: {todo_tasks[_]}\n")
        allMessages.append(message)
        message=""
    return allMessages

def todo_delete(task_del):
    with open(TODO_JSON) as f:
        todo_tasks = json.load(f)
        
    try:
        todo_tasks.pop(str(task_del))
    except:
        return 0

    with open(TODO_JSON, "w") as f:
        json.dump(todo_tasks, f)
    return 1

def todo_add(task_add):
    with open(TODO_JSON) as f:
        todo_tasks = json.load(f)
    
    if len(todo_tasks) == 0:
        todo_tasks = {"0":task_add}
    else:
        _temp = 0
        for _ in todo_tasks:
            if int(_) > _temp:
                _temp = int(_)
        todo_tasks[str(_temp+1)] = str(task_add)

    with open(TODO_JSON, "w") as f:
        json.dump(todo_tasks, f)

def saveReminder():
    pass

def getReminder():
    pass
