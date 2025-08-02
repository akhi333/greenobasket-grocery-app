# GreenObasket Deployment Guide

## 🌱 Enhanced Organic Grocery App with PWA Features

### Quick Deployment Options

#### Option 1: Local Development
```bash
# Clone the repository
git clone https://github.com/akhi333/greenobasket-grocery-app.git
cd greenobasket-grocery-app

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

#### Option 2: Production Deployment

##### Render.com (Recommended)
1. Connect your GitHub repository to Render
2. Use the following build command: `pip install -r requirements.txt`
3. Use the following start command: `python main.py`
4. Set environment variables:
   - `PORT=5001` (optional, will auto-detect)
   - `FLASK_ENV=production`

##### Railway
1. Connect your GitHub repository
2. Railway will auto-detect the Python app
3. No additional configuration needed

##### Heroku
1. Create a `Procfile` with: `web: python main.py`
2. Deploy using Heroku CLI or GitHub integration

### Environment Variables for Production
```bash
PORT=5001                    # Port number (auto-detected on most platforms)
FLASK_ENV=production        # Set to production for deployment
SECRET_KEY=your-secret-key  # Change the default secret key
ADMIN_USERNAME=admin        # Admin username (can be customized)
ADMIN_PASSWORD=secure-pass  # Change default admin password
```

### Database Migration (Optional)
Currently uses in-memory storage. For production, consider:
- PostgreSQL for scalability
- SQLite for simple deployments
- MongoDB for NoSQL approach

### PWA Features Included
- ✅ Offline functionality with Service Worker
- ✅ App installation prompt
- ✅ Mobile-optimized interface
- ✅ Push notification ready
- ✅ App-like experience on mobile devices

### API Endpoints Available
- `/api/products` - Get all organic products
- `/api/products/organic-info/<id>` - Get detailed organic information
- `/api/search?q=<query>` - Enhanced organic-focused search
- `/api/cart/*` - Cart management
- `/api/orders/*` - Order processing
- `/admin` - Admin dashboard

### Organic Features
- 🌿 USDA Organic certification tracking
- 🚜 Farm source information
- 🍎 Nutritional benefits data
- 🌱 Pesticide-free and GMO-free indicators
- 🌍 Carbon footprint tracking
- 📅 Seasonal harvest information
- 🥬 Storage tips for organic products

### Performance Optimizations
- Service Worker caching for offline access
- Optimized product images
- Responsive design for all devices
- Fast search with organic keyword matching

### Security Considerations for Production
1. Change default admin credentials
2. Use environment variables for secrets
3. Enable HTTPS in production
4. Consider rate limiting for APIs
5. Implement proper session management

### Monitoring and Analytics
Consider adding:
- Google Analytics for user behavior
- Error tracking (Sentry)
- Performance monitoring
- Order and sales analytics

### Support and Maintenance
- Regular updates to product database
- Seasonal product availability updates
- Customer feedback integration
- Admin dashboard monitoring

---

## 🚀 Ready to Deploy!

Your GreenObasket organic grocery app is production-ready with modern PWA features and comprehensive organic product management.