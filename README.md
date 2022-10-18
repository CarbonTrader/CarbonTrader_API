# CarbonTrader API

--Insert description here --

# Instructions

## Prerequisites

- This program must be run in a linux or unix machine, it can also be run in WSL. 
- There should be a file in `app/secrets` named service-account-info.json with the credentials of your google cloud Pub/Sub.
- There should be a file in `app/secrets` named credential.json with the credentials of your firebase storage.
- The machine must have `make` install.
- There must be internet connection.
### Prerequisites for deployment
- Must have a heroku account
- Must have docker installed


## Running the API.
- To run the API run the command `make serve`. This will command will do the following:
  - Create a python environment.
  - Install the requirements.
  - Run the uvicorn server in localhost and in the port 8000.
- For cleaning cache you can use the following commands:
  - `make clean_blockchain`
  - `make clean_app`
  - `make clean_services`
  - `make clean_routes`
  - `make clean_model`

## Deploying to heroku
For deploying you first must login to heroku using the command
-  `sudo heroku auth:login`<br />
then you need to login to your docker account with the command
- `heroku container:login`<br />
then you need to build the project image using the command
- `docker-compose build`<br />
then you'll need to publish your image
- `heroku container:push web <name of your heroku server>`<br />
after publishin your image you can release it to heroku
- `heroku container:release web <name of your heroku server>`
