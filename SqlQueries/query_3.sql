WITH get_category("ProductOrSectorCode", "stddevVal")
AS (
    SELECT "ProductOrSectorCode", stddev_samp("Value")
    FROM "wto_timeseries"
    GROUP BY "ProductOrSectorCode"
    HAVING stddev_samp("Value") > 0
)
SELECT "ProductOrSector" , "stddevVal"
FROM  get_category JOIN "services"
    USING("ProductOrSectorCode")
WHERE "stddevVal" IN (
                      SELECT MIN("stddevVal")
                      FROM get_category
                      );
