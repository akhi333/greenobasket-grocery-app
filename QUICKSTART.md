# 🚀 Quick Start Guide - GreenObasket

Get your grocery delivery app running in **2 minutes**!

## ⚡ Super Fast Setup

### Option 1: Automatic Setup (Recommended)
```bash
# 1. Install dependencies
python setup.py install

# 2. Run the app
python setup.py run
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Run the app
python app.py
```

## 🌐 Access Your App

**🛒 Customer App (Shopping):**
- URL: http://localhost:5001
- Features: Browse products, add to cart, checkout

**👨‍💼 Admin Panel (Management):**
- URL: http://localhost:5001/admin
- Username: `admin`
- Password: `greenbasket123`

## 🎯 Test the Features

### As a Customer:
1. ✅ Browse organic products
2. ✅ Add items with gram selection (250g-10000g)
3. ✅ See live cart total on left sidebar
4. ✅ Click "Proceed to Checkout"
5. ✅ Use saved address or enter new one
6. ✅ Choose payment method (UPI/COD/Pay Later)
7. ✅ Complete order

### As an Admin:
1. ✅ Login to admin panel
2. ✅ Add/edit products
3. ✅ Manage stock levels
4. ✅ View order notifications
5. ✅ Check detailed order items
6. ✅ Hide/show products

## 📱 Key Features

| Feature | Customer | Admin |
|--------|----------|-------|
| Product browsing | ✅ | ✅ |
| Gram-based ordering | ✅ | - |
| Live cart | ✅ | - |
| Saved addresses | ✅ | - |
| Order management | - | ✅ |
| Stock control | - | ✅ |
| Notifications | - | ✅ |

## 🛠 Troubleshooting

**Port already in use?**
```bash
# The app uses port 5001, check if anything is running on it
lsof -i :5001
```

**Missing dependencies?**
```bash
pip install flask flask-cors
```

**Can't access admin?**
- Check you're using the correct URL: http://localhost:5001/admin
- Username: `admin`, Password: `greenbasket123`

## 📂 Project Structure
```
GreenObasket/
├── 🎯 QUICKSTART.md     ← You are here
├── 📋 PROJECT_STRUCTURE.md
├── ⚙️ setup.py
├── backend/
│   ├── app.py          ← Flask server
│   └── requirements.txt
├── frontend/
│   ├── grocery_app.html    ← Customer app
│   └── admin_dashboard.html ← Admin panel
└── docs/
    └── README.md       ← Full documentation
```

## 🎉 You're Ready!

Your GreenObasket grocery app is now running! 

Start shopping at: http://localhost:5001 🛒 