SELECT
        "main"."card_names_prices_finishes"."date" AS "date",
        "main"."card_names_prices_finishes"."name" AS "name",
        "main"."card_names_prices_finishes"."finish" AS "finish",
        AVG("main"."card_names_prices_finishes"."price") AS "avg"
FROM
        {{ ref('card_names_prices_finishes') }}
GROUP BY
        "main"."card_names_prices_finishes"."name",
        "main"."card_names_prices_finishes"."finish",
        "main"."card_names_prices_finishes"."date",
ORDER BY
        "main"."card_names_prices_finishes"."name" ASC,
        "main"."card_names_prices_finishes"."date" ASC,
    CASE 
        WHEN "main"."card_names_prices_finishes"."finish" = 'nonfoil' THEN 1
        WHEN "main"."card_names_prices_finishes"."finish" = 'etched' THEN 2
        WHEN "main"."card_names_prices_finishes"."finish" = 'foil' THEN 3
        ELSE 4  -- This will ensure any unexpected values are sorted last
END