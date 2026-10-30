-- Incidents by severity
SELECT severity, COUNT(*) AS incident_count
FROM incidents
GROUP BY severity
ORDER BY incident_count DESC;

-- Incidents by department
SELECT department, COUNT(*) AS incident_count
FROM incidents
GROUP BY department
ORDER BY incident_count DESC;

-- High-priority incidents still requiring attention
SELECT incident_id, reported_at, department, location,
       incident_type, severity, status
FROM incidents
WHERE is_high_priority = 1
  AND status IN ('OPEN', 'IN_REVIEW')
ORDER BY reported_at DESC;

-- Incidents by month
SELECT month, COUNT(*) AS incident_count
FROM incidents
GROUP BY month
ORDER BY month;
