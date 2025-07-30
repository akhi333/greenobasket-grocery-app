# 🌱 GreenObasket - Premium Grocery App

A modern, full-featured grocery ordering platform built with Flask and vanilla JavaScript.

![GreenObasket Screenshot](frontend/static/images/logo.png)

## ✨ Features

### 🛒 **Customer Features**
- **User Authentication** - Register, login, password reset with OTP
- **Product Browsing** - Category-wise product filtering
- **Smart Cart** - Add to cart with quantity management
- **Multiple Payment Options** - COD, UPI, Pay in App
- **Order Tracking** - Real-time order status updates
- **Responsive Design** - Works on desktop and mobile

### 👨‍💼 **Admin Features**
- **Product Management** - Add, edit, delete products
- **Order Management** - View and update order status
- **Inventory Control** - Stock management
- **Admin Dashboard** - Sales statistics and notifications
- **User Management** - View customer orders and data

### 🎯 **Technical Features**
- **RESTful API** - Clean API endpoints
- **Real-time Updates** - Live inventory and order updates
- **Image Management** - Product image handling
- **Session Management** - Secure user sessions
- **Error Handling** - Comprehensive error management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Modern web browser

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/greenobasket.git
   cd greenobasket
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python backend/app.py
   ```

4. **Open your browser**
   - **Customer App**: http://localhost:5001
   - **Admin Panel**: http://localhost:5001/admin

## 🔑 Default Credentials

### Admin Access
- **Username**: `admin`
- **Password**: `greenbasket123`

## 📱 API Endpoints

### User Authentication
- `POST /api/user/register` - Register new user
- `POST /api/user/login` - User login
- `POST /api/user/logout` - User logout

### Shopping
- `GET /api/products` - Get all products
- `GET /api/products?category=fruits` - Filter by category
- `POST /api/cart/add` - Add to cart
- `POST /api/orders` - Create order

### Admin
- `GET /admin` - Admin dashboard
- `POST /api/admin/products` - Add product
- `GET /api/admin/orders` - View all orders

## 🏗️ Project Structure

```
GreenObasket/
├── backend/
│   └── app.py                 # Flask application
├── frontend/
│   ├── grocery_app.html       # Customer interface
│   ├── admin_dashboard.html   # Admin interface
│   └── static/
│       └── images/            # Product images
├── requirements.txt           # Python dependencies
└── README.md                 # This file
```

## 🛠️ Technologies Used

- **Backend**: Flask, Python
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Storage**: In-memory database (easily upgradeable to SQL)
- **Authentication**: Session-based with tokens
- **Styling**: Custom CSS with modern design

## 🌟 Key Highlights

- **Zero Database Setup** - Runs immediately without database configuration
- **Mobile Responsive** - Optimized for all device sizes
- **Modern UI/UX** - Clean, intuitive interface
- **Scalable Architecture** - Easy to extend and modify
- **Production Ready** - Error handling and security considerations

## 📦 Deployment

This app is ready for deployment on platforms like:
- **Render** (Recommended)
- **Railway**
- **Heroku**
- **AWS**
- **DigitalOcean**

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

Built with ❤️ by [Your Name]

## 🙏 Acknowledgments

- Flask community for the excellent web framework
- All contributors and testers
- Inspiration from modern e-commerce platforms

---

**⭐ If you like this project, please give it a star on GitHub! ⭐** 