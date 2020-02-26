FROM library/postgres
COPY ./sql_commands/init_db.sh /docker-entrypoint-initdb.d/
COPY ./sql_commands/domain_table.csv /docker-entrypoint-initdb.d/
COPY ./sql_commands/domain_flag_table.csv /docker-entrypoint-initdb.d/