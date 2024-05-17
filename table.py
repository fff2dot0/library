from typing import Dict, List, Union

from terminaltables import AsciiTable # type: ignore


def print_table( table: List [ Dict[ str, Union[ int, str ] ] ] ) -> bool:
    if not table:
        return False

    new: List[ List[ Union[ int, str ] ] ] = [ list( table[ 0 ] ) ]

    for dict in table:
        add: List[ Union[ int, str ] ] = []
        for _, v in dict.items():
            add.append( v )
        new.append( add )

    ascii_table = AsciiTable( new )
    print( ascii_table.table )
    print()
    return True
