from typing import List

from colors import Color


def print_color_lines( lines: List[ str ], color: str, fst: int, lst: int ):
    for i in range( fst, lst + 1 ):
        print( color, lines[ i ], Color.RESET, sep='' )


def print_logo():
    logo = [ " _________________________________________________________",
             "||-------------------------------------------------------||",
             "||.--.    .-._                        .----.             ||",
             '|||==|____| |H|___            .---.___|""""|_____.--.___ ||',
             "|||  |====| | |xxx|_          |+++|=-=|_  _|-=+=-|==|---|||",
             "|||==|    | | |   | \         |   |   |_\/_|Black|  | ^ |||",
             "|||  |    | | |   |\ \   .--. |   |=-=|_/\_|-=+=-|  | ^ |||",
             "|||  |    | | |   |_\ \_( oo )|   |   |    |Magus|  | ^ |||",
           '''|||==|====| |H|xxx|  \ \ |''| |+++|=-=|""""|-=+=-|==|---|||''',
           '''||`--^----'-^-^---'   `-' ""  '---^---^----^-----^--^---^||''',
             "||-------------------------------------------------------||",
             "||-------------------------------------------------------||",
             "||               ___                   .-.__.-----. .---.||",
             "||              |===| .---.   __   .---| |XX|<(*)>|_|^^^|||",
             "||         ,  /(|   |_|III|__|''|__|:x:|=|  |     |=| Q |||",
             "||      _a'{ / (|===|+|   |++|  |==|   | |  |Illum| | R |||",
             "||      '/\// _(|===|-|   |  |''|  |:x:|=|  |inati| | Y |||",
             "||_____  -\{___(|   |-|   |  |  |  |   | |  |     | | Z |||",
             "||       _(____)|===|+|[I]|DK|''|==|:x:|=|XX|<(*)>|=|^^^|||",
             "||              `---^-^---^--^--'--^---^-^--^-----^-^---^||",
             "||-------------------------------------------------------||",
             "||_______________________________________________________||",
    ]

    print_color_lines( logo, Color.DARK_YELLOW, 0, 1 )

    for i in range( 2, 10 ):
        print(
            Color.DARK_YELLOW,  logo[ i ][    : 2 ],
            Color.CYAN,         logo[ i ][  2 : 6 ],
            Color.BLUE,         logo[ i ][  6 : 10 ],
            Color.GREEN,        logo[ i ][ 10 : 13 ],
            Color.YELLOW,       logo[ i ][ 13 : 15 ],
            Color.RED,          logo[ i ][ 15 : 19 ],
            Color.DARK_GREEN,   logo[ i ][ 19 : 24 ],
            Color.WHITE,        logo[ i ][ 24 : 30 ],
            Color.DARK_GREEN,   logo[ i ][ 30 : 35 ],
            Color.DARK_CYAN ,   logo[ i ][ 35 : 38 ],
            Color.DARK_RED,     logo[ i ][ 38 : 44 ],
            Color.YELLOW,       logo[ i ][ 44 : 49 ],
            Color.DARK_MAGENTA, logo[ i ][ 49 : 53 ],
            Color.LIGHT_GRAY,   logo[ i ][ 53 : 57 ],
            Color.DARK_YELLOW,  logo[ i ][ 57 : ],
            Color.RESET, sep=''
        )

    print_color_lines( logo, Color.DARK_YELLOW, 10, 11 )

    for i in range( 12, 20 ):
        print(
            Color.DARK_YELLOW,  logo[ i ][    : 8 ],
            Color.DARK_GREEN,   logo[ i ][  8 : 16 ],
            Color.YELLOW,       logo[ i ][ 16 : 21 ],
            Color.DARK_RED,     logo[ i ][ 21 : 22 ],
            Color.CYAN,         logo[ i ][ 22 : 27 ],
            Color.MAGENTA,      logo[ i ][ 27 : 29 ],
            Color.BLUE,         logo[ i ][ 29 : 33 ],
            Color.RED,          logo[ i ][ 33 : 35 ],
            Color.DARK_CYAN,    logo[ i ][ 35 : 39 ],
            Color.YELLOW,       logo[ i ][ 39 : 42 ],
            Color.RED,          logo[ i ][ 42 : 44 ],
            Color.GREEN,        logo[ i ][ 44 : 51 ],
            Color.WHITE,        logo[ i ][ 51 : 52 ],
            Color.BLUE,         logo[ i ][ 52 : 57 ],
            Color.DARK_YELLOW,  logo[ i ][ 57 : ],
            Color.RESET, sep=''
        )

    print_color_lines( logo, Color.DARK_YELLOW, 20, 21 )
    print()
