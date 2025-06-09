WITH scoring_percentiles AS (
    SELECT
        *
        ,NTILE(100) OVER (ORDER BY risk) AS percentil
    FROM scoring
),
percentile_stats AS (
    SELECT
        percentil
        ,MIN(risk) AS valor_min
        ,MAX(risk) AS valor_max
        ,SUM(monto) AS monto_total
        ,SUM(CASE WHEN esFraude = 'Y' THEN monto ELSE 0 END) AS monto_fraude
        ,COUNT(*) AS cant_total
        ,SUM(CASE WHEN esFraude = 'Y' THEN 1 ELSE 0 END) AS cant_fraude
    FROM scoring_percentiles
    GROUP BY percentil
)
SELECT
    percentil
    ,valor_min
    ,valor_max
    ,monto_total
    ,monto_fraude
    ,(CASE WHEN monto_total > 0 THEN monto_fraude / monto_total ELSE 0 END) AS ratio_fraude_monto
    ,cant_total
    ,cant_fraude
    ,(CASE WHEN cant_total > 0 THEN CAST(cant_fraude AS DOUBLE) / cant_total ELSE 0 END) AS ratio_fraude_cant
FROM percentile_stats
ORDER BY percentil;