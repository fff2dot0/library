from typing import Union

from harperdb import HarperDB # type: ignore

from db_ops import BookRead, BookLib, UserLib, UserAdm, SQL_RETURN, parse_dates


class User:
    def __init__( self, hdb: HarperDB, id: str, username: str ) -> None:
        self.hdb = hdb
        self.id = id
        self.username = username
        self.book_search = BookRead( hdb )

    def view_acc_info( self ) -> SQL_RETURN:
        return self.hdb.sql( "SELECT username, name_surname, email, phone_number "
                             "FROM library.users "
                            f"WHERE id = \"{ self.id }\"" )

    def is_avail_in_users( self, val: str ) -> bool:
        found = self.hdb.sql( "SELECT id "
                              "FROM library.users "
                             f"WHERE username = \"{ val }\"" )
        return not found or found[ 0 ][ "id" ] == self.id

    def change_field( self, fname: str, val: Union[ int, str ] ) -> None:
        cng = str( val ) if isinstance( val, int ) else f"\"{ val }\""
        self.hdb.sql( f"UPDATE library.users "
                      f"SET { fname } = { cng } "
                      f"WHERE id = \"{ self.id }\"" )


class Reader( User ):
    def my_books( self ) -> SQL_RETURN:
        return self.hdb.sql( f"SELECT b.name, b.author, ub.date_start, ub.date_ret_exp "
                             f"FROM library.users AS u JOIN library.books AS b JOIN library.user_books AS ub "
                             f"WHERE u.username = \"{ self.username }\" AND u.id = ub.uid AND b.id = ub.bid AND "
                                    "ub.date_ret_act IS NULL" )

    def history( self ) -> SQL_RETURN:
        hist = self.hdb.sql( f"SELECT b.name, b.author, ub.date_start, ub.date_ret_exp, ub.date_ret_act "
                             f"FROM library.users AS u JOIN library.books AS b JOIN library.user_books AS ub "
                             f"WHERE u.username = \"{ self.username }\" AND u.id = ub.uid AND b.id = ub.bid" )
        return parse_dates( hist )

    def req_purchase( self, bid: str ) -> None:
        self.hdb.sql( f"INSERT INTO library.waiting_queue( bid, uid, date_create, priority ) "
                      f"VALUES ( \"{ bid }\", \"{ self.id }\", GETDATE(), 0 )" )

    def send_feedback( self, txt: str ) -> bool:
        if not txt:
            return False
        self.hdb.sql( "INSERT INTO library.feedback( uid, text ) "
                     f"VALUES ( \"{ self.id }\", { txt } )" )
        return True


class Librarian( User ):
    book_search: BookLib
    def __init__( self, hdb: HarperDB, id: str, username: str ) -> None:
        User.__init__( self, hdb, id, username )
        self.book_search = BookLib( hdb )
        self.usr_op = UserLib( hdb )


class Admin( User ):
    def __init__( self, hdb: HarperDB, id: str, username: str ) -> None:
        User.__init__( self, hdb, id, username )
        self.book_search = BookLib( hdb )
        self.usr_op = UserAdm( hdb )

    def get_feedback( self ) -> SQL_RETURN:
        return self.hdb.sql( "SELECT text FROM library.feedback" )
