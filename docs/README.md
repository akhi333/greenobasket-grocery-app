# GreenObasket - Premium Online Grocery Store

A modern, responsive premium organic grocery store built with Flask backend and vanilla JavaScript frontend, featuring comprehensive admin controls and authentic Indian products.

## 🌟 Features

### Customer Features
- 🛒 **Live Shopping Cart**: Real-time cart sidebar with instant calculations and smart delivery logic
- 💰 **Smart Delivery**: FREE delivery on orders ≥ ₹200, 10% delivery fee on smaller orders
- 📱 **UPI Payments**: Integrated PhonePe/Google Pay/Paytm support via secure UPI links  
- 🔍 **Advanced Search**: Search by name, description, or category with instant results
- 🏷️ **Horizontal Categories**: Smooth scrolling category navigation with "All Products" button
- 📱 **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- 🛍️ **Enhanced Checkout**: Complete address collection with mobile verification
- ⭐ **Product Ratings**: Detailed customer ratings and reviews
- 📊 **Auto-Refresh**: Hidden products automatically removed from cart
- 🌿 **Organic Focus**: Premium organic and fresh products
- 🇮🇳 **Indian Specialties**: Authentic Indian spices, oils, pickles, and fresh produce

### Admin Features
- 🔐 **Secure Admin Panel**: Password-protected dashboard
- 🔔 **Real-time Notifications**: Instant order alerts with complete customer details
- ➕ **Product Management**: Add, edit, and delete products
- 👁️ **Visibility Control**: Hide/show products from customer view (auto-removes from carts)
- 📊 **Analytics Dashboard**: Real-time business statistics and order tracking
- 🏪 **Inventory Management**: Stock tracking and management
- 🖼️ **Image Management**: Support for Google Drive and other image sources
- 📱 **Auto-refresh**: Notifications update every 30 seconds

### Technical Features
- **RESTful API**: Clean, well-documented API endpoints
- **Session Management**: Persistent cart across browser sessions
- **Real-time Updates**: Dynamic content loading without page refresh
- **Comprehensive Error Handling**: User-friendly error messages
- **Stock Management**: Automatic stock deduction on orders
- **Admin Authentication**: Secure login system for administrators

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd greenobasket-grocery-app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - 🌐 **Customer Store**: http://localhost:5001
   - 🔒 **Admin Panel**: http://localhost:5001/admin
   - 🔗 **API Base**: http://localhost:5001/api

### Admin Access
- **Username**: `admin`
- **Password**: `greenbasket123`

## 📡 API Endpoints

### Customer Endpoints
- `GET /api/products` - Get all visible products
- `GET /api/products/<id>` - Get specific product
- `GET /api/categories` - Get all product categories
- `GET /api/cart/<session_id>` - Get cart contents
- `POST /api/cart/<session_id>/add` - Add item to cart
- `PUT /api/cart/<session_id>/update` - Update item quantity
- `DELETE /api/cart/<session_id>/remove` - Remove item from cart
- `POST /api/orders` - Create new order
- `GET /api/orders/<id>` - Get order details
- `GET /api/stats` - Get application statistics

### Admin Endpoints (Requires Authentication)
- `GET /admin` - Admin dashboard
- `POST /admin/login` - Admin login
- `GET /admin/logout` - Admin logout
- `GET /api/admin/products/all` - Get all products (including hidden)
- `POST /api/admin/products` - Add new product
- `PUT /api/admin/products/<id>` - Update product
- `DELETE /api/admin/products/<id>` - Delete product
- `PUT /api/admin/products/<id>/toggle-visibility` - Toggle product visibility

## 🛍️ Product Categories

### 🍎 Fresh Fruits
- Organic Bananas, Himalayan Apples
- Alphonso & Kesar Mangoes
- Organic Pomegranates, Papayas, Guavas
- Premium Avocados

### 🥕 Organic Vegetables
- Farm Fresh Tomatoes, Baby Spinach
- Fresh Ginger, Garlic, Turmeric Root
- Organic Onions, Potatoes
- Brinjal, Okra (Bhindi)

### 🌿 Leafy Vegetables & Herbs
- Fresh Coriander, Mint Leaves
- Organic Fenugreek Leaves (Methi)
- Aromatic Curry Leaves

### 🌶️ Spices & Condiments
- Organic Turmeric Powder
- Red Chilli Powder
- Handground Garam Masala
- Whole Cumin Seeds, Black Mustard Seeds

### 🛢️ Organic Oils
- Cold-Pressed Coconut Oil
- Organic Mustard Oil
- Premium Sesame Oil

### 🥜 Nuts & Dry Fruits
- Premium Dry Fruits Mix
- Dry Coconut (Copra)

### 🥒 Pickles & Traditional Foods
- Homemade Mango Pickle
- Organic Lemon Pickle
- Mixed Vegetable Pickle

### 🥛 Dairy & Fresh
- A2 Organic Milk
- Fresh Paneer

### 🍹 Beverages
- Cold-Pressed Juices
- Probiotic Kombucha

### 🍯 Healthy Snacks
- Raw Organic Honey
- Baked Quinoa Chips
- Artisan Sourdough Bread

## 🖼️ Image Management

### Google Drive Integration
You can use Google Drive images by converting the sharing link:

**Original Format:**
```
https://drive.google.com/file/d/FILE_ID/view?usp=sharing
```

**Direct Access Format:**
```
https://drive.google.com/uc?export=view&id=FILE_ID
```

### Supported Image Sources
- Google Drive (converted links)
- Unsplash
- Any direct image URL
- Local images (relative paths)

## 🔧 Technical Stack

- **Backend**: Flask (Python) with session management
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Storage**: In-memory with persistent sessions
- **Styling**: Custom CSS with mobile-first responsive design
- **Icons**: Font Awesome 6.0
- **Authentication**: Flask sessions with secure cookies

## 👨‍💼 Admin Panel Features

### Dashboard Overview
- 📊 **Real-time Statistics**: Products, orders, revenue, active carts
- 📈 **Visual Analytics**: Clean, modern dashboard design

### Product Management
- ➕ **Add Products**: Rich form with all product details
- ✏️ **Edit Products**: Inline editing with validation
- 🗑️ **Delete Products**: Safe deletion with confirmation
- 👁️ **Visibility Toggle**: Hide/show products from customers
- 📦 **Stock Management**: Real-time stock tracking

### Advanced Features
- 🔐 **Secure Authentication**: Session-based login system
- 📱 **Mobile-Optimized**: Responsive admin interface
- 🎨 **Modern UI**: Clean, professional design
- ⚡ **Real-time Updates**: Instant feedback and updates

## 🛡️ Security Features

- Session-based authentication
- CSRF protection ready
- Input validation and sanitization
- Secure password handling
- Error message sanitization

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Considerations
1. **Database**: Replace in-memory storage with PostgreSQL/MySQL
2. **Authentication**: Implement OAuth or JWT tokens
3. **Security**: Add HTTPS, rate limiting, input validation
4. **Performance**: Add Redis caching, CDN for images
5. **Monitoring**: Implement logging and error tracking
6. **Scaling**: Use Docker, load balancers

### Environment Variables
```bash
export FLASK_ENV=production
export SECRET_KEY=your-secret-key
export ADMIN_USERNAME=your-admin-username
export ADMIN_PASSWORD=your-secure-password
```

## 🔧 Customization

### Adding New Products
```python
{
    "id": unique_id,
    "name": "Product Name",
    "category": "category_name", 
    "price": 150.0,
    "image": "image_url",
    "description": "Detailed description",
    "stock": 25,
    "rating": 4.5,
    "visible": True
}
```

### Adding New Categories
Update both backend categories list and frontend category handling.

## 🐛 Troubleshooting

### Common Issues

1. **Port 5001 already in use**
   ```python
   app.run(debug=True, host='0.0.0.0', port=5002)
   ```

2. **Admin access issues**
   - Check username/password combination
   - Clear browser cookies and try again

3. **Image loading problems**
   - Verify Google Drive links are in correct format
   - Check image URLs are publicly accessible

4. **Cart persistence issues**
   - Enable browser cookies
   - Check session storage

## 📱 Browser Compatibility

- ✅ Chrome 80+
- ✅ Firefox 75+  
- ✅ Safari 13+
- ✅ Edge 80+
- ❌ Internet Explorer (not supported)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🚀 Future Roadmap

### 📱 Mobile App Development
We're planning to expand GreenObasket to mobile platforms:

- **🤖 Android App**: Google Play Store release
- **🍎 iOS App**: Apple App Store release
- **📱 React Native**: Cross-platform development
- **🔄 Sync**: Real-time data sync between web and mobile
- **📳 Push Notifications**: Order updates and promotional offers
- **📍 GPS Integration**: Location-based delivery tracking
- **📷 Barcode Scanner**: Quick product search and add-to-cart

### 🆕 Upcoming Features
- **🎯 Personalized Recommendations**: AI-powered product suggestions
- **🎁 Loyalty Program**: Reward points and exclusive offers
- **📊 Advanced Analytics**: Business intelligence dashboard
- **🌍 Multi-language Support**: Regional language options
- **💳 Enhanced Payment**: UPI, Wallet, and cryptocurrency support
- **🚚 Real-time Tracking**: Live delivery status updates
- **⭐ Review System**: Customer ratings and detailed reviews

## 📞 Support

For support and questions:
- 📚 Check the documentation above
- 🐛 Create an issue for bugs
- 💡 Submit feature requests
- 📧 Contact the development team
- 📱 Mobile app inquiries: contact@greenobasket.com

## 📈 Performance & Scalability

### Current Architecture
- **Frontend**: Responsive web application
- **Backend**: Flask with session management
- **Storage**: In-memory (development)
- **Real-time**: Auto-refresh notifications

### Production Ready Features
- **📊 Live Cart**: Real-time cart updates with delivery calculation
- **🔔 Admin Notifications**: Instant order alerts for administrators
- **💰 Smart Pricing**: Dynamic delivery fee calculation
- **📱 Mobile-First**: Responsive design for all devices
- **🔒 Secure Checkout**: Multiple payment options with validation
- **📦 Stock Management**: Real-time inventory tracking

---

**GreenObasket** - Your trusted partner for fresh, organic groceries delivered to your doorstep! 🌱🛒🥬

*Ready for mobile app deployment on Google Play Store and Apple App Store* 📱✨ 