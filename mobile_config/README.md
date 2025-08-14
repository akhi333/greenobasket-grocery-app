# 🔧 Mobile Development Configuration

This directory contains configuration files and templates for mobile app development.

## Files Overview

### API Configuration
- `api-config.json` - Backend API endpoints configuration
- `firebase-config.json` - Firebase configuration template
- `app-config.json` - App-wide configuration settings

### Development Templates
- `component-template.tsx` - React Native component template
- `screen-template.tsx` - React Native screen template
- `service-template.js` - API service template

### Build Configuration
- `android-config.gradle` - Android build configuration
- `ios-config.plist` - iOS configuration template

### Environment Setup
- `env-template` - Environment variables template
- `development.json` - Development environment config
- `production.json` - Production environment config

## Usage

1. Copy template files and remove `-template` suffix
2. Update configuration values for your environment
3. Follow the main guide: `../MOBILE_APP_DEVELOPMENT_GUIDE.md`

## Quick Commands

```bash
# Setup mobile development environment
../setup_mobile.sh

# Start development
../mobile_dev.sh start

# Run on Android
../mobile_dev.sh android
```