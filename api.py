from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "database.db"

# Function to connect to the database
def connect_to_database():
    return sqlite3.connect(DATABASE, check_same_thread=False)

# Users Endpoints

@app.route("/users", methods=["GET"])
def get_all_users():
    connection = connect_to_database()
    users = []
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor.fetchall():
        user = {
            "id": row[0],
            "username": row[1],
            "admin": row[3]
        }
        users.append(user)
    connection.close()
    return jsonify(users)

@app.route("/users/<name>", methods=["GET"])
def get_user_by_name(name):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (name,))
    user = cursor.fetchone()
    connection.close()
    if user:
        user_info = {
            "id": user[0],
            "username": user[1],
            "admin": user[3]
        }
        return jsonify(user_info)
    else:
        return jsonify({"message": "User not found"}), 404

# Posts Endpoints

@app.route("/posts", methods=["GET"])
def get_all_posts():
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts")
    posts = []
    for row in cursor.fetchall():
        post = {
            "post_id": row[0],
            "user_id": row[1],
            "description": row[3],
            "image_data": row[4],
            "image_ext": row[5],
            "date": row[2],
        }
        posts.append(post)
    connection.close()
    return jsonify(posts)

@app.route("/users/<name>/posts", methods=["GET"])
def get_posts_by_username(name):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM posts WHERE user_id=(SELECT id FROM users WHERE username=?)", (name,))
    posts = []
    for row in cursor.fetchall():
        post = {
            "post_id": row[0],
            "user_id": row[1],
            "description": row[3],
            "image_data": row[4],
            "image_ext": row[5],
            "date": row[2],
        }
        posts.append(post)
    connection.close()
    return jsonify(posts)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
