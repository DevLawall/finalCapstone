# finalCapstone

Task Manager

This project is a relatively rudimentary system of tracking tasks (which are read from/written to a text file - tasks.txt) that are assigned to various users (same - user.txt). Each user can see and modify (but not delete) the tasks assigned to them, and their details; admin can also add users and tasks, and view statistical data, some of which are also exported to separate files (task_overview.txt, user_overview.txt).

To install, simply download task_manager_improved.py. Downloading the other files is optional; at runtime, tasks.txt and user.txt will be autogenerated if absent (in which case they will be empty initially, except that user.txt will have the admin account added immediately), and said admin can then generate the statistical files from the menu.

Use task_manager_improved.py by running it in your IDE of choice and interacting with it by entering the appropriate commands into the terminal.

![Correct password enforcement](https://github.com/DevLawall/finalCapstone/assets/134338669/20d434a3-475d-4e62-abd0-37e6a47e56c4)
![Main menu for admin user](https://github.com/DevLawall/finalCapstone/assets/134338669/80ff55ac-3870-49cc-9af4-b71729c4637a)
![Task view and selection](https://github.com/DevLawall/finalCapstone/assets/134338669/bf101c5f-676a-4abf-89c1-ee56529b73f9)

task_manager_improved.py is based on task_manager.py by HyperionDev: https://www.hyperiondev.com/
