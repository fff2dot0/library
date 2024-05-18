from email_validator import validate_email, EmailNotValidError

from phonenumbers import is_valid_number, parse, NumberParseException # type: ignore

from input import ask_open_question, get_uint, get_nemty_str, get_valid_str
from print import print_error


def get_code( quest: str = "Enter book's code." ) -> int:
    return get_uint( ask_open_question, quest )


def get_book_name( quest: str = "Enter book's name." ) -> str:
    return get_nemty_str( ask_open_question, quest )


def get_author( quest: str = "Enter author's name." ) -> str:
    return get_name_surname( quest )


def get_usrname( quest: str = "Enter username." ) -> str:
    return get_nemty_str( ask_open_question, quest )


def get_name_surname( quest: str = "Enter user's name and surname." ) -> str:
    def is_valid_pers_name( name: str ) -> bool:
        for chr in name:
            if chr in "0123456789":
                print_error( "Person's name can not contain numbers." )
                return False
        return True

    get_pers_name = lambda pname : get_nemty_str( ask_open_question, pname )

    return get_valid_str( is_valid_pers_name, get_pers_name, quest )


def get_genre( quest: str = "Enter book's genre." ) -> str:
    return get_nemty_str( ask_open_question, quest )


def get_pages( quest: str ) -> int:
    return get_uint( ask_open_question, quest )


def get_email( quest: str ) -> str:
    email = ''
    while not email:
        email = ask_open_question( quest )
        try:
            validate_email( email )
        except EmailNotValidError:
            print_error( f"E-mail address { email } is not valid." )
            email = ''
    return email


def get_phone( quest: str ) -> str:
    phone = ''
    while not phone:
        phone = ask_open_question( quest )
        try:
            if not is_valid_number( parse( phone, None ) ):
                print_error( f"Phone number { phone } is not valid." )
                phone = ''
        except NumberParseException:
            print_error( f"Phone number { phone } is not valid." )
            phone = ''
    return phone
