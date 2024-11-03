CREATE TABLE messages (id SERIAL PRIMARY KEY, content TEXT, sent_by TEXT, created_at TIMESTAMP);
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT UNIQUE, password TEXT, admin BOOLEAN);
INSERT INTO users (username, password, admin) VALUES ('admin', 'admin', true);