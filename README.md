This is a library backend.

Before starting 
   1. the .env variables must be set, the .env file is in the root of the project (mysql was used when creating the project)
   2. create the necessary tables either by using alembic or by hand (look at the models) 
   3. populate the database with roles first from the script app/database/seeds/role.py
   4. create the admin user by starting the script app/database/seeds/users.py
   5. you may populate the base with books.py found in the same location as other seeds

For Testing:
   1. Create the test database and add it into .env file (mysql was used when testing the project)

When working with the library frontent:
  You must set the address allow_origins in the .env file (the set address is an example) 

