# Search Grounding Toggle Guide

## 🎛️ NEW FEATURE: Toggleable Search Grounding

You can now **toggle search grounding ON/OFF** using an environment variable!

---

## 📝 How to Configure

### Step 1: Edit Your `.env` File

```bash
cd card-discount-agent/backend
nano .env  # or notepad .env on Windows
```

### Step 2: Set the Toggle

```bash
# For TESTING/DEVELOPMENT (recommended now)
ENABLE_SEARCH_GROUNDING=false

# For PRODUCTION (after quota resets)
ENABLE_SEARCH_GROUNDING=true
```

### Step 3: Restart Backend

```bash
python app.py
```

---

## 🔍 What Each Mode Does

### Mode 1: Search Grounding OFF (Testing)

**Setting**: `ENABLE_SEARCH_GROUNDING=false`

**What You Get**:
- ✅ **1,500 searches per day** (vs 50-100)
- ✅ **15 RPM** (vs 2-5)
- ✅ **Fast responses** (2-5 seconds)
- ✅ **No rate limit issues**
- ⚠️ Example/estimated prices (not real-time)
- ⚠️ No actual product URLs
- ⚠️ Mock offers based on typical patterns

**Backend Startup Message**:
```
⚡ Gemini 2.5 Flash WITHOUT search grounding (testing: 10 RPM, ~1500 RPD, example data)
```

**Best For**:
- Testing and development
- Demos and prototypes
- UI/UX verification
- When daily quota is exhausted

---

### Mode 2: Search Grounding ON (Production)

**Setting**: `ENABLE_SEARCH_GROUNDING=true`

**What You Get**:
- ✅ **Real-time prices** from actual websites
- ✅ **Actual product URLs**
- ✅ **Current bank offers**
- ✅ **Live stock availability**
- ⚠️ Only 50-100 searches per day (free tier)
- ⚠️ 2-5 RPM (very strict)
- ⚠️ Slower responses (30-60 seconds)

**Backend Startup Message**:
```
🌐 Gemini 2.5 Flash WITH search grounding (production: 2 RPM, ~50-100 RPD, real prices)
```

**Best For**:
- Production with real users
- Actual shopping decisions
- When you need accurate data
- After daily quota resets (midnight PT)
- Paid tier users

---

## 🚀 Quick Start for Windows Users

### Current Setup (Testing Mode)

1. **Create/Edit `.env` file**:
   ```bash
   cd C:\Users\adity\OneDrive\Documents\GitHub\Projects_with_claude_code\card-discount-agent\backend
   notepad .env
   ```

2. **Add this line**:
   ```
   ENABLE_SEARCH_GROUNDING=false
   ```

3. **Save and restart**:
   ```bash
   python app.py
   ```

4. **Verify in logs**:
   ```
   ⚡ Gemini 2.5 Flash WITHOUT search grounding
   ```

---

## 📊 Feature Comparison

| Feature | Without Grounding | With Grounding |
|---------|-------------------|----------------|
| **Model** | gemini-2.5-flash | gemini-2.5-flash + tools |
| **RPM** | 10 (safe buffer under 15) | 2 (safe buffer under 5) |
| **RPD** | ~1,500 | ~50-100 |
| **Response Time** | 2-5 seconds | 30-60 seconds |
| **Data Type** | Example/Estimated | Real-time/Live |
| **Product URLs** | ❌ null | ✅ Actual links |
| **Price Accuracy** | ⚠️ Typical/Estimated | ✅ Current/Real |
| **Bank Offers** | ⚠️ Common patterns | ✅ Live offers |
| **Best For** | Testing/Development | Production/Real users |

---

## 🔄 When to Switch Modes

### Use `false` (No Grounding) When:
- ✅ Testing new features
- ✅ Demoing to stakeholders
- ✅ Verifying UI/UX
- ✅ Daily quota exhausted
- ✅ Developing locally
- ✅ Don't need real prices

### Use `true` (With Grounding) When:
- ✅ Deploying to production
- ✅ Real users need accurate prices
- ✅ Making purchase decisions
- ✅ Daily quota available
- ✅ Have paid tier
- ✅ Need actual product URLs

---

## 🧪 Testing Both Modes

### Test Mode 1: No Grounding

**`.env`**:
```
ENABLE_SEARCH_GROUNDING=false
```

**Expected Result**:
```
Product: Philips OneBlade Intimate Trimmer
Amazon: ₹2,499 (example)
Flipkart: ₹2,399 (example)
Blinkit: ₹2,599 (example)
Discounts: HDFC Millennia 10%, ICICI 5%
```

**Time**: 2-5 seconds

---

### Test Mode 2: With Grounding (After Quota Reset)

**`.env`**:
```
ENABLE_SEARCH_GROUNDING=true
```

**Expected Result**:
```
Product: Philips OneBlade Intimate Trimmer QP2834/40
Amazon: ₹3,495 (real price from website)
URL: https://www.amazon.in/...
Flipkart: ₹3,299 (real price)
URL: https://www.flipkart.com/...
Discounts: Current live offers
```

**Time**: 30-60 seconds

---

## ⚙️ Advanced Configuration

### Environment Variable Options

```bash
# In backend/.env

# Search Grounding Toggle
ENABLE_SEARCH_GROUNDING=false  # or true

# Google API Key (Required)
GOOGLE_API_KEY=your_actual_api_key

# Server Settings
HOST=0.0.0.0
PORT=8000
DEBUG=true

# Cache Settings
ENABLE_CACHING=true
CACHE_TTL_MINUTES=60

# CORS (Frontend URLs)
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

---

## 🎯 Recommended Workflow

### Development Workflow

1. **Start with grounding OFF**:
   ```
   ENABLE_SEARCH_GROUNDING=false
   ```

2. **Test everything**:
   - UI/UX
   - Card selection
   - Discount calculations
   - Results display

3. **Verify it works**:
   - No crashes
   - Results display correctly
   - Calculations are accurate

4. **Then switch to ON** (for final testing):
   ```
   ENABLE_SEARCH_GROUNDING=true
   ```

5. **Test with real data**:
   - Verify prices make sense
   - Check URLs work
   - Confirm offers are current

---

### Production Workflow

1. **Deploy with grounding ON**:
   ```
   ENABLE_SEARCH_GROUNDING=true
   ```

2. **Monitor usage**:
   ```bash
   curl localhost:8000/api/stats
   ```

3. **If hitting limits**:
   - Upgrade to paid tier OR
   - Implement request caching OR
   - Build custom web scraping

---

## 🆘 Troubleshooting

### Issue: Still seeing "4 RPM" in logs

**Cause**: Backend running old code

**Fix**:
```bash
git pull origin claude/card-discount-ai-agent-S6LAR
python app.py
```

---

### Issue: Getting 429 errors with grounding=false

**Cause**: Still using old backend process

**Fix**:
1. Stop backend (Ctrl+C)
2. Verify .env has `ENABLE_SEARCH_GROUNDING=false`
3. Restart: `python app.py`
4. Look for: `⚡ Gemini 2.5 Flash WITHOUT search grounding`

---

### Issue: Want real prices but hitting limits

**Options**:
1. **Wait** until midnight Pacific Time (quota resets)
2. **Upgrade** to paid tier ($30-150/month)
3. **Build** custom web scraping
4. **Hybrid**: Use grounding for final checkout only

---

## 📋 Quick Reference

### To DISABLE search grounding (testing):
```bash
# In .env
ENABLE_SEARCH_GROUNDING=false
```

### To ENABLE search grounding (production):
```bash
# In .env
ENABLE_SEARCH_GROUNDING=true
```

### To verify mode:
```bash
# Look for one of these in backend logs:
⚡ WITHOUT search grounding  # Testing mode
🌐 WITH search grounding     # Production mode
```

### To check current stats:
```bash
curl localhost:8000/api/stats
```

---

## 🎉 Summary

✅ **Single environment variable** controls everything
✅ **Easy to switch** between testing and production
✅ **Automatic rate limiting** adjusts based on mode
✅ **Different prompts** for grounded vs non-grounded
✅ **Clear logging** shows which mode is active
✅ **No code changes** needed - just edit .env

**For testing now**: `ENABLE_SEARCH_GROUNDING=false`
**For production later**: `ENABLE_SEARCH_GROUNDING=true`

Simple! 🚀
