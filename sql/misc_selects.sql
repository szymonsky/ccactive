------- selecty do ogólnego sprawdzania i testowania

select * from users order by 1 desc;
select * from roles order by 1 desc;
select * from VIEW_CURRENT_STATUS order by 1 desc;
select * from work_sessions order by 1 desc;
SELECT * FROM status_logs ORDER BY timestamp_start desc;
SELECT * FROM status_logs ORDER BY timestamp_start DESC;
SELECT * FROM status_logs where source = 'voip' ORDER BY timestamp_start DESC;
select * from view_today_agent_status_time order by 1,2;

SELECT 
    log_id,
    user_id,
    status_id,
    timestamp_start,
    timestamp_end,
    source,
    external_call_id
FROM status_logs
ORDER BY user_id, timestamp_start;;

SELECT COUNT(*) as StatusLogsCount FROM status_logs;
SELECT COUNT(*) as WorkSessionsCount FROM work_sessions;

/*
--czyszczenie
DELETE FROM status_logs;
DELETE FROM work_sessions;
COMMIT;
*/