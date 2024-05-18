from getpass import getpass
from typing import Callable, List

from colors import Color
from print import *


def get_input( is_pass = False ) -> str:
    prompt = f"{ Color.DARK_GREEN }[#library#]{ Color.RESET }-->"
    return getpass( prompt=prompt ) if is_pass else input( prompt )


def get_num( fun: Callable[ [ str ], str ], input: str ) -> int:
    while True:
        try:
            return int( fun( input ) )
        except ValueError:
            print_error( "You should use numbers." )


def get_uint( fun: Callable[ [ str ], str ], input: str ) -> int:
    num = get_num( fun, input )
    while num < 0:
        print_error( "Number should be non-negative." )
        num = get_num( fun, input )
    return num


def get_nemty_str( fun: Callable[ [ str ], str ], input: str ) -> str:
    ans = fun( input )
    while not ans:
        print_error( "Field can not be empty." )
        ans = fun( input )
    return ans


def get_valid_str( is_valid: Callable[ [ str ], bool ], input: Callable[ [ str ], str ], quest: str ) -> str:
    ans = ''
    while not ans:
        ans = input( quest )
        if not is_valid( ans ):
            ans = ''
    return ans


def ask_question( quest: str, pos_ans: List[ str ] = [] ) -> str:
    print( Color.GREEN, "[?] ", Color.RESET, quest, sep='', end=' ' )
    for i, ans in enumerate( pos_ans ):
        print( ' (', str( i + 1 ), ')', ans, sep='', end='' )
    print()

    return get_input().strip().replace('"', '”').replace( "'", "’" )


def ask_open_question( quest: str, is_pass = False ) -> str:
    print( Color.GREEN, "[+] ", Color.RESET, quest, sep='' )
    return get_input( is_pass ).strip().replace('"', '”').replace( "'", "’" )
