import sys
import os

from column import Column


class Screen():
    """
    Class controlling printing each column of falling ASCII characters
    and controlling terminal's overall apearence

    _row_num: int - number of terminal rows
    _col_num: int - number of terminal columns
    _columns: tuple(Column) - tuple containing all terminal columns  
    """

    def __init__(self) -> None:
        """
        Check the terminal size and creates needed number of columns to
        fill the whole terminal
        """
        self._row_num = os.get_terminal_size().lines
        self._col_num = os.get_terminal_size().columns
        self._columns = ()
        for col_index in range(0, self._col_num):
            self._columns += (Column(self._row_num, col_index), )

    @property
    def columns(self):
        return self._columns

    @staticmethod
    def clear()-> None:
        """Clears the whole terminal"""
        sys.stdout.write("\033[2J")
        sys.stdout.flush()

    @staticmethod
    def hide_cursor() -> None:
        """Hides terminal cursor"""
        sys.stdout.write("\033[?25l")
        sys.stdout.flush()

    @staticmethod
    def show_cursor() -> None:
        """Shows terminal cursor"""
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()

    @staticmethod
    def render() -> None:
        """Prints out the text written to the stdout buffer"""
        sys.stdout.flush()

    def move(self, row: int, col: int) -> None:
        """Moves terminal cursor to the [row, column] position

        Args:
            row (int): row number to put cursor
            col (int): column number to put cursor

        Raises:
            IndexError: when tries to move the cursor outside 
                        the terminal's boundried 
        """
        if row > self._row_num or col > self._col_num:
            raise IndexError(f"Exceeded terminal size - move index{[row,col]}, max size {[self._row_num, self._col_num]}")
        # add 1 to row and col - terminal indexing starts at [1,1]
        sys.stdout.write("\033[" + str(row + 1) + ";" + str(col + 1) + "H")
    
    # refactor !! @staticfun ?
    def stdout_write_column(self, column) -> None:
        """Writes whole column to the stdout"""
        colored = column.colored
        for row_num in range(0, column.line_end - column.line_start):
            self.move(row_num + column.line_start, column.index)
            sys.stdout.write(colored[row_num])

    def change_columns_characters(self) -> None:
        """Changes random character in random started columns line
        to another random character
        """
        for column in self._columns:
            if column.started:
                column.change_random_character()

    def next_iteration(self):
        """Generates next iterarion of falling ASCII characters 
        for all columns
        """
        for column in self._columns:
            column.iter()

    def image_render(self) -> None:
        """Renders whole image on the terminal"""
        self.clear()
        self.next_iteration()
        for column in self._columns:
            if column.started:
                self.stdout_write_column(column)
        self.render()

    def clean(self) -> None:
        """Cleaning function after rendering ends"""
        self.show_cursor()
        self.move(0,0)
        self.clear()
