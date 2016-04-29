# -*- coding: utf-8 -*-
__author__ = 'Jerry'



def fetch_bigtable_rows(big_table, keys, other_silly_variable=None):
	"""Fetches rows from a Bigtable.

	Retrieves rows pertaining to the given keys from the Table instance
	represented by big_table.  Silly things may happen if
	other_silly_variable is not None.

	Args:
		big_table: An open Bigtable Table instance.
		keys: A sequence of strings representing the key of each table row
            to fetch.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {'Serak': ('Rigel VII', 'Preparer'),
         'Zim': ('Irk', 'Invader'),
         'Lrrr': ('Omicron Persei 8', 'Emperor')}
    """

	pass

def main():
	pass

if __name__ == '__main__':
    main()