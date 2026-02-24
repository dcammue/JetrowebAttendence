# JetrowebAttendence
Jetro Web Development Attendence application

## The Jetroweb Attendance or Worker hours Tracker has successfully been completed for use!!

### This application was designed to handle worker hours at Jetro Web Development and generate a monthly pdf to ensure Justic, free and fair work collaboration among Jetro members.

### This application contains both User and Admin Dashboards and each dashboard has a very nice features that has been explained in the below instructions.

#### the project will be hosted for internet access any moment from now, but it can be run on your local machine for tesing.

## How to get the project running on your local machine?

### 1. Firstly get the project to you local machine by clonning it from this page.

### Instructions

#### Clone the project

##### cd into a directory that you want to clone the project.
  
  cd Desktop/yourdirectory
  
  git clone https://github.com/dcammue/JetrowebAttendence.git

#### 2. After the clonning has been completed, cd into the project directory
  cd JetrowebAttendence

### 3. Activate the virsual environment (venv)

  python3 -m venv venv
  or
  python -m venv venv

  source venv/bin/activate

#### You will see something like (venv) user@localhost. That's mean, your virsual environment has been activated.

### 4. Install all django dependences for smooth operation of the project

  #### YOU will use pip to insatall the dependences. If pip not installed on your machine, install it using "  sudo apt install pip  "

  After installing pip, do this to install the django dependences;

  pip install -r requirement.txt

### 5. After the 'requirement.txt is install successfully, run or start the server

  python3 manage.py runserver

  #### You will see the server running on the port at http://127.0.0.1:8000/ Click on the URL to 
  gets you into the login page.

### 6. when you get into the login page, yuo will see a registration link at the upper right coner of the page, click and register for New Account. 
After the registration has been completed, you will be redirected to the login page for access to User Account, login with you credendials.

### 7. After successfull logged in, you will be welcome to the user dashboard. In the user dashboard, you will see today's dashboard,

### start and stop buttons that you can use to start or stop work session and your dashboard will be updates or reloads after every 30 sec,

### which will allow you to see or track the hour you have spent while working. At the lower bottom left coner, you will see the 

#### 'Delete Account' request, if you wish to delete your account.



### 8. you can also access the Admin Dashboard

  credentials: Username: dcammue Password: daniel0775123
  
  #### The Admin Dashboard is designed to allows admin to monetor the work sessions of every worker logged into application. The admin dashboard contain; today's dashboard, all user dashboard, start and stop buttons, monthly pdf generatable 
  
  ### session. This app is designed in a way that admin is not allow; to login into user account with admin password lesswise user, to start or stop user work session, it is free and fair, Justic for all app.


### 9. Feature to expect sooner or later;

 #### User viewing their work history, meaning you will be able to see how many hours you have spent for the past days within the current month,
 
 ### User will logout when work is over, which will enable the app to automatically stop work session if user forgot to stop work.
 
 #### Logging out user after screen has fall to sleep 5 minutes
 
 #### And many more feature to comes as knowledge and skill grow over time.
  


  

  
