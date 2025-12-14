# ccactive

Projekt aplikacji CCActive - aplikacja desktopowa do analizy czasu pracy agentów call center.


## Oracle XE troubleshooting

In Oracle Database XE 21c on Windows, connection issues (ORA-12514)
may occur after system restart due to incorrect LOCAL_LISTENER configuration.

To fix the issue, connect as SYSDBA and execute:

ALTER SYSTEM SET LOCAL_LISTENER =
'(ADDRESS=(PROTOCOL=TCP)(HOST=<HOSTNAME>)(PORT=1521))'
SCOPE=BOTH;

ALTER SYSTEM REGISTER;
