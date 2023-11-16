-- users table: 
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    registration_token VARCHAR(255)
);

-- games table:
CREATE TABLE games (
    game_id SERIAL NOT NULL,
    title VARCHAR(255) NOT NULL,
    game_cover_url VARCHAR(255),
    short_description VARCHAR(255),
    long_description TEXT,
    release_date VARCHAR(255) NOT NULL,
    game_url VARCHAR(255) NOT NULL,
    author_id INT NOT NULL,
    PRIMARY KEY (game_id),
    FOREIGN KEY (author_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE
);