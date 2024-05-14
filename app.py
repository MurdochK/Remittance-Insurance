from flask import Flask, render_template, redirect, url_for, request
from flask import Flask

# Import Square SDK components
import squareup
from squareup.apis.orders_api import OrdersApi
from squareup.configuration import Configuration
from squareup.models import CreateOrderRequest, OrderLineItem

# Initialize Flask app
app = Flask(__name__)

# Square API configuration
square_access_token = 'EAAAlzfcmZv_YiE-IO6r87tHqNHYx0Y-2boubyAGvgEbsPM4gArWkrQwSMoXufAU'
square_location_id = 'LDSS82RKX7DDH'
configuration = Configuration()
configuration.access_token = square_access_token
api_instance = OrdersApi(squareup.ApiClient(configuration))

# Function to create an order
def create_order():
    # Define line items for the order (example)
    line_items = [OrderLineItem(name='Item 1', quantity=1, base_price_money={'amount': 1000, 'currency': 'USD'})]
    
    # Construct the order request object
    create_order_request = CreateOrderRequest(location_id=square_location_id, line_items=line_items)

    # Send request to create the order
    try:
        created_order = api_instance.create_order(create_order_request)
        return created_order.order.id
    except Exception as e:
        return str(e)

# Function to update an order
def update_order(order_id, updated_order_details):
    # Send request to update the order
    try:
        updated_order = api_instance.update_order(order_id, updated_order_details)
        return "Order updated successfully"
    except Exception as e:
        return str(e)

# Function to retrieve a list of orders
def list_orders():
    # Send request to list orders
    try:
        orders = api_instance.list_orders()
        return [order.id for order in orders.orders]
    except Exception as e:
        return str(e)

# Route for creating an order
@app.route('/create_order')
def create_order_route():
    order_id = create_order()
    return f"Order created successfully with ID: {order_id}"

# Route for updating an order
@app.route('/update_order')
def update_order_route():
    order_id = 'YOUR_ORDER_ID'  # Replace with an actual order ID
    updated_order_details = CreateOrderRequest() 
    response = update_order(order_id, updated_order_details)
    return response

# Route for listing orders
@app.route('/list_orders')
def list_orders_route():
    orders = list_orders()
    return f"List of orders: {orders}"


# Dummy user data for demonstration
users = [
    {'username': 'user1', 'password': 'password1'},
    {'username': 'user2', 'password': 'password2'}
]

# Square Customers API integration
def create_customer(email, given_name, family_name):
    url = 'https://connect.squareup.com/v2/customers'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'given_name': given_name,
        'family_name': family_name,
        'email_address': email
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['customer']
    else:
        return None

# Square Catalog API integration
def create_catalog_item(name, description, price):
    url = 'https://connect.squareup.com/v2/catalog/object'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    
    # Generate a UUID for idempotency_key
    idempotency_key = str(uuid.uuid4())
    
    data = {
        'type': 'ITEM',
        'idempotency_key': idempotency_key,
        'item_data': {
            'name': name,
            'description': description,
            'variations': [{
                'type': 'FIXED_PRICING',
                'price_money': {
                    'amount': price,
                    'currency': 'USD'
                }
            }]
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['catalog_object']
    else:
        return None
        
# Square Loyalty API integration
def enroll_customer_in_loyalty_program(customer_id, loyalty_program_id):
    url = f'https://connect.squareup.com/v2/loyalty/customers/{customer_id}/enroll'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'program_id': loyalty_program_id
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        return False

def accumulate_points(customer_id, loyalty_program_id, points):
    url = f'https://connect.squareup.com/v2/loyalty/customers/{customer_id}/accumulate'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'program_id': loyalty_program_id,
        'accumulate_points': {
            'points': points
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        return False

def redeem_rewards(customer_id, loyalty_program_id, reward_id):
    url = f'https://connect.squareup.com/v2/loyalty/customers/{customer_id}/redeem'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'program_id': loyalty_program_id,
        'redeem_rewards': {
            'reward_id': reward_id
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return True
    else:
        return False

def create_loyalty_program(name, points_type):
    url = 'https://connect.squareup.com/v2/loyalty/programs'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'name': name,
        'points_type': points_type
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['loyalty_program']
    else:
        return None
        
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        given_name = request.form['given_name']
        
        # Register the user and call the create_customer function to create a customer in Square
        create_customer(email, given_name, family_name)

        print(f"Registered: Username - {username}, Password - {password}")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username and password match any user in the users list
        for user in users:
            if user['username'] == username and user['password'] == password:
                return redirect(url_for('dashboard'))
        # If no matching user found, redirect back to the login page
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Logic for displaying user dashboard
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
