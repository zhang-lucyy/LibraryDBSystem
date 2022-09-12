CREATE SCHEMA library;

CREATE TABLE library.users(
    id SERIAL NOT NULL PRIMARY KEY,
    name TEXT NOT NULL,
    conact_info TEXT NOT NULL 
);

CREATE TABLE library.inventory(
    book_id SERIAL NOT NULL PRIMARY KEY,
    title TEXT NOT NULL,
    type TEXT NOT NULL,
    author TEXT NOT NULL,
    publish_date INTEGER NOT NULL,
    copies INTEGER DEFAULT 0 NOT NULL
);

CREATE TABLE library.checkout(
    checked_out INTEGER,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES library.users(id),
    FOREIGN KEY(book_checked_out_id) REFERENCES library.inventory(book_id)
);