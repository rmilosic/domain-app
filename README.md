# Domain app


## Background
This is a test project on setting up a Django project with the following features:
- manual postgresdb setup and population
- 2 sql query scripts
- admin model management
- 2 custom views
- custom manage.py management command `set_expiration_flags`
- views and management command tests


## SQL part

Scripts for db setup are located in `./sql_commands/` folder
- `setup_db_and_load_initial_data.sql`
- `query_once_expired_or_outzone.sql`
- `query_active_domains.sql`


## Django part

App name: `domain_app`

