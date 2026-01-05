# Custom Conditions Guide

The stock monitor supports advanced custom conditions including technical indicators, commodity prices, forex rates, and more!

## How It Works

Alerts trigger when **ANY** condition is met (OR logic):
- Stock price enters entry zone **OR**
- Stop loss is hit **OR**
- Target is reached **OR**
- RSI drops below threshold **OR**
- Aluminum price exceeds threshold **OR**
- Any custom condition you define

## Supported Metrics

### 1. Technical Indicators

| Metric | Description | Example |
|--------|-------------|---------|
| `rsi` | Relative Strength Index (14-day) | `rsi<30` (oversold) |
| `ma20` | 20-day Moving Average | `ma20>500` |
| `ma50` | 50-day Moving Average | `ma50>300` |
| `ma200` | 200-day Moving Average | `ma200<price` |

### 2. Commodity Prices

| Metric | Description | Example |
|--------|-------------|---------|
| `aluminum_lme` | Aluminum LME price (USD/tonne) | `aluminum_lme>2400` |
| `copper_lme` | Copper LME price | `copper_lme>8000` |
| `crude_oil` | Crude oil futures | `crude_oil<80` |
| `gold` | Gold futures | `gold>2000` |
| `silver` | Silver futures | `silver>25` |
| `zinc` | Zinc futures | `zinc>2500` |
| `natural_gas` | Natural gas futures | `natural_gas<3` |

### 3. Forex & Indices

| Metric | Description | Example |
|--------|-------------|---------|
| `usd_inr` | USD to INR exchange rate | `usd_inr>83` |
| `nifty50` | Nifty 50 index | `nifty50>24000` |
| `sensex` | BSE Sensex | `sensex>80000` |
| `dow` | Dow Jones | `dow>42000` |
| `sp500` | S&P 500 | `sp500>5800` |
| `nasdaq` | NASDAQ | `nasdaq>19000` |

### 4. Stock Fundamentals

| Metric | Description | Example |
|--------|-------------|---------|
| `pe_ratio` | Price to Earnings ratio | `pe_ratio<15` |
| `price` | Current stock price | `price>500` |

## CSV Format

Add custom conditions in the `custom_conditions` column:

```csv
ticker,strategy,entry_zone,stop_loss,target,custom_conditions
HINDALCO,Commodity,600-620,580,750,aluminum_lme>2400,rsi<35
ONGC,Energy,280-290,270,350,crude_oil<80,usd_inr>82.5
RELIANCE,Large Cap,2800-2850,2700,3200,nifty50>24000
TATASTEEL,Cyclical,160-165,155,190,rsi<30
```

## Syntax Rules

### Format
```
metric operator threshold
```

### Operators
- `>` Greater than
- `<` Less than
- `>=` Greater than or equal
- `<=` Less than or equal
- `==` Equal to

### Multiple Conditions
Separate with commas. Alert triggers if **ANY** condition is met:

```
rsi<30,crude_oil<75,aluminum_lme>2400
```

This means: Alert if RSI < 30 **OR** crude oil < 75 **OR** aluminum > 2400

## Examples

### Example 1: Aluminum Stock with Commodity Alert
```csv
HINDALCO,Commodity,600-620,580,750,aluminum_lme>2400
```
**Triggers when:**
- Price enters 600-620 **OR**
- Aluminum price > $2400/tonne

### Example 2: Oil Stock with Multiple Conditions
```csv
ONGC,Energy,280-290,270,350,crude_oil<75,rsi<35,usd_inr>83
```
**Triggers when:**
- Price enters 280-290 **OR**
- Crude oil < $75 **OR**
- RSI < 35 **OR**
- USD/INR > 83

### Example 3: Bank Stock with Index Condition
```csv
HDFCBANK,Banking,1600-1650,1550,1800,nifty50>24000,rsi<40
```
**Triggers when:**
- Price enters 1600-1650 **OR**
- Nifty 50 > 24,000 **OR**
- RSI < 40

### Example 4: Technical Indicators Only
```csv
RELIANCE,Momentum,2800-2900,2700,3200,rsi<30,ma50>2700
```
**Triggers when:**
- Price enters 2800-2900 **OR**
- RSI < 30 (oversold) **OR**
- 50-day MA > 2700

## Real-World Use Cases

### 1. Commodity-Linked Stocks
For stocks affected by commodity prices:
```csv
HINDALCO,Aluminum,600-620,580,750,aluminum_lme>2400
TATASTEEL,Steel,160-165,155,190,crude_oil<75
VEDL,Mining,400-410,390,480,copper_lme>8000,zinc>2500
```

### 2. Oil & Gas Stocks
Monitor crude oil prices:
```csv
ONGC,Oil,280-290,270,350,crude_oil<75
BPCL,Refining,350-360,340,420,crude_oil>85
IOC,Energy,140-145,135,165,crude_oil<70
```

### 3. Export-Oriented Stocks
Watch forex rates:
```csv
TCS,IT,3500-3600,3400,4000,usd_inr>83.5
INFOSYS,IT,1400-1450,1350,1600,usd_inr>84
WIPRO,IT,450-465,440,520,usd_inr>83
```

### 4. Technical Setups
RSI and moving averages:
```csv
RELIANCE,Momentum,2800-2900,2700,3200,rsi<30
HDFCBANK,Reversal,1600-1650,1550,1800,rsi>70,ma50<price
ICICIBANK,Breakout,1100-1150,1080,1250,price>ma200
```

### 5. Market-Dependent Plays
Conditional on market indices:
```csv
BANKBEES,ETF,490-500,480,550,nifty50>24500
JUNIORBEES,ETF,650-670,640,730,sensex>81000
```

## Alert Output Examples

When a custom condition triggers, you'll see:

```
🔔 HINDALCO @ ₹615.50 - CUSTOM: Aluminum Lme=2,450.00 > 2400
🔔 ONGC @ ₹285.00 - IN ENTRY ZONE (₹280-₹290), CUSTOM: Crude Oil=74.50 < 75
🔔 TATASTEEL @ ₹162.30 - CUSTOM: RSI=28.50 < 30
🔔 TCS @ ₹3,580.00 - CUSTOM: Usd Inr=83.75 > 83.5
```

## Tips

1. **Keep it simple**: Start with 1-2 custom conditions per stock
2. **Use meaningful thresholds**: Research typical ranges for each metric
3. **Combine wisely**: Mix price targets with external factors
4. **Test first**: Run `python main.py once` to verify conditions work
5. **Monitor logs**: Check `logs/monitor.log` for detailed condition checking

## Performance Notes

- Technical indicators require historical data fetching (adds 2-3 seconds per stock)
- External metrics (commodities, forex) are cached for 5 minutes
- Price data is cached for 1 minute
- Use custom conditions selectively for critical stocks to optimize performance

## Troubleshooting

### Condition Not Triggering?

1. **Check the log**: `logs/monitor.log` shows which values were fetched
2. **Verify metric name**: Must match exactly (case-insensitive)
3. **Syntax check**: Ensure `metric operator value` format
4. **Data availability**: Some metrics may not be available 24/7

### Getting "No data available"?

- Technical indicators need sufficient historical data (50+ days for MA50)
- Some commodities only update during trading hours
- Check internet connection

## Adding Custom Metrics

To add your own metrics, edit `src/services/metrics_fetcher.py` and add to the `symbol_map`:

```python
symbol_map = {
    'your_metric': 'SYMBOL',  # Yahoo Finance symbol
    # ... existing mappings
}
```

## Advanced: Custom Formulas

For complex conditions, you can modify `src/models/stock.py` to add custom logic:

```python
# Example: PE ratio from stock info
elif condition.metric == 'pe_ratio':
    # Add your custom fetching logic here
    pass
```

## Summary

Custom conditions make the stock monitor incredibly powerful:
- ✅ Monitor multiple factors simultaneously
- ✅ Alert on **ANY** condition (OR logic)
- ✅ Combine price, technical, fundamental, and external data
- ✅ Perfect for commodity-linked and export stocks
- ✅ Easy CSV configuration

Start simple and expand as you become familiar with the system!
