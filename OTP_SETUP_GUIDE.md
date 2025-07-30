# 🔐 OTP Setup Guide - Real Email & SMS Integration

## Current Status
- ✅ **Mock System**: OTPs appear in server console (for testing)
- 🚀 **Ready for Real OTPs**: Just add your credentials below

## 📧 Email OTPs (FREE with Gmail)

### Step 1: Enable Gmail App Password
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Factor Authentication** if not already enabled
3. Go to **App Passwords** → Generate new app password
4. Select **Mail** and **Other** → Name it "GreenObasket"
5. Copy the 16-character password (like: `abcd efgh ijkl mnop`)

### Step 2: Configure Email in Backend
Edit `backend/app.py` and update `EMAIL_CONFIG`:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'your-email@gmail.com',        # Your Gmail address
    'password': 'abcd efgh ijkl mnop'       # Your App Password (16 chars)
}
```

**✅ That's it! Email OTPs will now be sent for FREE!**

---

## 📱 SMS OTPs (FREE Trial with Twilio)

### Step 1: Sign Up for Twilio
1. Go to [Twilio.com](https://www.twilio.com/try-twilio)
2. Sign up for free account
3. Verify your phone number
4. You get **$15 FREE credit** (~150 SMS)

### Step 2: Get Twilio Credentials
1. From Twilio Console Dashboard, copy:
   - **Account SID** (like: `ACxxxxx...`)
   - **Auth Token** (like: `xxxxx...`)
2. Go to **Phone Numbers** → Get a free Twilio number (like: `+1234567890`)

### Step 3: Install Twilio Package
```bash
pip install twilio
```

### Step 4: Configure SMS in Backend
Edit `backend/app.py` and update `SMS_CONFIG`:

```python
SMS_CONFIG = {
    'account_sid': 'ACxxxxx...',           # Your Account SID
    'auth_token': 'xxxxx...',              # Your Auth Token  
    'from_number': '+1234567890'           # Your Twilio number
}
```

**✅ SMS OTPs will now be sent using your FREE Twilio credits!**

---

## 🌍 Alternative FREE Options

### Email Services:
| Service | Free Limit | Setup Difficulty |
|---------|------------|------------------|
| **Gmail SMTP** | 500/day | ⭐ Easy |
| SendGrid | 100/day forever | ⭐⭐ Medium |
| AWS SES | 62K/month (1st year) | ⭐⭐⭐ Hard |

### SMS Services:
| Service | Free Limit | Setup Difficulty |
|---------|------------|------------------|
| **Twilio** | $15 credit (~150 SMS) | ⭐⭐ Medium |
| AWS SNS | 100 SMS/month | ⭐⭐⭐ Hard |
| TextLocal (India) | Limited free tier | ⭐⭐ Medium |

---

## 🧪 Testing Your Setup

### 1. Check Console Output
When you start the Flask app, you'll see:
```bash
📧 [MOCK EMAIL] Configure EMAIL_CONFIG to send real emails
📱 [MOCK SMS] Configure SMS_CONFIG to send real SMS
```

After configuration:
```bash
✅ [REAL EMAIL] OTP sent to user@example.com: 123456
✅ [REAL SMS] OTP sent to 9876543210: 654321
```

### 2. Test the Flow
1. Go to `http://localhost:5001`
2. Click "Forgot Password?"
3. Choose Email or SMS
4. Enter your details
5. Check your email/phone for the OTP!

---

## 💰 Cost Breakdown

### Gmail SMTP (Recommended)
- **Cost**: 100% FREE
- **Limit**: 500 emails/day
- **Perfect for**: Small to medium apps

### Twilio SMS
- **Free Trial**: $15 credit
- **Cost After**: ~$0.10 per SMS
- **Perfect for**: Testing and small scale

### For Production Scale:
- Email: SendGrid Pro ($15/month) = 40K emails
- SMS: Twilio Pay-as-go = ~$0.05 per SMS

---

## 🔧 Quick Start (5 Minutes)

**Want email OTPs right now?**

1. **Get Gmail App Password** (2 minutes)
2. **Edit 2 lines** in `backend/app.py`:
   ```python
   'email': 'your-email@gmail.com',
   'password': 'your-app-password'
   ```
3. **Restart Flask app**
4. **Test it!** 🎉

**No purchases needed for email OTPs!**

---

## 🆘 Need Help?

**Common Issues:**
- Gmail error → Check App Password (not regular password)
- SMS error → Verify Twilio phone number format
- Still showing mock → Restart Flask app after config changes

**Pro Tip:** Start with email OTPs (free Gmail) and add SMS later when needed! 