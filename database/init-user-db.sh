!/bin/bash

set -e
echo "Executing sql"
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
CREATE TABLE users (
  id     SERIAL PRIMARY KEY,
  name   TEXT,
  email  TEXT,
  city   TEXT,
  phone  TEXT
);
EOSQL