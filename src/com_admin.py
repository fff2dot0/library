from roles import Admin
from input import *
from com_usr import acc_det, search_book, hash_password
from com_lib import search_usr
from table import print_table
from get_attr import get_email, get_phone, get_usrname, get_name_surname

ROLES = [ "reader", "librarian", "administrator" ]


def book_op( usr: Admin ) -> None:
    ans = ask_question( "What you would like to do?", [ "Search", "View all" ] )
    match ans:
        case '1':
            search_book( usr.book_search )
        case '2':
            table = usr.book_search.all()
            print_table( table )


def usr_op( usr: Admin ) -> None:
    ans = ask_question( "What would you like to do?",
                        [ "User search", "View all users", "Add user", "Remove user", "Change user role" ] )
    match ans:
        case '1':
            search_usr( usr.usr_op )
        case '2':
            table = usr.usr_op.view_all()
            print_table( table )
        case '3':
            add_usr( usr )
        case '4':
            remove_usr( usr )
        case '5':
            change_role( usr )


def add_usr( usr: Admin ) -> None:
    role = ask_question( "Choose the role of the new user.", [ "Reader", "Librarian", "Administrator" ] )
    if role not in "123":
        return
    role = ROLES[ int( role ) - 1 ]
    name = get_name_surname( "Enter name and surname." )
    email = get_email( "Enter e-mail." )
    phone = get_phone( "Enter phone number." )
    usrnm = get_usrname()
    while not usr.is_avail_in_users( usrnm ):
        print_error( f"Username '{ usrnm }' is already taken." )
        usrnm = get_usrname()
    pwd = ask_open_question( "Enter password.", True )
    while pwd != ask_open_question( "Enter the same password again.", True ):
        print_error( "Incorrect password." )

    usr.usr_op.add( role, name, email, int( phone ), usrnm, hash_password( pwd ) )
    print_info( f"New { role } was successfully added." )


def remove_usr( usr: Admin ) -> None:
    usrname = get_usrname()
    purchased = usr.usr_op.purchased_books_of_usrname( usrname )
    if purchased:
        print_error( f"Aborted. User '{ usrname }' still has purchased books( { len( purchased ) } )." )
        return
    if not usr.usr_op.remove( usrname ):
        print_warn( f"User '{ usrname }' does not exist." )
        return
    print_info( "Success." )


def change_role( usr: Admin ) -> None:
    usrname = get_usrname()
    if not usr.usr_op.by_username( usrname ):
        print_error( f"User '{ usrname }' does not exist." )
        return
    role = ask_question( "Choose new role:", ROLES )
    if role not in "123":
        return
    usr.usr_op.change( usrname, ROLES[ int( role ) - 1 ] )


def com_admin( usr: Admin ) -> None:
    ops = [ book_op, usr_op, acc_det ]
    while True:
        ans = ask_question( f"What would you like to do?",
                            [ "Book operations", "User operations", "Account details", "View feedback" ] )
        match ans:
            case '1' | '2' | '3':
                ops[ int( ans ) - 1 ]( usr )
            case '4':
                table = usr.get_feedback()
                if not print_table( table ):
                    print_info( "No feedback yet." )
            case _:
                return
