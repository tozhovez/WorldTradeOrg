WITH get_transport("Period", "AVGVal")
AS (
    SELECT "Period", AVG("Value")
    FROM "wto_timeseries"
        JOIN "periods"
        USING("PeriodCode")
    WHERE "ProductOrSectorCode" IN (
                                    SELECT "ProductOrSectorCode"
                                    FROM "services"
                                    WHERE "ProductOrSector" = 'Transport'
                                    LIMIT 1
                                    )
    GROUP BY "Period"
)
SELECT "Period", "AVGVal"
FROM "get_transport"
WHERE "AVGVal" IN (
                   SELECT MAx("AVGVal")
                   FROM "get_transport"
                   );
