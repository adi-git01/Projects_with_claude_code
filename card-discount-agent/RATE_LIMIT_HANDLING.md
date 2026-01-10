# Rate Limit Handling - Implementation Guide

## Overview

The Card Discount Agent now includes comprehensive rate limit handling for the Gemini API free tier. This document explains the implementation and how to manage rate limits.

## What Was Added

### 1. Backend: Retry Logic with Exponential Backoff

**File**: `backend/services/gemini_service.py`

**Changes**:
- Added `time` and `google.api_core.exceptions` imports
- Implemented retry logic with exponential backoff (2s, 4s, 8s)
- Catches `ResourceExhausted` exceptions from Gemini API
- Provides user-friendly error messages after retries exhausted

```python
# Retry logic for rate limits
max_retries = 3
base_delay = 2  # seconds

for attempt in range(max_retries + 1):
    try:
        response = self.model.generate_content(prompt)
        return result
    except google_exceptions.ResourceExhausted as e:
        if attempt < max_retries:
            delay = base_delay * (2 ** attempt)  # 2s, 4s, 8s
            logger.warning(f"Rate limit hit. Retrying in {delay}s...")
            time.sleep(delay)
        else:
            raise ValueError("Gemini API rate limit exceeded...")
```

### 2. Backend: HTTP 429 Error Responses

**File**: `backend/api/routes.py`

**Changes**:
- Added specific handling for `ValueError` from rate limits
- Returns HTTP 429 (Too Many Requests) instead of 500
- Provides structured error response with suggestions

```python
except ValueError as e:
    if "rate limit" in str(e).lower():
        raise HTTPException(
            status_code=429,
            detail={
                "error": "rate_limit_exceeded",
                "message": str(e),
                "suggestion": "Please wait a few minutes and try again..."
            }
        )
```

### 3. Frontend: User-Friendly Error Messages

**File**: `frontend/src/services/api.ts`

**Changes**:
- Added axios response interceptor
- Detects 429 status codes
- Extracts detailed error messages from backend
- Shows "Rate Limit:" prefix for clarity

```typescript
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    if (error.response?.status === 429) {
      const detail = error.response.data as any;
      throw new Error(`Rate Limit: ${detail.message}`);
    }
    // ... other error handling
  }
);
```

## Gemini API Free Tier Limits

Google's Gemini API free tier has the following limits:

### Rate Limits
- **Requests per minute**: 15 requests
- **Requests per day**: 1,500 requests
- **Tokens per minute**: 1,000,000 input tokens

### What Triggers Rate Limits

Each product search consumes:
- **1 request** to Gemini API
- **~2,000-5,000 tokens** (depending on prompt size)

With 25+ platforms and detailed prompts, you can hit limits quickly when:
- Testing repeatedly within minutes
- Multiple users searching simultaneously
- Making many searches in a day

## Error Flow

### User Experience

**Before** (without rate limit handling):
```
Search → 500 Internal Server Error → Generic error message
```

**After** (with rate limit handling):
```
Search → Rate limit hit
      → Auto retry after 2s
      → Auto retry after 4s
      → Auto retry after 8s
      → If still failing: HTTP 429 with clear message
      → Frontend shows: "Rate Limit: Gemini API rate limit exceeded.
                         Please try again in a few minutes."
```

### Technical Flow

```
1. User searches for product
   ↓
2. Backend calls Gemini API
   ↓
3. Gemini returns 429 ResourceExhausted
   ↓
4. Backend catches exception
   ↓
5. Wait 2 seconds → Retry
   ↓
6. Still 429? Wait 4 seconds → Retry
   ↓
7. Still 429? Wait 8 seconds → Retry
   ↓
8. Still failing after 3 retries?
   ↓
9. Raise ValueError with clear message
   ↓
10. API routes catch ValueError
    ↓
11. Return HTTP 429 with details
    ↓
12. Frontend interceptor catches 429
    ↓
13. Extract error message
    ↓
14. Display to user: "Rate Limit: ..."
```

## Solutions for Rate Limits

### Option 1: Wait and Retry (Free)
- **Best for**: Individual users, development, testing
- **How**: Wait 5-10 minutes between searches
- **Cost**: $0

### Option 2: Upgrade to Paid Tier
- **Best for**: Production use, multiple users
- **Limits**: Much higher (60 RPM, higher daily limits)
- **Cost**: Pay-as-you-go pricing
- **Link**: https://ai.google.dev/pricing

### Option 3: Implement Caching (Future Enhancement)
- Cache search results for same product
- Reduce redundant API calls
- Set TTL (e.g., 1 hour for prices)

### Option 4: Queue System (Future Enhancement)
- Queue search requests
- Process one at a time
- Respect rate limits automatically

## Testing the Implementation

### Test 1: Verify Retry Logic

```bash
# In backend directory
python -c "
import asyncio
import os
from services.gemini_service import GeminiService

async def test():
    os.environ['GOOGLE_API_KEY'] = 'your_key_here'
    service = GeminiService()

    # This will trigger rate limits if you've already hit them
    try:
        result = await service.search_product_deals(
            query='iPhone 15',
            selected_cards=['hdfc-millennia']
        )
        print('Success:', result)
    except ValueError as e:
        print('Expected rate limit error:', e)

asyncio.run(test())
"
```

### Test 2: Verify Frontend Error Display

```bash
# Start backend and frontend
# In backend:
python app.py

# In frontend:
npm run dev

# Open browser console and try multiple searches quickly
# You should see clean error messages instead of raw 500 errors
```

### Test 3: Monitor Logs

Backend logs now show clear messages:

```
✓ Normal request:
INFO: Searching for deals: iPhone 15...
INFO: Found 8 deals

✓ Rate limit with retry:
WARNING: Rate limit hit. Retrying in 2s... (attempt 1/3)
WARNING: Rate limit hit. Retrying in 4s... (attempt 2/3)
INFO: Found 8 deals

✗ Rate limit exhausted:
WARNING: Rate limit hit. Retrying in 2s... (attempt 1/3)
WARNING: Rate limit hit. Retrying in 4s... (attempt 2/3)
WARNING: Rate limit hit. Retrying in 8s... (attempt 3/3)
ERROR: Rate limit exhausted after all retries
INFO: 127.0.0.1:55245 - "POST /api/search HTTP/1.1" 429 Too Many Requests
```

## Files Modified

### Backend
1. **services/gemini_service.py**
   - Lines 8-12: Added imports (time, google_exceptions)
   - Lines 72-104: Added retry logic with exponential backoff

2. **api/routes.py**
   - Lines 118-133: Added rate limit error handling
   - Returns HTTP 429 instead of 500

### Frontend
3. **src/services/api.ts**
   - Lines 1, 14-45: Added response interceptor
   - Extracts detailed error messages for 429 responses

## Configuration

### Adjust Retry Behavior

Edit `backend/services/gemini_service.py:73-74`:

```python
# Current: 3 retries with 2s, 4s, 8s delays
max_retries = 3
base_delay = 2

# More aggressive (faster give up):
max_retries = 2
base_delay = 1

# More patient (longer waits):
max_retries = 5
base_delay = 3
```

### Adjust API Timeout

Edit `frontend/src/services/api.ts:8`:

```typescript
// Current: 2 minutes
timeout: 120000,

// Shorter for faster failure:
timeout: 60000,  // 1 minute

// Longer for slow searches:
timeout: 180000,  // 3 minutes
```

## Monitoring Rate Limits

### Check Current Usage

Google doesn't provide a direct API to check quota usage, but you can:

1. **Monitor logs**: Count 429 errors in backend logs
2. **Google Cloud Console**: View API usage metrics
3. **Time-based estimates**: Track searches per minute/day

### Log Analysis

```bash
# Count 429 errors today
grep "429" backend/logs/*.log | wc -l

# Find rate limit patterns
grep "Rate limit hit" backend/logs/*.log

# See retry attempts
grep "Retrying in" backend/logs/*.log
```

## Future Improvements

### 1. Redis-based Rate Limiting
- Track requests per user/IP
- Enforce client-side limits before hitting API
- Fair usage across multiple users

### 2. Response Caching
```python
# Pseudo-code
cache_key = f"search:{product_name}:{card_ids}"
if cached := redis.get(cache_key):
    return cached
result = gemini_search(...)
redis.setex(cache_key, 3600, result)  # 1 hour TTL
```

### 3. Queue System
```python
# Pseudo-code
from celery import Celery
app = Celery('card-discount', broker='redis://localhost:6379')

@app.task(rate_limit='15/m')  # 15 per minute
def search_deals(query, cards):
    return gemini_search(query, cards)
```

### 4. Smart Retry with Jitter
```python
import random

# Add randomness to prevent thundering herd
delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
```

## FAQ

### Q: Why am I still getting errors after this fix?

A: The 500 error is fixed. The 429 error means you've hit actual API limits. Wait 5-10 minutes or upgrade to paid tier.

### Q: How many searches can I do per day?

A: Free tier: ~1,500 searches/day. But you'll hit rate limits at 15 requests/minute.

### Q: Can I increase the timeout?

A: Yes, edit `frontend/src/services/api.ts:8`, but Gemini usually responds in 30-60 seconds.

### Q: Should I upgrade to paid tier?

A: For production with real users: Yes. For development/personal use: No, free tier is fine.

### Q: What if retries don't help?

A: Retries only help with temporary spikes. If you've exhausted daily quota, you must wait 24 hours or upgrade.

## Summary

✅ **Implemented**:
- Automatic retry with exponential backoff (2s, 4s, 8s)
- HTTP 429 responses instead of 500 errors
- User-friendly error messages
- Clear logging for debugging

✅ **Benefits**:
- Graceful handling of rate limits
- Better user experience
- Clear error messaging
- No more confusing 500 errors for rate limits

⏳ **Future enhancements**:
- Response caching to reduce API calls
- Request queue system
- Redis-based rate limiting
- Per-user quota tracking

## Getting Help

If you continue having issues:

1. **Check logs**: `backend/logs/` or console output
2. **Verify API key**: `backend/.env` has valid `GOOGLE_API_KEY`
3. **Check quota**: Visit https://console.cloud.google.com/
4. **Wait**: If daily quota exhausted, wait 24 hours
5. **Upgrade**: Consider paid tier for production use

For API quotas and pricing:
- **Quotas**: https://ai.google.dev/gemini-api/docs/rate-limits
- **Pricing**: https://ai.google.dev/pricing
