#!/bin/bash

# 📱 GreenObasket Mobile App Setup Script
# This script automates the mobile app development environment setup

set -e  # Exit on any error

echo "🌱 GreenObasket Mobile App Setup Starting..."
echo "============================================================"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running on macOS or Linux
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="Linux"
else
    print_error "Unsupported operating system. This script supports macOS and Linux."
    exit 1
fi

print_info "Detected OS: $OS"

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
check_prerequisites() {
    echo ""
    echo "🔍 Checking Prerequisites..."
    echo "----------------------------------------"
    
    # Check Node.js
    if command_exists node; then
        NODE_VERSION=$(node --version)
        print_status "Node.js installed: $NODE_VERSION"
        
        # Check if version is >= 16
        MAJOR_VERSION=$(echo $NODE_VERSION | cut -d'v' -f2 | cut -d'.' -f1)
        if [ "$MAJOR_VERSION" -lt 16 ]; then
            print_warning "Node.js version should be >= 16. Current: $NODE_VERSION"
            print_info "Please update Node.js: https://nodejs.org/"
        fi
    else
        print_error "Node.js not found. Please install Node.js first: https://nodejs.org/"
        exit 1
    fi
    
    # Check npm
    if command_exists npm; then
        NPM_VERSION=$(npm --version)
        print_status "npm installed: $NPM_VERSION"
    else
        print_error "npm not found. Please install Node.js with npm."
        exit 1
    fi
    
    # Check Java (for Android development)
    if command_exists java; then
        JAVA_VERSION=$(java -version 2>&1 | head -n1)
        print_status "Java installed: $JAVA_VERSION"
    else
        print_warning "Java not found. Install JDK 11+ for Android development."
        print_info "Download from: https://www.oracle.com/java/technologies/downloads/"
    fi
    
    # Check Android Studio / Android SDK
    if [ -d "$HOME/Android/Sdk" ] || [ -d "$HOME/Library/Android/sdk" ]; then
        print_status "Android SDK found"
    else
        print_warning "Android SDK not found. Make sure Android Studio is installed."
        print_info "Download from: https://developer.android.com/studio"
    fi
    
    # Check for Xcode (macOS only)
    if [[ "$OS" == "macOS" ]]; then
        if command_exists xcodebuild; then
            XCODE_VERSION=$(xcodebuild -version | head -n1)
            print_status "Xcode installed: $XCODE_VERSION"
        else
            print_warning "Xcode not found. Install from App Store for iOS development."
        fi
        
        if command_exists pod; then
            POD_VERSION=$(pod --version)
            print_status "CocoaPods installed: $POD_VERSION"
        else
            print_warning "CocoaPods not found. Installing..."
            sudo gem install cocoapods
            print_status "CocoaPods installed"
        fi
    fi
}

# Install React Native CLI
install_react_native_cli() {
    echo ""
    echo "📱 Installing React Native CLI..."
    echo "----------------------------------------"
    
    if command_exists npx && npx react-native --version >/dev/null 2>&1; then
        print_status "React Native CLI already installed"
    else
        print_info "Installing React Native CLI globally..."
        npm install -g @react-native-community/cli
        print_status "React Native CLI installed"
    fi
}

# Create React Native project
create_react_native_project() {
    echo ""
    echo "🚀 Creating React Native Project..."
    echo "----------------------------------------"
    
    PROJECT_NAME="GreenObasketMobile"
    
    if [ -d "$PROJECT_NAME" ]; then
        print_warning "Project directory '$PROJECT_NAME' already exists."
        read -p "Do you want to remove it and create a new one? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$PROJECT_NAME"
            print_info "Removed existing project directory"
        else
            print_info "Using existing project directory"
            return
        fi
    fi
    
    print_info "Creating new React Native project with TypeScript..."
    npx react-native init "$PROJECT_NAME" --template react-native-template-typescript
    
    print_status "React Native project created: $PROJECT_NAME"
}

# Install project dependencies
install_dependencies() {
    echo ""
    echo "📦 Installing Mobile App Dependencies..."
    echo "----------------------------------------"
    
    cd GreenObasketMobile
    
    print_info "Installing navigation dependencies..."
    npm install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs
    npm install react-native-screens react-native-safe-area-context
    
    print_info "Installing HTTP client..."
    npm install axios
    
    print_info "Installing state management..."
    npm install @reduxjs/toolkit react-redux
    
    print_info "Installing UI components..."
    npm install react-native-elements react-native-vector-icons
    
    print_info "Installing utility libraries..."
    npm install @react-native-async-storage/async-storage
    npm install react-native-image-picker
    npm install @react-native-community/geolocation
    
    print_info "Installing camera and scanner..."
    npm install react-native-qrcode-scanner react-native-camera
    
    print_info "Installing Firebase (for push notifications)..."
    npm install @react-native-firebase/app @react-native-firebase/messaging
    
    print_status "All dependencies installed successfully!"
    
    cd ..
}

# Setup iOS dependencies (macOS only)
setup_ios_dependencies() {
    if [[ "$OS" != "macOS" ]]; then
        return
    fi
    
    echo ""
    echo "🍎 Setting up iOS Dependencies..."
    echo "----------------------------------------"
    
    cd GreenObasketMobile/ios
    
    print_info "Installing iOS pods..."
    pod install
    
    print_status "iOS dependencies installed successfully!"
    
    cd ../..
}

# Create basic project structure
create_project_structure() {
    echo ""
    echo "📁 Creating Project Structure..."
    echo "----------------------------------------"
    
    cd GreenObasketMobile
    
    # Create directory structure
    mkdir -p src/{components,screens,services,store,utils,assets/{images,fonts}}
    mkdir -p src/components/{ProductCard,CartItem,Header,SearchBar}
    mkdir -p src/screens/{HomeScreen,ProductListScreen,ProductDetailScreen,CartScreen,CheckoutScreen,ProfileScreen,AuthScreen}
    mkdir -p src/store/slices
    
    print_status "Project structure created"
    
    cd ..
}

# Create configuration files
create_config_files() {
    echo ""
    echo "⚙️ Creating Configuration Files..."
    echo "----------------------------------------"
    
    cd GreenObasketMobile
    
    # API Configuration
    cat > src/utils/constants.js << 'EOF'
// GreenObasket Mobile App Constants

export const API_CONFIG = {
  // Update this with your actual backend URL
  BASE_URL: __DEV__ ? 'http://10.0.2.2:5001/api' : 'https://your-production-url.com/api',
  TIMEOUT: 10000,
};

export const APP_CONFIG = {
  name: 'GreenObasket',
  version: '1.0.0',
  supportEmail: 'support@greenobasket.com',
};

export const COLORS = {
  primary: '#2ecc71',
  secondary: '#27ae60',
  accent: '#f39c12',
  background: '#f8f9fa',
  surface: '#ffffff',
  text: '#2c3e50',
  textLight: '#7f8c8d',
  error: '#e74c3c',
  success: '#2ecc71',
  warning: '#f39c12',
};

export const SIZES = {
  base: 16,
  small: 12,
  medium: 18,
  large: 24,
  xlarge: 32,
};

export const SPACING = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
  xxl: 48,
};
EOF

    # API Service
    cat > src/services/api.js << 'EOF'
import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { API_CONFIG } from '../utils/constants';

class APIService {
  constructor() {
    this.api = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      timeout: API_CONFIG.TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor to add auth token
    this.api.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem('userToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor for error handling
    this.api.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          // Token expired, redirect to login
          await AsyncStorage.removeItem('userToken');
          await AsyncStorage.removeItem('currentUser');
          // Navigate to login screen
        }
        return Promise.reject(error);
      }
    );
  }

  // Authentication APIs
  async login(mobile, password) {
    const response = await this.api.post('/user/login', { mobile, password });
    return response.data;
  }

  async register(userData) {
    const response = await this.api.post('/user/register', userData);
    return response.data;
  }

  async logout() {
    const response = await this.api.post('/user/logout');
    return response.data;
  }

  // Product APIs
  async getProducts(category = null) {
    let url = '/products';
    if (category) {
      url += `?category=${encodeURIComponent(category)}`;
    }
    const response = await this.api.get(url);
    return response.data;
  }

  async getProduct(id) {
    const response = await this.api.get(`/products/${id}`);
    return response.data;
  }

  async getCategories() {
    const response = await this.api.get('/categories');
    return response.data;
  }

  // Cart APIs
  async getCart() {
    const response = await this.api.get('/cart');
    return response.data;
  }

  async addToCart(productId, quantity) {
    const response = await this.api.post('/cart/add', {
      product_id: productId,
      quantity: quantity,
    });
    return response.data;
  }

  async updateCart(productId, quantity) {
    const response = await this.api.put('/cart/update', {
      product_id: productId,
      quantity: quantity,
    });
    return response.data;
  }

  async removeFromCart(productId) {
    const response = await this.api.delete(`/cart/remove`, {
      data: { product_id: productId }
    });
    return response.data;
  }

  // Order APIs
  async createOrder(orderData) {
    const response = await this.api.post('/orders', orderData);
    return response.data;
  }

  async getUserOrders() {
    const response = await this.api.get('/user/orders');
    return response.data;
  }

  // User Profile APIs
  async getUserProfile() {
    const response = await this.api.get('/user/profile');
    return response.data;
  }

  async updateUserProfile(profileData) {
    const response = await this.api.put('/user/profile', profileData);
    return response.data;
  }

  // Customer Info APIs
  async getCustomerInfo() {
    const response = await this.api.get('/customer-info');
    return response.data;
  }

  async saveCustomerInfo(customerInfo) {
    const response = await this.api.post('/customer-info', customerInfo);
    return response.data;
  }
}

export default new APIService();
EOF

    print_status "Configuration files created"
    
    cd ..
}

# Generate app icons and splash screen templates
create_app_assets() {
    echo ""
    echo "🎨 Creating App Assets..."
    echo "----------------------------------------"
    
    cd GreenObasketMobile
    
    # Create placeholder for app icons
    cat > src/assets/README.md << 'EOF'
# App Assets

## App Icons
Place your app icons in the following directories:
- **Android**: `android/app/src/main/res/mipmap-*`
- **iOS**: `ios/GreenObasketMobile/Images.xcassets/AppIcon.appiconset/`

## Icon Sizes Needed:

### Android:
- 36x36 (ldpi)
- 48x48 (mdpi)
- 72x72 (hdpi)
- 96x96 (xhdpi)
- 144x144 (xxhdpi)
- 192x192 (xxxhdpi)

### iOS:
- 20x20, 29x29, 40x40, 58x58, 60x60, 80x80, 87x87, 120x120, 180x180, 1024x1024

## Tools for Icon Generation:
- https://appicon.co/
- https://makeappicon.com/

## Splash Screen:
Use `react-native-splash-screen` package for custom splash screens.
EOF

    print_status "App assets structure created"
    
    cd ..
}

# Create development scripts
create_dev_scripts() {
    echo ""
    echo "📝 Creating Development Scripts..."
    echo "----------------------------------------"
    
    # Main development script
    cat > mobile_dev.sh << 'EOF'
#!/bin/bash

# GreenObasket Mobile Development Helper Script

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

show_help() {
    echo "GreenObasket Mobile Development Helper"
    echo ""
    echo "Usage: ./mobile_dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start           Start Metro bundler"
    echo "  android         Run Android app"
    echo "  ios             Run iOS app"
    echo "  clean           Clean build cache"
    echo "  reset           Reset Metro cache"
    echo "  install         Install dependencies"
    echo "  build-android   Build Android APK"
    echo "  help            Show this help"
    echo ""
}

case "$1" in
    "start")
        print_info "Starting Metro bundler..."
        cd GreenObasketMobile
        npx react-native start
        ;;
    "android")
        print_info "Running Android app..."
        cd GreenObasketMobile
        npx react-native run-android
        ;;
    "ios")
        print_info "Running iOS app..."
        cd GreenObasketMobile
        npx react-native run-ios
        ;;
    "clean")
        print_info "Cleaning build cache..."
        cd GreenObasketMobile
        cd android && ./gradlew clean && cd ..
        if [[ "$OSTYPE" == "darwin"* ]]; then
            cd ios && xcodebuild clean && cd ..
        fi
        print_success "Build cache cleaned"
        ;;
    "reset")
        print_info "Resetting Metro cache..."
        cd GreenObasketMobile
        npx react-native start --reset-cache
        ;;
    "install")
        print_info "Installing dependencies..."
        cd GreenObasketMobile
        npm install
        if [[ "$OSTYPE" == "darwin"* ]]; then
            cd ios && pod install && cd ..
        fi
        print_success "Dependencies installed"
        ;;
    "build-android")
        print_info "Building Android APK..."
        cd GreenObasketMobile/android
        ./gradlew assembleRelease
        print_success "APK built: android/app/build/outputs/apk/release/app-release.apk"
        ;;
    "help"|"")
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
EOF

    chmod +x mobile_dev.sh
    
    print_status "Development scripts created"
}

# Create README for mobile development
create_mobile_readme() {
    echo ""
    echo "📖 Creating Mobile Development README..."
    echo "----------------------------------------"
    
    cat > MOBILE_DEVELOPMENT_QUICK_START.md << 'EOF'
# 📱 GreenObasket Mobile - Quick Start

## 🚀 Development Commands

### Basic Operations:
```bash
# Start development
./mobile_dev.sh start

# Run on Android
./mobile_dev.sh android

# Run on iOS (macOS only)
./mobile_dev.sh ios

# Install dependencies
./mobile_dev.sh install
```

### Troubleshooting:
```bash
# Clean build cache
./mobile_dev.sh clean

# Reset Metro cache
./mobile_dev.sh reset
```

### Building:
```bash
# Build Android APK
./mobile_dev.sh build-android
```

## 📁 Project Structure

```
GreenObasketMobile/
├── src/
│   ├── components/          # Reusable UI components
│   ├── screens/            # App screens
│   ├── services/           # API services
│   ├── store/             # Redux store
│   ├── utils/             # Helper functions
│   └── assets/            # Images, fonts
├── android/               # Android-specific files
├── ios/                   # iOS-specific files
└── package.json
```

## 🔧 Configuration

### API Configuration:
Edit `src/utils/constants.js` to update your backend URL:

```javascript
export const API_CONFIG = {
  BASE_URL: 'http://YOUR_BACKEND_IP:5001/api',
  TIMEOUT: 10000,
};
```

### Backend Connection:
Make sure your Flask backend is running on `http://localhost:5001`

## 📱 Device Testing

### Android:
- Connect Android device via USB
- Enable Developer Options & USB Debugging
- Run: `./mobile_dev.sh android`

### iOS (macOS only):
- Connect iPhone/iPad via USB
- Trust computer on device
- Run: `./mobile_dev.sh ios`

## 🔔 Push Notifications Setup

1. Create Firebase project
2. Add `google-services.json` to `android/app/`
3. Add `GoogleService-Info.plist` to iOS project
4. Configure Firebase in your app

## 🛒 Key Features Implementation

### ✅ Completed:
- [x] Project structure setup
- [x] API service configuration
- [x] Navigation setup
- [x] Basic UI components

### 🚧 In Progress:
- [ ] User authentication screens
- [ ] Product listing screens
- [ ] Shopping cart functionality
- [ ] Checkout process
- [ ] Push notifications
- [ ] Barcode scanner
- [ ] GPS integration

## 📞 Support

For development help:
1. Check the main guide: `MOBILE_APP_DEVELOPMENT_GUIDE.md`
2. Create issues on GitHub
3. Check React Native documentation

---

**Happy coding! 🚀📱**
EOF

    print_status "Mobile development README created"
}

# Main execution
main() {
    echo "🌱 Starting GreenObasket Mobile App Setup"
    echo "This will set up everything you need for mobile app development!"
    echo ""
    
    # Ask user confirmation
    read -p "Do you want to continue with the mobile app setup? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Setup cancelled by user"
        exit 0
    fi
    
    check_prerequisites
    install_react_native_cli
    create_react_native_project
    install_dependencies
    setup_ios_dependencies
    create_project_structure
    create_config_files
    create_app_assets
    create_dev_scripts
    create_mobile_readme
    
    echo ""
    echo "🎉 Mobile App Setup Complete!"
    echo "============================================================"
    print_success "React Native project created: GreenObasketMobile"
    print_success "Development scripts created: ./mobile_dev.sh"
    print_success "Quick start guide: MOBILE_DEVELOPMENT_QUICK_START.md"
    print_success "Comprehensive guide: MOBILE_APP_DEVELOPMENT_GUIDE.md"
    echo ""
    print_info "Next steps:"
    echo "1. Start your Flask backend: python backend/app.py"
    echo "2. Update API URL in GreenObasketMobile/src/utils/constants.js"
    echo "3. Start development: ./mobile_dev.sh start"
    echo "4. Run on device: ./mobile_dev.sh android or ./mobile_dev.sh ios"
    echo ""
    print_warning "Make sure to read MOBILE_APP_DEVELOPMENT_GUIDE.md for detailed instructions!"
}

# Run main function
main "$@"