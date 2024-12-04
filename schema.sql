-- This file contains all of the SQL commands to create the database, tables and relationships for the Movies Database
DROP TABLE IF EXISTS movie_genres;
DROP TABLE IF EXISTS movie;
DROP TABLE IF EXISTS genre;
DROP TABLE IF EXISTS language;
DROP TABLE IF EXISTS country;

-- Create language table
CREATE TABLE language (
    language_id BIGINT,
    language_name VARCHAR,
    PRIMARY KEY (language_id)
);

-- Create country table
CREATE TABLE country (
    country_id BIGINT,
    country_name VARCHAR,
    PRIMARY KEY (country_id)
);

-- Create genre table
CREATE TABLE genre (
    genre_id BIGINT,
    genre_name VARCHAR,
    PRIMARY KEY (genre_id)
);

-- Create movie table
CREATE TABLE movie (
    movie_id INT GENERATED ALWAYS AS IDENTITY,
    title VARCHAR,
    release_date DATE,
    score FLOAT,
    overview VARCHAR,
    orig_title VARCHAR,
    status VARCHAR,
    orig_lang INT,
    budget FLOAT,
    revenue FLOAT,
    country INT,
    PRIMARY KEY (movie_id),
    FOREIGN KEY (orig_lang) REFERENCES language (language_id),
    FOREIGN KEY (country) REFERENCES country (country_id)
);

-- Create movie_genres table
CREATE TABLE movie_genres (
    movie_genre_id BIGINT GENERATED ALWAYS AS IDENTITY,
    movie_id BIGINT,
    genre_id BIGINT,
    PRIMARY KEY (movie_genre_id),
    FOREIGN KEY (movie_id) REFERENCES movie (movie_id),
    FOREIGN KEY (genre_id) REFERENCES genre (genre_id)
);

-- Create index for movie_genres
CREATE INDEX movie_genres_idx ON movie_genres (movie_id, genre_id);

INSERT INTO language (language_id, language_name) VALUES
(1, 'English'),
(2, 'Spanish'),
(3, 'Norwegian'),
(4, 'Japanese'),
(5, 'Korean'),
(6, 'Russian'),
(7, 'Cantonese'),
(8, 'Ukrainian'),
(9, 'Italian'),
(10, 'German'),
(11, 'French'),
(12, 'Finnish'),
(13, 'Icelandic'),
(14, 'Indonesian'),
(15, 'Dutch'),
(16, 'Portuguese'),
(17, 'Telugu'),
(18, 'Polish'),
(19, 'Danish'),
(20, 'Turkish'),
(21, 'Chinese'),
(22, 'Thai'),
(23, 'Romanian'),
(24, 'Tagalog'),
(25, 'Macedonian'),
(26, 'Swedish'),
(27, 'Tamil'),
(28, 'Vietnamese'),
(29, 'Hindi'),
(30, 'Arabic'),
(31, 'Serbian'),
(32, 'No Language'),
(33, 'Galician'),
(34, 'Greek'),
(35, 'Hungarian'),
(36, 'Malayalam'),
(37, 'Marathi'),
(38, 'Oriya'),
(39, 'Bengali'),
(40, 'Persian'),
(41, 'Latvian'),
(42, 'Basque'),
(43, 'Malay'),
(44, 'Central Khmer'),
(45, 'Irish'),
(46, 'Czech'),
(47, 'Gujarati'),
(48, 'Kannada'),
(49, 'Serbo-Croatian'),
(50, 'Latin'),
(51, 'Dzongkha'),
(52, 'Slovak');

INSERT INTO country (country_id, country_name) VALUES
(1, 'AU'),
(2, 'US'),
(3, 'MX'),
(4, 'GB'),
(5, 'CL'),
(6, 'NO'),
(7, 'ES'),
(8, 'AR'),
(9, 'KR'),
(10, 'HK'),
(11, 'UA'),
(12, 'IT'),
(13, 'RU'),
(14, 'CO'),
(15, 'DE'),
(16, 'JP'),
(17, 'FR'),
(18, 'FI'),
(19, 'IS'),
(20, 'ID'),
(21, 'BR'),
(22, 'BE'),
(23, 'DK'),
(24, 'TR'),
(25, 'TH'),
(26, 'PL'),
(27, 'GT'),
(28, 'CN'),
(29, 'CZ'),
(30, 'PH'),
(31, 'ZA'),
(32, 'CA'),
(33, 'NL'),
(34, 'TW'),
(35, 'PR'),
(36, 'IN'),
(37, 'IE'),
(38, 'SG'),
(39, 'PE'),
(40, 'CH'),
(41, 'SE'),
(42, 'IL'),
(43, 'DO'),
(44, 'VN'),
(45, 'GR'),
(46, 'SU'),
(47, 'HU'),
(48, 'BO'),
(49, 'SK'),
(50, 'UY'),
(51, 'BY'),
(52, 'AT'),
(53, 'PY'),
(54, 'MY'),
(55, 'MU'),
(56, 'LV'),
(57, 'XC'),
(58, 'PT'),
(59, 'KH'),
(60, 'IR');

INSERT INTO genre (genre_id, genre_name) VALUES
(1, 'Fantasy'),
(2, 'Science Fiction'),
(3, 'Comedy'),
(4, 'Family'),
(5, 'Animation'),
(6, 'Romance'),
(7, 'Drama'),
(8, 'TV Movie'),
(9, 'War'),
(10, 'Mystery'),
(11, 'Music'),
(12, 'Horror'),
(13, 'History'),
(14, 'Adventure'),
(15, 'Documentary'),
(16, 'Action'),
(17, 'Western'),
(18, 'Thriller'),
(19, 'Crime'),
(20, 'No Genre');