-- Terminate existing connections (necessary before dropping the DB)
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE datname = 'calihub_dev_db' or usename = 'app_user';

-- Drop user and database
DROP DATABASE IF EXISTS calihub_dev_db;
DROP USER IF EXISTS app_user;

-- Create user and database
CREATE USER app_user PASSWORD 'devpassword';
CREATE DATABASE calihub_dev_db owner app_user ENCODING = 'UTF-8';
