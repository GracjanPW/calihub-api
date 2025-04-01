CREATE TYPE ROLE AS ENUM ('admin', 'user');
CREATE TYPE DIFFICULTY AS ENUM (
    'beginner', 
    'novice', 
    'intermediate', 
    'advanced', 
    'expert'
);

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- PUBLIC
    email TEXT NOT NULL UNIQUE,
    role ROLE NOT NULL DEFAULT 'user',
    -- PRIVATE
    hashed_password BYTEA NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    -- PUBLIC
    name TEXT NOT NULL,
    description TEXT DEFAULT '',
    difficulty DIFFICULTY NOT NULL DEFAULT 'beginner',

    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE muscle_groups (
    id SERIAL PRIMARY KEY,
    -- PUBLIC
    name TEXT NOT NULL,

    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    -- PUBLIC
    name TEXT NOT NULL,
    description TEXT,

    created_at TIMESTAMP NOT NULL DEFAULT now(),
    updated_at TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE exercise_muscle_groups (
    exercise_id INT REFERENCES exercises(id) ON DELETE CASCADE,
    muscle_group_id INT REFERENCES muscle_groups(id) ON DELETE CASCADE,
    
    PRIMARY KEY (exercise_id, muscle_group_id)
);

CREATE TABLE exercise_equipment (
    exercise_id INT REFERENCES exercises(id) ON DELETE CASCADE,
    equipment_id INT REFERENCES equipment(id) ON DELETE CASCADE,

    PRIMARY KEY (exercise_id, equipment_id)
)