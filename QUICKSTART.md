# Quick Start Guide

Get your stock monitoring system running in 5 minutes!

## Step 1: Install Dependencies (1 minute)

```bash
pip install -r requirements.txt
```

## Step 2: Configure Your Stocks (2 minutes)

Edit `config/stocks.csv` with your watchlist. Use this format:

```csv
ticker,strategy,trend_score,quality_score,value_score,forensic_verdict,action,entry_zone,stop_loss,target,notes
RELIANCE,Momentum,100,9,7,Strong momentum,BUY,2800-2850,2700,3200,Large cap
INFY,Quality,85,10,6,High quality,ACCUMULATE,1500-1550,1450,1700,IT stock
```

**Important**: Only edit the stock rows, keep the header row as-is.

## Step 3: Set Up Environment (1 minute)

```bash
cp .env.example .env
```

That's it! The default settings work fine. Edit `.env` later if you want email alerts.

## Step 4: Test Run (1 minute)

```bash
python main.py once
```

You should see:
- Current prices for all your stocks
- Any alerts if conditions are met
- A status table

## Step 5: Start Monitoring

```bash
python main.py
```

The system will now:
- Check stocks every 15 minutes
- Only run during market hours (9 AM - 3:30 PM)
- Alert you when conditions are met

Press `Ctrl+C` to stop.

## That's It!

Your stock monitor is now running. Check the logs in the `logs/` folder for history.

## Common Questions

**Q: How do I add more stocks?**
A: Just add more rows to `config/stocks.csv`

**Q: How do I change check frequency?**
A: Edit `CHECK_INTERVAL_MINUTES` in `.env` file

**Q: Can I run it 24/7?**
A: Yes! It automatically skips non-market hours

**Q: How do I enable email alerts?**
A: See README.md section "Email Alerts Setup"

## Example Stock Entry

Here's what each field means:

```csv
SARDA,Deep Value,64,10,8.7,High growth + low valuation,AGGRESSIVE BUY,525,475,650,Waking up
```

- **SARDA**: Stock ticker (will auto-add .NS for NSE)
- **Deep Value**: Your strategy label
- **64**: Trend score (your own rating)
- **10**: Quality score
- **8.7**: Value score
- **High growth...**: Your analysis notes
- **AGGRESSIVE BUY**: Action recommendation
- **525**: Entry price (or use range like "80-84")
- **475**: Stop loss price
- **650**: Target price
- **Waking up**: Additional notes

## Alert Examples

When alerts trigger, you'll see:

```
🔔 SARDA @ ₹527.50 - IN ENTRY ZONE (₹525-₹535)
🔔 INFY @ ₹1700.00 - TARGET REACHED (₹1700)
🔔 RELIANCE @ ₹2690.00 - STOP LOSS HIT (₹2700)
```

## Next Steps

1. Run `python main.py status` to see current prices
2. Run `python main.py` to start continuous monitoring
3. Check `logs/alerts.log` for alert history
4. Customize `.env` for your preferences

For detailed documentation, see [README.md](README.md)
