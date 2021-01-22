WITH get_travel("Year", "sumVal")
AS (
    SELECT "Year", SUM("Value")
    FROM "wto_timeseries"
    WHERE "ProductOrSectorCode" IN (
                                    SELECT "ProductOrSectorCode"
                                    FROM "services"
                                    WHERE "ProductOrSector" = 'Travel'
                                    LIMIT 1
                                    )
    GROUP BY "Year"
)
SELECT "Year", "sumVal"
FROM "get_travel"
WHERE "sumVal" IN (
                   SELECT MAX("sumVal")
                   FROM "get_travel"
                   );
