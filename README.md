# About Project
###### This project is a web application written in python Flask Framework.
###### The application uses MySQL database. the database is included in the project as cyberdb.sql
###### In this Flask application different Security Measures are taken , ie XSS Protection, CSRF Protection, SQL Injection, Password strength, hashing/salting of password,  Sessions Security, Access Control Checks etc 
##### Project Setup
###### Download this project in your computer and extract!
##### Database
###### Create a database in Xampp named cyberdb, select the database you just created, at the Top menu click on import and browse the cyberdb.sql(Found inside the downloaded folder)
###### Once you browse the cyberdb.sql click on Go. The tables register and products_table will be loaded in your database.

#### Pycharm Project SetUp
###### The Pycharm project includes the templates, static and app.py
###### Create a pycharm project and put the above folders(templates, static) and app.py in the new project.
###### In your project install the required packages i.e flask, pymysql.

###### Once setup, you are ready to go.
#### Routes
###### The app includes several routes i.e /register    /login      /sell    /buy    /checkout  /logout   where each route has its own logic.

##### /register Route
###### This route registers users of the system to the database, it includes password strength checks(Hard to guess), password re enter feature, HTM escaping(to stop XSS) and password hashing and salting(Hard to guess), also uses prepared statements in SQL to control SQL Injection

##### /Login Route
###### This route includes login logic verifying hasked/salted password from the database, also uses prepared statements in SQL to control SQL Injection, creates user session and role  i.e admin or user.

##### /sell Route
###### This routes allows ONLY ADMIN to post or sell, includes HTML escaping(to stop XSS) , also uses prepared statements in SQL to control SQL Injection
###### This routes includes Access Control Checks, only admin can view this route. see line 75

##### /buy Route
###### This route displays products for buying, HTM escaping(to stop XSS) and password hashing and salting(Hard to guess), also uses prepared statements in SQL to control SQL Injection
###### normal users and admin can view.

##### /register Route
###### This is a logout route to clear sessions set earlier in login route.

