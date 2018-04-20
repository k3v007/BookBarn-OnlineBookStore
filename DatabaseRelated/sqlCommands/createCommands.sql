create table publishers
(
  pID varchar(20) not null,
  pName varchar(255) not null,
  primary key(pID)
);


create table authors
(
  aID varchar(20) not null,
  fName varchar(20),
  mName varchar(20),
  lName varchar(20),
  About text,
  primary key(aID)
);


create table genres
(
  gID varchar(20) not null,
  gName varchar(100) not null,
  primary key(gID)
);


create table books
(
  ISBN varchar(20) not null,
  BookTitle varchar(255) not null,
  Description text,
  PageCount int not null,
  Rating  numeric(3, 2),
  Language varchar(20),
  CoverImage varchar(255),
  Price numeric(5, 2),
  PublishedDate date,
  publisher_pID varchar(20) not null,
  VoteCount int default 0,
  primary key(ISBN),
  foreign key(publisher_pID) references publishers(pID)
);



create table books_authors
(
  SrNo int not null auto_increment primary key,
  Book_ISBN varchar(20) not null,
  Author_aID varchar(20) not null,
  unique(Book_ISBN, Author_aID),
  foreign key(Book_ISBN) references books(ISBN) on delete cascade,
  foreign key(Author_aID) references authors(aID) on delete cascade
);


create table books_genres
(
  SrNo int not null auto_increment primary key,
  Book_ISBN varchar(20) not null,
  Genre_gID varchar(20) not null,
  unique(Book_ISBN, Genre_gID),
  foreign key(Book_ISBN) references books(ISBN) on delete cascade,
  foreign key(Genre_gID) references genres(gID) on delete cascade
);
