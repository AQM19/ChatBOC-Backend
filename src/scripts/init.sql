-- init.sql

-- Habilitar la extensión uuid-ossp
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Creación de los esquemas
-- CREATE SCHEMA security;
-- CREATE SCHEMA statistics;

-- Creación de las bases de datos
CREATE TABLE rols (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nemonic VARCHAR(20) NOT NULL
);

INSERT INTO rols (nemonic)
VALUES ('Admin'), ('User');

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(512) NOT NULL,
    role_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT False,

    CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES rols(id)
);

CREATE TABLE chats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,

    CONSTRAINT fk_chat FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id UUID,
    user_id UUID,
    "message" TEXT,

    CONSTRAINT fk_chat_messages_1 FOREIGN KEY (chat_id) REFERENCES chats(id),
    CONSTRAINT fk_chat_messages_2 FOREIGN KEY (user_id) REFERENCES users(id)
);

INSERT INTO users (username, email, password_hash, role_id) 
VALUES ('admin', 'aquintanalm01@educantabria.es', '$2b$12$RUpUBCNuRpM19gxtiEFfWeRR6iNrJvUPjMw/L8dNLXmzAQO1r1Vda', (SELECT id FROM rols WHERE nemonic = 'Admin'));

CREATE TABLE model_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    done BOOLEAN,
    done_reason VARCHAR(100),
    eval_count BIGINT,
    eval_duration BIGINT,
    load_duration BIGINT,
    model VARCHAR(50),
    prompt_eval_duration BIGINT,
    total_duration BIGINT,

    CONSTRAINT fk_model_run FOREIGN KEY (user_id) REFERENCES users(id)
);