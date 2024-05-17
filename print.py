from colors import Color


def print_info( info: str ) -> None:
    print( Color.BLUE, "[I] ", Color.RESET, info, sep='' )
    print()


def print_error( text: str ) -> None:
    print( Color.RED, "[!] error: ", text, Color.RESET, sep='' )
    print()


def print_warn( text: str ) -> None:
    print( Color.YELLOW, "[W] warning: ", text, Color.RESET, sep='' )
    print()
