import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

#=====GATHERING EXTERNAL DATA===========

def scan_users():
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    with open("user.txt", "r") as user_file:
        #read the data
        user_info = user_file.read().split("\n")
        #remove any blank lines
        user_info = [u for u in user_info if u != ""]
        #convert to a dictionary
        user_dict = {}
        for v in user_info:
            username, password = v.split(";")
            user_dict[username] = password
        return user_dict

def scan_tasks():
    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass

    with open("tasks.txt", "r") as task_file:
        #read the data
        task_data = task_file.read().split("\n")
        #remove any blank lines
        task_data = [t for t in task_data if t != ""]
        #convert to a dictionary
        task_details = []
        for t_str in task_data:
            curr_t = {}
            # Split by semicolon and manually add each component
            task_components = t_str.split(";")
            curr_t["username"] = task_components[0]
            curr_t["title"] = task_components[1]
            curr_t["description"] = task_components[2]
            curr_t["due_date"] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
            curr_t["assigned_date"] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
            curr_t["completed"] = True if task_components[5] == "Yes" else False
            task_details.append(curr_t)
        return task_details

#=====FURTHER FUNCTION DEFINITIONS=======

def write_task_file(): #see add_task(), edit_task(), complete_task()
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t["username"],
                t["title"],
                t["description"],
                t["due_date"].strftime(DATETIME_STRING_FORMAT),
                t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                "Yes" if (t["completed"] == True) else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))    

def reg_user():
    print("New User Registration")
    while True:
        newuser_username = input("Please enter the new user's username: ")
        # Helps to prevent breaking functionality pertaining to user.txt
        if ";" in newuser_username:
            print("Illegal character used: semicolon (;). Please try again.")
        # Disallows a blank username
        elif newuser_username == "":
            print("Please enter an actual value.")
        elif newuser_username in username_password.keys():
            print("A user with that name already exists. Please try again.")
        else:
            break
    while True:
        newuser_password = input("Please enter the new user's password: ")
        if newuser_password == "":
            print("Please enter an actual value.")
            continue
        if ";" in newuser_password:
            print("Illegal character used: semicolon (;). Please try again.")
            continue
        newuser_confirm = input("Please confirm the new user's password: ")
        if newuser_password == newuser_confirm:
            #Add to the dictionary username_password,
            username_password[newuser_username] = newuser_confirm
            print("Saving details...")
            #then the file user.txt
            with open("user.txt", "w") as out_file:
                user_list = []
                for k in username_password:
                    user_list.append(f"{k};{username_password[k]}")
                out_file.write("\n".join(user_list))
            print(f"User {newuser_username} added.")
            break
        else:
            # - Otherwise you present a relevant message.
            print("The passwords do not match. Please try again.")
            continue

def add_task():
    """Allow a user to add a new task to task.txt file
        Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task and 
            - the due date of the task."""
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
        else:
            break    
    # Helps to prevent breaking functionality pertaining to tasks.txt
    print("Please note that semicolons in the task title or description will be automatically removed.")
    task_title = input("Task title: ").replace(";","")
    task_description = input("Task description: ").replace(";","")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    """ Add the data to the file task.txt and
        Include 'No' to indicate that the task has not yet been completed."""
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    write_task_file()
    print("Task successfully added.")

def view_all():
    for t in task_list:
        disp_str = f"Task Title: \t\t {t['title']}\n"
        disp_str += f"Assigned To: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n{t['description']}\n"
        print(disp_str if disp_str != "" else "No tasks are being tracked")

def view_mine():
    #First, display (and assign numbers to) the appropriate tasks
    print(f"\nTasks assigned to {curr_user}:")
    print("----------------------------------------")
    my_task_list = []
    for i in range(0, len(task_list)):
        if task_list[i]["username"] == curr_user:
            #Make a sublist of task_list containing only this user's tasks
            my_task_list.append(task_list[i])
            disp_str = f"Task {len(my_task_list)}: \t{task_list[i]['title']}\n"
            disp_str += f"Date Assigned: \t{task_list[i]['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t{task_list[i]['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n{task_list[i]['description']}\n"
            print(disp_str)
    #Second, if the user has a task assigned to them,
    if len(my_task_list) == 0:
        print("none")
    #let the user select one or return to the main menu
    else:
        while True:
            try:
                #Note that the UI will start at 1 when listing tasks,
                #so 1 must be subtracted from the user's input
                #in order to realign it with the appropriate index
                selected_task = int(input("Please select a task by typing the appropriate number.\n"+
                                          "Alternatively, type -1 to return to the main menu.\n")) -1
                if selected_task == -2:
                    #return to main
                    break
                elif selected_task not in range(0,len(my_task_list)):
                    print("That number is not within the appropriate range. Please try again.")
                elif my_task_list[selected_task]["completed"] == True:
                    #Completed tasks can't be edited
                    print("That task has already been completed and thus cannot be modified.")
                    continue
                else:
                    #Options for what to do with the task
                    while True:
                        print(f"Task {selected_task +1}: \t{my_task_list[selected_task]['title']}")
                        my_task_choice = input("Please select one of the following options by inputting the corresponding letter:\n"+
                                               "m\tModify this task\n"+
                                               "c\tMark this task as complete\n"+
                                               "e\tExit to task selection\n").lower()
                        if my_task_choice == "m":
                            edit_task(my_task_list, selected_task)
                            break
                        elif my_task_choice == "c":
                            complete_task(my_task_list, selected_task)
                            break
                        elif my_task_choice == "e":
                            break
                        else:
                            print("Input not recognised. Please try again.")
            
            except ValueError:
                print("Input not recognised. Please try again.")

def edit_task(user_tasks_indices, chosen_task): #see view_mine()
    #reassign or change deadline
    task_to_modify = user_tasks_indices[chosen_task]
    print(f"Modifying Task {chosen_task +1}: {user_tasks_indices[chosen_task]['title']}")
    while True:
        task_modify_choice = input("Please select one of the following options by inputting the corresponding letter:\n"+
                                   "a\tAssign this task to another user\n"+
                                   "d\tChange this task's deadline\n"+
                                   "e\tExit to task selection\n").lower()
        if task_modify_choice == "a":
            #First enforce valid input
            while True:
                reassigned_to = input("Enter the username of the person to assign this task to.\n"+
                                      "Note that this is case-sensitive.\n")
                if reassigned_to in username_password.keys():
                    break
                else:
                    print("User not recognised. Please try again.")
                    continue
            #Then make the changes
            task_to_modify["username"] = reassigned_to
            user_tasks_indices[chosen_task] = task_to_modify
            write_task_file()
            print("Task successfully reassigned.")
            break
        elif task_modify_choice == "d":
            while True:
                try:
                    task_new_deadline = input("New task deadline (YYYY-MM-DD): ")
                    new_deadline_time = datetime.strptime(task_new_deadline, DATETIME_STRING_FORMAT)
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified")
            task_to_modify["due_date"] = new_deadline_time
            user_tasks_indices[chosen_task] = task_to_modify
            write_task_file()
            print("Task deadline successfully rescheduled.")
            break
        elif task_modify_choice == "e":
            break
        else:
            print("Input not recognised. Please try again.")

def complete_task(user_tasks_indices, chosen_task): #see view_mine()
    task_to_modify = user_tasks_indices[chosen_task]
    task_to_modify["completed"] = True
    user_tasks_indices[chosen_task] = task_to_modify
    write_task_file()
    print("Task successfully marked complete.")

def overview_tasks():
    #firstly, get the raw data
    tasks_complete = [t for t in task_list if t["completed"] == True]
    tasks_incomplete = [t for t in task_list if t["completed"] == False]
    tasks_overdue = [t for t in task_list if (t["completed"] == False \
                                              and t["due_date"] < datetime.today())]
    #then calculate the percentages
    try:
        percent_tasks_incomplete = 100 * (len(tasks_incomplete) / len(task_list))
    except ZeroDivisionError:
        percent_tasks_incomplete = 0
    try:
        percent_tasks_overdue = 100 * (len(tasks_overdue) / len(task_list))
    except ZeroDivisionError:
        percent_tasks_overdue = 0
    #now display these contents and output them to a file
    task_stat_str =  f"Total number of tasks:          {len(task_list)}\n"
    task_stat_str += f"Number of completed tasks:      {len(tasks_complete)}\n"
    task_stat_str += f"Number of incomplete tasks:     {len(tasks_incomplete)}\n"
    task_stat_str += f"Number of overdue tasks:        {len(tasks_overdue)}\n"
    task_stat_str += f"Proportion of incomplete tasks: {'{0:.4g}'.format(percent_tasks_incomplete)}%\n"
    task_stat_str += f"Proportion of overdue tasks:    {'{0:.4g}'.format(percent_tasks_overdue)}%"
    print("----------------------------------------")
    print("===============TASK DATA================")
    print(task_stat_str)
    print("----------------------------------------\n")
    with open("task_overview.txt", "w") as file:
        file.write(task_stat_str)

def overview_users():
    with open("user_overview.txt", "w") as file:
        file.write("")
    #firstly, get the totals
    totals_str =  f"Total users registered:\t{len(username_password)}\n"
    totals_str += f"Total tasks tracked:\t{len(task_list)}"
    print("----------------------------------------")
    print("===============USER DATA================")
    print(totals_str)
    print("----------------------------------------\n")
    with open("user_overview.txt", "a") as file:
        file.write(f"{totals_str}\n")
        file.write(f"----------------------------------------\n\n")
    #now get the raw user data
    for user_record in username_password.keys():
        user_tasks_assigned = [t for t in task_list if t["username"] == user_record]
        user_tasks_complete = [t for t in task_list if ((t["username"] == user_record) \
                                                        and (t["completed"] == True))]
        user_tasks_incomplete = [t for t in task_list if ((t["username"] == user_record) \
                                                          and (t["completed"] == False))]
        user_tasks_overdue = [t for t in task_list if ((t["username"] == user_record) \
                                                       and (t["completed"] == False) \
                                                       and (t["due_date"] < datetime.today()))]
        #then calculate the percentages, guarding against dividing by zero
        percent_user_tasks_assigned =   0 if len(task_list) == 0 else \
                                        100 * (len(user_tasks_assigned) / len(task_list))
        percent_user_tasks_complete =   0 if len(user_tasks_assigned) == 0 else \
                                        100 * (len(user_tasks_complete) / len(user_tasks_assigned))
        percent_user_tasks_incomplete = 0 if len(user_tasks_assigned) == 0 else \
                                        100 * (len(user_tasks_incomplete) / len(user_tasks_assigned))
        percent_user_tasks_overdue =    0 if len(user_tasks_assigned) == 0 else \
                                        100 * (len(user_tasks_overdue) / len(user_tasks_assigned))
        #now display these contents and output them to the file
        user_stat_str =  f"Task history for:       {user_record}\n"
        user_stat_str += f"Number of assigned tasks:       {len(user_tasks_assigned)}\n"
        user_stat_str += f"Assigned/total task ratio:      {'{0:.4g}'.format(percent_user_tasks_assigned)}%\n"
        user_stat_str += f"Completed/assigned task ratio:  {'{0:.4g}'.format(percent_user_tasks_complete)}%\n"
        user_stat_str += f"Incomplete/assigned task ratio: {'{0:.4g}'.format(percent_user_tasks_incomplete)}%\n"
        user_stat_str += f"Overdue/assigned task ratio:    {'{0:.4g}'.format(percent_user_tasks_overdue)}%"
        print(user_stat_str)
        print("----------------------------------------\n")
        with open("user_overview.txt", "a") as file:
            file.write(f"{user_stat_str}\n")
            file.write(f"----------------------------------------\n\n")

#=====STARTUP FUNCTIONALITY=============

#1: Acquire task data
task_list = scan_tasks()

#2: Acquire user data to enable login
username_password = scan_users()

#3: Have the user log in
logged_in = False
while not logged_in:

    print("LOGIN")
    # Verify valid username
    curr_user = input("Username: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    curr_pass = input("Password: ")
    while curr_pass != username_password[curr_user]:
        print("Wrong password")
        curr_pass = input("Password: ")
    print("Login Successful!")
    logged_in = True

#=====MAIN MENU=========================
admin_options_1 =   "r\tregister user\n" +\
                    "a\tadd task\n" +\
                    "va\tview all tasks\n"      if curr_user == "admin" else ""
admin_options_2 =   "gr\tgenerate reports\n" +\
                    "ds\tdisplay statistics\n"  if curr_user == "admin" else ""

while True:    
    menu = input("""Please select one of the following options:\n"""
                 +admin_options_1+
                 """vm\tview my tasks\n"""
                 +admin_options_2+
                 """e\texit\n""").lower()

    if menu == "r" and curr_user == "admin":
        """Add a new user to the user.txt file"""
        reg_user()

    elif menu == "a" and curr_user == "admin":
        add_task()

    elif menu == "va" and curr_user == "admin":
        view_all()           

    elif menu == "vm":
        view_mine()    

    elif menu == "gr" and curr_user == "admin":
        overview_tasks()
        overview_users()
    
    elif menu == "ds" and curr_user == "admin": 
        """Re-check the user and task data, as per the instructions for this assignment"""
        task_list = scan_tasks()
        username_password = scan_users()

        print("----------------------------------------")
        print(f"Number of users: \t\t {len(username_password.keys())}")
        print(f"Number of tasks: \t\t {len(task_list)}")
        print("----------------------------------------")     

    elif menu == "e":
        print("Goodbye!")
        exit()

    else:
        print("Invalid menu input. Please try again.")

#Attributions
#I learned about restricting the number of decimal digits to display from here:
#https://stackoverflow.com/questions/2389846/python-decimals-format
#There was also some useful information here, though I ended up not using it:
#https://stackoverflow.com/questions/56217081/force-python-to-print-a-certain-number-of-decimal-places