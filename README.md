# htn-challenge

Summary
========
This is a RESTful API run by a Flask Server that deals with data about users participating in a hackathon. The following are the main functionalities of the API
-Getting data about all users participating in the hackathon
-Getting data about a specific user participating in the hackathon
-Update the information about a specific user
-Get a summary of all the skills that the users have

Testing was done using Postman

The Database
============
The database used is SQLite3 and two tables were created: users and skills.

users includes
- Unique ID
- name
- company
- email
- phone

skills includes
- User ID (references a particular user's unique ID)
- skill
- rating

The API
=======

All Users Endpoint
-------------------
Gets all users' data

Example
```GET http://localhost:5000/users``` 
![image](https://user-images.githubusercontent.com/58784851/220806126-4c0a581b-dc34-4c7c-8d7a-459171542dd9.png)

User Information Endpoint
-------------------------
Gets a specific user's data. Use their Unique ID to reference them.

Example
```GET localhost:5000/users/55```
![image](https://user-images.githubusercontent.com/58784851/220806277-7c36f05d-7791-412d-a83f-9936e9611c19.png)

Updating User Data Endpoint
---------------------------
Update User's Data using their unique ID.

Examples
```PUT localhost:5000/users/55```
Updating phone number
![image](https://user-images.githubusercontent.com/58784851/220806591-8abdb73c-386c-44d9-b167-8ff2cfda846c.png)

Adding a new skill
![image](https://user-images.githubusercontent.com/58784851/220806722-427b0e06-e6a6-405d-8482-f3bf7286f5d6.png)

Updating a skill
![image](https://user-images.githubusercontent.com/58784851/220806759-26729bf6-1df9-4587-8ebe-32a312e0ef43.png)


Skills Endpoints
-----
Show a list of skills and aggregate info about them. 

Example
```GET localhost:5000/skills/?min_frequency=24&max_frequency=25```

![image](https://user-images.githubusercontent.com/58784851/220807024-af9f9359-dafc-44b4-ac1f-69e2b4f8dda8.png)


Possible additional improvements and features
=
- It would be useful for both organizers and hackers to know the different hacker teams there are. This can be done by creating a new SQL table called "teams" with its own unique ID. Each "users" table would have a new parameter called "team_id" which references a foreign key of a particular team. This way, we can make easy SQL queries in order to get team members, projects, etc.
- There should also be an "events" table in the database. This way, hackers can make requests to possible events being held by the hackathon. In order to check which events a particular user has attended, we can implement an "events" table similar to the "skills" table I created in the challenge. Each row in "events" will include information like the user_id it refers to and the event_name they attended. Similarly to the "skills" api, we can easily get a list of events and aggregate information about them. This will let us know how many people are attending a particular event and gauge its success.
