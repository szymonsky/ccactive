-- tylko do testowania
-- dodaje przykładowych użytkowników do tabeli USERS z hasłami w SHA-256
-- wykonywac z usera ccactive_user
-- UWAGA: dane testowe z jawnymi hasłami (w formie hashów SHA-256)


-- Użytkownik 1: Agent Jan (hasło: password)
INSERT INTO users (username, password_hash, role_id)
VALUES ('agent_jan', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8', 1);

-- Użytkownik 2: Agent Anna (hasło: test123)
INSERT INTO users (username, password_hash, role_id)
VALUES ('agent_anna', 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f', 1);

-- Użytkownik 3: Admin Marek (hasło: 123456)
INSERT INTO users (username, password_hash, role_id)
VALUES ('admin_marek', '8d969eef6ecad3c29a3a629280e686cff8fab43bd57452f5f92c3f2a0f7b3e8f', 2);
