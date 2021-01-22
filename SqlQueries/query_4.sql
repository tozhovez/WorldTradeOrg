WITH get_data("yid", "pid", "pcid", "Year", "Period", "Value")
AS (
    SELECT  "Year" AS "yid", "PeriodCode" AS "pid", "ProductOrSectorCode" AS "pcid"
            , "Year", "Period", "Value"
    FROM "wto_timeseries"
        JOIN "periods"
        USING("PeriodCode")
    WHERE "ProductOrSectorCode" IN (
                                    SELECT "ProductOrSectorCode"
                                    FROM "services"
                                    WHERE "ProductOrSector" LIKE '%Telecommunications, computer, and information%'
                                    LIMIT 1
                                    )
    ORDER BY "Year", "PeriodCode"
),

get_fillup AS (
    SELECT  "yid", "pid", "pcid"
            , ("Period"||' '||"Year")::text AS "nqp", "Value"
            ,LAG("Value", 1, 0.0) OVER (PARTITION BY "pcid" ORDER BY "yid", "pid") AS "fillupValue"
            ,"Value" - LAG("Value", 1, 0.0) OVER (PARTITION BY "pcid" ORDER BY "yid", "pid") > 0.0 AS "fillup"
    FROM get_data
),

get_counts_groups AS(
    SELECT  *
            ,COUNT(*) FILTER (WHERE "fillup") OVER (PARTITION BY "pcid" ORDER BY "yid", "pid") AS "tank"
            ,COUNT("fillup") FILTER (WHERE "Value" < "fillupValue") OVER (PARTITION BY "pcid" ORDER BY "yid", "pid") AS "ftank"
    FROM get_fillup
),
consistent_increase AS(
    SELECT  "ftank", COUNT("Value") AS "nvals"
            ,STRING_AGG("nqp", ' , ') AS "c_q"
            ,STRING_AGG("Value"::text , ', ') AS "vals"
    FROM get_counts_groups
    GROUP BY "ftank"
    HAVING COUNT("Value") >= 3
)
SELECT "c_q" AS "Consecutive Quarters", "nvals" AS "number quarters", "vals" AS "Values"
FROM consistent_increase;
