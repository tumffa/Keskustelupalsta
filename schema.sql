CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT, admin BOOLEAN);
CREATE TABLE topics (id SERIAL PRIMARY KEY, name TEXT, description TEXT DEFAULT '', owner_id INTEGER);
INSERT INTO topics (name, owner_id) VALUES ('General', 0);
CREATE TABLE posts (id SERIAL PRIMARY KEY, topic_id INTEGER REFERENCES topics ON DELETE CASCADE, user_id INTEGER REFERENCES users ON DELETE CASCADE, username TEXT, name TEXT, description TEXT DEFAULT '', date TEXT);
CREATE TABLE comments (id SERIAL PRIMARY KEY, post_id INTEGER REFERENCES posts ON DELETE CASCADE, user_id INTEGER REFERENCES users ON DELETE CASCADE, username TEXT, description TEXT DEFAULT '', date TEXT);