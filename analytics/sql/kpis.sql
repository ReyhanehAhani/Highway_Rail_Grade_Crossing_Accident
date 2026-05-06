-- DuckDB KPIs on published crossing aggregates

CREATE OR REPLACE VIEW sy AS
SELECT * FROM read_csv_auto('{{PUBLISHED}}/severity_by_state_year.csv');

CREATE OR REPLACE VIEW dev AS
SELECT * FROM read_csv_auto('{{PUBLISHED}}/crossing_device_mix.csv');

-- Incidents by year (national roll-up)
SELECT Year, SUM(Incident_Count) AS incidents
FROM sy
GROUP BY Year
ORDER BY Year;

-- Top risk states (total incidents)
SELECT State, SUM(Incident_Count) AS incidents
FROM sy
GROUP BY State
ORDER BY incidents DESC
LIMIT 15;

-- YoY national
WITH t AS (
  SELECT Year, SUM(Incident_Count) AS inc FROM sy GROUP BY Year
)
SELECT cur.Year AS y,
       cur.inc AS incidents,
       prev.inc AS prev_inc,
       ROUND(100.0 * (cur.inc - prev.inc) / NULLIF(prev.inc, 0), 2) AS yoy_pct
FROM t cur
LEFT JOIN t prev ON prev.Year = cur.Year - 1
ORDER BY y;

-- Device mix sanity
SELECT * FROM dev ORDER BY Incident_Count DESC;
