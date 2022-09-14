INSERT INTO users(name, contact_info) VALUES
    ('Ada Lovelace', 'ALovelace@gmail.com'),
    ('Mary Shelley', 'MShelley@gmail.com'),
    ('Jackie Gleason', 'JGleason@gmail.com'),
    ('Art Garfunkel', 'AGarfunkel@gmail.com');

INSERT INTO inventory(title, book_type, author, publish_date, copies) VALUES
    ('Figuring', 'Non-fiction', 'Maria Popova', 2019, 5),
    ('In Defence of Witches', 'Non-fiction', 'Mona Chollet', 2022, 3),
    ('Scary Smart', 'Non-fiction', 'Mo Gawdat', 2021, 7),
    ('The Princess Spy', 'Non-fiction', 'Larry Loftis', 2022, 2),
    ('The Dead Romantics', 'Fiction', 'Ashley Poston', 2022, 6),
    ('The Lord of the Rings', 'Fiction', 'J.R.R. Tolkien', 1954, 9),
    ('The Lightning Thief', 'Fiction', 'Rick Riordan', 2005, 4),
    ('To Kill a Mockingbird', 'Fiction', 'Harper Lee', 1960, 1);

INSERT INTO checkout(user_id, checked_out)VALUES
    --Ada checked out "In Defence of Witches"
    (1, 2),
    --Mary checked out "Scary Smart"
    (2, 3),
    --Jackie checked out "The Lightning Thief" and "To Kill a Mockingbird"
    (3, 7),
    (3, 8);

INSERT INTO checkout(user_id)VALUES
    --Art does not have any books checked out
    (4);