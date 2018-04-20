'''
It open the scrapped csv files and then load the data in mysql database

Note:
1. In order to connect to the database, 'mysqlclient' module must be installed
2. To install the module, run 'pip install mysqlclient'
3. Set properly the user, password, host and database in mysql.connector.connect
4. Use mysql.connector.Error for specifying the proper MySQL error
'''

from time import sleep
import os
import getpass
import glob
import csv
import mysql.connector
from datetime import date, datetime, timedelta

print('\nEnter MySQL Connector Details:')
database = input("Database Name: ")
password = getpass.getpass('Database Password: ')

check = False

try :
    db = mysql.connector.connect(
                                user = 'root',
                                password = password,
                                host = 'localhost',
                                database = database,
                                )
except:
    print('\n## Unmatched Connection!!')
    print("Note: Check out your Database connection parameters!!")
    exit()

#setting cursor to your database
cursor = db.cursor()


#username is fetched and other path is same in all linux systems
username = os.environ.get('USERNAME')
#Moving to ScriptGenerated folder containing authorID etc csv files
dir = '/home/' + username + '/Documents/GitRepositories/bookbarnv2/ScrappedData/csvFiles/ScriptGenerated'
try:
    os.chdir(dir)
except:
    print('\n## Wrong directory!!')
    print('Note : Correct the directory path in loadCSV.py line no. 42')
    exit()


#contains unique authors and their IDs
authorDict = {}
#contains unique genres and their IDs
genreDict = {}
#contains unique publishers and their IDs
publisherDict = {}


#loading from authorIDs.csv into authorDict
with open('authorIDs.csv', 'r') as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        authorDict[row['Author_about']] = row['AuthorID']


#loading from genreIDs.csv into genreDict
with open('genreIDs.csv', 'r') as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        genreDict[row['Genre']] = row['GenreID']


#loading from publisherIDs.csv into publisherDict
with open('publisherIDs.csv', 'r') as f:
    csv_reader = csv.DictReader(f)

    for row in csv_reader:
        publisherDict[row['Publisher']] = row['PublisherID']


#Loading CSV file to add genres details
print('\nLoading CSV file to add genres details...')
with open('genreIDs.csv', 'r') as f:
    csv_reader = csv.DictReader(f)

    #SQL Command to insert genres data
    add_genre = ("INSERT INTO genres"
                 "(gid, gName)"
                 "VALUES(%s, %s)")

    for col in csv_reader:
        #corresponding SQL data
        data_genre = (col['GenreID'], col['Genre'])

        try:
            cursor.execute(add_genre, data_genre)
            db.commit()
        except mysql.connector.Error as err:
            print("MySQLError : " + str(err))
            db.rollback()
print("Completed!")


#Loading CSV file to add publishers details
print('\nLoading CSV file to add publishers details...')
with open('publisherIDs.csv', 'r') as f:
    csv_reader = csv.DictReader(f)

    #SQL Command to insert publishers data
    add_publisher = ("INSERT INTO publishers"
                     "(pid, pName)"
                     "VALUES(%s, %s)")

    for col in csv_reader:
        #corresponding SQL data
        data_publisher = (col['PublisherID'], col['Publisher'])

        try:
            cursor.execute(add_publisher, data_publisher)
            db.commit()
        except mysql.connector.Error as err:
            print("MySQLError : " + str(err))
            db.rollback()
print("Completed!")


#Moving to SpiderGenerated folder containing book*.csv files
dir = '/home/' + username + '/Documents/GitRepositories/bookbarnv2/ScrappedData/csvFiles/SpiderGenerated'
try:
    os.chdir(dir)
except:
    print('\n## Wrong directory!!')
    print('Note : Correct the directory path in loadCSV.py line no. 130')
    exit()

#List containing all book*.csv files
FileList = sorted(glob.glob('book*.csv'))


#Loading CSV file to add author details
print('\nLoading CSV file to add author details...')
for fName in FileList:
    with open(fName, 'r') as f:
        csv_reader = csv.DictReader(f)

        #SQL Command to insert authors data
        add_author =  ("INSERT INTO authors"
                       "(aid, fName, lName, about)"
                       "VALUES(%s, %s, %s, %s)")

        for col in csv_reader:
            aName = (col['AuthorName']).split()
            fname, lname = ('', '')
            if(len(aName) == 1):
                fname = aName[0]
            else:
                fname, lname = (" ".join(aName[:-1]), aName[-1])
            
            abtAuthor = col['AboutAuthor']
            authKey = col['AuthorName'] + ' ' + abtAuthor[:50]
            aid = authorDict[authKey]

            #corresponding SQL data
            data_author = (aid, fname, lname, abtAuthor)

            try:
                cursor.execute(add_author, data_author)
                db.commit()
            except mysql.connector.Error as err:
                print("MySQLError : " + str(err))
                db.rollback()
print("Completed!")


#Loading CSV file to add book details
print('\nLoading CSV file to add book details...')
for fName in FileList:
    print("Currently reading : " + fName)
    with open(fName, 'r') as f:
        csv_reader = csv.DictReader(f)

        for col in csv_reader:
            #Correcting ISBN no. (starting 0 were stripped in CSV files)
            isbn = col['ISBN']
            r = 10 - len(isbn)
            isbn = ('0' * r) + isbn

            #Correct format of published date YY-MM-DD in MySQL database
            pDate = col['PublishedYear']
            pDate = str((datetime.strptime(pDate, '%m/%d/%Y')).date())

            #Fetching publisher ID from publisherDict
            pid = ''
            if(col['Publisher'] != ''):
                pid = publisherDict[col['Publisher']]
            else:
                pid = publisherDict['No Publisher']

            #SQL commands to enter books data
            add_book = ("INSERT INTO books"
                        "(isbn, bookTitle, description, pageCount, rating, language, coverImage, price, publishedDate, booksCount, bookFormat, publisher_id)"
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
            book_data = (isbn, col['Title'], col['Description'], col['NumberOfPages'], col['BookRating'], col['Lang'], col['CoverImage'], col['BookPrice'], pDate, col['BookCount'], col['BookFormat'], pid)

            try:
                #corresponding SQL data
                cursor.execute(add_book, book_data)
                db.commit()
            except mysql.connector.Error as err:
                print("MySQLError : " + str(err))
                db.rollback()


            #SQL commands to create book-author relation
            key = col['AuthorName'] + ' ' + col['AboutAuthor'][:50]
            aid = authorDict[key]
            add_book_author = ("INSERT INTO books_authors"
                               "(books_id, authors_id)"
                               "VALUES(%s, %s)")
            data_book_author = (isbn, aid)
            try:
                #corresponding SQL data
                cursor.execute(add_book_author, data_book_author)
                db.commit()
            except mysql.connector.Error as err:
                print("MySQLError : " + str(err))
                db.rollback()


            #SQL commands to create book-genre relation
            gList = col['Genres'].split(',')
            add_book_genre = ("INSERT INTO books_genres"
                               "(books_id, genres_id)"
                               "VALUES(%s, %s)")
            for gkey in gList:
                gkey = gkey.strip()
                if(gkey != ''):
                    data_book_genre = (isbn, genreDict[gkey])
                else:
                    data_book_genre = (isbn, genreDict['No Genre'])
                # print(data_book_genre)

                try:
                    #corresponding SQL data
                    cursor.execute(add_book_genre, data_book_genre)
                    db.commit()
                except mysql.connector.Error as err:
                    print("MySQLError : " + str(err))
                    db.rollback()
print("Completed!")

cursor.close()
db.close()
