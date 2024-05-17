from datetime import datetime

from roles import Librarian
from db_ops import BookLib, UserLib, UserOp
from com_usr import search_book, acc_det
from input import ask_question, ask_open_question, get_uint, get_num
from get_attr import get_code, get_name_surname, get_usrname, get_book_name, get_author, get_genre, get_pages
from table import print_table
from print import *


def check_date( date: str ) -> bool:
    """
    return True if <date> is correct date and is at least today, else False
    """
    ldate = date.split( '-' )
    if len( ldate ) != 3:
        return False
    try:
        d, m, y = int( ldate[ 0 ] ), int( ldate[ 1 ] ), int( ldate[ 2 ] )
        dt = datetime( day=d, month=m, year=y )
    except ValueError:
        return False

    return dt >= datetime.today()


def book_ops( usr: Librarian ) -> None:
    ans = ask_question( f"What you would like to do?",
                        [ "Search", "View all", "Add", "Remove", "Update info", "Give", "Return" ] )
    match ans:
        case '1':
            search_book( usr.book_search )
        case '2':
            table = usr.book_search.all()
            print_table( table )
        case '3':
            add_books( usr.book_search )
        case '4':
            remove_books( usr.book_search )
        case '5':
            update_book( usr.book_search )
        case '6':
            give_book( usr.usr_op )
        case '7':
            return_book( usr.usr_op )


def update_book( book_op: BookLib ) -> None:
    code = get_code()
    update = [ ( "Enter new book's name.",            get_book_name, book_op.update_name ),
               ( "Enter new book's author.",          get_author,    book_op.update_author ),
               ( "Enter new book's genre.",           get_genre,     book_op.update_genre )
                 ]
    while True:
        ans = ask_question( "What info would you like to update?", [ "Name", "Author", "Genre", "Pages" ] )
        match ans:
            case '1' | '2' | '3':# | '4':
                quest, get_new, updatef = update[ int( ans ) - 1 ]
                new = get_new( quest )
                updatef( code, new )
            case '4':
                lambda quest : get_uint( ask_open_question, quest )
                pages = get_uint( ask_open_question, "Enter new book's amount of pages." )
                book_op.update_pages( code, pages )
            case _:
                return


def add2q( usr_op: UserLib, code: int = -1, username: str = "" ) -> None:
    while True:
        if code == -1:
            code = get_code( "Enter book's code." )
        if not username:
            username = get_usrname( "Enter reader's username." )
        prior = get_num( ask_open_question, "Enter priority." )
        if usr_op.add2queue( code, username, prior ):
            print_info( "Success." )
            return
        print_error( f"Either book( { code= } ) or user( { username= } ) does not exist." )
        ans = ask_question( "Would you like to retry?", [ "Yes", "No" ] )
        if ans != '1':
            return


def give_book( usr_op: UserLib ) -> None:
    while True:
        code = get_code( "Enter book's code." )
        username = get_usrname( "Enter reader's username." )
        date_ret_exp = ask_open_question( "When should reader return this book( day-month-year )?" )
        while not check_date( date_ret_exp ):
            print_error( f"The date <{ date_ret_exp }> is either incorrect date or is less than today." )
            date_ret_exp = ask_open_question( "When should reader return this book( day-month-year )?" )
        ok = usr_op.give_book( code, username, date_ret_exp )
        if ok == 0:
            print_info( "Success." )
            return

        if ok == -3:
            print_warn( f"Book({ code = } ) is not currently available." )
            ans = ask_question( "Would you like to add user to waiting queue?", [ "Yes", "No" ] )
            if ans == "1":
                add2q( usr_op, code, username )
            return

        if ok == -2:
            print_error( f"User({ username = } ) does not exist." )
        if ok == -1:
            print_error( f"Book({ code = } ) does not exist." )

        ans = ask_question( "Would you like to retry?", [ "Yes", "No" ] )
        if ans != '1':
            return


def return_book( usr_op: UserLib ) -> None:
    while True:
        code = get_num( ask_open_question, "Enter book's code." )
        username = ask_open_question( "Enter reader's username." )
        if usr_op.ret_book( code, username ):
            print_info( "Success." )
            return

        print_error( f"Either book( { code= } ) or user( { username= } ) does not exist, "
                      "or user has not purchased this book." )
        ans = ask_question( "Would you like to retry?", [ "Yes", "No" ] )
        if ans != '1':
            return


def add_books( ops: BookLib ) -> None:
    code = get_code()
    add = get_uint( ask_open_question, "How many books to add?" )
    if ops.by_code( code ):
        ops.add( code, add )
        print_info( "Success." )
        return

    name = ask_open_question( "Enter book's name." )
    author = ask_open_question( "Enter author's name and surname." )
    genre = ask_open_question( "Enter genre." )
    pages = get_uint( ask_open_question, "Enter amount of pages." )
    loc = ops.add( code, add, name, author, genre, pages )
    print_info( f"New books were successfully added, location of these books: { loc }." )


def remove_books( ops: BookLib ) -> None:
    code = get_code()
    book = ops.by_code( code )
    if not book:
        print_error( f"Book with code { code } was not found." )
        return

    remove = get_uint( ask_open_question, "How many books to remove?" )
    assert( isinstance( book[ 0 ][ "available" ], int ) )   # for MyPy
    if book[ 0 ][ "available" ] < remove:
        print_error( f"Can not remove more books( { remove } ), "
                     f"than currently available( { book[ 0 ][ 'available' ] } )." )
        return
    ops.add( code, -remove )
    print_info( "Success." )


def display_q( book_op: BookLib ) -> None:
    ans = ask_question( "Choose how to display.", [ "For book", "View all" ] )
    match ans:
        case '1':
            code = get_code()
            table = book_op.view_queue4code( code )
            if not print_table( table ):
                print_warn( "There is no queue for this book." )
        case '2':
            table = book_op.view_all_q()
            if not print_table( table ):
                print_warn( "There are no queues." )


def search_usr( search: UserOp ) -> None:
    ans = ask_question( "Would you like to search by:", [ "username", "name surname" ] )
    match ans:
        case '1':
            usrname = get_usrname()
            table = search.by_username( usrname )
            if not print_table( table ):
                print_warn( f"User with username { usrname } was not found" )
        case '2':
            ns = get_name_surname()
            table = search.by_name_surname( ns )
            if not print_table( table ):
                print_warn( f"Users '{ ns }' were not found." )


def usr_with_purchased_bs( usr_op: UserLib ) -> None:
    ans = ask_question( "Would you like to search by:", [ "username", "name_surname", "view all" ] )
    match ans:
        case '1':
            usrname = get_usrname()
            table = usr_op.purchased_books_of_usrname( usrname )
            if not print_table( table ):
                print_warn( f"User '{ usrname }' either does not exist or has no purchased books." )
        case '2':
            ns = get_name_surname()
            table = usr_op.purchased_books_by_ns( ns )
            if not print_table( table ):
                print_warn( f"Users '{ ns }' either do not exist or have no purchased books." )
        case '3':
            table = usr_op.purchased_books_all()
            if not print_table( table ):
                print_warn( "No one has purchased any books." )


def usr_ops( usr: Librarian ) -> None:
    ans = ask_question( "What would you like to do?", [ "Search", "View all", "Debtors",
                                                        "Readers with purchased books", "Waiting" ] )
    match ans:
        case '1':
            search_usr( usr.usr_op )
        case '2':
            table = usr.usr_op.view_all()
            print_table( table )
        case '3':
            table = usr.usr_op.debtors()
            if not print_table( table ):
                print_info( "There are no debtors." )
        case '4':
            usr_with_purchased_bs( usr.usr_op )
        case '5':
            display_q( usr.book_search )


def com_librarian( usr: Librarian ) -> None:
    ops = [ book_ops, usr_ops, acc_det ]
    while True:
        ans = ask_question( "What you would like to do?",
                            [ "Book operations", "Reader operations", "Account details" ] )
        match ans:
            case '1' | '2' | '3':
                ops[ int( ans ) - 1 ]( usr )
            case _:
                return
