-- from system user - create new db user ccactive_user
ALTER SESSION SET CONTAINER = XEPDB1;
CREATE USER ccactive_user IDENTIFIED BY &ccactive_user_password;--set password
--drop user ccactive_user;
GRANT CONNECT, RESOURCE TO ccactive_user;
GRANT CREATE VIEW TO ccactive_user;
GRANT CREATE PROCEDURE TO ccactive_user;
