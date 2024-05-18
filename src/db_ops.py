from typing import List, Dict, Union
from datetime import datetime, timedelta

from harperdb import HarperDB # type: ignore

SQL_RETURN = List[ Dict[ str , Union[ int, str ] ] ]


def my_date2db( date: str ) -> str:
    new = datetime.strptime( date, "%d-%m-%y" ) + timedelta( 1 )
    return f"{ new.year }-{ new.month }-{ new.day }"


def parse_date( date_time: str ) -> str:
    date = date_time.split( "T" )[ 0 ].split( "-" )

    return f"{ date[ 2 ] }-{ date[ 1 ] }-{ date[ 0 ] }"


def parse_dates( sql: SQL_RETURN ) -> SQL_RETURN:
    if not sql:
        return sql
    fields: List[ str ] = []
    for k in sql[ 0 ]:
        if k.find( "date" ) != -1:
            fields.append( k )

    for row in sql:
        for date in fields:
            if row[ date ] is not None:
                row[ date ] = parse_date( str( row[ date ] ) )

    return sql


class BookRead:
    def __init__( self, hdb: HarperDB ) -> None:
        self.hdb = hdb
        self.select = "name, author, genre, pages, location"

    def search( self, find: Dict[ str, str ] ) -> SQL_RETURN:
        where = ''
        for k, v in find.items():
            where += f"{ k } LIKE '%{ v }%' AND "
        return self.hdb.sql( f"SELECT { self.select } "
                              "FROM library.books "
                             f"WHERE { where }amount > 0" )


    def by_na_exact( self, name: str, author: str ) -> SQL_RETURN:
        return self.hdb.sql( f"SELECT id "
                              "FROM library.books "
                             f"WHERE name = \"{ name }\" AND author = \"{ author }\" AND amount > 0" )

    def all( self ) -> SQL_RETURN:
        return self.hdb.sql( f"SELECT { self.select } FROM library.books WHERE amount > 0" )


class BookLib( BookRead ):
    def __init__( self, hdb: HarperDB ) -> None:
        self.hdb = hdb
        self.select = "code, name, author, genre, pages, location, amount, available"

    def by_code( self, code: int ) -> SQL_RETURN:
        return self.hdb.sql( f"SELECT { self.select } "
                              "FROM library.books "
                             f"WHERE books.code = { code }" )

    def add( self, code: int, amount: int, name: str = "", author: str = "", genre: str = "", pages: int = 0 ) -> int:
        exist = self.by_code( code )
        if exist:
            self.hdb.sql( f"UPDATE library.books "
                          f"SET books.amount = {    int( exist[ 0 ][ 'amount' ] )    + amount }, "
                              f"books.available = { int( exist[ 0 ][ 'available' ] ) + amount } "
                          f"WHERE books.code = { code }" )
            return int( exist[ 0 ][ "location" ] )

        locs: SQL_RETURN = self.hdb.sql( "SELECT location FROM library.books ORDER BY location" )
        location = 0
        for book in locs:
            if int( book[ "location" ] ) != location:
                break
            location += 1

        self.hdb.sql( f"INSERT INTO library.books( code, name, author, location, amount, available, genre, pages ) "
                      f"VALUES ( { code }, \"{ name }\", \"{ author }\", { location }, "
                               f"{ amount }, { amount }, \"{ genre }\", { pages } )" )
        return location

    def update( self, code: int, field: str, new: str | int ) -> None:
        if isinstance( new, str ):
            new = f"\"{ new }\""
        self.hdb.sql( "UPDATE library.books "
                     f"SET { field } = { new } "
                     f"WHERE code = { code }" )

    def update_name( self, code: int, name: str ) -> None:
        self.update( code, "name", name )

    def update_author( self, code: int, author: str ) -> None:
        self.update( code, "author", author )

    def update_genre( self, code: int, genre: str ) -> None:
        self.update( code, "genre", genre )

    def update_pages( self, code: int, pages: int ) -> None:
        self.update( code, "pages", pages )

    def view_queue4code( self, code: int ) -> SQL_RETURN:
        queue = self.hdb.sql( "SELECT u.username, q.date_create, q.priority "
                              "FROM library.users AS u JOIN library.books AS b JOIN library.waiting_queue AS q "
                             f"WHERE u.id = q.uid AND b.id = q.bid AND b.code = { code } "
                              "ORDER BY q.priority DESC, q.date_create ASC" )
        return parse_dates( queue )

    def view_all_q( self ) -> SQL_RETURN:
        queue = self.hdb.sql( "SELECT b.code, u.username, q.date_create, q.priority "
                              "FROM library.users AS u JOIN library.books AS b JOIN library.waiting_queue AS q "
                              "WHERE u.id = q.uid AND b.id = q.bid "
                              "ORDER BY q.priority DESC, q.date_create ASC" )
        return parse_dates( queue )

    def add2queue( self, code: int, username: str, priority: str ) -> None:
        bid = self.hdb.sql( f"SELECT id FROM library.books WHERE books.code = { code }" )[ 0 ][ "id" ]
        uid = self.hdb.sql( f"SELECT id FROM library.users WHERE users.username = \"{ username }\"" )[ 0 ][ "id" ]

        self.hdb.sql( f"INSERT INTO library.waiting_queue( bid, uid, date_create, priority ) "
                      f"VALUES ( \"{ bid }\", \"{ uid }\", GETDATE(), { priority } )" )


class UserOp:
    PURCHASED_SELECT_FROM = "SELECT u.name_surname, u.username, b.name, b.author, ub.date_ret_exp " \
                            "FROM library.books AS b JOIN library.user_books AS ub JOIN library.users AS u "
    PURCHASED_WHERE       = "WHERE u.id = ub.uid AND b.id = ub.bid AND u.username IS NOT NULL AND ub.date_ret_act IS NULL "
    PURCHASED_ORDER_BY    = "ORDER BY u.name_surname, b.author, b.name"
    def __init__( self, hdb: HarperDB ) -> None:
        self.hdb = hdb

    def by_name_surname( self, name_surname: str ) -> SQL_RETURN:
        return self.hdb.sql( "SELECT name_surname, username, role "
                             "FROM library.users "
                            f"WHERE name_surname LIKE \"%{ name_surname }%\" AND username IS NOT NULL" )

    def by_username( self, username: str ) -> SQL_RETURN:
        found = self.hdb.sql( "SELECT u.name_surname, b.code, b.name, b.author, ub.date_ret_exp "
                              "FROM library.books AS b JOIN library.user_books AS ub JOIN library.users AS u "
                             f"WHERE u.username = \"{ username }\" AND u.id = ub.uid AND b.id = ub.bid" )
        if found:
            return found
        return self.hdb.sql( "SELECT name_surname, 'None' name, 'None' author, 'None' date_ret_exp "
                             "FROM library.users "
                            f"WHERE username = \"{ username }\"" )

    def view_all( self ) -> SQL_RETURN:
        return self.hdb.sql( "SELECT name_surname, username, role FROM library.users WHERE username IS NOT NULL" )

    def get_email( self, username: str ) -> str:
        email: SQL_RETURN = self.hdb.sql( "SELECT email FROM library.users "
                                         f"WHERE username = \"{ username }\"" )
        if email:
            return str( email[ 0 ][ "email" ] )
        return ""

    def get_number( self, username: str ) -> int:
        num: SQL_RETURN = self.hdb.sql( "SELECT phone_number FROM library.users "
                                       f"WHERE username = \"{ username }\"" )
        if num:
            return int( num[ 0 ][ "phone_number" ] )
        return -1

    def check_exist( self, username: str ) -> bool:
        usr = self.hdb.sql( "SELECT username "
                            "FROM library.users "
                           f"WHERE username = \"{ username }\"" )
        return bool( usr )

    def purchased_books_by_ns( self, name_surname: str ) -> SQL_RETURN:
        res = self.hdb.sql( f"{ self.PURCHASED_SELECT_FROM }"
                            f"{ self.PURCHASED_WHERE } AND u.name_surname LIKE \"%{ name_surname }%\" "
                            f"{ self.PURCHASED_ORDER_BY }" )
        for row in res:
            row[ "date_ret_exp" ] = parse_date( row[ "date_ret_exp" ] )
        return res

    def purchased_books_of_usrname( self, usrname: str ) -> SQL_RETURN:
        res = self.hdb.sql( f"{ self.PURCHASED_SELECT_FROM }"
                            f"{ self.PURCHASED_WHERE } AND u.username = \"{ usrname }\""
                            f"{ self.PURCHASED_ORDER_BY }" )
        for row in res:
            row[ "date_ret_exp" ] = parse_date( row[ "date_ret_exp" ] )
        return res

    def purchased_books_all( self ) -> SQL_RETURN:
        res = self.hdb.sql( f"{ self.PURCHASED_SELECT_FROM }"
                            f"{ self.PURCHASED_WHERE }"
                            f"{ self.PURCHASED_ORDER_BY }" )
        for row in res:
            row[ "date_ret_exp" ] = parse_date( row[ "date_ret_exp" ] )
        return res

    def remove_from_q( self, username: str ) -> bool:
        found = self.hdb.sql( "SELECT id FROM library.users "
                             f"WHERE username = \"{ username }\"" )
        if not found:
            return False
        uid = str( found[ 0 ][ "id" ] )
        self.remove_from_q_uid( uid )
        return True

    def remove_from_q_uid( self, uid: str ) -> None:
        self.hdb.sql( "DELETE FROM library.waiting_queue "
                     f"WHERE uid = \"{ uid }\"" )
    
    def add2queue( self, code: int, username: str, priority: int ) -> bool:
        bid = self.hdb.sql( f"SELECT id FROM library.books WHERE books.code = { code }" )[ 0 ][ "id" ]
        uid = self.hdb.sql( f"SELECT id FROM library.users WHERE users.username = \"{ username }\"" )[ 0 ][ "id" ]
        if not bid or not uid:
            return False

        self.hdb.sql( f"INSERT INTO library.waiting_queue( bid, uid, date_create, priority ) "
                      f"VALUES ( \"{ bid }\", \"{ uid }\", GETDATE(), { priority } )" )
        return True


class UserLib( UserOp ):
    def __init__( self, hdb: HarperDB ) -> None:
        self.hdb = hdb

    def debtors( self ) -> SQL_RETURN:
        res = self.hdb.sql( "SELECT u.username, u.name_surname, b.code, b.name, b.author, ub.date_ret_exp "
                            "FROM library.users AS u JOIN library.books AS b JOIN library.user_books AS ub "
                           f"{ self.PURCHASED_WHERE }AND ub.date_ret_exp < DATE( GETDATE() ) "
                            "ORDER BY ub.date_ret_exp" )
        return parse_dates( res )

    def give_book( self, code: int, username: str, ret_exp: str ) -> int:
        book = self.hdb.sql( "SELECT id, available "
                             "FROM library.books "
                            f"WHERE code = { code }" )
        usr = self.hdb.sql( f"SELECT id FROM library.users WHERE username = \"{ username }\"" )

        if not book:
            return -1
        if not usr:
            return -2
        if book[ 0 ][ "available" ] == 0:
            return -3

        ret_exp = my_date2db( ret_exp )

        bid, uid = book[ 0 ][ "id" ], usr[ 0 ][ "id" ]
        self.hdb.sql( "DELETE FROM library.waiting_queue "
                     f"WHERE uid = \"{ uid }\" AND bid = \"{ bid }\"" )

        self.hdb.sql( "UPDATE library.books "
                     f"SET available = available - 1 "
                     f"WHERE code = { code }" )
        self.hdb.sql( "INSERT INTO library.user_books ( bid, uid, date_ret_exp, date_start ) "
                     f"VALUES( \"{ bid }\", \"{ uid }\", \"{ ret_exp }\", GETDATE() )" )
        return 0

    def ret_book( self, code: int, username: str ) -> bool:
        book = self.hdb.sql( f"SELECT id FROM library.books WHERE code = { code }" )
        usr = self.hdb.sql(  f"SELECT id FROM library.users WHERE username = \"{ username }\"" )
        if not book or not usr:
            return False

        bid, uid = book[ 0 ][ "id" ], usr[ 0 ][ "id" ]
        to_upd = self.hdb.sql( "SELECT id "
                               "FROM library.user_books "
                              f"WHERE uid = \"{ uid }\" AND bid = \"{ bid }\" AND date_ret_act IS NULL" )
        if not to_upd:
            return False
        self.hdb.sql( "UPDATE library.user_books "
                      "SET date_ret_act = GETDATE() "
                     f"WHERE id = \"{ to_upd[ 0 ][ 'id' ] }\"" )

        self.hdb.sql( "UPDATE library.books "
                     f"SET available = available + 1 "
                     f"WHERE code = { code }" )

        return True


class UserAdm( UserOp ):
    def __init__( self, hdb: HarperDB ) -> None:
        self.hdb = hdb

    def add( self, role: str, name: str, email: str, phone: int, usrname: str, pwd: str ) -> None:
        self.hdb.sql( "INSERT INTO library.users ( role, username, name_surname, email, phone_number, password ) "
                     f"VALUES( \"{ role }\", \"{ usrname }\", \"{ name }\", \"{ email }\", { phone }, \"{ pwd }\" )" )

    def remove( self, username: str ) -> bool:
        found = self.hdb.sql( "SELECT id FROM library.users "
                             f"WHERE username = \"{ username }\"" )
        if not found:
            return False
        uid = str( found[ 0 ][ "id" ] )
        self.remove_from_q_uid( uid )

        self.hdb.sql( "UPDATE library.users "
                      "SET username = NULL "
                     f"WHERE uid = \"{ uid }\"" )

        return True

    def change( self, usrname: str, role: str ) -> None:
        self.hdb.sql( "UPDATE library.users "
                     f"SET role = \"{ role }\" "
                     f"WHERE username = \"{ usrname }\"" )
