from sqlalchemy.sql import text
# from werkzeug.security import generate_password_hash
from db import db

def get_messages():
    sql = "SELECT id, content, sent_by, created_at FROM messages ORDER BY id DESC"
    result = db.session.execute(text(sql))
    msgs = result.fetchall()
    return msgs

def register_new(username, password):
    # password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password, admin) VALUES (:username, :password, FALSE)"
        # db.session.execute(text(sql), {"username":username, "password":password_hash})
        db.session.execute(text(sql), {"username":username, "password":password})
        db.session.commit()
    except:
        return False
    return username, password

def fetch_user(username):
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    return result.fetchone()

def create_message(content, sent_by):
    sql = "INSERT INTO messages (content, sent_by, created_at) VALUES (:content, :sent_by, NOW()) RETURNING id"
    db.session.execute(text(sql), {"content":content, "sent_by":sent_by})
    db.session.commit()

def fetch_messages(query):
    sql = "SELECT * FROM messages WHERE lower(content) LIKE lower(:query)"
    result = db.session.execute(text(sql), {"query":"%"+query+"%"})
    return result.fetchall()

def fetch_messages_by_user(sent_by):
    sql = "SELECT * FROM messages WHERE sent_by=:sent_by"
    result = db.session.execute(text(sql), {"sent_by":sent_by})
    return result.fetchall()

def delete_message(id):
    sql = "DELETE FROM messages WHERE messages.id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()

def get_users_by_query(query):
    sql = "SELECT * FROM users WHERE lower(username) LIKE lower(:query)"
    users = db.session.execute(text(sql), {"query":"%"+query+"%"})
    return users.fetchall()

def delete_user(id):
    sql = "DELETE FROM users WHERE users.id=:id"
    db.session.execute(text(sql), {"id":id})
    db.session.commit()