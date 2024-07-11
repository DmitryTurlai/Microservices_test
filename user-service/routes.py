from flask import Blueprint, request, jsonify
from models import db, User

bp = Blueprint('routes', __name__)

@bp.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'], age=data['age'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email, 'age': user.age})

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.age = data.get('age', user.age)
    db.session.commit()
    return jsonify({'message': 'User updated successfully'})
