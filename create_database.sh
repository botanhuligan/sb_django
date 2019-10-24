CREATE DATABASE sber_back;
CREATE USER sber WITH PASSWORD 'hfdbb73hGGh3';
ALTER ROLE sber SET client_encoding TO 'utf8';
ALTER ROLE sber SET default_transaction_isolation TO 'read committed';
ALTER ROLE sber SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE sber_back TO sber;