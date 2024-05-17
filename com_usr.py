from bcrypt import checkpw, gensalt, hashpw
from typing import Dict

from roles import User
from db_ops import BookRead
from get_attr import get_email, get_phone, get_usrname
from input import ask_question, ask_open_question
from print import print_info, print_error
from table import print_table


def hash_password( pwd: str ) -> str:
    pwd_bytes = pwd.encode()
    salt = gensalt()
    return hashpw( pwd_bytes, salt ).decode()


def check_pwd( usr: User, quest: str ) -> None:
    pwd: str = usr.hdb.sql( "SELECT password FROM library.users "
                           f"WHERE username = \"{ usr.username }\"" )[ 0 ][ "password" ]
    attempts = 3
    while attempts > 0 and not checkpw( ask_open_question( quest, True ).encode(), pwd.encode() ):
        print_error( "Incorrect password." )
        attempts -= 1
    if attempts == 0:
        print_error( "Too many unsuccessful attempts. Terminate." )
        raise EOFError


def search_book( search: BookRead ) -> None:
    while True:
        print_info( "If you don't want to search by a parameter, leave the line empty." )
        params: Dict[ str, str ] = {}
        params[ "name" ]   = ask_open_question( "Enter book name." )
        params[ "author" ] = ask_open_question( "Enter author's name." )
        params[ "genre" ]  = ask_open_question( "Enter genre of the book." )
        if print_table( search.search( params ) ):
            return
        print_info( f"No such books were found." )


def set_new_usrname( usr: User ) -> None:
    while True:
        new = get_usrname( "Enter new username." )
        if usr.is_avail_in_users( new ):
            usr.change_field( "username", new )
            print_info( "Success." )
            return
        print_error( f"Username '{ new }' is already taken." )


def set_new_pwd( usr: User ) -> None:
    check_pwd( usr, "Enter your old password." )
    pwd = ask_open_question( "Enter password.", True )
    while pwd != ask_open_question( "Enter the same password again.", True ):
        print_error( "Incorrect password." )
    new = hash_password( pwd )
    usr.change_field( "password", new )
    print_info( "Success." )


def acc_det( usr: User ) -> None:
    ans = ask_question( "What would you like to do?", [ "View", "Change" ] )
    match ans:
        case '1':
            table = usr.view_acc_info()
            print_table( table )
        case '2':
            while True:
                cng = ask_question( "Would you like to change:",
                                    [ "username", "e-mail", "phone_number", "password" ] )
                match cng:
                    case '1':
                        set_new_usrname( usr )

                    case '2':
                        new = get_email( "Enter new e-mail address." )
                        usr.change_field( "email", new )
                        print_info( "Success." )

                    case '3':
                        new = get_phone( "Enter new phone number." )
                        usr.change_field( "phone_number", int( new ) )
                        print_info( "Success." )

                    case '4':
                        set_new_pwd( usr )
                    case _:
                        return
