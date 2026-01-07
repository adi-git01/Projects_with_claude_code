# 🚀 START HERE - 5 Minute Setup

Super quick guide to get started with Card Discount Agent!

## ⚡ Prerequisites (2 minutes)

1. **Get Google AI API Key** (FREE): https://aistudio.google.com/apikey
   - Sign in → Click "Create API Key" → Copy it

2. **Check you have:**
   - Node.js 18+ → `node --version`
   - Python 3.9+ → `python --version`

## 🔧 Setup (3 minutes)

### Backend (90 seconds)

```bash
# 1. Go to backend folder
cd card-discount-agent/backend

# 2. Install packages
pip install -r requirements.txt

# 3. Create config file
cp .env.example .env

# 4. Edit .env and add your API key
# Change this line: GOOGLE_API_KEY=your_key_here
nano .env   # or use any text editor

# 5. Start server
python app.py
```

✅ You should see: `Uvicorn running on http://0.0.0.0:8000`

**Keep this terminal open!**

---

### Frontend (90 seconds)

Open a **NEW terminal**:

```bash
# 1. Go to frontend folder
cd card-discount-agent/frontend

# 2. Install packages
npm install

# 3. Start app
npm run dev
```

✅ You should see: `Local: http://localhost:5173/`

---

## 🎯 Use It!

1. **Open browser**: http://localhost:5173

2. **Select cards**:
   - Type "HDFC Millennia" → Click it
   - Type "Amazon Pay" → Click it
   - Type "Axis Airtel" → Click it

3. **Search product**:
   - Type "iPhone 15" in search box
   - Click "Search"
   - Wait 60 seconds
   - See results!

## ❌ Problems?

**Backend won't start:**
```bash
# Did you add API key to .env file?
cat backend/.env
# Should show: GOOGLE_API_KEY=AIza...
```

**Frontend won't start:**
```bash
# Clear and reinstall
rm -rf node_modules
npm install
```

**Can't connect:**
- Make sure BOTH backend AND frontend are running
- Check backend: http://localhost:8000/health
- Should see: `{"status":"healthy"}`

## 📚 Want More Details?

- **Complete Guide**: Read `QUICKSTART.md`
- **All Features**: Read `README_V2.md`
- **Troubleshooting**: Read `SETUP.md`

---

**That's it! You're ready to find the best deals! 🎉**
