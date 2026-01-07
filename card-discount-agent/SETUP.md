# Card Discount AI Agent - Setup Guide

Complete setup instructions for the Card Discount AI Shopping Agent.

## Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.9+ (for backend)
- **Google AI API Key** (for Gemini 2.5 Flash)

## Getting Your Google AI API Key

1. Visit [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Get API Key" or "Create API Key"
4. Copy the generated API key
5. Keep it secure - you'll need it for the backend setup

## Backend Setup

### 1. Navigate to Backend Directory
```bash
cd card-discount-agent/backend
```

### 2. Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# Required: GOOGLE_API_KEY=your_actual_api_key_here
```

Example `.env` file:
```env
GOOGLE_API_KEY=AIzaSyD...your_key_here
HOST=0.0.0.0
PORT=8000
DEBUG=true
ENABLE_CACHING=true
CACHE_TTL_MINUTES=60
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
```

### 5. Start Backend Server
```bash
python app.py
```

The backend will start on `http://localhost:8000`

**API Documentation**: Visit `http://localhost:8000/docs` for interactive API docs

## Frontend Setup

### 1. Navigate to Frontend Directory
```bash
cd card-discount-agent/frontend
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment (Optional)
```bash
# Copy example file
cp .env.example .env

# The default settings work fine for local development
# VITE_API_URL defaults to http://localhost:8000/api
```

### 4. Start Development Server
```bash
npm run dev
```

The frontend will start on `http://localhost:3000` (or the next available port)

## Running Both Services

### Option 1: Two Terminal Windows

**Terminal 1 - Backend:**
```bash
cd card-discount-agent/backend
source venv/bin/activate  # if using venv
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd card-discount-agent/frontend
npm run dev
```

### Option 2: Background Process (Unix/macOS/Linux)
```bash
# Start backend in background
cd card-discount-agent/backend
source venv/bin/activate
python app.py &

# Start frontend
cd ../frontend
npm run dev
```

## Verifying Installation

### 1. Check Backend Health
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Check Frontend
Open `http://localhost:3000` in your browser

You should see the Card Discount Agent interface.

### 3. Test Search Functionality

1. Enter a product name like "iPhone 15" or paste an Amazon/Flipkart URL
2. Select your credit cards
3. Click "Search"
4. Wait for results to load (may take 30-60 seconds for Gemini to search)

## Troubleshooting

### Backend Issues

**Error: "GOOGLE_API_KEY not found"**
- Make sure you created `.env` file in `backend/` directory
- Verify the API key is correctly pasted without extra spaces
- Don't use quotes around the key: `GOOGLE_API_KEY=AIza...` not `GOOGLE_API_KEY="AIza..."`

**Error: "Module not found"**
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again
- Check Python version: `python --version` (should be 3.9+)

**Port 8000 already in use**
- Change `PORT=8001` in `.env` file
- Update frontend to use new port: `VITE_API_URL=http://localhost:8001/api`

### Frontend Issues

**Error: "Failed to fetch" or CORS errors**
- Make sure backend is running on port 8000
- Check `CORS_ORIGINS` in backend `.env` includes your frontend URL
- Verify `VITE_API_URL` in frontend `.env` points to correct backend URL

**npm install fails**
- Try `npm install --legacy-peer-deps`
- Make sure Node.js version is 18+: `node --version`
- Clear npm cache: `npm cache clean --force`

**Build fails**
- Delete `node_modules` and `package-lock.json`
- Run `npm install` again
- Check for TypeScript errors: `npm run build`

### Search Not Working

**No results returned**
- Check backend logs for errors
- Verify API key is valid and has quota remaining
- Try a simpler search query (e.g., "iPhone 15" instead of long URL)
- Check your internet connection (Gemini needs to access Google Search)

**Search taking too long (> 2 minutes)**
- Gemini search can take 30-90 seconds
- Check backend logs for timeout errors
- Reduce number of platforms in search query

## Production Deployment

### Backend

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend

```bash
# Build for production
npm run build

# Serve the built files
npm run preview
```

For actual production, deploy:
- **Backend**: Railway, Render, Google Cloud Run, AWS Lambda
- **Frontend**: Vercel, Netlify, Cloudflare Pages

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| GOOGLE_API_KEY | ✅ Yes | - | Google AI API key for Gemini |
| HOST | No | 0.0.0.0 | Server host |
| PORT | No | 8000 | Server port |
| DEBUG | No | true | Enable debug mode |
| ENABLE_CACHING | No | true | Enable response caching |
| CACHE_TTL_MINUTES | No | 60 | Cache lifetime in minutes |
| CORS_ORIGINS | No | localhost:3000 | Allowed CORS origins |

### Frontend (.env)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| VITE_API_URL | No | /api | Backend API URL |

## Next Steps

After successful setup:

1. **Test with Real Products**: Try searching for actual products
2. **Add Your Cards**: Select only the cards you own
3. **Bookmark Best Deals**: Save money on your next purchase!

## Support

- **Issues**: Check logs in both frontend and backend
- **API Docs**: Visit `/docs` endpoint on backend
- **Logs Location**:
  - Backend: Console output
  - Frontend: Browser console (F12)

## License

MIT License
