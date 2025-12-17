-- dashboard admina: zliczenie liczby agentów w poszczególnych statusach (stan bieżący)

SELECT
    status_name,
    COUNT(*) AS agent_count
FROM view_current_status
GROUP BY status_name
ORDER BY status_name