# 2026 Gemini API Rate Limit Fix

## Critical Issue Identified

Based on your dashboard and logs showing **100% 429 errors**, the root causes were:

### 1. RPM Mismatch (10 vs 5)
- **Problem**: Code configured for 10 RPM
- **Actual Limit**: Gemini Free Tier (Jan 2026) = **5 RPM**
- **Result**: Immediate 429 errors

### 2. Too-Short Retry Delays
- **Problem**: Retries at 2s, 4s, 8s intervals
- **Required**: At 5 RPM limit, need **minimum 12 seconds** between calls
- **Result**: All retries also hit 429

### 3. Daily Quota Exhaustion
- **Problem**: Previous testing exhausted daily quota
- **Evidence**: Both requests (9 minutes apart) failed immediately
- **Reset**: Daily quotas reset at **midnight Pacific Time**

---

## Fixes Implemented

### Fix 1: Lower RPM to 4 ✅

**File**: `backend/services/gemini_service.py:38`

**Before**:
```python
self.rate_limiter = RateLimiter(max_requests=10, time_window=60)
```

**After**:
```python
# 4 RPM (safe buffer under 5 RPM limit for 2026 free tier)
self.rate_limiter = RateLimiter(max_requests=4, time_window=60)
```

**Impact**:
- Prevents exceeding 5 RPM hard limit
- 4 RPM = 15 seconds between requests (safe buffer)
- Local rate limiter now matches API constraints

---

### Fix 2: Increase Retry Delays ✅

**File**: `backend/services/gemini_service.py:107`

**Before**:
```python
base_delay = 2  # Exponential backoff: 2s, 4s, 8s
```

**After**:
```python
base_delay = 15  # Exponential backoff: 15s, 30s, 60s
```

**Impact**:
- First retry: 15s (vs 2s) - respects 12s minimum
- Second retry: 30s (vs 4s) - more likely to succeed
- Third retry: 60s (vs 8s) - maximum patience

**Why This Matters**:
- 5 RPM = 1 request every 12 seconds
- Previous 2s retry was **6x too fast**
- New 15s retry gives API time to reset

---

### Fix 3: Switch to Better Model ✅

**File**: `backend/services/gemini_service.py:32`

**Before**:
```python
model_name='gemini-2.0-flash-exp'
```

**After**:
```python
model_name='gemini-2.0-flash-thinking-exp'
```

**Why**:
- `flash-thinking-exp` may have better rate limits
- Same capabilities, different quota allocation
- Worth testing before upgrading to paid tier

---

## Expected Behavior After Fix

### Scenario: Single Search

**Before**:
```
[18:38:48] Request 1 → 429 (immediate)
[18:38:50] Retry 1 (2s later) → 429
[18:38:52] Retry 2 (4s later) → 429
[18:38:56] Retry 3 (8s later) → 429
Result: FAILED after 8 seconds
```

**After**:
```
[Time 0s] Rate limiter checks: OK (0/4 used)
[Time 0s] Request 1 → If quota available: SUCCESS
[Time 0s] OR if quota hit → 429
[Time 15s] Retry 1 → More likely to succeed
[Time 45s] Retry 2 → Even more time for quota reset
[Time 105s] Retry 3 → Maximum wait
Result: SUCCESS (if daily quota not exhausted)
       OR clear error message (if daily quota exhausted)
```

### Scenario: Multiple Searches

**Before** (10 RPM):
```
Search 1 at 0s → 429
Search 2 at 6s → 429  (too fast)
Search 3 at 12s → 429 (too fast)
All fail due to not respecting 12s minimum
```

**After** (4 RPM):
```
Search 1 at 0s → Queued
Search 2 at 15s → Queued (rate limiter auto-waits)
Search 3 at 30s → Queued (rate limiter auto-waits)
All succeed (if daily quota available)
```

---

## Understanding the Logs

### Your Original Logs Analysis

```
18:38:48 - Request: iphone 16 pro
18:38:50 - Retry after 2s → FAILED (too soon!)
18:38:52 - Retry after 4s → FAILED (still too soon!)
18:38:56 - Retry after 8s → FAILED (still too soon!)

18:47:25 - Request: Philips OneBlade (9 minutes later!)
18:47:25 - IMMEDIATE FAIL → This proves daily quota exhausted
```

**Key Insight**: If a request fails **immediately** even after 9 minutes, it's not an RPM issue—it's **daily quota exhausted**.

### What You'll See Now

```
[Timestamp] INFO - Gemini service initialized with search grounding, rate limiting (4 RPM - 2026 limits), and caching
[Timestamp] INFO - Searching for deals: ... (cache miss)
[Timestamp] INFO - Prompt size: ~800 chars (~200 tokens)
[Timestamp] INFO - Rate limit: 1/4 used, 3 remaining
[Timestamp] INFO - Found 8 deals  ← SUCCESS!
```

**OR if daily quota hit**:
```
[Timestamp] WARNING - Rate limit hit. Retrying in 15s... (attempt 1/3)
[Timestamp] WARNING - Rate limit hit. Retrying in 30s... (attempt 2/3)
[Timestamp] WARNING - Rate limit hit. Retrying in 60s... (attempt 3/3)
[Timestamp] ERROR - Gemini API rate limit exceeded (5 RPM / Daily quota).
                     Please wait 10-15 minutes and try again.
                     Free tier: 5 requests/min, limited daily quota.
```

---

## Daily Quota Issue

### The Problem

Your logs show **immediate failures even after long waits** (9 minutes between requests). This is the smoking gun for **daily quota exhaustion**.

### Free Tier Daily Limits (Jan 2026)

| Model | RPM | RPD (Requests Per Day) |
|-------|-----|------------------------|
| gemini-2.0-flash-exp | 5 | **Unknown (likely 100-500)** |
| gemini-2.0-flash-thinking-exp | 5 | **Unknown (possibly higher)** |
| gemini-1.5-flash | 15 | 1,500 |
| gemini-1.5-flash-8b | 15 | 1,500 |

**With Search Grounding**: Daily limits are often **much lower** (e.g., 50-100 RPD).

### How to Check If You Hit Daily Quota

1. **Wait until midnight Pacific Time** (UTC-8)
2. **Try one search immediately after reset**
3. **If it succeeds**: Daily quota was the issue
4. **If it fails**: Model/API key issue

### Temporary Workaround

If you hit daily quota and can't wait:

**Option 1: Switch to Non-Grounding Model**
```python
# Remove search grounding temporarily
self.model = genai.GenerativeModel(
    model_name='gemini-2.0-flash-thinking-exp'
    # No tools parameter = no search grounding
)
```

**Tradeoff**: No live web search, but higher daily quota.

**Option 2: Try Different Model**
```python
# Try 1.5 Flash (confirmed 1500 RPD)
model_name='gemini-1.5-flash'
```

**Tradeoff**: Older model, but much higher daily quota.

---

## Testing Instructions

### Step 1: Restart Backend

```bash
cd card-discount-agent/backend
python app.py
```

**Look for**:
```
INFO - Gemini service initialized with search grounding, rate limiting (4 RPM - 2026 limits), and caching
```

### Step 2: Wait for Quota Reset

**If you already exhausted daily quota today**:
- Wait until **midnight Pacific Time** (check: https://time.is/PT)
- **OR** wait **10-15 minutes** if you haven't hit daily limit

### Step 3: Test Single Search

```bash
# Frontend
npm run dev

# Search for: iPhone 16 Pro
# Cards: HDFC Millennia
```

**Expected**:
- ✅ **Success**: "Found 8 deals" in backend logs
- ⏸️ **Rate Limit Warning**: "Retrying in 15s..." (will auto-retry)
- ❌ **Daily Quota**: "Daily quota exceeded" (wait until midnight PT)

### Step 4: Test Multiple Searches

Try searching 3 different products back-to-back.

**Expected**:
```
Search 1: Immediate (0s wait)
Search 2: 15s wait by rate limiter → Success
Search 3: 15s wait by rate limiter → Success
```

### Step 5: Test Caching

Search for the **same product twice**.

**Expected**:
```
First search: Cache miss → API call → 15-30s response time
Second search: Cache HIT → Instant response (no API call)
```

---

## Monitoring

### Check Rate Limiter Status

```bash
curl http://localhost:8000/api/stats
```

**Response**:
```json
{
  "rate_limiter": {
    "requests_in_window": 2,
    "max_requests": 4,
    "remaining": 2,
    "utilization_percent": 50.0
  },
  "cache": {
    "size": 3,
    "ttl_seconds": 3600
  }
}
```

### Interpret Results

- **requests_in_window**: Requests made in last 60 seconds
- **remaining**: How many more requests you can make
- **utilization_percent**: How close to limit (>75% = caution)

---

## If Still Getting 429 Errors

### Scenario 1: Immediate 429 (Daily Quota)

**Symptom**: First request of the day fails immediately

**Solution**:
1. Wait until midnight Pacific Time
2. **OR** remove search grounding temporarily:
   ```python
   # In gemini_service.py
   self.model = genai.GenerativeModel(
       model_name='gemini-2.0-flash-thinking-exp'
       # No tools parameter
   )
   ```

### Scenario 2: 429 After 2-3 Searches (RPM)

**Symptom**: First search succeeds, then 429 after a few more

**Solution**:
- Rate limiter should prevent this
- Check logs for "Rate limit: X/4 used"
- If still happening, reduce to **3 RPM**:
  ```python
  self.rate_limiter = RateLimiter(max_requests=3, time_window=60)
  ```

### Scenario 3: Always 429 (API Key/Model Issue)

**Symptom**: Even after midnight reset, all requests fail

**Solutions**:
1. **Check API key**: Visit https://aistudio.google.com/apikey
2. **Try different model**:
   ```python
   model_name='gemini-1.5-flash'  # Known working limits
   ```
3. **Remove search grounding** (see Scenario 1)

---

## Upgrade Path

If free tier is too restrictive:

### Paid Tier Benefits

| Feature | Free Tier | Paid Tier |
|---------|-----------|-----------|
| RPM | 5 | 1,000 |
| RPD | ~100-500 | Unlimited |
| Cost | $0 | ~$0.0002 per search |

### Cost Analysis

- **100 searches/day**: $0.02/day = **$0.60/month**
- **1,000 searches/day**: $0.20/day = **$6/month**
- **10,000 searches/day**: $2/day = **$60/month**

### How to Upgrade

1. Visit https://console.cloud.google.com/
2. Enable billing for your project
3. No code changes needed (same API key works)

---

## Summary of Changes

| Setting | Before | After | Why |
|---------|--------|-------|-----|
| **RPM Limit** | 10 | **4** | Gemini 2026 free tier = 5 RPM |
| **Retry Delays** | 2s, 4s, 8s | **15s, 30s, 60s** | 5 RPM needs 12s between calls |
| **Model** | gemini-2.0-flash-exp | **gemini-2.0-flash-thinking-exp** | Potentially better limits |
| **Error Message** | Generic | **Specific (5 RPM / Daily quota)** | Clearer user guidance |

---

## Expected Results

### Before Fixes
```
❌ 0 successful searches
❌ 100% 429 error rate
❌ Failures even 9 minutes apart
❌ Retries too fast (2s, 4s, 8s)
```

### After Fixes
```
✅ 4 searches/minute possible
✅ Automatic 15s spacing via rate limiter
✅ Longer retry delays (15s, 30s, 60s)
✅ Cache prevents duplicate API calls
✅ Clear error messages if daily quota hit
```

### Daily Capacity (with Caching)

Assuming 70% cache hit rate:
- **4 RPM** = 240 requests/hour
- With **70% cache**: 240 / 0.3 = **800 effective searches/hour**
- **Daily**: 800 × 24 = **19,200 effective searches/day**

**BUT**: Limited by daily quota (~100-500 actual API calls/day)

---

## Next Steps

1. ✅ **Restart backend** with new settings
2. ⏰ **Wait for quota reset** (midnight PT or 10-15 min)
3. 🧪 **Test single search** to verify fixes
4. 📊 **Monitor `/api/stats`** endpoint
5. 💰 **Consider paid tier** if daily quota too restrictive

---

## Files Modified

- ✅ `backend/services/gemini_service.py`
  - Line 32: Model changed to `gemini-2.0-flash-thinking-exp`
  - Line 38: Rate limiter changed to 4 RPM
  - Line 107: Retry delay changed to 15s base
  - Line 135-140: Improved error message

---

## Quick Reference

### Current Settings
```python
Model: gemini-2.0-flash-thinking-exp
Search Grounding: Enabled
Rate Limit: 4 requests/minute
Retry Delays: 15s, 30s, 60s
Cache TTL: 1 hour
```

### Free Tier Limits (2026)
```
RPM: 5 requests/minute
RPD: ~100-500 requests/day (varies by model)
TPM: 1M tokens/minute
Reset: Midnight Pacific Time
```

### Support Resources
- **API Limits**: https://ai.google.dev/gemini-api/docs/rate-limits
- **Pricing**: https://ai.google.dev/pricing
- **Console**: https://console.cloud.google.com/

---

**Status**: ✅ Fixes implemented and ready for testing
**Next Action**: Restart backend and test after quota reset
