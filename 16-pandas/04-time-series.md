# 04 — Time series

pandas has first-class support for dates and times. Use it — date arithmetic with raw `datetime` is painful, and rolling/resampling are central to data work.

## Parsing dates on load

```python
df = pd.read_csv("events.csv", parse_dates=["timestamp"])

# Or after the fact
df["ts"] = pd.to_datetime(df["ts"])
df["ts"] = pd.to_datetime(df["ts"], format="%Y-%m-%d %H:%M:%S")  # explicit
```

Parsed columns have dtype `datetime64[ns]` — fast to operate on, no per-row Python objects.

## A DatetimeIndex is the move

```python
df = df.set_index("ts").sort_index()
```

With a `DatetimeIndex`, you get powerful slicing:

```python
df["2026"]                     # all of 2026
df["2026-06"]                  # all of June 2026
df["2026-06-01":"2026-06-30"]  # range (inclusive)
df.between_time("09:00", "17:00")
```

## Resample — change frequency

```python
df["amount"].resample("D").sum()         # daily totals
df["amount"].resample("h").mean()        # hourly means  (note: lowercase 'h' is modern)
df["amount"].resample("W").max()         # weekly max
df["amount"].resample("ME").sum()        # month-end totals
```

`resample` is like a time-aware groupby. The string codes you'll use most: `D` (day), `h` (hour), `min` (minute), `W` (week), `MS`/`ME` (month start/end), `QS`/`QE`, `YS`/`YE`.

## Rolling windows

```python
df["amount"].rolling(7).mean()           # 7-row moving average
df["amount"].rolling("7D").mean()        # 7-DAY moving average (needs DatetimeIndex)
df["amount"].expanding().sum()           # cumulative
df["amount"].ewm(span=10).mean()         # exponentially weighted
```

Rolling with a string (`"7D"`) respects irregular timestamps. Rolling with an integer (`7`) just counts rows — easier but less correct for time-spaced data.

## Time zones

```python
ts = pd.to_datetime("2026-06-29 14:30")  # naive — no tz
ts_utc = ts.tz_localize("UTC")           # attach UTC
ts_ist = ts_utc.tz_convert("Asia/Kolkata")  # convert
```

Mixing naive and tz-aware timestamps raises an error. Pick one convention per project — storing as UTC and converting at display time is the safest default.

## Common pitfalls

- **Loading dates as strings.** If you skip `parse_dates`, everything is text and `df["ts"] > "2026-06-01"` does string compare, which works only by coincidence.
- **Mixed timezones.** UTC in storage; convert on the way out.
- **Daylight saving.** Resampling around DST transitions can produce surprising gaps or doubles. Use UTC for storage.

## Read deeper

- **PfDA** 3e, Ch. 11 — time series in pandas
