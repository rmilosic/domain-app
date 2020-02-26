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

- `init_db.sh` (script for docker postgres container db initialization)


## Django part


### Get started

Requirements: installed Docker

Clone repository
`git clone https://github.com/rmilosic/domain-app.git`

Run docker-compose comand from the root folder
`docker-compose up --build -d web`

To create a user for the admin, run the following
1. `docker exec -it domain_app_web_1 bash` 
2. `python manage.py createsuperuser` then follow the prompt to input user details


Server is running at `localhost:8000` and admin view is available at path `/admin/`
