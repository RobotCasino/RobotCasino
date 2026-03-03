---
trigger: always_on
---

# Aviator Tendency

## Support and Resistance Levels
These are horizontal "boundaries" created by historical data points.
Support (Floor): A specific multiplier level (e.g., 1.20x) where the results consistently stop falling and start to rise again. In a script, this is a Local Minimum.
Resistance (Ceiling): A multiplier level (e.g., 2.50x) that the game struggles to break through. When a result finally "breaks" this resistance, it usually signals a Breakout, often leading to a high multiplier (Pink/Golden).
## Trend States (Global Sentiment)
This is the "background color" of the market (the game's current algorithm state).
Bullish Trend (High): Characterized by "Higher Highs" (each peak is higher than the last). The script should identify this as a high-confidence entry zone for multipliers above 10x.
Bearish Trend (Low): Characterized by "Lower Lows" or a sequence of "Blues" (1.0x - 1.2x). The script should trigger a Cooldown/Stop-Loss period here.
Sideways/Ranging (Stable): The results oscillate between a fixed support and resistance. Ideal for Scalping (small, quick wins).
## Pattern Recognition (Mirroring & Confluence)
Sequencing: Detecting repeated color strings (e.g., [Blue, Blue, Purple] -> [Blue, Blue, ?]).
Confluence: The moment when a Time Interval (e.g., "A Pink usually drops every 15 minutes") aligns with a Support Level. This is the highest probability signal for your script.
Relative Strength: Analyzing if the current "climb" has more momentum than the previous one by comparing the Slope of the graph.

