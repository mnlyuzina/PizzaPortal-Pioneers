import connexion
import requests
from flask import Flask, jsonify, request, render_template
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import bcrypt

#app = connexion.App(__name__, specification_dir="./")

app = Flask(__name__)
# app.add_api("swagger.yml")
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

users = []

pizzas = [
    {'id': 1, 'name': 'Margherita', 'description': 'Tomato sauce, mozzarella, and basil', 'price': 9.99},
    {'id': 2, 'name': 'Pepperoni', 'description': 'Tomato sauce, mozzarella, and pepperoni', 'price': 11.99},
    {'id': 3, 'name': 'Veggie', 'description': 'Tomato sauce, mozzarella, mushrooms, peppers, and onions', 'price': 10.99}
]

orders = []

@app.route("/")
def home():
    return render_template("registration.html")

# User authentication routes
@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if any(user['email'] == email for user in users):
        return jsonify({'error': 'Email already exists'}), 400
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {'id': len(users) + 1, 'username': username, 'email': email, 'password': hashed_password.decode('utf-8')}
    users.append(user)
    return jsonify({'id': user['id'], 'username': user['username'], 'email': user['email']}), 201

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = next((user for user in users if user['email'] == email), None)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        access_token = create_access_token(identity=user['id'])
        return jsonify({'token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401
    
# Pizza routes
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    return jsonify(pizzas), 200

# Order routes
@app.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    pizza_ids = [item['id'] for item in data['pizzas']]
    customer = data['customer']
    user_id = get_jwt_identity()

    order = {
        'id': len(orders) + 1,
        'pizzas': [{'id': pizza['id'], 'name': pizza['name'], 'quantity': next(item['quantity'] for item in data['pizzas'] if item['id'] == pizza['id'])} for pizza in pizzas if pizza['id'] in pizza_ids],
        'customer': customer,
        'user_id': user_id,
        'total': sum(pizza['price'] * next(item['quantity'] for item in data['pizzas'] if item['id'] == pizza['id']) for pizza in pizzas if pizza['id'] in pizza_ids),
        'status': 'Pending'
    }
    orders.append(order)
    return jsonify(order), 201

@app.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = get_jwt_identity()
    order = next((order for order in orders if order['id'] == order_id and order['user_id'] == user_id), None)
    if order:
        return jsonify(order), 200
    else:
        return jsonify({'error': 'Order not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/')
# def home():
#     return render_template("registration.html")




# if __name__ == '__main__':

#     app.run("app:app",host="127.0.1.0", port=8000, reload=True)