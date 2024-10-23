SELECT DISTINCT date, name, JSON_EXTRACT(prices, '$.usd') AS usd_prices
FROM scryfall_data