from sqlalchemy.sql import text
from werkzeug.security import generate_password_hash
from db import db

def get_messages():
    sql = "SELECT id, content, sent_by, created_at FROM messages ORDER BY id DESC"
    result = db.session.execute(text(sql))
    msgs = result.fetchall()
    return msgs

def register_new(username, password):
    password_hash = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(text(sql), {"username":username, "password":password_hash})
        db.session.commit()
    except:
        return False
    return username, password

def fetch_user(username):
    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(text(sql), {"username":username})
    return result.fetchone()

def create_message(content, sent_by):
    sql = "INSERT INTO messages (content, sent_by, created_at) VALUES (:content, :sent_by, NOW()) RETURNING id"
    db.session.execute(text(sql), {"content":content, "sent_by":sent_by})
    db.session.commit()

def view_resto(id):
    sql = "SELECT name, location FROM restos WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    resto = result.fetchone()
    name = resto[0]
    location = resto[1]
    sql = "SELECT * FROM reviews WHERE resto_id=:id"
    result = db.session.execute(text(sql), {"id":id})
    reviews = result.fetchall()
    return [name, location, reviews]

def fetch_resto_name(id):
    sql = "SELECT name FROM restos WHERE id=:id"
    result = db.session.execute(text(sql), {"id":id})
    return result.fetchone()[0]

def create_review(id, content, username):
    sql = "INSERT INTO reviews (resto_id, content, sent_at, sent_by, visible) VALUES (:resto_id, :content, NOW(), :username, TRUE) RETURNING id"
    db.session.execute(text(sql), {"resto_id":id, "content":content, "username":username})
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
