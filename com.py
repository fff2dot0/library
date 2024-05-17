from bcrypt import checkpw

from harperdb import HarperDB # type: ignore

from colors import Color
from roles import *
from print_logo import print_logo
from print import *
from input import ask_open_question
from get_attr import *
from com_read import com_reader
from com_lib import com_librarian
from com_admin import com_admin
from settings import URL, LOGIN, PWD
from table import print_table   #TODO: remove


# def get_ids( hdb: HarperDB, db: str, table: str, where: str ) -> SQL_RETURN:
#     return hdb.sql( f"SELECT id FROM { db }.{ table } WHERE { where }" )


def sign_in() -> None:
    hdb = HarperDB( URL, LOGIN, PWD )
    print_info( "Welcome to the Library." )
    usr: SQL_RETURN = []
    while not usr:
        username = ask_open_question( "Enter your username." )
        usr = hdb.sql( f"SELECT id, role, password FROM library.users WHERE username = \"{ username }\"" )
        if not usr:
            print_error( f"Incorrect username { username }." )
            continue
        pwd = ask_open_question( "Enter your password.", True )
        if not checkpw( pwd.encode(), str( usr[ 0 ][ "password" ] ).encode() ):
            print_error( f"Incorrect password for { username }." )
            usr = []

    com( str( usr[ 0 ][ "id" ] ), username, str( usr[ 0 ][ "role" ] ), hdb )


def com( uid: str, usrname: str, role: str, hdb: HarperDB ) -> None:
    print_logo()
    print( f"{ Color.CYAN }Welcome back, { usrname }.{ Color.RESET }" )

    if role == "reader":
        com_reader( Reader( hdb, uid, usrname ) )
    elif role == "librarian":
        com_librarian( Librarian( hdb, uid, usrname ) )
    elif role == "administrator":
        com_admin( Admin( hdb, uid, usrname ) )

def test() -> None:
    hdb = HarperDB( URL, LOGIN, PWD )
    table = hdb.sql( "SELECT name, author, genre, pages, location FROM library.books WHERE author LIKE \"%%\"" )
    print_table( table )    ## OK
    # table = hdb.sql( f"SELECT u.name_surname, b.name, b.author, ub.date_ret_exp "
    #                  f"FROM library.users AS u LEFT OUTER JOIN library.user_books AS ub "
    #                   "ON u.id = 'ub.uid' "
    #                   "JOIN library.books AS b "
    #                   "ON b.id = 'ub.bid' "
    #                  f"WHERE u.username = \"reg_reader\" " )
    # username = "mivi"
    # table = hdb.sql(
    #                  f"SELECT u.name_surname, b.name, b.author, ub.date_ret_exp "
    #                  f"FROM library.books AS b JOIN library.user_books AS ub JOIN library.users AS u "
    #                  f"WHERE u.username = \"{ username }\" AND u.id = ub.uid AND b.id = ub.bid "
    #                   "UNION "
    #                   "SELECT u.name_surname, '' name, '' author, ub.date_ret_exp "
    #                  f"FROM library.user_books AS ub RIGHT JOIN library.users AS u "
    #                   "ON ub.uid = u.id "
    #                  f"WHERE u.username = \"{ username }\" AND ub.uid IS NULL"
    # )
    # table = hdb.sql( "SELECT id FROM library.books "
    #                  "UNION ALL "
    #                  "SELECT id FROM library.users " )
    # table = hdb.sql( "SELECT name_surname "
    #                  "FROM library.users "
    #                  "WHERE id IN ("
    #                                "SELECT DISTINCT uid FROM library.user_books "
    #                                "WHERE date_ret_act IS NULL)" )
    # table = hdb.sql( "SELECT DISTINCT uid FROM library.user_books "
    #                  "WHERE date_ret_act IS NULL" )
    # print_table( table )
# Test users
# pwd: easy1,           role: reader,       usr: no1else
# pwd: B_happy4U,       role: reader,       usr: reg_reader
# pwd: kugus_pychatik,  role: librarian,    usr: mivi
#      best1,                 admin,             master
#      donut,                 lib,          usr: tmnt_girl

# def sign_in_test():
#     # TODO: comunicate through functions
#     # print( "Enter your role: " )
#     # role = "admin"#input()
#     print( "Enter your username: " )
#     usrname = "mivi"#input()
#     print( "Enter your password: " )
#     password = "kugus_pychatik"#input() # TODO desiphere
#     url = "http://localhost:9925"
#     hdb = HarperDB( url, "hdb_admin", "Ar11052005" )

#     user = hdb.sql( f"SELECT id, role FROM library.users WHERE username = "
#                     f"'{ usrname }' AND password = '{ password }'" )
#     if not user:
#         print_error( "Incorrect username or password." )
#         #TODO end
#         return

#     if user[ 0 ][ "role" ] == "reader":
#         reader = Reader( hdb, usrname )
#         ans = ask_question( "What book do you want to find?", [ "search by author", "search by name" ] )
#         found = ""
#         if ans == '1':
#             author = ask_question( "Write your author" )
#             found = reader.book_search.by_author( author )
#             return found # TODO print_table()

#     elif user[ 0 ][ "role" ] == "librarian":
#         #
#         input_surname = "Chornohub"
#         # found = hdb.sql( "SELECT name FROM library.books JOIN library.user_books where books.id = user_books.bid" )
#         # print( "SELECT name_surname, name, author, date_ret_exp FROM library.books AS b, library.user_books AS ub, library.users AS u " +
#         #       "WHERE u.name_surname LIKE '%" + input_surname + "%' AND u.id = ub.uid AND b.id = ub.bid" )
#         found = hdb.sql( "SELECT u.name_surname, b.name, b.author, ub.date_ret_exp "
#                          "FROM library.books AS b JOIN library.user_books AS ub JOIN library.users AS u "
#                         f"WHERE u.name_surname LIKE '%{ input_surname }%' AND u.id = ub.uid AND b.id = ub.bid "
#                          "ORDER BY u.name_surname, b.author, b.name" )
#         print( found )


#         code = '1'
#         usrname = "reg_reader"
#         date_ret_exp = "2024-12-03"
#         uid = get_ids( hdb, "library", "users", f"users.username = '{ usrname }'" )
#         if not uid:
#             print_error( f"User with username '{ usrname }' was not found" )
#             return

#         book = hdb.sql( f"SELECT books.id, books.available FROM library.books WHERE books.code = { code }" )
#         if not book:
#             print_error( f"Book with '{ code= }' was not found" )
#             return
#         if book[ 0 ][ "available" ] == 0:
#             print_error( f"Book with '{ code= }' is not currently available" )
#             return

#         k = hdb.sql( "INSERT INTO library.user_books ( bid, uid, date_start, date_ret_exp ) "
#                     f"VALUES ( '{ book[ 0 ][ 'id' ] }', '{ uid[ 0 ][ 'id ' ] }', GETDATE(), '{ date_ret_exp }' )" )
#         print( k )

#         hdb.sql( "UPDATE library.books "
#                 f"SET books.available = { book[ 0 ][ 'available' ] - 1 } "
#                 f"WHERE books.id = '{ book[ 0 ][ 'id' ] }'" )
#         return found
