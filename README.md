# Cyber Security Base Project 1

This repository consists of a vulnerable messaging application with five different cyber security flaws. I opted to use flask when creating the app, since I have much better knowledge over that than Django that was used in the course material.

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

7. Now the application starts at localhost:5000 by using this command:
```bash
flask run
```
