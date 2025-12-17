-- dashboard admina: czas pracy agentów w statusach (bieżący dzień) – widok bazy
-- wykonywac z usera ccactive_user

CREATE OR REPLACE VIEW view_today_agent_status_time AS
SELECT
    u.username,
    s.status_name,
    ROUND(
        SUM(
            EXTRACT(DAY FROM (NVL(sl.timestamp_end, CURRENT_TIMESTAMP) - sl.timestamp_start)) * 24 * 60 +
            EXTRACT(HOUR FROM (NVL(sl.timestamp_end, CURRENT_TIMESTAMP) - sl.timestamp_start)) * 60 +
            EXTRACT(MINUTE FROM (NVL(sl.timestamp_end, CURRENT_TIMESTAMP) - sl.timestamp_start))
        )
    ) AS minutes_today
FROM status_logs sl
JOIN users u ON u.user_id = sl.user_id
JOIN statuses s ON s.status_id = sl.status_id
WHERE TRUNC(sl.timestamp_start) = TRUNC(CURRENT_DATE)
GROUP BY
    u.username,
    s.status_name
ORDER BY
    u.username,
    s.status_name;
