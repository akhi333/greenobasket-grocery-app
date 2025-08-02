from flask import Flask, jsonify, request, render_template_string, send_from_directory, session, redirect, url_for
from flask_cors import CORS
import json
import uuid
from datetime import datetime
import os
import hashlib
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='../static', static_url_path='/static')
app.secret_key = 'greenobasket_admin_secret_key_2024'  # Change this in production
CORS(app)  # Enable CORS for frontend-backend communication

# Admin credentials (in production, use a proper authentication system)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "greenbasket123"  # Change this in production

# In-memory storage (in production, use a database)
admin_notifications = []  # Store admin notifications
user_notifications = {}  # Store user notifications by mobile number: {mobile: [notifications]}

# User authentication storage
users_db = {}  # {mobile_number: {password: str, name: str, address: str, email: str, created_at: datetime}}
user_sessions = {}  # {session_token: mobile_number}

# OTP storage for forgot password
otp_storage = {}  # {mobile_or_email: {otp: str, expires_at: datetime, type: 'mobile'|'email'}}

# In-memory database for products (extended with quantity types)
products_db = {
    "1": {
        "id": "1",
        "name": "Organic Bananas",
        "price": 60,
        "category": "Fruits",
        "image": "/static/images/products/fruits/small_banana.jpg",
        "description": "Fresh organic bananas, rich in potassium",
        "weight": "1kg",
        "stock": 50,
        "visible": True,
        "quantity_type": "grams",  # New field: "grams", "pieces", "liters"
        "min_quantity": 250,       # Minimum quantity for this type
        "max_quantity": 5000       # Maximum quantity for this type
    },
    "2": {
        "id": "2",
        "name": "Fresh Apples",
        "price": 120,
        "category": "Fruits",
        "image": "/static/images/products/fruits/apples.jpg",
        "description": "Crispy red apples from Kashmir",
        "weight": "1kg",
        "stock": 30,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 3000
    },
    "3": {
        "id": "3",
        "name": "Alphonso Mangoes",
        "price": 200,
        "category": "Fruits",
        "image": "/static/images/products/fruits/Mango_1.jpg",
        "description": "Sweet Alphonso mangoes from Maharashtra",
        "weight": "1kg",
        "stock": 25,
        "visible": True,
        "quantity_type": "pieces",  # Sold by pieces
        "min_quantity": 1,
        "max_quantity": 12
    },
    "4": {
        "id": "4",
        "name": "Fresh Grapes",
        "price": 80,
        "category": "Fruits",
        "image": "/static/images/products/fruits/Grapes.jpg",
        "description": "Sweet green grapes",
        "weight": "500g",
        "stock": 40,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 2000
    },
    "5": {
        "id": "5",
        "name": "Pomegranate",
        "price": 150,
        "category": "Fruits",
        "image": "/static/images/products/fruits/Pomegrenate.jpg",
        "description": "Fresh red pomegranate",
        "weight": "1kg",
        "stock": 20,
        "visible": True,
        "quantity_type": "pieces",
        "min_quantity": 1,
        "max_quantity": 6
    },
    "6": {
        "id": "6",
        "name": "Kesar Mangoes",
        "price": 300,
        "category": "Fruits",
        "image": "/static/images/products/fruits/KESAR-Magoes.webp",
        "description": "Premium Kesar mangoes",
        "weight": "1kg",
        "stock": 15,
        "visible": True,
        "quantity_type": "pieces",
        "min_quantity": 1,
        "max_quantity": 8
    },
    "7": {
        "id": "7",
        "name": "Fresh Papaya",
        "price": 40,
        "category": "Fruits",
        "image": "/static/images/products/fruits/papaya.jpg",
        "description": "Sweet ripe papaya",
        "weight": "1kg",
        "stock": 35,
        "visible": True,
        "quantity_type": "pieces",
        "min_quantity": 1,
        "max_quantity": 3
    },
    "8": {
        "id": "8",
        "name": "Fresh Guava",
        "price": 50,
        "category": "Fruits",
        "image": "/static/images/products/fruits/Guava.jpg",
        "description": "Sweet guava fruit",
        "weight": "1kg",
        "stock": 30,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 2000
    },
    "9": {
        "id": "9",
        "name": "Fresh Tomatoes",
        "price": 30,
        "category": "Vegetables",
        "image": "/static/images/products/vegetables/Tomato.avif",
        "description": "Fresh red tomatoes",
        "weight": "1kg",
        "stock": 60,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 5000
    },
    "10": {
        "id": "10",
        "name": "Organic Spinach",
        "price": 25,
        "category": "Leafy Vegetables",
        "image": "/static/images/products/leafy-vegetables/spinach.avif",
        "description": "Fresh organic spinach leaves",
        "weight": "250g",
        "stock": 40,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 1000
    },
    "11": {
        "id": "11",
        "name": "Fresh Carrots",
        "price": 35,
        "category": "Vegetables",
        "image": "/static/images/products/vegetables/Carrot.jpeg",
        "description": "Fresh orange carrots",
        "weight": "1kg",
        "stock": 50,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 3000
    },
    "12": {
        "id": "12",
        "name": "Red Onions",
        "price": 25,
        "category": "Vegetables",
        "image": "/static/images/products/vegetables/Onion.avif",
        "description": "Fresh red onions",
        "weight": "1kg",
        "stock": 80,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 500,
        "max_quantity": 5000
    },
    "13": {
        "id": "13",
        "name": "Fresh Potatoes",
        "price": 20,
        "category": "Vegetables",
        "image": "/static/images/products/vegetables/Potato.avif",
        "description": "Fresh potatoes",
        "weight": "1kg",
        "stock": 100,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 500,
        "max_quantity": 10000
    },
    "14": {
        "id": "14",
        "name": "Fresh Ginger",
        "price": 120,
        "category": "Vegetables",
        "image": "/static/images/products/vegetables/Ginger.avif",
        "description": "Fresh ginger root",
        "weight": "250g",
        "stock": 30,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 100,
        "max_quantity": 1000
    },
    "15": {
        "id": "15",
        "name": "Fresh Garlic",
        "price": 180,
        "category": "Vegetables",
        "image": "/static/images/products/vegetables/Garlic.jpg",
        "description": "Fresh garlic bulbs",
        "weight": "250g",
        "stock": 25,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 100,
        "max_quantity": 1000
    },
    "16": {
        "id": "16",
        "name": "Turmeric Root",
        "price": 200,
        "category": "Spices",
        "image": "/static/images/products/spices/Turmeric_root.webp",
        "description": "Fresh turmeric root",
        "weight": "250g",
        "stock": 20,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 100,
        "max_quantity": 1000
    },
    "17": {
        "id": "17",
        "name": "Fresh Brinjal",
        "price": 35,
        "category": "Vegetables",
        "image": "/static/images/products/vegetables/Brinjal.jpg",
        "description": "Fresh purple brinjal",
        "weight": "1kg",
        "stock": 35,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 2000
    },
    "18": {
        "id": "18",
        "name": "Black Pepper",
        "price": 800,
        "category": "Spices",
        "image": "/static/images/products/spices/BlackPepper - Miriyalu.jpg",
        "description": "Premium black pepper",
        "weight": "100g",
        "stock": 15,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 50,
        "max_quantity": 500
    },
    "19": {
        "id": "19",
        "name": "Green Cardamom",
        "price": 1500,
        "category": "Spices",
        "image": "/static/images/products/spices/Cardamom-Elachi.jpg",
        "description": "Premium green cardamom",
        "weight": "50g",
        "stock": 10,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 25,
        "max_quantity": 250
    },
    "20": {
        "id": "20",
        "name": "Cinnamon Sticks",
        "price": 400,
        "category": "Spices",
        "image": "/static/images/products/spices/Cinamon-DlachamChekka.jpg",
        "description": "Premium cinnamon sticks",
        "weight": "100g",
        "stock": 12,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 50,
        "max_quantity": 500
    },
    "21": {
        "id": "21",
        "name": "Chana Dal",
        "price": 90,
        "category": "Pulses",
        "image": "/static/images/products/pulses/Chenadal.jpeg",
        "description": "Premium chana dal",
        "weight": "1kg",
        "stock": 40,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 500,
        "max_quantity": 5000
    },
    "22": {
        "id": "22",
        "name": "Red Kidney Beans",
        "price": 120,
        "category": "Pulses",
        "image": "/static/images/products/pulses/kidney-beans-1296x728-feature.jpg",
        "description": "Premium red kidney beans",
        "weight": "1kg",
        "stock": 25,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 500,
        "max_quantity": 5000
    },
    "23": {
        "id": "23",
        "name": "Finger Millet",
        "price": 150,
        "category": "Millets",
        "image": "/static/images/products/millets/fingermillet.jpg",
        "description": "Organic finger millet",
        "weight": "1kg",
        "stock": 20,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 500,
        "max_quantity": 5000
    },
    "24": {
        "id": "24",
        "name": "Pearl Millet",
        "price": 100,
        "category": "Millets",
        "image": "/static/images/products/millets/PearMillet-Sajjalu.jpg",
        "description": "Organic pearl millet",
        "weight": "1kg",
        "stock": 18,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 500,
        "max_quantity": 5000
    },
    "25": {
        "id": "25",
        "name": "Fresh Coriander",
        "price": 20,
        "category": "Leafy Vegetables",
        "image": "/static/images/products/leafy-vegetables/Kothimeera or Coriander Leaves.png",
        "description": "Fresh coriander leaves",
        "weight": "100g",
        "stock": 50,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 100,
        "max_quantity": 500
    },
    "26": {
        "id": "26",
        "name": "Fresh Mint",
        "price": 25,
        "category": "Leafy Vegetables",
        "image": "/static/images/products/leafy-vegetables/Pudina.jpg",
        "description": "Fresh mint leaves",
        "weight": "100g",
        "stock": 40,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 100,
        "max_quantity": 500
    },
    "27": {
        "id": "27",
        "name": "Organic Milk",
        "price": 65,
        "category": "Dairy",
        "image": "/static/images/products/dairy/OraganicMilk.jpg",
        "description": "Fresh organic milk",
        "weight": "1L",
        "stock": 30,
        "visible": True,
        "quantity_type": "pieces",  # Sold by bottles/packets
        "min_quantity": 1,
        "max_quantity": 10
    },
    "28": {
        "id": "28",
        "name": "Fenugreek Leaves",
        "price": 30,
        "category": "Leafy Vegetables",
        "image": "/static/images/products/leafy-vegetables/Menthi.jpg",
        "description": "Fresh fenugreek leaves",
        "weight": "250g",
        "stock": 25,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 1000
    },
    "29": {
        "id": "29",
        "name": "Ladies Finger",
        "price": 40,
        "category": "Vegetables",
        "image": "/static/images/products/vegetables/LadysFinger.jpg",
        "description": "Fresh ladies finger",
        "weight": "500g",
        "stock": 35,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 2000
    },
    "30": {
        "id": "30",
        "name": "Curry Leaves",
        "price": 15,
        "category": "Leafy Vegetables",
        "image": "/static/images/products/leafy-vegetables/curryleaves.jpg",
        "description": "Fresh curry leaves",
        "weight": "50g",
        "stock": 60,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 50,
        "max_quantity": 200
    },
    "31": {
        "id": "31",
        "name": "Red Chili Powder",
        "price": 150,
        "category": "Spices",
        "image": "/static/images/products/spices/Chillipowder.jpg",
        "description": "Pure red chili powder",
        "weight": "250g",
        "stock": 30,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 100,
        "max_quantity": 1000
    },
    "32": {
        "id": "32",
        "name": "Mustard Seeds",
        "price": 120,
        "category": "Spices",
        "image": "/static/images/products/spices/MustardSeeds - Aavalu.jpg",
        "description": "Premium mustard seeds",
        "weight": "250g",
        "stock": 25,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 100,
        "max_quantity": 1000
    },
    "33": {
        "id": "33",
        "name": "Cumin Seeds",
        "price": 400,
        "category": "Spices",
        "image": "/static/images/products/spices/Cuminseeds-Jeelakarra.jpg",
        "description": "Premium cumin seeds",
        "weight": "250g",
        "stock": 20,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 100,
        "max_quantity": 1000
    },
    "34": {
        "id": "34",
        "name": "Pure Coconut Oil",
        "price": 350,
        "category": "Others",
        "image": "/static/images/products/others/Pure-Coconut-Oil.jpg",
        "description": "Cold pressed coconut oil",
        "weight": "1L",
        "stock": 15,
        "visible": True,
        "quantity_type": "pieces",  # Sold by bottles
        "min_quantity": 1,
        "max_quantity": 5
    },
    "35": {
        "id": "35",
        "name": "Mustard Oil",
        "price": 200,
        "category": "Others",
        "image": "/static/images/products/others/Mustard_oil.avif",
        "description": "Pure mustard oil",
        "weight": "1L",
        "stock": 20,
        "visible": True,
        "quantity_type": "pieces",
        "min_quantity": 1,
        "max_quantity": 5
    },
    "36": {
        "id": "36",
        "name": "Fresh Coconut",
        "price": 30,
        "category": "Vegetables",
        "image": "/static/images/products/vegetables/Cocunut.jpeg",
        "description": "Fresh coconut",
        "weight": "1 piece",
        "stock": 40,
        "visible": True,
        "quantity_type": "pieces",
        "min_quantity": 1,
        "max_quantity": 10
    },
    "37": {
        "id": "37",
        "name": "Sesame Oil",
        "price": 300,
        "category": "Others",
        "image": "/static/images/products/others/seaseme_oil.jpeg",
        "description": "Pure sesame oil",
        "weight": "500ml",
        "stock": 18,
        "visible": True,
        "quantity_type": "pieces",
        "min_quantity": 1,
        "max_quantity": 5
    },
    "38": {
        "id": "38",
        "name": "Dry Fruit Mix",
        "price": 500,
        "category": "Others",
        "image": "/static/images/products/others/df_mix.jpeg",
        "description": "Premium dry fruit mix",
        "weight": "500g",
        "stock": 12,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 2000
    },
    "39": {
        "id": "39",
        "name": "Mango Pickle",
        "price": 180,
        "category": "Pickles",
        "image": "/static/images/products/Pickels/Mango_pickle.webp",
        "description": "Traditional mango pickle",
        "weight": "500g",
        "stock": 25,
        "visible": True,
        "quantity_type": "pieces",  # Sold by jars/containers
        "min_quantity": 1,
        "max_quantity": 5
    },
    "40": {
        "id": "40",
        "name": "Lemon Pickle",
        "price": 160,
        "category": "Pickles",
        "image": "/static/images/products/Pickels/lemon.jpg",
        "description": "Tangy lemon pickle",
        "weight": "500g",
        "stock": 20,
        "visible": True,
        "quantity_type": "pieces",
        "min_quantity": 1,
        "max_quantity": 5
    },
    "41": {
        "id": "41",
        "name": "Mixed Vegetable Pickle",
        "price": 200,
        "category": "Pickles",
        "image": "/static/images/products/Pickels/Mixed_Vegetable_Pickle.jpg",
        "description": "Mixed vegetable pickle",
        "weight": "500g",
        "stock": 15,
        "visible": True,
        "quantity_type": "pieces",
        "min_quantity": 1,
        "max_quantity": 5
    },
    "42": {
        "id": "42",
        "name": "Fresh Paneer",
        "price": 280,
        "category": "Dairy",
        "image": "/static/images/products/dairy/Panner.jpeg",
        "description": "Fresh homemade paneer",
        "weight": "250g",
        "stock": 20,
        "visible": True,
        "quantity_type": "grams",
        "min_quantity": 250,
        "max_quantity": 1000
    }
}

orders_db = []
carts_db = {}  # {user_mobile: [cart_items]}
customer_info_db = {}  # Store customer info by user_mobile

# User Authentication Helper Functions
def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def generate_session_token():
    """Generate a unique session token"""
    return str(uuid.uuid4())

def authenticate_user(mobile, password):
    """Authenticate user with mobile and password"""
    if mobile in users_db:
        hashed_password = hash_password(password)
        if users_db[mobile]['password'] == hashed_password:
            return True
    return False

def create_user_session(mobile):
    """Create a session token for user"""
    session_token = generate_session_token()
    user_sessions[session_token] = mobile
    return session_token

def get_user_from_token(session_token):
    """Get user mobile from session token"""
    return user_sessions.get(session_token)

def is_user_authenticated(session_token):
    """Check if user is authenticated"""
    return session_token in user_sessions

# OTP Management Functions
# Email Configuration (Gmail SMTP - Free)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'greenobasket333@gmail.com',  # Your Gmail address (set this to enable real emails)
    'password': 'lptr vygm zcpe sxlp'  # Your Gmail App Password (not regular password)
}

# SMS Configuration (MSG91 - Better for India, you'll need to sign up)
SMS_CONFIG = {
    'auth_key': '',     # Your MSG91 Auth Key
    'template_id': '',  # Your MSG91 Template ID for OTP
    'sender_id': ''     # Your MSG91 Sender ID (like: GRNBSK)
}

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def store_otp(identifier, otp_type='mobile'):
    """Store OTP for mobile number or email"""
    otp = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=10)  # OTP expires in 10 minutes
    
    otp_storage[identifier] = {
        'otp': otp,
        'expires_at': expires_at,
        'type': otp_type
    }
    
    return otp

def verify_otp(identifier, otp):
    """Verify OTP for mobile number or email"""
    if identifier not in otp_storage:
        return False
    
    stored_otp_data = otp_storage[identifier]
    
    # Check if OTP has expired
    if datetime.now() > stored_otp_data['expires_at']:
        del otp_storage[identifier]  # Clean up expired OTP
        return False
    
    # Check if OTP matches
    if stored_otp_data['otp'] == otp:
        del otp_storage[identifier]  # OTP used, remove it
        return True
    
    return False

def send_otp_email(email, otp):
    """Send OTP via email (Real Gmail SMTP or Mock)"""
    if EMAIL_CONFIG['email'] and EMAIL_CONFIG['password']:
        try:
            # Real email sending using Gmail SMTP
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['email']
            msg['To'] = email
            msg['Subject'] = "GreenObasket - Password Reset OTP"
            
            body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                <div style="background: linear-gradient(135deg, #2ecc71, #27ae60); padding: 30px; text-align: center; color: white;">
                    <h1>🌱 GreenObasket</h1>
                    <h2>Password Reset Request</h2>
                </div>
                
                <div style="padding: 30px; background: #f8f9fa;">
                    <p style="font-size: 16px; color: #333;">Hi there!</p>
                    <p style="font-size: 16px; color: #333;">You requested to reset your password. Use the OTP below:</p>
                    
                    <div style="background: white; padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;">
                        <h1 style="color: #2ecc71; font-size: 32px; letter-spacing: 5px; margin: 0;">{otp}</h1>
                        <p style="color: #666; margin: 10px 0 0 0;">This OTP is valid for 10 minutes</p>
                    </div>
                    
                    <p style="font-size: 14px; color: #666;">If you didn't request this, please ignore this email.</p>
                    
                    <div style="text-align: center; margin-top: 30px;">
                        <p style="color: #2ecc71; font-weight: bold;">Happy Shopping! 🛒</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(body, 'html'))
            
            # Send email
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
            server.starttls()
            server.login(EMAIL_CONFIG['email'], EMAIL_CONFIG['password'])
            text = msg.as_string()
            server.sendmail(EMAIL_CONFIG['email'], email, text)
            server.quit()
            
            print(f"✅ [REAL EMAIL] OTP sent to {email}: {otp}")
            return True
            
        except Exception as e:
            print(f"❌ [EMAIL ERROR] Failed to send to {email}: {str(e)}")
            print(f"📧 [FALLBACK MOCK] OTP for {email}: {otp}")
            return False
    else:
        # Mock email (current behavior)
        print(f"📧 [MOCK EMAIL] Configure EMAIL_CONFIG to send real emails")
        print(f"📧 To: {email}")
        print(f"📧 OTP: {otp}")
        print(f"📧 Valid for: 10 minutes")
        print(f"📧 " + "="*50)
        return True

def send_otp_sms(mobile, otp):
    """Send OTP via SMS (MSG91 or Mock)"""
    if SMS_CONFIG['auth_key'] and SMS_CONFIG['template_id']:
        try:
            # Real SMS sending using MSG91 (Better for India)
            import requests
            
            url = "https://control.msg91.com/api/v5/otp"
            
            # MSG91 payload
            payload = {
                "template_id": SMS_CONFIG['template_id'],
                "mobile": f"91{mobile}",  # Indian numbers with country code
                "authkey": SMS_CONFIG['auth_key'],
                "otp": otp,
                "otp_expiry": "10"  # 10 minutes expiry
            }
            
            # Optional: Add sender ID if configured
            if SMS_CONFIG['sender_id']:
                payload['sender'] = SMS_CONFIG['sender_id']
            
            headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            }
            
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ [REAL SMS] OTP sent to {mobile}: {otp} (MSG91 Request ID: {result.get('request_id', 'N/A')})")
                return True
            else:
                print(f"❌ [SMS ERROR] MSG91 API failed: {response.status_code} - {response.text}")
                print(f"📱 [FALLBACK MOCK] OTP for {mobile}: {otp}")
                return False
            
        except Exception as e:
            print(f"❌ [SMS ERROR] Failed to send to {mobile}: {str(e)}")
            print(f"📱 [FALLBACK MOCK] OTP for {mobile}: {otp}")
            return False
    else:
        # Mock SMS (current behavior)
        print(f"📱 [MOCK SMS] Configure SMS_CONFIG to send real SMS")
        print(f"📱 To: +91{mobile}")
        print(f"📱 OTP: {otp}")
        print(f"📱 Message: Your GreenObasket password reset OTP is: {otp}. Valid for 10 minutes.")
        print(f"📱 " + "="*50)
        return True

def find_user_by_email(email):
    """Find user mobile number by email"""
    for mobile, user_data in users_db.items():
        if user_data.get('email', '').lower() == email.lower():
            return mobile
    return None

# Routes
@app.route('/')
def home():
    """Serve the user login page"""
    try:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, '..', 'frontend', 'user_login.html')
        with open(html_path, 'r') as file:
            return render_template_string(file.read())
    except FileNotFoundError:
        return jsonify({"error": "User login page not found"}), 404

@app.route('/shop')
def shop():
    """Serve the main grocery app (requires login)"""
    try:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, '..', 'frontend', 'grocery_app.html')
        with open(html_path, 'r') as file:
            return render_template_string(file.read())
    except FileNotFoundError:
        return jsonify({"error": "HTML file not found"}), 404

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all visible products or filter by category (Customer facing)"""
    category = request.args.get('category')
    search = request.args.get('search', '').lower()
    
    # Only show visible products to customers - convert dict to list
    filtered_products = [p for p in products_db.values() if p.get('visible', True)]
    
    # Filter by category
    if category and category != 'all':
        filtered_products = [p for p in filtered_products if p.get('category', '').lower() == category.lower()]
    
    # Filter by search term
    if search:
        filtered_products = [
            p for p in filtered_products 
            if search in p.get('name', '').lower() or 
               search in p.get('description', '').lower() or 
               search in p.get('category', '').lower()
        ]
    
    return jsonify({
        "success": True,
        "products": filtered_products,
        "total": len(filtered_products)
    })

@app.route('/api/admin/products/all', methods=['GET'])
def get_all_products_admin():
    """Get all products including hidden ones (Admin only)"""
    if not is_admin_authenticated():
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    category = request.args.get('category')
    search = request.args.get('search', '').lower()
    
    # Convert dictionary to list of products
    filtered_products = list(products_db.values())
    
    # Filter by category
    if category and category != 'all':
        filtered_products = [p for p in filtered_products if p.get('category', '').lower() == category.lower()]
    
    # Filter by search term
    if search:
        filtered_products = [
            p for p in filtered_products 
            if search in p.get('name', '').lower() or 
               search in p.get('description', '').lower() or 
               search in p.get('category', '').lower()
        ]
    
    return jsonify({
        "success": True,
        "products": filtered_products,
        "total": len(filtered_products)
    })

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a specific product by ID"""
    product = products_db.get(str(product_id))
    
    if not product:
        return jsonify({"success": False, "error": "Product not found"}), 404
    
    return jsonify({"success": True, "product": product})

@app.route('/api/cart', methods=['GET'])
def get_cart():
    """Get cart items for authenticated user"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    cart = carts_db.get(user_mobile, [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    
    return jsonify({
        "success": True,
        "cart": cart,
        "total": total,
        "items_count": sum(item['quantity'] for item in cart)
    })

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add item to cart for authenticated user"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    quantity_grams = data.get('quantity_grams')
    quantity_type = data.get('quantity_type', 'pieces')  # Default to pieces if not specified
    total_price = data.get('total_price')
    
    # Find product
    product = products_db.get(product_id)
    if not product:
        return jsonify({"success": False, "error": "Product not found"}), 404
    
    # Initialize cart if doesn't exist
    if user_mobile not in carts_db:
        carts_db[user_mobile] = []
    
    cart = carts_db[user_mobile]
    
    # Handle different quantity types
    if quantity_grams and total_price:  # Legacy gram-based system
        # Check stock (for grams, we'll assume each stock unit can provide base weight)
        weight_str = product.get('weight', '100g')
        # Parse weight string to extract grams
        try:
            if 'kg' in weight_str.lower():
                base_weight = float(weight_str.lower().replace('kg', '').replace(' ', '')) * 1000
            elif 'g' in weight_str.lower():
                base_weight = float(weight_str.lower().replace('g', '').replace(' ', ''))
            else:
                base_weight = float(weight_str.replace(' ', ''))
                if base_weight < 100:  # Assume it's in kg if less than 100
                    base_weight *= 1000
        except:
            base_weight = 100  # Default fallback
            
        max_grams = product['stock'] * base_weight
        
        if quantity_grams > max_grams:
            return jsonify({"success": False, "error": f"Insufficient stock. Maximum available: {max_grams}g"}), 400
        
        # Check if item already in cart (gram-based)
        existing_item = next((item for item in cart if item['id'] == product_id and 'quantity_grams' in item), None)
        
        if existing_item:
            existing_item['quantity_grams'] += quantity_grams
            existing_item['total_price'] += total_price
        else:
            cart.append({
                "id": product['id'],
                "name": product['name'],
                "base_price": product['price'],
                "image": product['image'],
                "weight": product.get('weight', 'N/A'),
                "quantity_grams": quantity_grams,
                "quantity_type": "grams",
                "total_price": round(total_price, 2),
                "price": round(total_price, 2),  # For compatibility
                "quantity": 1  # For compatibility with existing code
            })
    else:
        # Handle new quantity type system (pieces, liters, grams)
        product_quantity_type = product.get('quantity_type', 'pieces')
        
        # Validate quantity against product limits
        min_quantity = product.get('min_quantity', 1)
        max_quantity = product.get('max_quantity', 100)
        
        if quantity < min_quantity:
            return jsonify({"success": False, "error": f"Minimum quantity is {min_quantity}"}), 400
        if quantity > max_quantity:
            return jsonify({"success": False, "error": f"Maximum quantity is {max_quantity}"}), 400
        
        # Check stock availability
        if quantity_type == 'grams':
            # For grams, check if we have enough raw material
            weight_str = product.get('weight', '100g')
            try:
                if 'kg' in weight_str.lower():
                    base_weight = float(weight_str.lower().replace('kg', '').replace(' ', '')) * 1000
                elif 'g' in weight_str.lower():
                    base_weight = float(weight_str.lower().replace('g', '').replace(' ', ''))
                else:
                    base_weight = 100
            except:
                base_weight = 100
            
            max_available = product['stock'] * base_weight
            if quantity > max_available:
                return jsonify({"success": False, "error": f"Insufficient stock. Maximum available: {max_available}g"}), 400
        else:
            # For pieces/liters, check direct stock count
            if product['stock'] < quantity:
                return jsonify({"success": False, "error": f"Insufficient stock. Only {product['stock']} available"}), 400
        
        # Calculate total price based on quantity type
        if not total_price:
            if quantity_type == 'grams':
                # For grams, calculate based on price per gram
                weight_str = product.get('weight', '100g')
                try:
                    if 'kg' in weight_str.lower():
                        base_weight = float(weight_str.lower().replace('kg', '').replace(' ', '')) * 1000
                    elif 'g' in weight_str.lower():
                        base_weight = float(weight_str.lower().replace('g', '').replace(' ', ''))
                    else:
                        base_weight = 100
                except:
                    base_weight = 100
                
                price_per_gram = product['price'] / base_weight
                total_price = price_per_gram * quantity
            else:
                # For pieces/liters, multiply by unit price
                total_price = product['price'] * quantity
        
        # Check if item already in cart with same quantity type
        cart_key = f"{product_id}_{quantity_type}"
        existing_item = next((item for item in cart if item['id'] == product_id and item.get('quantity_type') == quantity_type), None)
        
        if existing_item:
            existing_item['quantity'] += quantity
            existing_item['total_price'] = existing_item.get('total_price', 0) + total_price
            if quantity_type == 'grams':
                existing_item['quantity_grams'] = existing_item.get('quantity_grams', 0) + quantity
        else:
            cart_item = {
                "id": product['id'],
                "name": product['name'],
                "base_price": product['price'],
                "image": product['image'],
                "weight": product.get('weight', 'N/A'),
                "quantity": quantity,
                "quantity_type": quantity_type,
                "total_price": round(total_price, 2),
                "price": round(total_price, 2)  # For compatibility
            }
            
            # Add specific quantity field for grams
            if quantity_type == 'grams':
                cart_item['quantity_grams'] = quantity
                
            cart.append(cart_item)
    
    return jsonify({
        "success": True,
        "message": "Item added to cart",
        "cart_count": len(cart)
    })

@app.route('/api/cart/update', methods=['PUT'])
def update_cart_item():
    """Update cart item quantity for authenticated user"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    if user_mobile not in carts_db:
        return jsonify({"success": False, "error": "Cart not found"}), 404
    
    cart = carts_db[user_mobile]
    item = next((item for item in cart if item['id'] == product_id), None)
    
    if not item:
        return jsonify({"success": False, "error": "Item not found in cart"}), 404
    
    if quantity <= 0:
        cart.remove(item)
        message = "Item removed from cart"
    else:
        item['quantity'] = quantity
        message = "Cart updated"
    
    return jsonify({
        "success": True,
        "message": message,
        "cart_count": sum(item['quantity'] for item in cart)
    })

@app.route('/api/cart/remove', methods=['DELETE'])
def remove_from_cart():
    """Remove item from cart for authenticated user"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    data = request.get_json()
    product_id = data.get('product_id')
    
    if user_mobile not in carts_db:
        return jsonify({"success": False, "error": "Cart not found"}), 404
    
    cart = carts_db[user_mobile]
    cart[:] = [item for item in cart if item['id'] != product_id]
    
    return jsonify({
        "success": True,
        "message": "Item removed from cart",
        "cart_count": sum(item['quantity'] for item in cart)
    })

@app.route('/api/orders/prepare', methods=['POST'])
def prepare_order():
    """Prepare order for UPI payment (don't deduct stock yet)"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    data = request.get_json()
    customer_info = data.get('customer_info', {})
    totals = data.get('totals', {})
    
    if user_mobile not in carts_db or not carts_db[user_mobile]:
        return jsonify({"success": False, "error": "Cart is empty"}), 400
    
    cart = carts_db[user_mobile]
    
    # Check stock availability (but don't deduct yet)
    for item in cart:
        product = products_db.get(item['id'])
        if not product:
            return jsonify({"success": False, "error": f"Product {item['name']} not found"}), 400
        
        if product['stock'] < item['quantity']:
            return jsonify({
                "success": False, 
                "error": f"Insufficient stock for {item['name']}. Only {product['stock']} items available."
            }), 400
    
    # Create pending order (without stock deduction)
    order = {
        "id": str(uuid.uuid4()),
        "customer_info": customer_info,
        "items": cart.copy(),
        "subtotal": totals.get('subtotal', 0),
        "delivery_fee": totals.get('deliveryFee', 0),
        "total": totals.get('total', 0),
        "payment_method": customer_info.get('paymentMethod', 'phonepe'),
        "status": "pending_payment",
        "created_at": datetime.now().isoformat(),
        "estimated_delivery": "45-60 minutes",
        "user_mobile": user_mobile  # Store user_mobile for later confirmation
    }
    
    return jsonify({
        "success": True,
        "message": "Order prepared for payment",
        "order": order
    })

@app.route('/api/orders/confirm', methods=['POST'])
def confirm_order():
    """Confirm order after payment"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    data = request.get_json()
    order_id = data.get('order_id')
    payment_status = data.get('payment_status', 'completed')
    
    # In a real app, you would verify payment status with UPI gateway here
    
    # Find the user_mobile from the prepared order
    order_user_mobile = None
    for existing_order in orders_db:
        if existing_order.get('id') == order_id and existing_order.get('status') == 'pending_payment':
            order_user_mobile = existing_order.get('user_mobile')
            break
    
    if not order_user_mobile or order_user_mobile != user_mobile or user_mobile not in carts_db or not carts_db[user_mobile]:
        return jsonify({"success": False, "error": "Order not found or cart is empty"}), 400
    
    cart = carts_db[user_mobile]
    
    # Double-check stock availability before final confirmation
    for item in cart:
        product = products_db.get(item['id'])
        if not product:
            return jsonify({"success": False, "error": f"Product {item['name']} not found"}), 400
        
        if product['stock'] < item['quantity']:
            return jsonify({
                "success": False, 
                "error": f"Insufficient stock for {item['name']}. Only {product['stock']} items available."
            }), 400
    
    # Now deduct stock for each item
    for item in cart:
        product = products_db.get(item['id'])
        if product:
            product['stock'] -= item['quantity']
    
    # Update order status and add to orders_db
    confirmed_order = None
    for existing_order in orders_db:
        if existing_order.get('id') == order_id and existing_order.get('status') == 'pending_payment':
            existing_order['status'] = 'received'
            existing_order['payment_status'] = payment_status
            existing_order['confirmed_at'] = datetime.now().isoformat()
            confirmed_order = existing_order
            break
    
    if not confirmed_order:
        # Create new confirmed order if not found in pending
        confirmed_order = {
            "id": order_id,
            "user_mobile": user_mobile,  # Link order to user
            "customer_info": data.get('customer_info', {}),
            "items": cart.copy(),
            "status": "received",
            "status_history": [
                {
                    "status": "received",
                    "timestamp": datetime.now().isoformat(),
                    "message": "Order received and payment confirmed"
                }
            ],
            "payment_status": payment_status,
            "created_at": datetime.now().isoformat(),
            "confirmed_at": datetime.now().isoformat(),
            "estimated_delivery_minutes": 60,
            "estimated_delivery_text": "45-60 minutes"
        }
        orders_db.append(confirmed_order)
    
    # Save customer info for future orders
    customer_info = confirmed_order.get('customer_info', {})
    if customer_info and user_mobile:
        customer_info_db[user_mobile] = {
            "name": customer_info.get('name', ''),
            "mobile": customer_info.get('mobile', ''),
            "addressType": customer_info.get('addressType', ''),
            "blockFlat": customer_info.get('blockFlat', ''),
            "fullAddress": customer_info.get('fullAddress', ''),
            "saved_at": datetime.now().isoformat()
        }
    
    # Clear cart
    carts_db[user_mobile] = []
    
    return jsonify({
        "success": True,
        "message": "Order confirmed successfully!",
        "order": confirmed_order
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order (for COD and Pay in App)"""
    try:
        session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
        
        if not is_user_authenticated(session_token):
            return jsonify({
                "success": False,
                "error": "Authentication required"
            }), 401
        
        user_mobile = get_user_from_token(session_token)
        
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No JSON data received"}), 400
            
        customer_info = data.get('customer_info', {})
        totals = data.get('totals', {})
        
        if user_mobile not in carts_db or not carts_db[user_mobile]:
            return jsonify({"success": False, "error": "Cart is empty"}), 400
        
        cart = carts_db[user_mobile]
        
        # Check stock availability before placing order
        for item in cart:
            product = next((p for p in products_db.values() if p['id'] == item['id']), None)
            if not product:
                return jsonify({"success": False, "error": f"Product {item['name']} not found"}), 400
            
            if product['stock'] < item['quantity']:
                return jsonify({
                    "success": False, 
                    "error": f"Insufficient stock for {item['name']}. Only {product['stock']} items available."
                }), 400
        
        # Deduct stock for each item
        for item in cart:
            product = next((p for p in products_db.values() if p['id'] == item['id']), None)
            if product:
                product['stock'] -= item['quantity']
        
        # Create order with enhanced details and status tracking
        order = {
            "id": str(uuid.uuid4()),
            "user_mobile": user_mobile,  # Link order to user
            "customer_info": customer_info,
            "items": cart.copy(),
            "subtotal": totals.get('subtotal', 0),
            "delivery_fee": totals.get('deliveryFee', 0),
            "total": totals.get('total', 0),
            "payment_method": customer_info.get('paymentMethod', 'cod'),
            "status": "received",
            "status_history": [
                {
                    "status": "received",
                    "timestamp": datetime.now().isoformat(),
                    "message": "Order received successfully"
                }
            ],
            "created_at": datetime.now().isoformat(),
            "estimated_delivery_minutes": 60,  # Default 60 minutes
            "estimated_delivery_text": "45-60 minutes"
        }
        
        orders_db.append(order)
        
        # Save customer info for future orders
        if customer_info and user_mobile:
            customer_info_db[user_mobile] = {
                "name": customer_info.get('name', ''),
                "mobile": customer_info.get('mobile', ''),
                "addressType": customer_info.get('addressType', ''),
                "blockFlat": customer_info.get('blockFlat', ''),
                "fullAddress": customer_info.get('fullAddress', ''),
                "saved_at": datetime.now().isoformat()
            }
        
        # Clear cart
        carts_db[user_mobile] = []
        
        return jsonify({
            "success": True,
            "message": "Order placed successfully!",
            "order": order
        })
    
    except Exception as e:
        print(f"❌ Error in create_order: {str(e)}")
        print(f"❌ Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/api/customer-info', methods=['GET'])
def get_customer_info():
    """Get saved customer information for authenticated user"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    customer_info = customer_info_db.get(user_mobile)
    
    if customer_info:
        return jsonify({
            "success": True,
            "customer_info": customer_info
        })
    else:
        return jsonify({
            "success": False,
            "message": "No saved customer information found"
        })

@app.route('/api/customer-info', methods=['POST'])
def save_customer_info():
    """Save customer information for authenticated user"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    data = request.get_json()
    customer_info = data.get('customer_info', {})
    
    if customer_info:
        customer_info_db[user_mobile] = {
            "name": customer_info.get('name', ''),
            "mobile": customer_info.get('mobile', ''),
            "addressType": customer_info.get('addressType', ''),
            "blockFlat": customer_info.get('blockFlat', ''),
            "fullAddress": customer_info.get('fullAddress', ''),
            "saved_at": datetime.now().isoformat()
        }
        
        return jsonify({
            "success": True,
            "message": "Customer information saved successfully"
        })
    else:
        return jsonify({
            "success": False,
            "error": "No customer information provided"
        }), 400

# User Authentication Routes
@app.route('/api/user/register', methods=['POST'])
def register_user():
    """Register a new user"""
    data = request.get_json()
    mobile = data.get('mobile', '').strip()
    password = data.get('password', '').strip()
    name = data.get('name', '').strip()
    address = data.get('address', '').strip()
    email = data.get('email', '').strip()
    
    # Validation
    if not mobile or len(mobile) != 10 or not mobile.isdigit():
        return jsonify({
            "success": False,
            "error": "Mobile number must be exactly 10 digits"
        }), 400
    
    if not password or len(password) < 6:
        return jsonify({
            "success": False,
            "error": "Password must be at least 6 characters long"
        }), 400
    
    if not name:
        return jsonify({
            "success": False,
            "error": "Name is required"
        }), 400
    
    if not email or '@' not in email:
        return jsonify({
            "success": False,
            "error": "Valid email is required"
        }), 400
    
    # Check if user already exists
    if mobile in users_db:
        return jsonify({
            "success": False,
            "error": "User with this mobile number already exists"
        }), 400
    
    # Check if email already exists
    if find_user_by_email(email):
        return jsonify({
            "success": False,
            "error": "User with this email already exists"
        }), 400
    
    # Create new user
    users_db[mobile] = {
        "password": hash_password(password),
        "name": name,
        "address": address,
        "email": email,
        "created_at": datetime.now().isoformat()
    }
    
    # Create session token
    session_token = create_user_session(mobile)
    
    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "session_token": session_token,
        "user": {
            "mobile": mobile,
            "name": name,
            "address": address,
            "email": email
        }
    })

@app.route('/api/user/login', methods=['POST'])
def login_user():
    """Login user"""
    data = request.get_json()
    mobile = data.get('mobile', '').strip()
    password = data.get('password', '').strip()
    
    # Validation
    if not mobile or not password:
        return jsonify({
            "success": False,
            "error": "Mobile number and password are required"
        }), 400
    
    # Authenticate user
    if not authenticate_user(mobile, password):
        return jsonify({
            "success": False,
            "error": "Invalid mobile number or password"
        }), 401
    
    # Create session token
    session_token = create_user_session(mobile)
    user_data = users_db[mobile]
    
    return jsonify({
        "success": True,
        "message": "Login successful",
        "session_token": session_token,
        "user": {
            "mobile": mobile,
            "name": user_data["name"],
            "address": user_data["address"]
        }
    })

@app.route('/api/user/logout', methods=['POST'])
def logout_user():
    """Logout user"""
    data = request.get_json()
    session_token = data.get('session_token', '')
    
    if session_token in user_sessions:
        del user_sessions[session_token]
    
    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })

@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    """Get user profile"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Not authenticated"
        }), 401
    
    mobile = get_user_from_token(session_token)
    user_data = users_db[mobile]
    
    return jsonify({
        "success": True,
        "user": {
            "mobile": mobile,
            "name": user_data["name"],
            "address": user_data["address"],
            "email": user_data["email"],
            "created_at": user_data["created_at"]
        }
    })

# Forgot Password Routes
@app.route('/api/user/forgot-password', methods=['POST'])
def forgot_password():
    """Send OTP for password reset"""
    data = request.get_json()
    identifier = data.get('identifier', '').strip()  # Can be mobile or email
    method = data.get('method', 'mobile')  # 'mobile' or 'email'
    
    if not identifier:
        return jsonify({
            "success": False,
            "error": "Mobile number or email is required"
        }), 400
    
    # Determine if identifier is mobile or email
    if method == 'email' or '@' in identifier:
        # Email-based reset
        mobile = find_user_by_email(identifier)
        if not mobile:
            return jsonify({
                "success": False,
                "error": "No user found with this email address"
            }), 404
        
        # Generate and store OTP
        otp = store_otp(identifier, 'email')
        
        # Send OTP via email (mock)
        send_otp_email(identifier, otp)
        
        return jsonify({
            "success": True,
            "message": f"OTP sent to email {identifier}",
            "identifier": identifier,
            "method": "email"
        })
    
    else:
        # Mobile-based reset
        if len(identifier) != 10 or not identifier.isdigit():
            return jsonify({
                "success": False,
                "error": "Mobile number must be exactly 10 digits"
            }), 400
        
        if identifier not in users_db:
            return jsonify({
                "success": False,
                "error": "No user found with this mobile number"
            }), 404
        
        # Generate and store OTP
        otp = store_otp(identifier, 'mobile')
        
        # Send OTP via SMS (mock)
        send_otp_sms(identifier, otp)
        
        return jsonify({
            "success": True,
            "message": f"OTP sent to mobile number {identifier}",
            "identifier": identifier,
            "method": "mobile"
        })

@app.route('/api/user/verify-otp', methods=['POST'])
def verify_password_reset_otp():
    """Verify OTP for password reset"""
    data = request.get_json()
    identifier = data.get('identifier', '').strip()
    otp = data.get('otp', '').strip()
    
    if not identifier or not otp:
        return jsonify({
            "success": False,
            "error": "Identifier and OTP are required"
        }), 400
    
    # Verify OTP
    if verify_otp(identifier, otp):
        # Generate a temporary reset token (valid for 15 minutes)
        reset_token = generate_session_token()
        reset_expires = datetime.now() + timedelta(minutes=15)
        
        # Store reset token (reusing otp_storage for simplicity)
        otp_storage[f"reset_{reset_token}"] = {
            'identifier': identifier,
            'expires_at': reset_expires,
            'type': 'reset_token'
        }
        
        return jsonify({
            "success": True,
            "message": "OTP verified successfully",
            "reset_token": reset_token
        })
    else:
        return jsonify({
            "success": False,
            "error": "Invalid or expired OTP"
        }), 400

@app.route('/api/user/reset-password', methods=['POST'])
def reset_password():
    """Reset password using reset token"""
    data = request.get_json()
    reset_token = data.get('reset_token', '').strip()
    new_password = data.get('new_password', '').strip()
    
    if not reset_token or not new_password:
        return jsonify({
            "success": False,
            "error": "Reset token and new password are required"
        }), 400
    
    if len(new_password) < 6:
        return jsonify({
            "success": False,
            "error": "Password must be at least 6 characters long"
        }), 400
    
    # Verify reset token
    reset_key = f"reset_{reset_token}"
    if reset_key not in otp_storage:
        return jsonify({
            "success": False,
            "error": "Invalid or expired reset token"
        }), 400
    
    reset_data = otp_storage[reset_key]
    
    # Check if token has expired
    if datetime.now() > reset_data['expires_at']:
        del otp_storage[reset_key]
        return jsonify({
            "success": False,
            "error": "Reset token has expired"
        }), 400
    
    identifier = reset_data['identifier']
    
    # Find user mobile number
    if '@' in identifier:
        # Email-based reset
        mobile = find_user_by_email(identifier)
    else:
        # Mobile-based reset
        mobile = identifier
    
    if not mobile or mobile not in users_db:
        return jsonify({
            "success": False,
            "error": "User not found"
        }), 404
    
    # Update password
    users_db[mobile]['password'] = hash_password(new_password)
    
    # Clean up reset token
    del otp_storage[reset_key]
    
    # Invalidate all existing sessions for this user (for security)
    sessions_to_remove = []
    for session_token, user_mobile in user_sessions.items():
        if user_mobile == mobile:
            sessions_to_remove.append(session_token)
    
    for session_token in sessions_to_remove:
        del user_sessions[session_token]
    
    return jsonify({
        "success": True,
        "message": "Password reset successfully. Please login with your new password."
    })

@app.route('/api/admin/notifications', methods=['POST'])
def admin_notification():
    """Receive admin notifications"""
    try:
        data = request.get_json()
        notification = {
            "id": str(uuid.uuid4()),
            "type": data.get('type'),
            "order": data.get('order'),
            "customer": data.get('customer'),
            "totals": data.get('totals'),
            "timestamp": data.get('timestamp'),
            "read": False
        }
        
        admin_notifications.append(notification)
        
        return jsonify({
            "success": True,
            "message": "Notification sent to admin"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/admin/notifications', methods=['GET'])
def get_admin_notifications():
    """Get admin notifications (Admin only)"""
    if not is_admin_authenticated():
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    try:
        # Sort notifications by timestamp (newest first)
        sorted_notifications = sorted(admin_notifications, key=lambda x: x['timestamp'], reverse=True)
        
        return jsonify({
            "success": True,
            "notifications": sorted_notifications,
            "unread_count": sum(1 for n in admin_notifications if not n['read'])
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/admin/notifications/<notification_id>/read', methods=['PUT'])
def mark_notification_read(notification_id):
    """Mark notification as read (Admin only)"""
    if not is_admin_authenticated():
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    try:
        notification = next((n for n in admin_notifications if n['id'] == notification_id), None)
        if not notification:
            return jsonify({"success": False, "error": "Notification not found"}), 404
        
        notification['read'] = True
        
        return jsonify({
            "success": True,
            "message": "Notification marked as read"
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route('/api/admin/orders/<order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status (Admin only)"""
    if not is_admin_authenticated():
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    data = request.get_json()
    new_status = data.get('status')
    estimated_minutes = data.get('estimated_minutes', 60)
    custom_message = data.get('message', '')
    
    # Valid status transitions - Updated to match requirements
    valid_statuses = ['received', 'packing', 'in_transit', 'delivered', 'cancelled']
    
    if new_status not in valid_statuses:
        return jsonify({"success": False, "error": "Invalid status"}), 400
    
    # Find order
    order = next((o for o in orders_db if o['id'] == order_id), None)
    if not order:
        return jsonify({"success": False, "error": "Order not found"}), 404
    
    # Status messages - Updated for new 4-state system
    status_messages = {
        'received': '📋 Order received successfully',
        'packing': '📦 Your order is being packed by our team',
        'in_transit': f'🚚 Your order is on the way! Expected delivery in {estimated_minutes} minutes',
        'delivered': '✅ Order delivered successfully',
        'cancelled': '❌ Order has been cancelled'
    }
    
    # Update order status
    order['status'] = new_status
    order['estimated_delivery_minutes'] = estimated_minutes
    order['estimated_delivery_text'] = f"{estimated_minutes} minutes" if estimated_minutes else "Soon"
    
    # Add to status history
    if 'status_history' not in order:
        order['status_history'] = []
    
    message = custom_message if custom_message else status_messages.get(new_status, f'Status updated to {new_status}')
    
    order['status_history'].append({
        "status": new_status,
        "timestamp": datetime.now().isoformat(),
        "message": message
    })
    
    # Send notification to user
    user_mobile = order.get('user_mobile')
    if user_mobile:
        if user_mobile not in user_notifications:
            user_notifications[user_mobile] = []
        
        user_notifications[user_mobile].append({
            "id": f"notif_{datetime.now().timestamp()}",
            "order_id": order_id,
            "type": "order_status_update",
            "title": f"Order Status Updated",
            "message": message,
            "status": new_status,
            "timestamp": datetime.now().isoformat(),
            "read": False
        })
    
    return jsonify({
        "success": True,
        "message": f"Order status updated to {new_status}",
        "order": order,
        "notification_sent": bool(user_mobile)
    })

@app.route('/api/user/notifications', methods=['GET'])
def get_user_notifications():
    """Get user notifications"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    notifications = user_notifications.get(user_mobile, [])
    
    # Sort by timestamp (newest first)
    notifications.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
    
    return jsonify({
        "success": True,
        "notifications": notifications,
        "unread_count": len([n for n in notifications if not n.get('read', False)])
    })

@app.route('/api/user/notifications/<notification_id>/read', methods=['PUT'])
def mark_user_notification_read(notification_id):
    """Mark notification as read"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    notifications = user_notifications.get(user_mobile, [])
    
    # Find and mark notification as read
    for notification in notifications:
        if notification.get('id') == notification_id:
            notification['read'] = True
            break
    
    return jsonify({
        "success": True,
        "message": "Notification marked as read"
    })

@app.route('/api/admin/orders', methods=['GET'])
def get_all_orders_admin():
    """Get all orders for admin dashboard"""
    if not is_admin_authenticated():
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    # Sort orders by creation date (newest first)
    sorted_orders = sorted(orders_db, key=lambda x: x.get('created_at', ''), reverse=True)
    
    return jsonify({
        "success": True,
        "orders": sorted_orders,
        "total_orders": len(sorted_orders)
    })

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    """Get order details"""
    order = next((o for o in orders_db if o['id'] == order_id), None)
    
    if not order:
        return jsonify({"success": False, "error": "Order not found"}), 404
    
    return jsonify({"success": True, "order": order})

@app.route('/api/user/orders', methods=['GET'])
def get_user_orders():
    """Get user's previous orders"""
    session_token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    if not is_user_authenticated(session_token):
        return jsonify({
            "success": False,
            "error": "Authentication required"
        }), 401
    
    user_mobile = get_user_from_token(session_token)
    
    # Get user's orders sorted by creation date (newest first)
    user_orders = [order for order in orders_db if order.get('user_mobile') == user_mobile]
    user_orders.sort(key=lambda x: x.get('created_at', ''), reverse=True)
    
    # Separate current and previous orders - Updated status names
    current_orders = [order for order in user_orders if order.get('status') in ['received', 'packing', 'in_transit']]
    previous_orders = [order for order in user_orders if order.get('status') in ['delivered', 'cancelled']]
    
    return jsonify({
        "success": True, 
        "current_orders": current_orders,
        "previous_orders": previous_orders,
        "total_orders": len(user_orders)
    })

@app.route('/api/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    # Define comprehensive categories for GreenObasket
    categories = [
        {"id": "fruits", "name": "Fresh Fruits", "icon": "fas fa-apple-alt"},
        {"id": "vegetables", "name": "Organic Vegetables", "icon": "fas fa-carrot"},
        {"id": "dairy", "name": "Dairy & Fresh", "icon": "fas fa-cheese"},
        {"id": "beverages", "name": "Beverages", "icon": "fas fa-coffee"},
        {"id": "spices", "name": "Spices & Herbs", "icon": "fas fa-pepper-hot"},
        {"id": "oils", "name": "Organic Oils", "icon": "fas fa-tint"},
        {"id": "nuts", "name": "Nuts & Dry Fruits", "icon": "fas fa-seedling"},
        {"id": "pickles", "name": "Pickles & Condiments", "icon": "fas fa-jar"},
        {"id": "snacks", "name": "Healthy Snacks", "icon": "fas fa-cookie-bite"}
    ]
    
    return jsonify({
        "success": True,
        "categories": categories
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get app statistics"""
    return jsonify({
        "success": True,
        "stats": {
            "total_products": len(products_db),
            "total_orders": len(orders_db),
            "active_carts": len(carts_db),
            "categories": len(set(product['category'] for product in products_db.values()))
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"success": False, "error": "Internal server error"}), 500

# Admin authentication helper
def is_admin_authenticated():
    return session.get('admin_logged_in', False)

# Admin routes
@app.route('/admin')
def admin_dashboard():
    """Admin dashboard"""
    if not is_admin_authenticated():
        return redirect('/admin/login')
    
    try:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, '..', 'frontend', 'admin_dashboard.html')
        with open(html_path, 'r') as file:
            return render_template_string(file.read())
    except FileNotFoundError:
        return jsonify({"error": "Admin dashboard not found"}), 404

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        data = request.get_json() if request.content_type == 'application/json' else request.form
        username = data.get('username')
        password = data.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return jsonify({"success": True, "message": "Login successful"})
        else:
            return jsonify({"success": False, "error": "Invalid credentials"}), 401
    
    # Return login form
    login_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GreenObasket Admin Login</title>
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #2ecc71, #27ae60); 
                   margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; }
            .login-container { background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); 
                              width: 300px; text-align: center; }
            .logo { font-size: 1.8rem; font-weight: bold; color: #2ecc71; margin-bottom: 1rem; }
            .logo i { color: #f1c40f; }
            input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 12px; background: #2ecc71; color: white; border: none; border-radius: 5px; 
                     cursor: pointer; font-size: 1rem; font-weight: bold; }
            button:hover { background: #27ae60; }
            .error { color: red; margin-top: 10px; }
        </style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    </head>
    <body>
        <div class="login-container">
            <div class="logo"><i class="fas fa-leaf"></i> GreenObasket Admin</div>
            <form id="loginForm">
                <input type="text" id="username" placeholder="Username" required>
                <input type="password" id="password" placeholder="Password" required>
                <button type="submit">Login</button>
                <div id="error" class="error"></div>
            </form>
        </div>
        <script>
            document.getElementById('loginForm').onsubmit = async function(e) {
                e.preventDefault();
                const response = await fetch('/admin/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        username: document.getElementById('username').value,
                        password: document.getElementById('password').value
                    })
                });
                const data = await response.json();
                if (data.success) {
                    window.location.href = '/admin';
                } else {
                    document.getElementById('error').textContent = data.error;
                }
            };
        </script>
    </body>
    </html>
    """
    return login_html

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    return redirect('/admin/login')

# Admin API routes
@app.route('/api/admin/products', methods=['POST'])
def add_product():
    """Add a new product (Admin only)"""
    if not is_admin_authenticated():
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    data = request.get_json()
    
    # Generate new product ID
    new_id = str(max([int(k) for k in products_db.keys()]) + 1)
    
    # Set default quantity type and limits if not provided
    quantity_type = data.get('quantity_type', 'grams')
    
    # Set default min/max based on quantity type
    if quantity_type == 'pieces':
        default_min, default_max = 1, 20
    elif quantity_type == 'grams':
        default_min, default_max = 250, 5000
    else:  # liters or other
        default_min, default_max = 1, 10
    
    new_product = {
        "id": new_id,
        "name": data.get('name', ''),
        "price": float(data.get('price', 0)),
        "category": data.get('category', ''),
        "image": data.get('image', ''),
        "description": data.get('description', ''),
        "weight": data.get('weight', ''),
        "stock": int(data.get('stock', 0)),
        "visible": data.get('visible', True),
        "quantity_type": quantity_type,
        "min_quantity": int(data.get('min_quantity', default_min)),
        "max_quantity": int(data.get('max_quantity', default_max))
    }
    
    products_db[new_id] = new_product
    
    return jsonify({
        "success": True,
        "message": "Product added successfully",
        "product": new_product
    })

@app.route('/api/admin/products/<product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product (Admin only)"""
    if not is_admin_authenticated():
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    if product_id not in products_db:
        return jsonify({"success": False, "error": "Product not found"}), 404
    
    data = request.get_json()
    product = products_db[product_id]
    
    # Update fields if provided
    if 'name' in data:
        product['name'] = data['name']
    if 'price' in data:
        product['price'] = float(data['price'])
    if 'category' in data:
        product['category'] = data['category']
    if 'image' in data:
        product['image'] = data['image']
    if 'description' in data:
        product['description'] = data['description']
    if 'weight' in data:
        product['weight'] = data['weight']
    if 'stock' in data:
        product['stock'] = int(data['stock'])
    if 'visible' in data:
        product['visible'] = data['visible']
    if 'quantity_type' in data:
        product['quantity_type'] = data['quantity_type']
        
        # Update default min/max if quantity type changed and no custom values provided
        if 'min_quantity' not in data or 'max_quantity' not in data:
            if data['quantity_type'] == 'pieces':
                if 'min_quantity' not in data:
                    product['min_quantity'] = 1
                if 'max_quantity' not in data:
                    product['max_quantity'] = 20
            elif data['quantity_type'] == 'grams':
                if 'min_quantity' not in data:
                    product['min_quantity'] = 250
                if 'max_quantity' not in data:
                    product['max_quantity'] = 5000
            else:  # liters or other
                if 'min_quantity' not in data:
                    product['min_quantity'] = 1
                if 'max_quantity' not in data:
                    product['max_quantity'] = 10
    
    if 'min_quantity' in data:
        product['min_quantity'] = int(data['min_quantity'])
    if 'max_quantity' in data:
        product['max_quantity'] = int(data['max_quantity'])
    
    return jsonify({
        "success": True,
        "message": "Product updated successfully",
        "product": product
    })

@app.route('/api/admin/products/<int:product_id>', methods=['DELETE'])
def admin_delete_product(product_id):
    """Delete product (Admin only)"""
    if not is_admin_authenticated():
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    product_id_str = str(product_id)
    if product_id_str not in products_db:
        return jsonify({"success": False, "error": "Product not found"}), 404
    
    del products_db[product_id_str]
    
    return jsonify({
        "success": True,
        "message": "Product deleted successfully"
    })

@app.route('/api/admin/products/<int:product_id>/toggle-visibility', methods=['PUT'])
def admin_toggle_product_visibility(product_id):
    """Toggle product visibility (Admin only)"""
    if not is_admin_authenticated():
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    product_id_str = str(product_id)
    if product_id_str not in products_db:
        return jsonify({"success": False, "error": "Product not found"}), 404
    
    product = products_db[product_id_str]
    
    # Toggle visibility
    product['visible'] = not product.get('visible', True)
    status = "visible" if product['visible'] else "hidden"
    
    return jsonify({
        "success": True,
        "message": f"Product {status} successfully",
        "visible": product['visible']
    })

if __name__ == '__main__':
    print("🌱 GreenObasket - Premium Grocery App Starting...")
    print("📱 Frontend: http://localhost:5001")
    print("🔗 API Base URL: http://localhost:5001/api")
    print("🔒 Admin Panel: http://localhost:5001/admin")
    print("=" * 60)
    print("🔐 User Authentication Endpoints:")
    print("POST /api/user/register - Register new user")
    print("POST /api/user/login - User login")
    print("POST /api/user/logout - User logout")
    print("GET  /api/user/profile - Get user profile")
    print("GET  /api/user/orders - Get user's previous orders")
    print("POST /api/user/forgot-password - Send OTP for password reset")
    print("POST /api/user/verify-otp - Verify OTP for password reset")
    print("POST /api/user/reset-password - Reset password with token")
    print("=" * 60)
    print("🛒 Shopping API Endpoints (Authentication Required):")
    print("GET  /api/products - Get all products")
    print("GET  /api/products/<id> - Get specific product")
    print("GET  /api/cart - Get user cart")
    print("POST /api/cart/add - Add to cart")
    print("PUT  /api/cart/update - Update cart")
    print("DEL  /api/cart/remove - Remove from cart")
    print("POST /api/orders - Create order")
    print("POST /api/orders/prepare - Prepare UPI order")
    print("POST /api/orders/confirm - Confirm UPI order")
    print("GET  /api/customer-info - Get saved customer info")
    print("POST /api/customer-info - Save customer info")
    print("GET  /api/categories - Get categories")
    print("GET  /api/stats - Get app stats")
    print("=" * 60)
    print("👨‍💼 Admin Endpoints:")
    print("GET  /admin - Admin dashboard")
    print("POST /admin/login - Admin login")
    print("POST /api/admin/products - Add product")
    print("PUT  /api/admin/products/<id> - Update product")
    print("DEL  /api/admin/products/<id> - Delete product")
    print("PUT  /api/admin/products/<id>/toggle-visibility - Toggle visibility")
    print("GET  /api/admin/notifications - Get admin notifications")
    print("GET  /api/admin/orders - Get all orders for admin")
    print("PUT  /api/admin/orders/<id>/status - Update order status")
    print("=" * 60)
    print("🔑 Admin Credentials:")
    print(f"Username: {ADMIN_USERNAME}")
    print(f"Password: {ADMIN_PASSWORD}")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5001) 