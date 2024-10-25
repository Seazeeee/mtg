WITH exploded_prices AS (
            SELECT
                set,
                name,
                CAST(JSON_EXTRACT(prices, '$.usd') AS DOUBLE) AS nonfoil_price,
                CAST(JSON_EXTRACT(prices, '$.usd_foil') AS DOUBLE) AS foil_price,
                CAST(JSON_EXTRACT(prices, '$.usd_etched') AS DOUBLE) AS etched_price,
                UNNEST(finishes) as finish
            FROM scryfall_data
        )
        SELECT
        set,
        name,
        finish,
        CASE
            WHEN finish LIKE '%nonfoil%' THEN nonfoil_price
            WHEN finish LIKE '%foil%' THEN foil_price
            WHEN finish LIKE '%etched%' THEN etched_price
        END AS price
        FROM exploded_prices
        WHERE price IS NOT NULL