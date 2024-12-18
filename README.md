# Cyber Security Base Project 1

**Note!** There was a typo in the Cryptographic Failures link. The correct one is https://github.com/hcaatu/csb-project1/blob/main/db_access.py#L20

This repository consists of a vulnerable messaging application with five different cyber security flaws. I opted to use Flask when creating the app, since I have much better knowledge over that than Django that was used in the course material. The app features user registration and login, adding messages and a separate admin control panel.

The application run locally with a local database, so no actual data is leaked online because of the security flaws.

### Install instructions

1. In the terminal, clone the repository locally:
```bash
git clone https://github.com/hcaatu/csb-project1
```

2. Move to correct directory:
```bash
cd csb-project1
```

3. Installing PostgresSQL:
- on Linux use [this installation script](https://github.com/hy-tsoha/local-pg)
- on Windows download the installation package directly from the [Postgres website](https://www.postgresql.org/download/)
- on Mac the easiest way is to use [Postgres.app](https://postgresapp.com/)

4. Create a new .env file
```bash
touch .env
```
Initialize the .env file with the following lines:


DATABASE_URL=< local address of the database >

SECRET_KEY=< 32-character hexadecimal secret key >


where the actual variables are inside tags. 

If Postgres was installed using the Linux script, use postgresql+psycopg2:// as the local address. Otherwise, use postgresql:///user where 'user' is the name of the database that shows up when opening the PostgreSQL interpreter.

The secret key is easily created in the root directory with the following command:
```bash
python3 secret.py
```

5. Activate a virtual environment and install the requirements using these commands:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

6. Define the database schema with the following command:
```bash
psql < schema.sql
```

7. Now the application starts (by default at localhost:5000) by using this command:
```bash
flask run
```

# Essay

I am using the OWASP 2021 Top 10 list. [1]

## Cryptographic Failures:
https://github.com/hcaatu/csb-project1/blob/main/db_access.py#L20

The module db_access.py is responsible for storing and fetching data from the database when specific HTTP requests are made. In this instance, the password submitted in the account registration form is stored in the database as plaintext. This leaves sensitive data vulnerable to data leaks. As we come to notice, attacks such as SQL injection can be used to extract sensitive data that wouldn’t ever be even displayed on the website and thus cryptography takes a big role in keeping our data safe. I’ve implemented a fix in practice that is commented on the code, since there exists such an easy fix.

Instead, sensitive data such as passwords must be hashed, i.e. turning the plaintext algorithmically into ciphertext. [2] This way, even if data leaks were to happen, the possible attacker is unable to reverse the password hashing into a readable format. Furthermore, when the correct password checks are made during logins, the password submitted during login is hashed each time and compared to the hashed password in the database. In addition to the server side fix, the browser side fix is presented in:

https://github.com/hcaatu/csb-project1/blob/main/routes.py#L55

During the password check the same hashing algorithm is used in the login handler function that was used in the database storing function.


## Identification and Authentication Failures:
https://github.com/hcaatu/csb-project1/blob/main/templates/register.html#L23

This flaw consists of permitting registration of new accounts with weak passwords. Common passwords are easily guessed with lists of the most common passwords and short ones can be brute forced in seconds. For exapmle, the application base includes a user with credentials admin/admin, where the password can be cracked in just 0.03 seconds by brute force. [3] The application doesn’t provide checks against automated attacks, like trying multiple different passwords in rapid succession. This leaves the door open for malicious users.

The pinpointed location is at the browser side HTML text. I’ve included this location, since there are HTML validators such as “minlength” that require the typed password to be at least the specified amount of characters long. However, the browser side validation checks are rarely secure enough. A malicious user could also probe the server and make a POST call directly to the registration handler URL with a password that is shorter than the browser validation check lets it be and bypass the validation this way. Considering this, password validation should also be done at the client side when storing it in the database. Since there are multiple possible fixes, I haven’t implemented one in code but will explain briefly what can be done. For instance, the function that handles saving the password in the database could raise an exception, when the password doesn’t meet the validation criteria. Login attempts could be delayed or even hard limited to a certain point in order to prevent brute force attacks, and implementing a password recovery feature if the person signing in has actually forgotten their credentials. Also, two-factor authentication has become common nowadays considering its ease of use with mobile apps that provide an access token only for the user’s eyes.


## Broken Access Control:
https://github.com/hcaatu/csb-project1/blob/main/routes.py#L80
https://github.com/hcaatu/csb-project1/blob/main/templates/admin.html

This is a major security flaw that permits unauthorized access to non-admin roles viewing the page. I’ve implemented an admin control panel page for that only the developer or administrator should have access to. By failing to check if a user is A) logged in and B) has the privilege to view the administrator page, any common user can view the page. By modifying the URL in a predictable manner, as in specifying the route to /admin_page, any user has access to sensitive information and can destroy the data from the database. It is also a questionable design choice to display all user information on the admin page. Even with hashed passwords, there should not be a way to display passwords of all users since there exists the risk of the sensitive data leak.

This flaw can be fixed by multiple ways. A secure method is to implement an admin privilege check to the server. When requesting the page with a GET request, the server would check for admin privileges and if lacking, should the server respond with a 403 Forbidden status code. This way any unauthorized users can’t access the page even by tampering with the URL. Second, some privilege checks may be done in HTML code for extra security, as in the following line of code:

https://github.com/hcaatu/csb-project1/blob/main/templates/layout.html#L24

In Flask, the variable “session” is used to store various information about the state of the application, such as whether the user is an administrator or not. In addition to making the admin page more secure, deleting user data, messages or credentials in this case, should enforce a double-check, such as re-typing the admin password or performing two-factor authentication on the user. Submitting the POST request of the data deletion must have client side checks on wheter the user is authorized to do so.


## Security Logging and Monitoring Failures:
https://github.com/hcaatu/csb-project1/blob/main/templates/layout.html#L41

Invalid logins are only logged to the user’s index page. On a failed login authentication, the “session” updates with invalid_user to true, which in turn displays an error message. However, invalid logins aren’t logged in the client at all. This prevents the ability to detect any suspicious or malicious activity. If this application was in production and the server was online, any attack attempts or breaches could not be detected by administrators. High-value transactions, in this context deleting user data should also be logged thoroughly. If a malicious user is able to destroy all data, it would go unnoticed.

An external logger middleware is a consistent way to get enough server side information of the requests sent. We can implement our own logger in a separate module that takes in all requests and extracts information such as IP addresses and payloads. By default, Flask displays IP addresses of all requests. This default feature is enough to rule out any possible attackers from compromising data by blocking specific addresses. This process however should be automated, so that when a threshold of, for example, login attempts is surpassed, an IP address gets blocked.

## Injection:
https://github.com/hcaatu/csb-project1/blob/main/db_access.py#L38

Injection is a type of flaw where an attacker is able to run arbitrary code on a server or execute a script. Usually this is possible due to the lack of filtering or sanitizing incoming data. In this particular example pinpointed, some hostile code may be directly concatenated to the SQL command string that is then executed. Even worse, the client doesn’t provide any filtering whatsoever over the search query string.

Filtering can be implemented by hard limiting for example a search query length, or limiting the query to just a few words. This way most SQL and JavaScript injections that use multiple lines of code are ruled out. Sanitization is even more effective, since SQLAlchemy, the database access tool the application uses, offers a way to convert any variable that is inserted into an SQL command to be treated as a string and not part of the code. This fix is shown just below the pinpointed flaw, commented out.


### References:
1. https://owasp.org/www-project-top-ten/
2. https://stytch.com/blog/what-is-password-hashing/
3. https://www.passwordmonster.com/
