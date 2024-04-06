# vmbloggr

## A blogger's delight


vmbloggr is an API that serves as the backend server for a simple blog reader app. It allows users to 
* Register and login to the API
* Create blog posts
* Get a list of blog posts from the database
* View the details of each post
* Update existing blog posts
* Delete existing blog posts


### Project specifications
Within the project, the three apps worthy of note are:
1. users - Creation, authentication, update and deletion of user accounts 
2. blog - Creation, listing, update and deletion of blogs by authorised users  



## Getting Started
* Create a new directory where you would like this project stored. e.g vm-Kaizen

* Change into that new directory

```
cd vm-Kaizen
```

* Get a copy of the source code of this project into your local repository.

```
git clone https://github.com/KelvinJC/vmbloggr.git
```

* The code will be packaged in a directory named vmbloggr so change into that directory

```
cd vmbloggr
```

* To begin using the application, initiate the server by running the following command to build and run the containers in one go

```
docker compose up --build 
```
(adding the extra flag "-f docker-compose.yml" works but since we are using a default file name that is unnecessary)


### Running the server:
By default, Django apps listen on ```http://127.0.0.1:8000``` so once the server is running, 
that is the link to copy and paste into your preferred browser.<br>

To prevent clashes on port 8000, make sure no other Django app is running on localhost.


### Documentation
While the default Django DRF doc is available, the preference here is for Swagger. <br>
vmblogger relies on Swagger for documentation which can be accessed at ```http://127.0.0.1:8000/api/docs/swagger``` <br>
You can view the documentation of the API as well as interact with its endpoints (even authenticate a user!) <br>
just as you would on Postman or any other API client.

<br>
screenshot of Swagger docs here !!


### Authentication and Authorisation.

JWT authentication ensures that users are properly authenticated. 
This serves to ensure that only authors can update or delete their posts

### Database choice
This project makes use of a Postgres database which is within a separate docker container 
for persistent storage of blog posts as well as user information. 

If you require a different database, customisation is possible via the settings.py file. <br><br>

#### NOTE: 
Database credentials should not be stored in code repositories! <br>
They belong in .env files which should be kept secret and remain local to the appropriate context (e.g. dev, test or prod). 
This is a unique case to facilitate your ease in spinning up the app.

### Django Admin User
This step is not critical to the usage of the app but if you are familiar with the Django Admin UI you can make use of an already created superuser 

```
username = Admin
password = Admin
```

To access the Django Admin UI visit ```http://127.0.0.1:8000/admin```

### Automated tests. 
Tests are pretty important. To aid test-driven development, ```vmbloggr``` comes with a test suite in each app. <br>
To run all tests, navigate to the src directory and run the commands to initiate django tests<br>

```
cd src
```
then 

```
python manage.py test
```

### System design

screenshots go here!