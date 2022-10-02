DROP SCHEMA IF EXISTS library CASCADE;
DROP TABLE IF EXISTS return;
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
    summary TEXT DEFAULT '' NOT NULL,
    copies INTEGER DEFAULT 0 NOT NULL
);

CREATE TABLE checkout(
    checked_out INTEGER,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(checked_out) REFERENCES inventory(book_id)
);

CREATE TABLE return(
    return_book_id INTEGER,
    return_book_date DATE,
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(return_book_id) REFERENCES inventory(book_id)
);

INSERT INTO users(name, contact_info) VALUES
    ('Ada Lovelace', 'ALovelace@gmail.com'),
    ('Mary Shelley', 'MShelley@gmail.com'),
    ('Jackie Gleason', 'JGleason@gmail.com'),
    ('Art Garfunkel', 'AGarfunkel@gmail.com');

INSERT INTO inventory(title, book_type, author, publish_date, summary, copies) VALUES
    ('Figuring', 'Non-fiction', 'Maria Popova', 2019, 'Explores the complexities
        of love and the human search for truth and meaning', 5),
    ('In Defence of Witches', 'Non-fiction', 'Mona Chollet', 2022, 'Explores how
        women who assert their powers are too often seen as a threat to men and society', 3),
    ('Scary Smart', 'Non-fiction', 'Mo Gawdat', 2021, 'Explores the future of artificial intelligence', 7),
    ('The Princess Spy', 'Non-fiction', 'Larry Loftis', 2022, 'Follows the hidden history 
        of an ordinary American girl who became one of the most daring WWII spies', 2),
    ('The Dead Romantics', 'Fiction', 'Ashley Poston', 2022,
        'The main character is a ghostwriter for a romance novelist', 6),
    ('The Lord of the Rings', 'Fiction', 'J.R.R. Tolkien', 1954, 
        'A group of heroes set forth to save their world', 9),
    ('The Lightning Thief', 'Fiction', 'Rick Riordan', 2005, 
        'A 12 year-old boy who learns that his true father is Poseidon', 4),
    ('To Kill a Mockingbird', 'Fiction', 'Harper Lee', 1960,
        'Chronicles the childhood of Scout and Jem Finch',1);

INSERT INTO checkout(user_id, checked_out)VALUES
    --Ada checked out "In Defence of Witches"
    (1, 2),
    --Mary checked out "Scary Smart"
    (2, 3),
    --Jackie checked out "The Lightning Thief" and "To Kill a Mockingbird"
    (3, 7),
    (3, 8);