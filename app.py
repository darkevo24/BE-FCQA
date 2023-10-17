from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "sqlite:///users.db"  # Use SQLite for simplicity
db = SQLAlchemy(app)

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


# Define a User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    firstName = db.Column(db.String(80), nullable=False)
    lastName = db.Column(db.String(80), nullable=False)

    def __init__(self, username, firstName, lastName):
        self.username = username
        self.firstName = firstName
        self.lastName = lastName


# Set up an application context
with app.app_context():
    # Create the database and tables
    db.create_all()


# Create a new user
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_username = data["username"]

    # Check if the username already exists
    if User.query.filter_by(username=new_username).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(
        username=data["username"],
        firstName=data["firstName"],
        lastName=data["lastName"],
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"})


# Retrieve all users
@app.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    user_list = [
        {
            "username": user.username,
            "firstName": user.firstName,
            "lastName": user.lastName,
        }
        for user in users
    ]
    return jsonify(user_list)


# Update an existing user
@app.route("/api/users/<username>", methods=["PUT"])
def update_user(username):
    data = request.get_json()
    user = User.query.filter_by(username=username).first()
    if user:
        user.firstName = data["firstName"]
        user.lastName = data["lastName"]
        db.session.commit()
        return jsonify({"message": "User updated successfully"})
    return jsonify({"message": "User not found"}, 404)


# Delete an existing user
@app.route("/api/users/<username>", methods=["DELETE"])
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted successfully"})
    return jsonify({"message": "User not found"}, 404)


if __name__ == "__main__":
    app.run(debug=True)
