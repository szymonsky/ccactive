-- select raportu czasu trwania statusów agentów w minutach, z podziałem na dzień
SELECT
    u.username,
    s.status_name,
    TRUNC(sl.timestamp_start) AS day,
    ROUND(
        SUM(
            EXTRACT(DAY FROM (COALESCE(sl.timestamp_end, CURRENT_TIMESTAMP) - sl.timestamp_start)) * 24 * 60 +
            EXTRACT(HOUR FROM (COALESCE(sl.timestamp_end, CURRENT_TIMESTAMP) - sl.timestamp_start)) * 60 +
            EXTRACT(MINUTE FROM (COALESCE(sl.timestamp_end, CURRENT_TIMESTAMP) - sl.timestamp_start))
        ), 0
    ) AS minutes_in_status
FROM status_logs sl
JOIN users u ON sl.user_id = u.user_id
JOIN statuses s ON sl.status_id = s.status_id
GROUP BY u.username, s.status_name, TRUNC(sl.timestamp_start)
ORDER BY u.username, day, s.status_name;