from com import sign_in
from print import print_info


def __main__():
    try:
        sign_in()
    except EOFError:
        pass
    finally:
        print( '\n' )
        print_info( "Good bye." )


if __name__ == "__main__":
    __main__()
