# Technical operation

When the application is launched, the system retrieves the execution mode (dev, prod, etc.).
From there, the system reads the contents of the corresponding file (e.g. .env_prod) and creates
the .env file. This file contains the password that allows access to the database.

