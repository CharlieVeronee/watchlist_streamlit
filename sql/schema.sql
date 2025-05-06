CREATE TABLE IF NOT EXISTS Users (
    app_username VARCHAR(255) PRIMARY KEY,
    app_password VARCHAR(255) NOT NULL --hashed with bcrypt--
);

CREATE TABLE IF NOT EXISTS People (
    lb_username VARCHAR(255),
    added_by VARCHAR(255) NOT NULL,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    added_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (lb_username, added_by),
    FOREIGN KEY (added_by) REFERENCES Users(app_username) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Movies (
    slug VARCHAR(255) PRIMARY KEY,
    title VARCHAR(255),
    poster_url VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Watchlist (
    lb_username VARCHAR(255) NOT NULL,
    slug VARCHAR(255) NOT NULL,
    added_by VARCHAR(255) NOT NULL,
    added_at    TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY (lb_username, slug, added_by),
    FOREIGN KEY (added_by) REFERENCES Users(app_username) ON DELETE CASCADE,
    FOREIGN KEY (lb_username, added_by) REFERENCES People(lb_username, added_by) ON DELETE CASCADE,
    FOREIGN KEY (slug) REFERENCES Movies(slug) ON DELETE CASCADE
);