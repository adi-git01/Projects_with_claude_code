# Beginner's Guide: Monitoring Your API with /stats Endpoint

## What is `curl`?

**curl** is a command-line tool for making HTTP requests. Think of it like visiting a website, but instead of using a browser, you use the terminal/command line.

---

## 📍 Where to Enter the Command

### Step 1: Open Your Terminal/Command Line

**On Linux/Mac:**
- Press `Ctrl + Alt + T` (or search for "Terminal")

**On Windows:**
- Press `Win + R`, type `cmd`, press Enter
- OR search for "Command Prompt" or "PowerShell"

### Step 2: Make Sure Backend is Running

Before using curl, your backend must be running:

```bash
# In your terminal, navigate to backend directory
cd /home/user/Projects_with_claude_code/card-discount-agent/backend

# Start the backend server
python app.py
```

**You should see**:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Application startup complete.
```

**Keep this terminal open** - the server needs to stay running.

### Step 3: Open a NEW Terminal

Open a **second terminal window** (leave the first one running the server).

In this new terminal, type:

```bash
curl localhost:8000/api/stats
```

Press **Enter**.

---

## 📊 Expected Output

### Example 1: Just Started, No Searches Yet

```json
{
  "rate_limiter": {
    "requests_in_window": 0,
    "max_requests": 4,
    "remaining": 4,
    "utilization_percent": 0.0,
    "window_seconds": 60
  },
  "cache": {
    "size": 0,
    "ttl_seconds": 3600
  },
  "status": "healthy"
}
```

**What This Means:**
- ✅ `requests_in_window: 0` - No searches made in last 60 seconds
- ✅ `max_requests: 4` - You can make 4 searches per minute
- ✅ `remaining: 4` - You have all 4 requests available
- ✅ `cache size: 0` - No searches cached yet
- ✅ `status: healthy` - Everything working

---

### Example 2: After Making 2 Searches

```json
{
  "rate_limiter": {
    "requests_in_window": 2,
    "max_requests": 4,
    "remaining": 2,
    "utilization_percent": 50.0,
    "window_seconds": 60
  },
  "cache": {
    "size": 2,
    "ttl_seconds": 3600
  },
  "status": "healthy"
}
```

**What This Means:**
- ⏱️ `requests_in_window: 2` - Made 2 searches in last 60 seconds
- ⚠️ `remaining: 2` - Can make 2 more before hitting limit
- 📊 `utilization_percent: 50%` - Used half your quota
- 💾 `cache size: 2` - 2 searches cached (will be instant if repeated)

---

### Example 3: Rate Limit Warning (Close to Limit)

```json
{
  "rate_limiter": {
    "requests_in_window": 3,
    "max_requests": 4,
    "remaining": 1,
    "utilization_percent": 75.0,
    "window_seconds": 60
  },
  "cache": {
    "size": 5,
    "ttl_seconds": 3600
  },
  "status": "healthy"
}
```

**What This Means:**
- ⚠️ `requests_in_window: 3` - Made 3 searches recently
- ⚠️ `remaining: 1` - Only 1 search left before rate limit
- ⚠️ `utilization_percent: 75%` - Close to limit!
- 💾 `cache size: 5` - 5 different searches cached

**What to Do**: Wait 60 seconds before making more searches, or search for something you've already searched (cache hit = no API call).

---

### Example 4: Rate Limit Exhausted

```json
{
  "rate_limiter": {
    "requests_in_window": 4,
    "max_requests": 4,
    "remaining": 0,
    "utilization_percent": 100.0,
    "window_seconds": 60
  },
  "cache": {
    "size": 8,
    "ttl_seconds": 3600
  },
  "status": "healthy"
}
```

**What This Means:**
- 🔴 `remaining: 0` - No searches available right now
- 🔴 `utilization_percent: 100%` - Completely used up
- ⏰ **Wait 60 seconds** for the oldest request to expire
- 💡 **OR** search for something from cache (instant, no API call)

---

## 🎯 Understanding the Fields

### Rate Limiter Section

| Field | Meaning | What to Watch |
|-------|---------|---------------|
| `requests_in_window` | How many searches in last 60 seconds | Higher = closer to limit |
| `max_requests` | Maximum allowed per minute | Currently set to **4** |
| `remaining` | How many searches left | **0 = wait before searching** |
| `utilization_percent` | How much quota used | **>75% = slow down** |
| `window_seconds` | Time window (always 60) | Quota resets after this time |

### Cache Section

| Field | Meaning | What to Watch |
|-------|---------|---------------|
| `size` | Number of searches cached | Higher = better (more cache hits) |
| `ttl_seconds` | How long cache lasts | 3600 = 1 hour |

---

## 🖥️ Alternative Ways to Check Stats

### Option 1: Using Your Browser

Instead of curl, open your browser and go to:

```
http://localhost:8000/api/stats
```

You'll see the same JSON output.

### Option 2: Using httpie (Prettier Output)

If you have `httpie` installed:

```bash
# Install httpie (optional)
pip install httpie

# Use it (prettier output)
http localhost:8000/api/stats
```

**Output is color-coded and easier to read!**

### Option 3: Using Postman/Insomnia

1. Download Postman: https://www.postman.com/downloads/
2. Create a new GET request
3. URL: `http://localhost:8000/api/stats`
4. Click "Send"

---

## 🔄 Real-Time Monitoring Script

Want to watch the stats update automatically? Create this script:

### Create `watch_stats.sh`

```bash
#!/bin/bash
# File: watch_stats.sh

while true; do
    clear
    echo "=== API Stats - $(date) ==="
    echo ""
    curl -s localhost:8000/api/stats | python -m json.tool
    echo ""
    echo "Refreshing in 5 seconds... (Press Ctrl+C to stop)"
    sleep 5
done
```

### Make it executable and run:

```bash
chmod +x watch_stats.sh
./watch_stats.sh
```

**This updates every 5 seconds automatically!**

---

## 📱 Quick Reference Commands

### Check if backend is running:
```bash
curl localhost:8000/health
```

**Expected Output:**
```json
{"status": "healthy", "service": "card-discount-agent"}
```

### Check API stats:
```bash
curl localhost:8000/api/stats
```

### Check in browser:
```
http://localhost:8000/api/stats
```

### Check backend logs:
```bash
# In the terminal where backend is running
# You'll see real-time logs like:
INFO - Searching for deals: iPhone 16 Pro...
INFO - Rate limit: 1/4 used, 3 remaining
INFO - Found 8 deals
```

---

## 🎨 Prettier JSON Output (Optional)

If the JSON looks ugly, pipe it through `python`:

```bash
curl localhost:8000/api/stats | python -m json.tool
```

**OR** use `jq` (if installed):

```bash
curl localhost:8000/api/stats | jq
```

---

## 🔍 Troubleshooting

### Error: "Connection refused"

**Problem**: Backend is not running.

**Solution**:
```bash
cd /home/user/Projects_with_claude_code/card-discount-agent/backend
python app.py
```

Wait for:
```
INFO: Application startup complete.
```

Then try curl again.

---

### Error: "command not found: curl"

**Problem**: curl is not installed (rare on Linux/Mac).

**Solution on Linux**:
```bash
sudo apt install curl
```

**Solution on Mac**:
```bash
brew install curl
```

**Alternative**: Use browser instead - go to `http://localhost:8000/api/stats`

---

### Backend running on different port?

If you see something like:
```
INFO: Uvicorn running on http://0.0.0.0:5000
```

Then use:
```bash
curl localhost:5000/api/stats
```

---

## 📊 Interpreting Health Signals

### 🟢 Healthy (All Good)

```json
{
  "requests_in_window": 1,
  "remaining": 3,
  "utilization_percent": 25.0
}
```

**Meaning**: You can search freely!

---

### 🟡 Warning (Getting Close)

```json
{
  "requests_in_window": 3,
  "remaining": 1,
  "utilization_percent": 75.0
}
```

**Meaning**: Slow down, only 1 search left.

**Action**:
- Wait 60 seconds OR
- Search for something you've already searched (cache hit)

---

### 🔴 Rate Limited

```json
{
  "requests_in_window": 4,
  "remaining": 0,
  "utilization_percent": 100.0
}
```

**Meaning**: Temporarily maxed out.

**Action**:
- Wait 60 seconds for quota to reset OR
- Check `cache.size` - search for cached items (instant, no API call)

---

## 💡 Pro Tips

### Tip 1: Use Cache Wisely

If `cache.size` is 5, you have 5 searches that will be **instant** (no API call). Search for these again to avoid rate limits!

### Tip 2: Monitor Before Searching

Before making multiple searches, check stats:
```bash
curl localhost:8000/api/stats | grep remaining
```

If `remaining` is low, wait a bit.

### Tip 3: Cache = Free Searches

Cache hits don't count against rate limits! Search for popular items multiple times:
- First time: Uses API call
- Second+ time: Cache hit (instant, free)

### Tip 4: Background Monitoring

Run the `watch_stats.sh` script in a separate terminal to always see your quota.

---

## 🎓 Summary for Beginners

### What You Need to Remember:

1. **Open Terminal** (Command Prompt on Windows)
2. **Backend must be running** (`python app.py`)
3. **In NEW terminal**, run: `curl localhost:8000/api/stats`
4. **Check `remaining`**:
   - 3-4 = plenty of searches available ✅
   - 1-2 = running low ⚠️
   - 0 = wait 60 seconds 🔴

### Quick Checklist:

- [ ] Backend is running (Terminal 1)
- [ ] Opened new terminal (Terminal 2)
- [ ] Ran `curl localhost:8000/api/stats`
- [ ] Saw JSON output
- [ ] Checked `remaining` field

---

## 🖼️ Visual Guide

```
Terminal 1 (Backend)              Terminal 2 (Monitoring)
┌─────────────────────┐          ┌─────────────────────┐
│ $ python app.py     │          │ $ curl localhost... │
│                     │          │                     │
│ INFO: Started...    │          │ {                   │
│ INFO: Healthy       │          │   "remaining": 4    │
│                     │          │ }                   │
│ [Keep Running]      │          │                     │
└─────────────────────┘          └─────────────────────┘
```

---

**Now try it!** Start your backend, open a new terminal, and run the curl command. You should see your stats! 🎉
