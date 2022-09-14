DROP TABLE IF EXISTS checkout;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS users;

CREATE TABLE users(
    id SERIAL NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    contact_info TEXT NOT NULL 
);

CREATE TABLE inventory(
    book_id SERIAL NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    book_type TEXT NOT NULL,
    author TEXT NOT NULL,
    publish_date INTEGER NOT NULL,
    copies INTEGER DEFAULT 0 NOT NULL
);

CREATE TABLE checkout(
    checked_out INTEGER,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(checked_out) REFERENCES inventory(book_id)
);