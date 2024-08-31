CREATE TABLE book (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);


CREATE TABLE lecture (
    id INTEGER PRIMARY KEY,
    number INTEGER NOT NULL,
    content_type VARCHAR(50) NOT NULL CHECK (content_type IN ('book', 'workbook')),
    content_id INTEGER NOT NULL,
    FOREIGN KEY (content_id) REFERENCES book(id)
);

CREATE TABLE audio (
    id INTEGER PRIMARY KEY,
    path VARCHAR(255) NOT NULL,
    number INTEGER NOT NULL,
    lecture_id INTEGER,
    FOREIGN KEY (lecture_id) REFERENCES lecture(id)
);
