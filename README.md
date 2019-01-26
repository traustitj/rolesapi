# Roles API

* [Introduction](#introduction)
* [Setup](#setup)
* [Alternative setup](#alternative-setup)
* [Examples](#examples)
* [Improvements Todo](#improvements-todo)

## Introduction
Roles API is a system for maintaining role based access to systems. This can help to keep developers and testers with all their settings and access rights.

## Setup
The system is made to run on Python 3.6 and tested as such.
Once the system is downloaded, the maintainer needs to run the following commands (for Linux)
* First run the python package manager, pip, to install required libraries. It is recommended to run the service either in Docker or Virtual environment (see #alternative-setup)
    * pip install -e requirements
    * python setup.py
        * Beware that this command will delete all data from the database if it exists
    ### Now you can run the service
    * python server.py
        * This will run the system using port 5000

## Alternative Setup
### Virtual environment
The system can be run either in a virtual environment using python virtualenv command. The setup procedure is the same but first you must make the environment and then activate it.
    #### virtualenv --python=<path to yor python command>/python env (will be named env)
    * (Linux) source env/bin/activate
    * (Windows) \env\Scripts\Activate.bat
    * Now run the commands like above
        * pip install -r requirements
        * python setup.py
        Then Start the system
        * python server.py

    #### Docker
    The service is perfectly suited to run inside a docker image. Docker file is included in the project. An example command to build your image is like this
    * docker build -t roleapi .
    This will build your images. If you are familiar with docker, you might want to seperate the base python system and use that as a base image instead of ubuntu:18.04. You can also use smaller base images, make sure you have the tools you need to run the project.

    Example to run the service and export the port locally to 5000 is like this
    * docker run -d --name rolenode1 -p 5000:5000 roleapi

    This should have your service up and running.

## Examples
The system relies on user information from 3rd party server but will cache each user for 5 minutes and then refetch. All successful calls will give you back JSON data.

    * To fetch a user
        * curl -X GET http://localhost:5000/user/1
            This would fetch user with userid 1. Example output would be like

            {
                "username": "superdog",
                "user_id": 1,
                "name": "Ava Nassau",
                "roles": [],
                "created": 1548497274.237531
            }
    * To list all possible roles
        * curl -X GET http://localhost:5000/
            The output would look like
            [
                {
                    "users": [],
                    "permanent": 1, 
                    "name": "developer",
                    "role_id": 1
                },
                {
                    "users": [],
                    "permanent": 1,
                    "name": "Product Owner",
                    "role_id": 2
                },
                {
                    "users": [],
                    "permanent": 1,
                    "name": "Tester",
                    "role_id": 3
                }
            ]
        These 3 ROLES are default roles and these roles can not be deleted

    * To add a role
        * curl -X PUT -H "content-type: application/json" -d '{"name": "example"}' http://localhost:5000/role
            The output would look like
            {
                "role_id": 30,
                "name": "EXAMPLE",
                "permanent": 0,
                "users": []
            }

    * To add user to role (example uses userid 1 and role id 2)
        * curl -X GET http://localhost:5000/add_user_to_role/<userid>/<roleid>
        * i.e. curl -X GET http://localhost:5000/add_user_to_role/1/2
        The output would be all information on the role with the user added

    * To remove a user from a role
        * curl -X DELETE http://localhost:5000/remove_user_from_role/<userid>/<roleid>
        * i.e. curl -X DELETE http://localhost:5000/remove_user_from_role/1/2
        The output would reflect the current state of the group

    * To remove the role
        * curl -X DELETE http://localhost:5000/remove_role/<roleid>
        * i.e. curl -X DELETE http://localhost:5000/remove_role/2

## Improvements Todo
There are a lot of improvements possible
* Like make a config system with the path to the 3rd party service for users and a possibility to set the cache time value and change it while the system is running which would be useful to make sure the system fetches fresh set of users.
* It is simple to change database, just overwrite the database object.
* Investigate if perhaps Redis would not be better suited as a database for the system
* With redis, other systems that rely on this system could subscrible to changes with a PUB-SUB interface
* See if it is possible to run this system and others that give it information and use the information here could be better off using a shared data store like firebase or a cloud database.
* The possibilities are endless
