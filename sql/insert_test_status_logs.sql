-- Testowe dane: historia zmian statusów agentów
-- wykonywać z usera: ccactive_user

-- Agent Jan: 2 statusy
INSERT INTO status_logs (user_id, status_id, timestamp_start, timestamp_end)
VALUES (1, 1, TO_TIMESTAMP('2025-12-13 08:00:00', 'YYYY-MM-DD HH24:MI:SS'), TO_TIMESTAMP('2025-12-13 08:30:00', 'YYYY-MM-DD HH24:MI:SS'));


INSERT INTO status_logs (user_id, status_id, timestamp_start, timestamp_end)
VALUES (1, 2, TO_TIMESTAMP('2025-12-13 08:30:00', 'YYYY-MM-DD HH24:MI:SS'), NULL);


-- Agent Anna: 1 status (offline)
INSERT INTO status_logs (user_id, status_id, timestamp_start, timestamp_end)
VALUES (2, 4, TO_TIMESTAMP('2025-12-13 07:45:00', 'YYYY-MM-DD HH24:MI:SS'), NULL);


-- Admin Marek: brak statusu (np. nieaktywny operacyjnie)