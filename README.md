Cab Booking System 

Introduction
----
Cab Booking System is a Simple Console Application where a user can book a cab between different client locations. Multiple employees can book the same cab to travel to client locations or in between stops. Each cab will have a dedicated route and will travel to and fro at different timings. 

### Configuration parameters
**Email and Password** are the configuration parameter required to make the login for each user.

### Database File
Database automatically created with mysql

### Different Roles(Level) in project 

**Admin:** This role of Admin is where admin can perform CRUD operation for employees and see all the bookings done by 
employees. Admin can also perform CRUD operation on cabs and also see the bookings of cabs between any period of time.

**Employee:** This role is for employees, where they can book cabs and see their past and upcoming bookings. Employees 
can also cancel their bookings prior to 30 min.

### run.py
This file has the mysql connection code and login code where after giving the right credentials schema.py file is called.
### schema.py
This file has all the schemas of the respective tables.
### admin.py
This file all the functionalities of admin related tasks.
### employee.py
This file is used to carry out all the Employee related functions.


Login credentials for Admin
---
```   
email: sayan@gmail.com
password: Sayan@1
```

Setup for Running the Project
---
```   
1. Open the project cabBooking
2. Run pythonn file 'run.py'
    -> python run.py

Note: Every employee added by admin has a set default password i.e. firstname + @123
e.g. if added user name is Josh, then its password will be 'josh@123'
```

Setup for running CRON jobs
---
```
1. Open new terminal
2. Go the project cab_booking
3. Run pythonn file 'booking_status_cron_job.py'
    -> python booking_status_cron_job.py
```

### DIRECTORY STRUCTURE
```
+-- cab_booking
|  +--run.py
|  +--admin.py
|  +--employee.py
|  +--schema.py
|  +--booking_status_cron_job.py
```


