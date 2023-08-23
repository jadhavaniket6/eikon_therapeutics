# eikon_therapeutics
A repo for take home task in regards with a software Engineer at Eikon Therapeutics

Commands to build the docker container
docker build -t my-flask-app .    
docker run -p 4000:80 my-flask-app

Once the docker container is up, we can even attach a shell to it and run the following commands:

To go to the homepage
curl -X GET http://localhost:5000/

To get the result in a JSON format
curl -X GET http://localhost:5000/show_data

To upload data to Postgres DB
curl -X POST http://localhost:5000/trigger_etl
