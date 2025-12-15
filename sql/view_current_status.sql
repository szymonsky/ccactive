-- wykonywać z usera: ccactive_user
-- widok pokazujący aktualny (najnowszy) status każdego użytkownika

CREATE OR REPLACE VIEW view_current_status AS
SELECT
    u.username,
    r.role_name,
    s.status_name,
    sl.timestamp_start
FROM status_logs sl
JOIN (
    SELECT user_id, MAX(timestamp_start) AS latest_start
    FROM status_logs
    GROUP BY user_id
) latest ON sl.user_id = latest.user_id AND sl.timestamp_start = latest.latest_start
JOIN users u ON sl.user_id = u.user_id
JOIN roles r ON u.role_id = r.role_id
JOIN statuses s ON sl.status_id = s.status_id;