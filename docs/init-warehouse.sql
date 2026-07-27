-- Crea la base y schemas del warehouse al iniciar Postgres
CREATE USER warehouse WITH PASSWORD 'warehouse';
CREATE DATABASE warehouse OWNER warehouse;
\connect warehouse
CREATE SCHEMA IF NOT EXISTS raw AUTHORIZATION warehouse;
CREATE SCHEMA IF NOT EXISTS analytics AUTHORIZATION warehouse;
