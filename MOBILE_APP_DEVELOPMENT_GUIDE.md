# 📱 GreenObasket Mobile App Development Guide

**Complete guide for developing Android & iOS mobile apps for GreenObasket Grocery Store**

---

## 🎯 Overview

This guide provides step-by-step instructions for developing mobile applications for the GreenObasket grocery delivery platform. Since you have already:
- ✅ Installed Android Studio
- ✅ Cloned the repository
- ✅ Web application running successfully

Let's now create native mobile apps!

---

## 📋 Prerequisites Checklist

### Required Software:
- [x] **Android Studio** - Already installed ✅
- [ ] **Node.js** (v16+) - For React Native development
- [ ] **React Native CLI** - Cross-platform mobile development
- [ ] **Java Development Kit** (JDK 11+) - For Android development
- [ ] **Xcode** (Mac only) - For iOS development

### Accounts Needed:
- [ ] **Google Play Console** account - For Android app publishing
- [ ] **Apple Developer** account ($99/year) - For iOS app publishing
- [ ] **Firebase** account - For push notifications

---

## 🚀 Development Options

### Option 1: React Native (Recommended) 🌟
**Best for**: Cross-platform development (Android + iOS from single codebase)
- ✅ Single codebase for both platforms
- ✅ Faster development
- ✅ Easier maintenance
- ✅ Perfect for grocery app UI

### Option 2: Native Android (Kotlin/Java)
**Best for**: Android-specific optimizations
- ✅ Full Android feature access
- ✅ Best performance on Android
- ❌ Requires separate iOS development

### Option 3: Native iOS (Swift)
**Best for**: iOS-specific features
- ✅ Full iOS feature access
- ✅ Best performance on iOS
- ❌ Requires separate Android development

---

## 🛠 Setup Instructions

### Step 1: Install Node.js and React Native

```bash
# 1. Install Node.js (if not already installed)
# Download from: https://nodejs.org/

# 2. Verify Node.js installation
node --version
npm --version

# 3. Install React Native CLI
npm install -g react-native-cli
npm install -g @react-native-community/cli

# 4. Verify React Native installation
npx react-native --version
```

### Step 2: Create React Native Project Structure

```bash
# Navigate to your GreenObasket directory
cd /path/to/greenobasket-grocery-app

# Create React Native mobile app
npx react-native init GreenObasketMobile --template react-native-template-typescript

# Navigate to the new mobile project
cd GreenObasketMobile
```

### Step 3: Install Required Dependencies

```bash
# Navigation
npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs

# HTTP Client
npm install axios

# State Management
npm install @reduxjs/toolkit react-redux

# UI Components
npm install react-native-elements react-native-vector-icons

# Camera/Scanner
npm install react-native-camera react-native-qrcode-scanner

# Location Services
npm install @react-native-community/geolocation

# Push Notifications
npm install @react-native-firebase/app @react-native-firebase/messaging

# Image Picker
npm install react-native-image-picker

# Async Storage
npm install @react-native-async-storage/async-storage

# Platform-specific installations
cd ios && pod install && cd .. # For iOS
```

---

## 📱 Mobile App Architecture

### Project Structure:
```
GreenObasketMobile/
├── src/
│   ├── components/          # Reusable UI components
│   │   ├── ProductCard/
│   │   ├── CartItem/
│   │   ├── Header/
│   │   └── SearchBar/
│   ├── screens/             # App screens
│   │   ├── HomeScreen/
│   │   ├── ProductListScreen/
│   │   ├── ProductDetailScreen/
│   │   ├── CartScreen/
│   │   ├── CheckoutScreen/
│   │   ├── ProfileScreen/
│   │   └── AuthScreen/
│   ├── services/            # API calls
│   │   ├── api.js
│   │   ├── auth.js
│   │   └── products.js
│   ├── store/              # Redux store
│   │   ├── slices/
│   │   └── index.js
│   ├── utils/              # Helper functions
│   │   ├── constants.js
│   │   ├── helpers.js
│   │   └── validators.js
│   └── assets/             # Images, fonts
│       ├── images/
│       └── fonts/
├── android/                # Android-specific files
├── ios/                    # iOS-specific files
└── package.json
```

### Core Features to Implement:

#### 1. **Authentication System** 🔐
- User registration/login
- OTP verification
- Guest session support
- Session management

#### 2. **Product Catalog** 🛒
- Category browsing
- Product search
- Product details with images
- Gram-based quantity selection
- Stock availability

#### 3. **Shopping Cart** 🛍️
- Add/remove items
- Update quantities
- Real-time total calculation
- Persistent cart storage

#### 4. **Checkout Process** 💳
- Address management
- Payment integration (UPI, COD)
- Order confirmation
- Delivery tracking

#### 5. **User Profile** 👤
- Profile management
- Order history
- Saved addresses
- Settings

#### 6. **Push Notifications** 📢
- Order updates
- Promotional offers
- Stock alerts

#### 7. **Barcode Scanner** 📷
- Quick product addition
- Product verification
- Inventory management

#### 8. **GPS Integration** 📍
- Location detection
- Delivery tracking
- Service area validation

---

## 🔧 Configuration Steps

### Step 1: API Integration Setup

Create `src/services/api.js`:

```javascript
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Your Flask backend URL
const BASE_URL = 'http://YOUR_BACKEND_IP:5001/api';

class APIService {
  constructor() {
    this.api = axios.create({
      baseURL: BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add auth token to requests
    this.api.interceptors.request.use(async (config) => {
      const token = await AsyncStorage.getItem('userToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  // Authentication
  async login(mobile, password) {
    const response = await this.api.post('/user/login', { mobile, password });
    return response.data;
  }

  async register(userData) {
    const response = await this.api.post('/user/register', userData);
    return response.data;
  }

  // Products
  async getProducts() {
    const response = await this.api.get('/products');
    return response.data;
  }

  async getProduct(id) {
    const response = await this.api.get(`/products/${id}`);
    return response.data;
  }

  // Cart
  async getCart() {
    const response = await this.api.get('/cart');
    return response.data;
  }

  async addToCart(productId, quantity) {
    const response = await this.api.post('/cart/add', { 
      product_id: productId, 
      quantity 
    });
    return response.data;
  }

  // Orders
  async createOrder(orderData) {
    const response = await this.api.post('/orders', orderData);
    return response.data;
  }
}

export default new APIService();
```

### Step 2: Configure Android Development

1. **Android Studio Setup**:
   ```bash
   # Open Android Studio
   # Go to Tools → SDK Manager
   # Install Android SDK Platform 33 (or latest)
   # Install Android SDK Build-Tools 33.0.0
   # Install Google Play services
   ```

2. **Environment Variables** (Add to `~/.bashrc` or `~/.zshrc`):
   ```bash
   export ANDROID_HOME=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/tools
   export PATH=$PATH:$ANDROID_HOME/tools/bin
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```

3. **Create Android Virtual Device (AVD)**:
   - Open Android Studio
   - Tools → AVD Manager
   - Create Virtual Device
   - Choose a device (Pixel 4 recommended)
   - Download Android API Level 33
   - Create and start emulator

### Step 3: Configure App Icons and Splash Screen

1. **App Icon Generation**:
   - Use your logo from `/static/images/icons/`
   - Generate icons for all sizes: https://appicon.co/
   - Replace default icons in:
     - `android/app/src/main/res/mipmap-*`
     - `ios/GreenObasketMobile/Images.xcassets/AppIcon.appiconset/`

2. **Splash Screen**:
   ```bash
   npm install react-native-splash-screen
   # Configure as per package documentation
   ```

---

## 🚀 Running Your Mobile App

### For Android:

```bash
# Start Metro bundler
npm start

# In another terminal, run Android app
npx react-native run-android

# Or with specific device
npx react-native run-android --deviceId=DEVICE_ID
```

### For iOS (Mac only):

```bash
# Start Metro bundler
npm start

# In another terminal, run iOS app
npx react-native run-ios

# Or with specific simulator
npx react-native run-ios --simulator="iPhone 14 Pro"
```

---

## 📦 Key Implementation Examples

### Product List Screen:

```typescript
import React, { useEffect, useState } from 'react';
import {
  View,
  FlatList,
  StyleSheet,
  ActivityIndicator,
  Text,
} from 'react-native';
import APIService from '../services/api';
import ProductCard from '../components/ProductCard';

const ProductListScreen = ({ navigation, route }) => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const { category } = route.params || {};

  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const data = await APIService.getProducts();
      let filteredProducts = data.products || [];
      
      if (category) {
        filteredProducts = filteredProducts.filter(
          p => p.category.toLowerCase() === category.toLowerCase()
        );
      }
      
      setProducts(filteredProducts);
    } catch (error) {
      console.error('Error loading products:', error);
    } finally {
      setLoading(false);
    }
  };

  const renderProduct = ({ item }) => (
    <ProductCard
      product={item}
      onPress={() => navigation.navigate('ProductDetail', { product: item })}
      onAddToCart={(product, quantity) => handleAddToCart(product, quantity)}
    />
  );

  const handleAddToCart = async (product, quantity) => {
    try {
      await APIService.addToCart(product.id, quantity);
      // Show success message
    } catch (error) {
      console.error('Error adding to cart:', error);
    }
  };

  if (loading) {
    return (
      <View style={styles.loadingContainer}>
        <ActivityIndicator size="large" color="#2ecc71" />
        <Text>Loading organic products...</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <FlatList
        data={products}
        renderItem={renderProduct}
        keyExtractor={(item) => item.id}
        numColumns={2}
        contentContainerStyle={styles.listContainer}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f8f9fa',
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContainer: {
    padding: 16,
  },
});

export default ProductListScreen;
```

---

## 🔔 Push Notifications Setup

### Firebase Configuration:

1. **Create Firebase Project**:
   - Go to https://console.firebase.google.com/
   - Create new project: "GreenObasket"
   - Enable Cloud Messaging

2. **Android Configuration**:
   - Download `google-services.json`
   - Place in `android/app/`
   - Update `android/build.gradle` and `android/app/build.gradle`

3. **iOS Configuration**:
   - Download `GoogleService-Info.plist`
   - Add to iOS project in Xcode

4. **Implementation**:
   ```javascript
   import messaging from '@react-native-firebase/messaging';

   // Request permission (iOS)
   const requestUserPermission = async () => {
     const authStatus = await messaging().requestPermission();
     return authStatus === messaging.AuthorizationStatus.AUTHORIZED;
   };

   // Get FCM token
   const getFCMToken = async () => {
     const fcmToken = await messaging().getToken();
     console.log('FCM Token:', fcmToken);
     return fcmToken;
   };

   // Handle foreground messages
   messaging().onMessage(async remoteMessage => {
     console.log('Foreground message:', remoteMessage);
   });
   ```

---

## 📍 GPS Integration

```javascript
import Geolocation from '@react-native-community/geolocation';
import { PermissionsAndroid, Platform } from 'react-native';

const LocationService = {
  async requestLocationPermission() {
    if (Platform.OS === 'android') {
      const granted = await PermissionsAndroid.request(
        PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION
      );
      return granted === PermissionsAndroid.RESULTS.GRANTED;
    }
    return true;
  },

  async getCurrentLocation() {
    return new Promise((resolve, reject) => {
      Geolocation.getCurrentPosition(
        position => {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
        },
        error => reject(error),
        { enableHighAccuracy: true, timeout: 15000, maximumAge: 10000 }
      );
    });
  },

  calculateDeliveryFee(userLat, userLng) {
    const storeLat = 17.385044; // Your store location
    const storeLng = 78.486671;
    
    const distance = this.calculateDistance(userLat, userLng, storeLat, storeLng);
    
    if (distance <= 10) return 0; // Free delivery within 10km
    return Math.min((distance - 10) * 5, 100); // ₹5/km, max ₹100
  },

  calculateDistance(lat1, lng1, lat2, lng2) {
    // Haversine formula implementation
    const R = 6371; // Earth's radius in kilometers
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLng = (lng2 - lng1) * Math.PI / 180;
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLng/2) * Math.sin(dLng/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    return R * c;
  }
};

export default LocationService;
```

---

## 📷 Barcode Scanner Integration

```bash
# Install barcode scanner
npm install react-native-qrcode-scanner react-native-camera
```

```javascript
import QRCodeScanner from 'react-native-qrcode-scanner';
import { RNCamera } from 'react-native-camera';

const BarcodeScannerScreen = ({ navigation }) => {
  const onSuccess = async (e) => {
    try {
      // e.data contains the barcode data
      const productId = e.data;
      
      // Search for product by barcode
      const product = await APIService.getProductByBarcode(productId);
      
      if (product) {
        navigation.navigate('ProductDetail', { product });
      } else {
        Alert.alert('Product not found', 'This product is not available in our store.');
      }
    } catch (error) {
      console.error('Barcode scan error:', error);
    }
  };

  return (
    <QRCodeScanner
      onRead={onSuccess}
      flashMode={RNCamera.Constants.FlashMode.auto}
      topContent={
        <Text style={styles.centerText}>
          Point camera at product barcode
        </Text>
      }
      bottomContent={
        <TouchableOpacity style={styles.buttonTouchable}>
          <Text style={styles.buttonText}>OK. Got it!</Text>
        </TouchableOpacity>
      }
    />
  );
};
```

---

## 🚀 App Store Deployment

### Android (Google Play Store):

1. **Generate Signed APK**:
   ```bash
   cd android
   ./gradlew assembleRelease
   ```

2. **Upload to Play Console**:
   - Create app listing
   - Upload APK/Bundle
   - Complete store listing
   - Submit for review

### iOS (Apple App Store):

1. **Build for Release**:
   ```bash
   npx react-native run-ios --configuration Release
   ```

2. **Archive in Xcode**:
   - Open project in Xcode
   - Product → Archive
   - Distribute to App Store Connect

---

## 🎯 Next Steps & Development Timeline

### Week 1-2: Setup & Basic Structure
- [x] ✅ Analyze existing web app
- [ ] 🔄 Set up React Native project
- [ ] 🔄 Configure development environment
- [ ] 🔄 Create basic navigation structure
- [ ] 🔄 Design UI components library

### Week 3-4: Core Features Implementation
- [ ] 📱 User authentication system
- [ ] 🛒 Product catalog & search
- [ ] 🛍️ Shopping cart functionality
- [ ] 💳 Checkout process
- [ ] 👤 User profile management

### Week 5-6: Advanced Features
- [ ] 🔔 Push notifications
- [ ] 📍 GPS & location services
- [ ] 📷 Barcode scanner
- [ ] 📦 Order tracking
- [ ] ⭐ Product reviews & ratings

### Week 7-8: Testing & Deployment
- [ ] 🧪 Unit testing
- [ ] 🔧 Performance optimization
- [ ] 📱 Device testing (Android/iOS)
- [ ] 🚀 App store submission
- [ ] 📊 Analytics integration

---

## 🆘 Troubleshooting & Support

### Common Issues:

1. **Metro bundler not starting**:
   ```bash
   npx react-native start --reset-cache
   ```

2. **Android build fails**:
   ```bash
   cd android && ./gradlew clean && cd ..
   npx react-native run-android
   ```

3. **iOS build fails**:
   ```bash
   cd ios && pod install && cd ..
   npx react-native run-ios
   ```

### Getting Help:
- 📚 React Native Documentation: https://reactnative.dev/
- 💬 Community Support: https://github.com/facebook/react-native/discussions
- 🐛 Issue Reporting: Create GitHub issues in your repository

---

## 📞 Support & Contact

For additional support with mobile app development:
- 📧 Technical queries: Create GitHub issues
- 🔧 Development support: Check documentation links
- 📱 Mobile-specific help: React Native community forums

---

**🎉 You're now ready to build a world-class mobile grocery delivery app!**

Start with the setup instructions above, and refer back to this guide as you implement each feature. Happy coding! 🚀📱