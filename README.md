# REST API

A REST API for a grocery store.

### Tech Stacks:


1. Python 3.8 - Scripting Language for Backend
2. Django 3.2 - Framework for Backend
3. SQLite3 - To store user information


### ER diagram:

The ER Diagram for this API can be found here.  
https://drawsql.app/society-management/diagrams/grocery-store#

### How to Reproduce:

To reproduce this code you need to go through the following steps:

1. Creating a Virtual Environment:(OPTIONAL)  
   Write the following commands in your command line. 
   1. pip install virtualenv 
   2. python3 -m virtualenv venv_name 
   3. source venv_name/bin/activate
   4. pip install Django
   5. pip install djangorestframework

2. Setting up MySQL: (OPTIONAL if you are using sqlite)
    1. Check in grocery_store/grocery_store.settings.py

3. Setting up Django:  
   Enter the following commands in your command line. 
   1. python3 manage.py makemigrations
   2. python3 manage.py migrate
   3. python3 manage.py createsuperuser
   4. python3 manage.py create_groups
   5. python3 manage.py runserver

4. To check the Backend you can go to:
    1. 127.0.0.1:8000/admin/
    2. 127.0.0.1:8000/api/slug  
    The appropriate slug can be found in grocery_store/api/urls.py or in the Postman Workspace

### Assumptions

1. User is identified by mobile number.
2. Grocery Items do not have taxes.
3. Bills can not be deleted. (Unethical to delete the bills)
4. Grocery Items are generally not identified by code, rather identified by name


### Features

1. As soon as a bill is generated, the corresponding items are subtracted from the inventory.
2. In case a bill is updated, the corresponding item quantity will also be updated.
3. Owner can segregate his staff into groups and give specific permissions.
4. Pagination provided. You can control pagination in grocery_store/grocery_store.settings.py
5. Added Search and Filtering to Item and Account
6. Total Price of the bill is adjusted according to the items.

### Postman Workspace
https://www.postman.com/technical-geologist-31086137/workspace/grocery-store

