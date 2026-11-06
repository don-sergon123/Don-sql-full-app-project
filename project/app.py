from flask import Flask, request, jsonify, session
from flask_migrate import Migrate
from models import db, bcrypt, User, Task

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'super-secret-key-change-this'

db.init_app(app)
bcrypt.init_app(app)
migrate = Migrate(app, db)


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=data.get('username'))
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()

    session['user_id'] = user.id
    return jsonify({'id': user.id, 'username': user.username}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'error': 'Invalid username or password'}), 401


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200


@app.route('/check-session', methods=['GET'])
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify({'id': user.id, 'username': user.username}), 200
    return jsonify({'error': 'Unauthorized'}), 401


@app.route('/tasks', methods=['GET'])
def get_tasks():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    pagination = Task.query.filter_by(user_id=user_id).paginate(
        page=page, per_page=per_page, error_out=False)

    return jsonify({
        'tasks': [task.to_dict() for task in pagination.items],
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page
    }), 200


@app.route('/tasks', methods=['POST'])
def create_task():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    task = Task(
        title=data.get('title'),
        description=data.get('description'),
        status=data.get('status', 'Pending'),
        priority=data.get('priority', 'Medium'),
        user_id=user_id
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201


@app.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.status = data.get('status', task.status)
    task.priority = data.get('priority', task.priority)
    db.session.commit()

    return jsonify(task.to_dict()), 200


@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    task = Task.query.filter_by(id=id, user_id=user_id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)
