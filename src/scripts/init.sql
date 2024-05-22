-- init.sql

-- Habilitar la extensión uuid-ossp
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Creación de los esquemas
CREATE SCHEMA security;
CREATE SCHEMA statistics;

-- Creación de las bases de datos
CREATE TABLE security.rols (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nemonic VARCHAR(20) NOT NULL
);

INSERT INTO security.rols (nemonic)
VALUES ('Admin'), ('User');

CREATE TABLE security.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(512) NOT NULL,
    role_id UUID,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT False,

    CONSTRAINT fk_role FOREIGN KEY (role_id) REFERENCES security.rols(id)
);

CREATE TABLE security.chats (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,

    CONSTRAINT fk_chat FOREIGN KEY (user_id) REFERENCES security.users(id)
);

CREATE TABLE security.chat_messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chat_id UUID,
    user_id UUID,
    "message" TEXT,

    CONSTRAINT fk_chat_messages_1 FOREIGN KEY (chat_id) REFERENCES security.chats(id),
    CONSTRAINT fk_chat_messages_2 FOREIGN KEY (user_id) REFERENCES security.users(id)
);

INSERT INTO security.users (username, email, password_hash, role_id) 
VALUES ('admin', 'aquintanalm01@educantabria.es', '$2b$12$RUpUBCNuRpM19gxtiEFfWeRR6iNrJvUPjMw/L8dNLXmzAQO1r1Vda', (SELECT id FROM security.rols WHERE nemonic = 'Admin'));

CREATE TABLE statistics.model_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID,
    run_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL,
    done BOOLEAN,
    done_reason VARCHAR(100),
    eval_count INTEGER,
    eval_duration INTEGER,
    load_duration INTEGER,
    model VARCHAR(50),
    prompt_eval_count INTEGER,
    prompt_eval_duration INTEGER,
    total_duration INTEGER
);