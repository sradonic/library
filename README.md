This is a library backend.

Before starting 
   1. the .env variables must be set, the .env file is in the root of the project (mysql was used when creating the project)
   2. populate the database with roles first from the script app/database/seeds/role.py
   3. create the admin user by starting the script app/database/seeds/users.py
   4. you may populate the base with books.py found in the same location as other seeds

When working with the library frontent:
  You must set the address allow_origins in the .env file (the set address is an example) 

