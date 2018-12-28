// This script has to run on the database in order for the app properly connect.
// Make sure it runs before the app loads. 

db = db.getSiblingDB('pandaserve');

db.createUser(
  {
    user: "panda",
    pwd: "pow",
    roles: [ { role: "root", db: "admin" } ]
  }
);
