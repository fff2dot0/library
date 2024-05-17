from com_usr import search_book, acc_det
from print import *
from table import print_table
from input import *
from roles import Reader
from get_attr import get_author, get_book_name


def purchase_req( usr: Reader ) -> None:
    name = get_book_name()
    author = get_author()
    found = usr.book_search.by_na_exact( name, author )
    if not found:
        print_error( f"Book { name } written by { author } was not found." )
        return
    usr.req_purchase( str( found[ 0 ][ "id" ] ) )
    print_info( "Success." )


def com_reader( usr: Reader ) -> None:
    while True:
        ans = ask_question( f"What would you like to do?",
                            [ "Book search", "View all books", "View my books", "Purchase request",
                              "View purchase history", "Account details", "Send feedback" ] )
        match ans:
            case '1':
                search_book( usr.book_search )
            case '2':
                table = usr.book_search.all()
                print_table( table )
            case '3':
                table = usr.my_books()
                if not print_table( table ):
                    print_info( "Currently you do not have books from this library." )
            case '4':
                purchase_req( usr )
            case '5':
                table = usr.history()
                if not print_table( table ):
                    print_info( "You have not purchased any books yet." )
            case '6':
                acc_det( usr )
            case '7':
                feed = ask_open_question( "Enter your feedback." )
                if usr.send_feedback( feed ):
                    print_info( "Your feedback was successfully sent." )
            case _:
                return
        print()
