CREATE TYPE ROLE AS ENUM ('admin', 'user');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    hashed_password BYTEA NOT NULL,
    role ROLE NOT NULL DEFAULT 'user'
);

CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    muscle_group TEXT NOT NULL,
    equipment TEXT[] NOT NULL DEFAULT '{}',
    difficulty INTEGER NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
)