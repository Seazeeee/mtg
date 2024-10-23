SELECT  date, 
        name,
        CAST(JSON_EXTRACT(prices, 'usd') AS VARCHAR(255)) AS usd_prices, 
        type_line,
        CAST(JSON_EXTRACT(image_uris, 'normal') AS VARCHAR(2000)) as image
FROM scryfall_data