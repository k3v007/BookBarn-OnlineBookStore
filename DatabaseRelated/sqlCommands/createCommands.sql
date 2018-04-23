-- •	Table Publishers
CREATE TABLE publishers (
  pid varchar(20) NOT NULL,
  pName varchar(255) NOT NULL,
  PRIMARY KEY (pID)
);

-- •	Table Authors
CREATE TABLE authors (
  aid varchar(20) NOT NULL,
  fName varchar(20) NOT NULL,
  lName varchar(20) NOT NULL,
  about text,
  PRIMARY KEY (aID)
);

-- •	Table Genres
CREATE TABLE genres (
  gid varchar(20) NOT NULL,
  gName varchar(100) NOT NULL,
  PRIMARY KEY (gID)
);

-- •	Table Books
CREATE TABLE books (
  isbn varchar(20) NOT NULL,
  bookTitle varchar(255) NOT NULL,
  description text,
  pageCount int NOT NULL,
  rating numeric(3, 2),
  language varchar(20),
  coverImage varchar(255),
  price numeric(5, 2),
  publishedDate date,
  publisher_pid varchar(20) NOT NULL,
  booksCount int default 0 not null , 
  bookFormat varchar(50) not null,
  PRIMARY KEY (isbn),
  FOREIGN KEY (publisher_pid) REFERENCES publishers (pid),
  CONSTRAINT page_chk CHECK(pageCount >= 0),	
  CONSTRAINT rating_chk CHECK(rating between 0 and 5),
	CONSTRAINT price_chk CHECK(price >= 0),
	CONSTRAINT booksCount_chk CHECK(booksCount >= 0)
);

-- •	Table Books_Authors
CREATE TABLE books_authors ( 
  id INT NOT NULL auto_increment PRIMARY KEY, 
  book_isbn VARCHAR(20) NOT NULL, 
  author_aid VARCHAR(20) NOT NULL, 
  UNIQUE(book_isbn, author_aid), 
  FOREIGN KEY(book_isbn) REFERENCES books(isbn) ON DELETE CASCADE, 
  FOREIGN KEY(author_aid) REFERENCES authors(aid) ON DELETE CASCADE 
);

-- •	Table Books_Genres
CREATE TABLE books_genres ( 
  id INT NOT NULL auto_increment PRIMARY KEY, 
  book_isbn VARCHAR(20) NOT NULL, 
  genre_gid VARCHAR(20) NOT NULL, 
  UNIQUE(book_isbn, genre_gid), 
  FOREIGN KEY(book_isbn) REFERENCES books(isbn) ON DELETE CASCADE, 
  FOREIGN KEY(genre_gid) REFERENCES genres(gid) ON DELETE CASCADE 
);

-- •	Table User
CREATE TABLE user ( 
  id         INT NOT NULL auto_increment, 
  username   VARCHAR(20) NOT NULL, 
  password   VARCHAR(20) NOT NULL, 
  first_name VARCHAR(20) NOT NULL, 
  last_name  VARCHAR(20) NOT NULL, 
  email      VARCHAR(20) NOT NULL, 
  PRIMARY KEY(id), 
  CONSTRAINT pwd CHECK(Length(password) >= 6) 
);

-- •	Table UserProfiles
CREATE TABLE userprofiles ( 
  id          INT NOT NULL auto_increment, 
  username    VARCHAR(20) NOT NULL, 
  password    VARCHAR(20) NOT NULL, 
  first_name  VARCHAR(20) NOT NULL, 
  last_name   VARCHAR(20) NOT NULL, 
  email       VARCHAR(20) NOT NULL, 
  phonenumber VARCHAR(10) NOT NULL, 
  address1    VARCHAR(100) NOT NULL, 
  address2    VARCHAR(100), 
  city        VARCHAR(20) NOT NULL, 
  state       VARCHAR(50) NOT NULL, 
  pincode     VARCHAR(6) NOT NULL, 
  PRIMARY KEY(id), 
  CONSTRAINT pwd CHECK(Length(password) >= 6), 
  CONSTRAINT phn CHECK(Length(phonenumber) = 10), 
  CONSTRAINT pin CHECK(Length(pincode) = 6) 
);

-- •	Table Cart
CREATE TABLE cart (
  id int NOT NULL AUTO_INCREMENT,
  user_id int NOT NULL,
  active boolean, total numeric(7, 2),
  order_date datetime DEFAULT now() ON UPDATE now(),
  payment_style varchar(100),
  delivery_address varchar(255),
  cardNumber varchar(16),
  PRIMARY key(id),
  FOREIGN key(user_id) REFERENCES userprofiles(id),
  CONSTRAINT total_chk check(total >= 0),
  CONSTRAINT pay_style check(pay_style IN ('cod', 'card')),
  CONSTRAINT card check(length(cardNumber) = 16)
);

-- •	Table BookOrder
CREATE TABLE bookorder ( 
  id       INT NOT NULL auto_increment, 
  cart_id  INT NOT NULL, 
  book_id  varchar(20) NOT NULL, 
  quantity INT, 
  PRIMARY KEY(id), 
  FOREIGN KEY(cart_id) REFERENCES cart(id) ON DELETE CASCADE, 
  FOREIGN KEY(book_id) REFERENCES books(isbn) ON DELETE CASCADE, 
  CONSTRAINT quant CHECK(quantity >= 0) 
);
