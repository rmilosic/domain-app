#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    

    DROP TABLE IF EXISTS public.domain CASCADE;
    DROP TABLE  IF EXISTS public.domain_flag CASCADE;


    CREATE SEQUENCE public.domain_id_seq START 1;
    CREATE SEQUENCE public.domain_flag_id_seq START 1;


    CREATE TABLE
    IF NOT EXISTS public.domain(
        id INTEGER PRIMARY KEY NOT NULL DEFAULT nextval('public.domain_id_seq'),
        fqdn VARCHAR(255) NOT NULL,
        crdate TIMESTAMP WITHOUT TIME ZONE DEFAULT (Now() AT TIME ZONE 'utc'),
        erdate TIMESTAMP WITHOUT TIME ZONE DEFAULT NULL
    );


    CREATE TYPE public.flag_type AS ENUM ('EXPIRED', 'OUTZONE', 'DELETE_CANDIDATE');

    CREATE TABLE 
    IF NOT EXISTS public.domain_flag(
        id INTEGER PRIMARY KEY  DEFAULT nextval('public.domain_flag_id_seq'),
        domain_id INTEGER NOT NULL,
        flag flag_type NOT NULL,
        valid_from TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        valid_to TIMESTAMP WITHOUT TIME ZONE
    );

    ALTER TABLE public.domain_flag
        ADD CONSTRAINT domain_flag_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES domain (id);

EOSQL

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL

\copy public.domain(id, fqdn, crdate, erdate) FROM '/docker-entrypoint-initdb.d/domain_table.csv' DELIMITER ',' CSV HEADER

\copy public.domain_flag(id, domain_id, flag, valid_from, valid_to) FROM '/docker-entrypoint-initdb.d/domain_flag_table.csv' DELIMITER ',' CSV HEADER


SELECT setval('domain_id_seq', (SELECT MAX(id) from "domain"));

SELECT setval('domain_flag_id_seq', (SELECT MAX(id) from "domain_flag"));

EOSQL