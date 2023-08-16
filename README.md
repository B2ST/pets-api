# pets-api
This is the pets api

## How to run
1. install fastapi: https://fastapi.tiangolo.com/#installation
2. install sqlalchemy: `pip3 install sqlalchemy`
3. install fastapi-filter `pip3 install fastapi-filter`
4. clone this repo
5. run `python3 -m uvicorn handlers:app --reload`

## Things to do in future if I had more time:

1. Fix up filter for species when listing pets (GET /pets). Didn't have enough time to figure out the cleaner solution via PetsFilter class, so the current solution is less optimal.

2. Implement pagination on pets endpoint (GET /pets) for listing pets.

3. Fix issue with FK constraint in db. Can create new pet with a non existant speciesID. This correctly fails when running query in DB browser for sqlite, but via ORM, it doesn't. Might have setup something incorrectly in code.

4. Split this service into api and srv. Srv should contain all business logic including comunicating with BE infrastructure. 

    4.1 Use gRPC and protobufs for communication between microservices for better performance. It's more efficient at serializing structured data than json.

    4.2. for using gRPC, we need to add api-gateway to convert http requests into gRPC call to appropriate microservice.

    eg. getPet call:
    client (getPet request) -> api-gateway -> pets-api microservice -> pets-srv microservice

5. containerise using docker - have seperate pods/containers for api-gateway, pets-api and pets-srv microservice for scalability.

6. Use Alembic for db migration files since we are using SQLAlchemy. This way, we can make updates to db easily.


Justification of design:

provided schema is denormalised. We need to normalise it. It doesn't adhere to 1NF as each record is not unique.
We could create a composite primary key, with species and name, but that woudn't adhere to 2NF. Also, if we need to restrict species when adding new ones, it would be better to have a seperate table for it. This way, we also get 2NF too. So we need to create a new table for species and have a speciesID FK in pets table.

Google's AIP standards were used when building the pets api. This was why /pets/ was used instead of /pet/ as we are requesting/creating a resource from a collection. eg: <br>
get pet: GET /pets/{pet_id} <br>
list pet: GET /pets/?{filters} <br>
create pet: POST /pets/ <br>
https://google.aip.dev/131