# 🔧 Troubleshooting Guide

Complete troubleshooting guide for Card Discount Agent

## 📑 Table of Contents

- [Backend Issues](#backend-issues)
- [Frontend Issues](#frontend-issues)
- [Search Issues](#search-issues)
- [Connection Issues](#connection-issues)
- [Performance Issues](#performance-issues)
- [Common Error Messages](#common-error-messages)

---

## Backend Issues

### ❌ Error: "GOOGLE_API_KEY not found in environment"

**Symptoms:**
- Backend crashes on startup
- Error message in terminal

**Solutions:**

1. **Check if .env file exists:**
```bash
cd backend
ls -la .env
# If "No such file", create it:
cp .env.example .env
```

2. **Verify API key is set:**
```bash
cat .env | grep GOOGLE_API_KEY
# Should show: GOOGLE_API_KEY=AIza...
```

3. **Common mistakes:**
- ❌ `GOOGLE_API_KEY="AIza..."` (don't use quotes)
- ❌ `GOOGLE_API_KEY = AIza...` (no spaces around =)
- ❌ `GOOGLE_API_KEY=` (empty value)
- ✅ `GOOGLE_API_KEY=AIzaSyD123abc...` (correct)

4. **Get a valid key:**
- Visit: https://aistudio.google.com/apikey
- Create new API key
- Copy entire key (starts with AIza)

---

### ❌ Error: "Module 'fastapi' not found"

**Symptoms:**
- Backend won't start
- `ModuleNotFoundError: No module named 'fastapi'`

**Solutions:**

1. **Activate virtual environment:**
```bash
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate

# You should see (venv) in prompt
```

2. **Reinstall dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
pip list | grep fastapi
# Should show: fastapi 0.115.5
```

4. **If still failing, recreate venv:**
```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### ❌ Error: "Address already in use" (Port 8000)

**Symptoms:**
- Backend won't start
- `OSError: [Errno 48] Address already in use`

**Solutions:**

**Option 1: Kill the process**

macOS/Linux:
```bash
# Find process
lsof -ti:8000

# Kill it
lsof -ti:8000 | xargs kill -9
```

Windows:
```cmd
# Find process
netstat -ano | findstr :8000

# Kill it (replace PID with actual number)
taskkill /PID 12345 /F
```

**Option 2: Change port**
```bash
# Edit backend/.env
PORT=8001

# Also update frontend/.env
VITE_API_URL=http://localhost:8001/api

# Restart both servers
```

---

### ❌ Backend starts but crashes immediately

**Check logs for:**

1. **Python version too old:**
```bash
python --version
# Need 3.9 or higher
```

2. **Missing dependencies:**
```bash
pip install -r requirements.txt --upgrade
```

3. **Permission errors:**
```bash
# macOS/Linux:
chmod +x app.py
```

---

## Frontend Issues

### ❌ Error: "npm install" fails

**Symptoms:**
- Package installation errors
- Dependency conflicts

**Solutions:**

1. **Clear npm cache:**
```bash
npm cache clean --force
```

2. **Delete old files:**
```bash
rm -rf node_modules
rm package-lock.json
```

3. **Reinstall with legacy peer deps:**
```bash
npm install --legacy-peer-deps
```

4. **Check Node version:**
```bash
node --version
# Need 18.0.0 or higher
```

5. **Update npm:**
```bash
npm install -g npm@latest
```

---

### ❌ Error: "Port 5173 already in use"

**Symptoms:**
- Frontend won't start
- Port conflict error

**Solutions:**

**Option 1: Vite auto-selects next port**
- Just use the URL shown in terminal
- Usually switches to 5174

**Option 2: Specify custom port**
```bash
npm run dev -- --port 3000
```

**Option 3: Kill the process**
```bash
# macOS/Linux:
lsof -ti:5173 | xargs kill -9

# Windows:
netstat -ano | findstr :5173
taskkill /PID 12345 /F
```

---

### ❌ Error: "Failed to fetch" or CORS error

**Symptoms:**
- Frontend loads but can't connect to backend
- Console shows CORS errors
- Red network errors in browser

**Solutions:**

1. **Verify backend is running:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

2. **Check CORS settings in backend/.env:**
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
# Make sure your frontend URL is listed
```

3. **Restart both servers:**
- Stop both (Ctrl+C)
- Start backend first, then frontend

4. **Check browser console (F12):**
- Look for the actual API URL being called
- Verify it matches backend URL

---

### ❌ White screen / App won't load

**Symptoms:**
- Browser shows blank page
- No errors in terminal

**Solutions:**

1. **Check browser console (F12):**
- Press F12 → Console tab
- Look for JavaScript errors

2. **Hard refresh:**
- Press Ctrl+Shift+R (or Cmd+Shift+R on Mac)
- Clears cache

3. **Clear browser cache:**
- Chrome: Settings → Privacy → Clear browsing data
- Firefox: Settings → Privacy → Clear Data

4. **Try different browser:**
- Test in Chrome, Firefox, or Edge

---

## Search Issues

### ❌ No results returned

**Symptoms:**
- Search completes but shows "No deals found"
- Empty results page

**Possible Causes & Solutions:**

1. **Invalid API key:**
```bash
# Test API key at:
curl -X POST http://localhost:8000/api/search \
  -H "Content-Type: application/json" \
  -d '{"query":"iPhone 15","selected_cards":["hdfc-millennia"]}'

# Check backend logs for API errors
```

2. **API quota exceeded:**
- Free tier: 60 requests/minute
- Wait 1 minute and retry
- Check quota: https://aistudio.google.com/apikey

3. **Product not found:**
- Try simpler search: "iPhone 15" instead of full model
- Use exact product name from Amazon/Flipkart
- Try different product

4. **Network issues:**
```bash
# Test internet connection
curl https://google.com
```

---

### ❌ Search takes too long (>2 minutes)

**Expected times:**
- First search: 60-90 seconds (normal)
- Cached search: 30-45 seconds

**If stuck/frozen:**

1. **Check backend logs:**
- Look for timeout errors
- Look for API rate limit errors

2. **Reduce card selection:**
- Try with just 2-3 cards
- More cards = more calculations

3. **Simplify search query:**
- "iPhone 15" instead of long URL
- Brand + model only

4. **Check backend CPU:**
```bash
# macOS/Linux:
top
# Look for python process

# Windows:
# Open Task Manager
# Check python.exe usage
```

---

### ❌ Error: "Please select at least one credit card"

**Symptoms:**
- Can't search
- Red error message

**Solutions:**

1. **Select cards:**
- Type in card search box
- Click on at least one card
- Selected cards show as badges above

2. **Clear browser storage and retry:**
```javascript
// In browser console (F12):
localStorage.clear()
// Refresh page
```

---

## Connection Issues

### ❌ Backend running but frontend can't connect

**Diagnosis steps:**

1. **Test backend directly:**
```bash
# Open in browser:
http://localhost:8000

# Should see JSON response
```

2. **Test API endpoint:**
```bash
curl http://localhost:8000/api/cards
# Should return list of cards
```

3. **Check frontend API URL:**
```bash
# frontend/.env or frontend/.env.local
VITE_API_URL=http://localhost:8000/api
```

4. **Check browser network tab:**
- Press F12 → Network tab
- Try searching
- Look at failed requests
- Check request URL and response

---

### ❌ Can't access app from other devices

**Symptoms:**
- Works on localhost
- Doesn't work from phone/tablet

**Solutions:**

1. **Find your local IP:**
```bash
# macOS/Linux:
ifconfig | grep "inet "

# Windows:
ipconfig
```

2. **Update backend to allow external connections:**
```bash
# Already configured in .env:
HOST=0.0.0.0  # Allows external connections
```

3. **Update CORS:**
```env
# backend/.env
CORS_ORIGINS=http://localhost:3000,http://192.168.1.100:5173
# Add your local IP
```

4. **Update frontend:**
```env
# frontend/.env
VITE_API_URL=http://192.168.1.100:8000/api
# Use your local IP
```

5. **Check firewall:**
- Allow ports 8000 and 5173
- macOS: System Preferences → Security → Firewall
- Windows: Control Panel → Firewall

---

## Performance Issues

### 🐌 App is slow

**Frontend slow:**

1. **Check browser:**
- Close other tabs
- Disable browser extensions
- Try incognito mode

2. **Check system resources:**
- Close other applications
- Check CPU/RAM usage

**Backend slow:**

1. **Check logs for:**
- API timeout errors
- Rate limiting
- Network delays

2. **Enable caching:**
```env
# backend/.env
ENABLE_CACHING=true
CACHE_TTL_MINUTES=60
```

---

### 🔄 Results are outdated

**Symptoms:**
- Old prices shown
- Deals no longer available

**Cause:** Caching (by design)

**Solutions:**

1. **Wait for cache to expire:**
- Default: 60 minutes
- Results refresh automatically

2. **Reduce cache time:**
```env
# backend/.env
CACHE_TTL_MINUTES=15  # Refresh every 15 min
```

3. **Restart backend** (clears cache)

---

## Common Error Messages

### Backend Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `GOOGLE_API_KEY not found` | Missing API key | Add to .env file |
| `Invalid API key` | Wrong or expired key | Get new key from Google AI Studio |
| `Rate limit exceeded` | Too many requests | Wait 1 minute, reduce requests |
| `Module not found` | Missing package | `pip install -r requirements.txt` |
| `Address in use` | Port conflict | Kill process or change port |
| `Connection refused` | Backend not running | Start backend server |

### Frontend Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `Failed to fetch` | Backend not running | Start backend first |
| `CORS error` | Wrong CORS config | Check CORS_ORIGINS in .env |
| `Network error` | Connection issue | Check backend URL |
| `Module not found` | Missing package | `npm install` |
| `Blank screen` | Build error | Check console (F12) |

### Search Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `No deals found` | Product not available | Try different product |
| `Invalid query` | Empty search | Enter product name/URL |
| `No cards selected` | No cards chosen | Select at least one card |
| `Timeout` | Search too slow | Simplify query, reduce cards |

---

## 🆘 Still Stuck?

### Debug Checklist

- [ ] Backend running? → `curl http://localhost:8000/health`
- [ ] Frontend running? → Visit http://localhost:5173
- [ ] API key valid? → Check Google AI Studio
- [ ] .env file correct? → `cat backend/.env`
- [ ] Dependencies installed? → `pip list`, `npm list`
- [ ] Ports available? → 8000, 5173
- [ ] Internet working? → `curl https://google.com`
- [ ] Logs checked? → Backend terminal, browser console

### Get Detailed Logs

**Backend verbose logs:**
```bash
# backend/.env
LOG_LEVEL=DEBUG

# Restart backend
```

**Frontend logs:**
- Press F12 → Console tab
- Check for red errors
- Check Network tab for failed requests

### Reset Everything

**Nuclear option** (if nothing else works):

```bash
# Backend
cd backend
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Re-add API key to .env
python app.py

# Frontend (new terminal)
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

## 📞 Additional Resources

- **Quick Start**: See `START_HERE.md`
- **Complete Guide**: See `QUICKSTART.md`
- **Setup Details**: See `SETUP.md`
- **Features**: See `README_V2.md`
- **Technical Details**: See `PROJECT_OVERVIEW.md`

---

**Most issues are fixed by:**
1. ✅ Checking .env has valid API key
2. ✅ Making sure both servers are running
3. ✅ Restarting both servers
4. ✅ Checking browser console for errors (F12)

Good luck! 🍀
