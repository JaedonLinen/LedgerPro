from flask import request, jsonify
from config import app, db
from models import users

@app.route("/users", methods=["GET"])
def get_users():
    all_users = users.query.all()
    json_users = list(map(lambda x: x.to_json(), all_users))
    return jsonify({"allUsers": json_users})


@app.route("/create_user", methods=["POST"])
def create_user():
    first_name = request.json.get("firstName")
    last_name = request.json.get("lastName")
    username = request.json.get("username")
    email = request.json.get("email")
    password_hash = request.json.get("passwordHash")
    role = request.json.get("role")
    date_of_birth = request.json.get("dateOfBirth")

    if not first_name or not last_name or not username or not email or not password_hash or not role or not date_of_birth :
        return (jsonify({"message": "You must include all fields"}), 400)
    
    new_user =  users(first_name=first_name, last_name=last_name, username=username, email=email, password_hash=password_hash, role=role, date_of_birth=date_of_birth)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
    return jsonify({"message": "User created!"}), 201

@app.route("/update_user/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    user = users.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    data = request.json
    user.first_name = data.get("firstName", user.first_name)
    user.last_name = data.get("lastName", user.last_name)
    user.username = data.get("username", user.username)
    user.email = data.get("email", user.email)
    user.password_hash = data.get("passwordHash", user.password_hash)
    user.role = data.get("role", user.role)
    user.date_of_birth = data.get("dateOfBirth", user.date_of_birth)

    db.session.commit()

    if not user:
        return jsonify({"message": "User updated!"}), 200

@app.route("/delete_user/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = users.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404
    
    db.session.delete(user)
    db.session.commit()

    if not user:
        return jsonify({"message": "User deleted!"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

