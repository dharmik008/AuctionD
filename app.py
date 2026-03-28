"""
Car Auction CRM - Premium Edition
Luxury Car Auction Platform with Elegant Design
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from functools import wraps
from datetime import datetime, timedelta
import uuid
import json

app = Flask(__name__)
app.secret_key = 'dealerhub-premium-secret-key-2025'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# ============================================================================
# DATA STORAGE (In-Memory for Demo - Replace with Database in Production)
# ============================================================================

users = {}
bids = {}
car_bids = {}

# ============================================================================
# PREMIUM CAR COLLECTION - Enhanced with Luxury Details
# ============================================================================

CARS = {
    "car_001": {
        "id": "car_001",
        "name": "BMW M5 Competition",
        "model": "M5 CS",
        "year": 2024,
        "base_price": 9500000,
        "max_price": 13500000,
        "current_bid": 9500000,
        "description": "The ultimate driving machine reimagined. Handcrafted 4.4L V8 with 627HP, carbon fiber roof, M compound brakes, and bespoke interior with Alcantara accents.",
        "image": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80",
        "brand": "BMW M",
        "fuel": "Premium Petrol",
        "transmission": "8-Speed M Steptronic",
        "km": "8,500",
        "color": "Frozen Dark Grey",
        "engine": "4.4L V8 Twin-Turbo",
        "power": "627 hp",
        "torque": "750 Nm",
        "acceleration": "3.1 sec",
        "top_speed": "305 km/h",
        "auction_end": (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d %H:%M:%S'),
        "status": "active",
        "featured": True,
        "badge": "Featured"
    },
    "car_002": {
        "id": "car_002",
        "name": "Mercedes-AMG GT 63 S",
        "model": "GT 63 S E Performance",
        "year": 2024,
        "base_price": 10500000,
        "max_price": 15800000,
        "current_bid": 10500000,
        "description": "The fastest AMG ever. 4.0L V8 Biturbo hybrid with 843HP, 0-100 in 2.9s, AMG ceramic brakes, and Nappa leather interior with carbon fiber trim.",
        "image": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80",
        "brand": "Mercedes-AMG",
        "fuel": "Premium Petrol Hybrid",
        "transmission": "AMG SPEEDSHIFT MCT 9G",
        "km": "3,200",
        "color": "Selenite Grey Magno",
        "engine": "4.0L V8 Biturbo + Electric",
        "power": "843 hp",
        "torque": "1400 Nm",
        "acceleration": "2.9 sec",
        "top_speed": "316 km/h",
        "auction_end": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
        "status": "active",
        "featured": True,
        "badge": "Featured"
    },
    "car_003": {
        "id": "car_003",
        "name": "Porsche 911 Turbo S",
        "model": "992.2 Turbo S",
        "year": 2024,
        "base_price": 19500000,
        "max_price": 26000000,
        "current_bid": 19500000,
        "description": "The icon of performance. 3.8L flat-six with 650HP, Porsche Active Suspension Management, and exclusive Heritage interior with Pepita pattern.",
        "image": "https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=800&q=80",
        "brand": "Porsche",
        "fuel": "Premium Petrol",
        "transmission": "8-Speed PDK",
        "km": "1,200",
        "color": "GT Silver Metallic",
        "engine": "3.8L Flat-Six",
        "power": "650 hp",
        "torque": "800 Nm",
        "acceleration": "2.6 sec",
        "top_speed": "330 km/h",
        "auction_end": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d %H:%M:%S'),
        "status": "active",
        "featured": True,
        "badge": "Featured"
    },
    "car_004": {
        "id": "car_004",
        "name": "Audi RS e-tron GT",
        "model": "RS e-tron GT",
        "year": 2024,
        "base_price": 12500000,
        "max_price": 16800000,
        "current_bid": 12500000,
        "description": "The future of performance. 646HP electric powertrain, 0-100 in 3.1s, 488km range, and sustainable luxury interior with recycled materials.",
        "image": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800&q=80",
        "brand": "Audi Sport",
        "fuel": "Electric",
        "transmission": "2-Speed Automatic",
        "km": "500",
        "color": "Tactical Green",
        "engine": "Dual Electric Motors",
        "power": "646 hp",
        "torque": "830 Nm",
        "acceleration": "3.1 sec",
        "top_speed": "250 km/h",
        "auction_end": (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d %H:%M:%S'),
        "status": "active",
        "featured": False,
        "badge": "New"
    },
    "car_005": {
        "id": "car_005",
        "name": "Lamborghini Urus Performante",
        "model": "Urus Performante",
        "year": 2024,
        "base_price": 38500000,
        "max_price": 52000000,
        "current_bid": 38500000,
        "description": "The Super SUV redefined. 4.0L V8 twin-turbo with 666HP, lightweight composite materials, and exclusive Ad Personam interior with Alcantara.",
        "image": "https://images.unsplash.com/photo-1544636331-e26879cd4d9b?w=800&q=80",
        "brand": "Lamborghini",
        "fuel": "Premium Petrol",
        "transmission": "8-Speed ZF",
        "km": "800",
        "color": "Grigio Telesto",
        "engine": "4.0L V8 Twin-Turbo",
        "power": "666 hp",
        "torque": "850 Nm",
        "acceleration": "3.3 sec",
        "top_speed": "306 km/h",
        "auction_end": (datetime.now() + timedelta(days=6)).strftime('%Y-%m-%d %H:%M:%S'),
        "status": "active",
        "featured": True,
        "badge": "Featured"
    },
    "car_006": {
        "id": "car_006",
        "name": "Range Rover SV",
        "model": "SV P530 SWB",
        "year": 2024,
        "base_price": 28500000,
        "max_price": 38000000,
        "current_bid": 28500000,
        "description": "Pinnacle of British luxury. 4.4L V8 with 530HP, executive seating, SV bespoke interior, and 29-speaker Meridian音响 with active noise cancellation.",
        "image": "https://images.unsplash.com/photo-1519245160712-ceed286a8f22?w=800&q=80",
        "brand": "Range Rover",
        "fuel": "Premium Petrol",
        "transmission": "8-Speed Auto",
        "km": "2,500",
        "color": "Santorini Black",
        "engine": "4.4L V8",
        "power": "530 hp",
        "torque": "750 Nm",
        "acceleration": "4.4 sec",
        "top_speed": "261 km/h",
        "auction_end": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'),
        "status": "active",
        "featured": False,
        "badge": "Premium"
    }
}

# Initialize bid tracking
for car_id, car in CARS.items():
    car_bids[car_id] = {
        "current_bid": car["base_price"],
        "bidder": None,
        "bidder_name": None,
        "bid_count": 0,
        "history": []
    }

# Seed demo user
users['demo'] = {
    'name': 'James Anderson',
    'email': 'james@luxuryauctions.com',
    'username': 'demo',
    'password': 'demo123',
    'joined': datetime.now().strftime('%Y-%m-%d'),
    'avatar': 'JA'
}

# Sample bid history
sample_bids = [
    {'bid_id': 'bid_001', 'car_id': 'car_001', 'car_name': 'BMW M5 Competition', 'amount': 9850000, 'days_ago': 2, 'status': 'won'},
    {'bid_id': 'bid_002', 'car_id': 'car_002', 'car_name': 'Mercedes-AMG GT 63 S', 'amount': 11200000, 'days_ago': 1, 'status': 'pending'},
    {'bid_id': 'bid_003', 'car_id': 'car_003', 'car_name': 'Porsche 911 Turbo S', 'amount': 20200000, 'days_ago': 0, 'status': 'pending'}
]

for bid in sample_bids:
    timestamp = datetime.now() - timedelta(days=bid['days_ago'])
    bids[bid['bid_id']] = {
        **bid,
        'user': 'demo',
        'user_name': 'James Anderson',
        'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
    }

# ============================================================================
# AUTHENTICATION HELPERS
# ============================================================================

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            flash('Please sign in to access premium features.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def get_current_user():
    username = session.get('user')
    if username and username in users:
        return users[username]
    return None

def format_currency(value):
    """Format number as Indian currency"""
    return f"₹{value:,.0f}"

app.jinja_env.filters['currency'] = format_currency

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    """Premium landing page"""
    user = get_current_user()
    featured_cars = [car for car in CARS.values() if car.get('featured', False)][:3]
    return render_template('index.html', current_user=user, featured_cars=featured_cars)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm_password', '').strip()

        if not all([name, email, username, password, confirm]):
            flash('All fields are required.', 'error')
            return render_template('signup.html', current_user=None)

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('signup.html', current_user=None)

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('signup.html', current_user=None)

        if username in users:
            flash('Username already exists. Please choose another.', 'error')
            return render_template('signup.html', current_user=None)

        users[username] = {
            'name': name,
            'email': email,
            'username': username,
            'password': password,
            'joined': datetime.now().strftime('%Y-%m-%d'),
            'avatar': ''.join([part[0].upper() for part in name.split()[:2]])
        }

        flash('Account created successfully! Welcome to AutoBidCRM.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html', current_user=None)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        user = users.get(username)
        if user and user['password'] == password:
            session['user'] = username
            flash(f'Welcome back, {user["name"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html', current_user=None)

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    user_bids = [bid for bid in bids.values() if bid.get('user') == session['user']]
    active_cars = [car for car in CARS.values() if car.get('status') == 'active']
    
    stats = {
        'total_auctions': len(active_cars),
        'my_bids': len(user_bids),
        'active_bids': len([b for b in user_bids if b.get('status') == 'pending']),
        'won_bids': len([b for b in user_bids if b.get('status') == 'won'])
    }
    
    return render_template('dashboard.html', 
                         dealer=user, 
                         cars=active_cars[:4],
                         stats=stats,
                         current_user=user,
                         bids=user_bids)

@app.route('/auction')
@login_required
def auction():
    user = get_current_user()
    active_cars = [car for car in CARS.values() if car.get('status') == 'active']
    return render_template('auction.html', current_user=user, cars=active_cars)

@app.route('/car/<car_id>')
@login_required
def car_detail(car_id):
    car = CARS.get(car_id)
    if not car:
        flash('Vehicle not found in our collection.', 'error')
        return redirect(url_for('auction'))
    
    user = get_current_user()
    bid_info = car_bids.get(car_id, {
        "current_bid": car["base_price"],
        "bidder": None,
        "bidder_name": None,
        "bid_count": 0,
        "history": []
    })
    
    # Calculate time remaining
    auction_end = datetime.strptime(car['auction_end'], '%Y-%m-%d %H:%M:%S')
    time_remaining = auction_end - datetime.now()
    remaining_seconds = max(0, int(time_remaining.total_seconds()))
    
    evaluation = {
        'condition': 'Mint / Showroom',
        'service_history': 'Complete dealership service history',
        'accident_history': 'Zero accidents — Pristine condition',
        'ownership': 'Single owner, meticulous care',
        'warranty': 'Balance factory warranty + extended coverage',
        'rating': 4.9,
        'recommended_price': car['base_price'],
        'market_value': int(car['base_price'] * 1.08),
        'certified': True
    }
    
    return render_template('car_detail.html', 
                         current_user=user, 
                         car=car, 
                         bid_info=bid_info,
                         evaluation=evaluation,
                         remaining_seconds=remaining_seconds)

@app.route('/bidding/<car_id>')
@login_required
def bidding(car_id):
    car = CARS.get(car_id)
    if not car:
        flash('Vehicle not found.', 'error')
        return redirect(url_for('auction'))
    
    user = get_current_user()
    bid_info = car_bids.get(car_id, {
        "current_bid": car["base_price"],
        "bidder": None,
        "bidder_name": None,
        "bid_count": 0,
        "history": []
    })
    
    return render_template('bidding.html', current_user=user, car=car, bid_info=bid_info)

@app.route('/api/place-bid', methods=['POST'])
@login_required
def place_bid():
    data = request.get_json()
    car_id = data.get('car_id')
    bid_amount = data.get('bid_amount')
    
    car = CARS.get(car_id)
    if not car:
        return jsonify({'success': False, 'message': 'Vehicle not found.'}), 404
    
    try:
        bid_amount = int(bid_amount)
    except (TypeError, ValueError):
        return jsonify({'success': False, 'message': 'Invalid bid amount.'}), 400
    
    current_bid_info = car_bids.get(car_id)
    current_bid = current_bid_info['current_bid']
    max_price = car['max_price']
    
    if bid_amount <= current_bid:
        return jsonify({
            'success': False,
            'message': f'Bid must exceed current bid of ₹{current_bid:,}'
        }), 400
    
    if bid_amount > max_price:
        return jsonify({
            'success': False,
            'message': f'Bid cannot exceed maximum price of ₹{max_price:,}'
        }), 400
    
    username = session['user']
    user = users[username]
    
    # Update car bid info
    car_bids[car_id]['history'].append({
        'bidder': user['name'],
        'amount': bid_amount,
        'time': datetime.now().strftime('%H:%M:%S')
    })
    car_bids[car_id]['current_bid'] = bid_amount
    car_bids[car_id]['bidder'] = username
    car_bids[car_id]['bidder_name'] = user['name']
    car_bids[car_id]['bid_count'] += 1
    
    # Update car's current bid
    CARS[car_id]['current_bid'] = bid_amount
    
    # Save bid to history
    bid_id = str(uuid.uuid4())[:8]
    bids[bid_id] = {
        'bid_id': bid_id,
        'car_id': car_id,
        'car_name': car['name'],
        'user': username,
        'user_name': user['name'],
        'amount': bid_amount,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'pending'
    }
    
    return jsonify({
        'success': True,
        'message': f'✨ Bid of ₹{bid_amount:,} placed successfully!',
        'new_bid': bid_amount,
        'bidder': user['name'],
        'bid_count': car_bids[car_id]['bid_count']
    })

@app.route('/api/bid-info/<car_id>')
@login_required
def get_bid_info(car_id):
    bid_info = car_bids.get(car_id)
    if not bid_info:
        return jsonify({'success': False}), 404
    return jsonify({
        'success': True,
        'current_bid': bid_info['current_bid'],
        'bidder': bid_info['bidder_name'],
        'bid_count': bid_info['bid_count'],
        'history': bid_info['history'][-5:]
    })

@app.route('/bidding-history')
@login_required
def bidding_history():
    user = get_current_user()
    username = session['user']
    
    user_bids = [bid for bid in bids.values() if bid.get('user') == username]
    user_bids.sort(key=lambda x: x['timestamp'], reverse=True)
    
    return render_template('bidding_history.html', current_user=user, bids=user_bids)

@app.route('/calculator')
@login_required
def calculator():
    user = get_current_user()
    car_id = request.args.get('car_id')
    car = CARS.get(car_id) if car_id else None
    return render_template('calculator.html', current_user=user, cars=list(CARS.values()), selected_car=car)

# ============================================================================
# TEMPLATE CONTEXT PROCESSOR
# ============================================================================

@app.context_processor
def inject_globals():
    return dict(current_user=get_current_user())

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', current_user=get_current_user()), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html', current_user=get_current_user()), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)