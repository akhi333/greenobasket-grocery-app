# 🌱 GreenObasket - Project Structure

## 📁 Directory Organization

```
GreenObasket/
├── backend/                 # Flask Backend Server
│   ├── app.py              # Main Flask application with APIs
│   └── requirements.txt    # Python dependencies
│
├── frontend/               # User Interface Files
│   ├── grocery_app.html    # Customer shopping interface
│   └── admin_dashboard.html # Admin management panel
│
├── docs/                   # Documentation
│   └── README.md          # Complete project documentation
│
├── static/                 # Static assets (CSS, JS, images)
│   └── images/
│       ├── products/       # Product photos (bananas.jpg, apples.jpg, etc.)
│       ├── categories/     # Category icons (fruits.png, vegetables.png, etc.)
│       └── icons/          # App icons (logo.png, cart.png, admin.png)
│
└── PROJECT_STRUCTURE.md   # This file - project overview
```

## 🎯 File Descriptions

### Backend (`/backend/`)
- **`app.py`** - Core Flask application containing:
  - REST API endpoints
  - Product management
  - Cart functionality
  - Order processing
  - Customer data persistence
  - Admin notifications

- **`requirements.txt`** - Python package dependencies:
  - Flask (web framework)
  - Flask-CORS (cross-origin requests)
  - UUID (unique identifiers)

### Frontend (`/frontend/`)
- **`grocery_app.html`** - Customer interface featuring:
  - Product browsing with categories
  - Gram-based quantity selection (250g-10000g)
  - Live cart sidebar with real-time totals
  - Saved address functionality
  - Multiple payment methods (UPI, COD, Pay Later)
  - Responsive design

- **`admin_dashboard.html`** - Admin panel providing:
  - Product CRUD operations
  - Stock management
  - Product visibility controls
  - Order notifications with detailed views
  - Sales statistics

## 🚀 Quick Start

### 1. Install Dependencies
```bash
cd GreenObasket/backend
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python app.py
```

### 3. Access the Application
- **Customer App**: http://localhost:5001
- **Admin Panel**: http://localhost:5001/admin

## 🔐 Admin Credentials
- **Username**: admin
- **Password**: greenbasket123

## 🎨 Key Features

### Customer Features
- ✅ Gram-based product ordering
- ✅ Saved address persistence
- ✅ Live cart with instant calculations
- ✅ Multiple payment options
- ✅ Real-time stock updates

### Admin Features
- ✅ Complete product management
- ✅ Order notification system
- ✅ Detailed order tracking
- ✅ Stock monitoring
- ✅ Product visibility controls

## 📱 Technology Stack
- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Storage**: In-memory (can be extended to database)
- **APIs**: RESTful JSON APIs

## 🔄 Development Workflow
1. Backend changes → Edit `backend/app.py`
2. Frontend changes → Edit files in `frontend/`
3. New features → Update both backend APIs and frontend
4. Documentation → Update `docs/README.md`

## 📞 Support
For questions or issues, refer to the complete documentation in `docs/README.md` 