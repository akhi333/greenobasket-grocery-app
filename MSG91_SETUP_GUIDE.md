# 📱 MSG91 SMS Setup Guide - Free OTP for India

## Why MSG91 is Better for India 🇮🇳

✅ **Indian Company** - Better India coverage  
✅ **Cheaper** - ₹0.50-0.80 per SMS vs Twilio's ₹2-3  
✅ **Free Trial** - ₹20 credit (~40 SMS)  
✅ **Easy Setup** - 5 minutes only  
✅ **OTP Templates** - Pre-approved by telecom operators  

---

## 🚀 Quick Setup (5 Minutes)

### Step 1: Create MSG91 Account (2 minutes)
1. **Go to**: [https://msg91.com/signup](https://msg91.com/signup)
2. **Sign up** with your mobile number
3. **Verify** your mobile number via OTP
4. **Complete profile** with business details

### Step 2: Get Your Credentials (2 minutes)
1. **Login** to MSG91 dashboard
2. **Go to**: Settings → API Keys
3. **Copy your Auth Key** (like: `123456A7uABCDEfghijk`)

### Step 3: Create OTP Template (1 minute)
1. **Go to**: SMS → Templates
2. **Click**: "Create Template"
3. **Template Type**: OTP
4. **Template Name**: GreenObasket_OTP
5. **Template Content**:
   ```
   Your GreenObasket password reset OTP is ##OTP##. Valid for 10 minutes. Don't share this code.
   ```
6. **Submit** for approval (usually approved in 2-4 hours)
7. **Copy Template ID** (after approval)

### Step 4: Get Sender ID (Optional)
1. **Go to**: SMS → Sender ID
2. **Create**: Custom Sender ID like `GRNBSK` 
3. **Wait for approval** (1-2 days)
4. **Use default** `TXTLCL` until approved

---

## ⚙️ Configure GreenObasket

### Update Backend Configuration
Edit `backend/app.py` and find `SMS_CONFIG`:

```python
SMS_CONFIG = {
    'auth_key': 'YOUR_MSG91_AUTH_KEY',           # From Step 2
    'template_id': 'YOUR_TEMPLATE_ID',           # From Step 3  
    'sender_id': 'GRNBSK'                        # From Step 4 (or use 'TXTLCL')
}
```

### Example Configuration:
```python
SMS_CONFIG = {
    'auth_key': '123456A7uABCDEfghijk',          # Your actual auth key
    'template_id': '64f8b2c3d1e4567890abcdef',   # Your template ID
    'sender_id': 'GRNBSK'                        # Your sender ID
}
```

---

## 🧪 Test Your Setup

### 1. Install Dependencies
```bash
cd GreenObasket
pip install -r backend/requirements.txt
```

### 2. Restart Your App
```bash
python backend/app.py
```

### 3. Test OTP
1. **Go to**: `http://localhost:5001`
2. **Click**: "Forgot Password?"
3. **Enter**: Your mobile number
4. **Check terminal** for success message:
   ```
   ✅ [REAL SMS] OTP sent to 9876543210: 123456 (MSG91 Request ID: xyz123)
   ```

---

## 💰 Pricing & Free Credits

| Service | Free Credits | Cost per SMS | India Focus |
|---------|-------------|--------------|-------------|
| **MSG91** | ₹20 (~40 SMS) | ₹0.50-0.80 | ✅ Excellent |
| **TextLocal** | 100 SMS | ₹0.40-0.60 | ✅ Good |
| **Fast2SMS** | 100 SMS/day | ₹0.35-0.50 | ✅ Good |
| **Twilio** | $15 (~150 SMS) | ₹2-3 | ❌ Expensive for India |

---

## ❓ Troubleshooting

### Template Not Approved Yet?
**Temporary Solution**: Use basic SMS API (not OTP API) until template approval:

```python
# In send_otp_sms function, replace the URL:
url = "https://api.msg91.com/api/sendhttp.php"

# Replace payload with:
payload = {
    "authkey": SMS_CONFIG['auth_key'],
    "mobiles": f"91{mobile}",
    "message": f"Your GreenObasket password reset OTP is: {otp}. Valid for 10 minutes.",
    "sender": SMS_CONFIG['sender_id'] or 'TXTLCL',
    "route": 4  # Transactional route
}
```

### Common Errors:
- **Authentication failed**: Check your Auth Key
- **Template not found**: Ensure template is approved
- **Invalid mobile**: Ensure 10-digit number
- **DND number**: User has DND enabled (use email instead)

---

## 🔐 Security Best Practices

✅ **Never commit** SMS credentials to Git  
✅ **Use environment variables** in production  
✅ **Set rate limiting** to prevent abuse  
✅ **Log request IDs** for tracking  
✅ **Handle failures gracefully** with fallback to email  

---

## 📞 MSG91 Support

- **Website**: https://msg91.com
- **Support**: https://help.msg91.com
- **API Docs**: https://docs.msg91.com
- **Phone**: +91-9654271234

---

**🎉 Your users will now receive real SMS OTPs for password reset!** 