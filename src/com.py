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
    print_help()
    print( f"{ Color.CYAN }Welcome back, { usrname }.{ Color.RESET }" )

    if role == "reader":
        com_reader( Reader( hdb, uid, usrname ) )
    elif role == "librarian":
        com_librarian( Librarian( hdb, uid, usrname ) )
    elif role == "administrator":
        com_admin( Admin( hdb, uid, usrname ) )
