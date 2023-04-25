from string import ascii_letters
from random import choice, randint


class Column:
    """Class representing terminal column.

    Generates random falling ASCII characters and
    controls it's color.  

    HEAD_COLORS: tuple(int) - Contains color integer value of first characters
                              in falling line
    MIDDLE_COLORS: tuple(int) - Contains color integer value of middle characters
                              in falling line
    TAIL_COLORS: tuple(int) - Contains color integer value of last characters
                              in falling line

    CHAR_POOL: (str): Class variable specifing available characters to display
    _index: int - Column order index in terminal
    _row_num: int: - Number of rows
    _end: int - Column's last element index  
    _col: list(str) - List containing randomly selected characters form the 
                      CHAR_POOL   
    _line_len: int: - Random length of the falling line
    _line_start: int - Row position of the first element of the line
    _line_end:int - Row position of the last element of the line
    _iter_after_end: int - Iteration number after _line_end reaches _end
    _iter_after_line_len: int - Iteration number after line is fully generated
                                (reaches _line_len length)
    _run_delay: int - Deley for column start 
    _started: bool: True if falling process has been started,
                    False if falling process in not started
    """
    CHAR_POOL = ascii_letters + '1234567890!@#$%^&?></|'

    HEAD_COLORS = (255, 228, 226, 118)
    MIDDLE_COLOR = (82,)
    TAIL_COLORS = (70, 64 ,241, 236)

    def __init__(self, row_num: int, index: int) -> None:
        self._index = index
        self._row_num = row_num
        self._end = self._row_num - 1

        self._col = []
        self._line_len = 0
        self._line_start = 0
        self._line_end = 0

        self._iter_after_end = 0
        self._iter_after_line_len = 0

        self._run_delay = randint(0,self._row_num) * randint(0, 10) + randint(0,100)
        self._started = False

    @property
    def index(self):
        return self._index
    
    @property
    def line_start(self):
        return self._line_start
    
    @property
    def line_end(self):
        return self._line_end

    @property
    def colored(self):
        return self.__wrap_color()

    @property
    def started(self):
        return self._started

    def start(self) -> None:
        """Defines falling line legth and sets default values 
        for instance values

        If falling process did not start yet randon line length 
        is set and previous column values are cleared
        """
        colors_num = len(self.HEAD_COLORS) + len(self.MIDDLE_COLOR) + len(self.TAIL_COLORS)

        self._col = []
        # line length equation can be changed but it must not be equal the _end value
        self._line_len = int((self._end - colors_num)/10 + randint(0, int((self._end - colors_num) * 9/10)) + colors_num)
        self._line_start = 0
        self._line_end = 0

        self._iter_after_end = 0
        self._iter_after_line_len = 0

        self._started = True

    def end(self) -> None:
        """Cleaning function after column falling animation ends"""
        self._run_delay = randint(0,self._row_num) * randint(0, 10)
        self._started = False

    def __wrap_color(self) -> list[str]:
        """Wraps all characters in proper colors creating 
        dimming visual efect.

        Returns:
            list[str]: list containing self.col characters
                       wraped in proper coloring string 
        """
        colored = self._col.copy()
        head_color_num = len(self.HEAD_COLORS)
        tail_color_num = len(self.TAIL_COLORS)

        col_len = len(self._col)

        # head color characters staring index
        head_color_start = 0 if (col_len - head_color_num) < 0 \
                             else (col_len - head_color_num + self._iter_after_end)
        # head colors characters color wrapping
        if self._line_end < self._end:
            for index in range(head_color_start, col_len):
                colored[index] = self.colorize(colored[index], self.HEAD_COLORS[head_color_start - index - 1])
        elif self._iter_after_end < head_color_num:
            for index in range(head_color_start , col_len):
                colored[index] = self.colorize(colored[index], self.HEAD_COLORS[head_color_start - index - 1])
            if self._iter_after_end < head_color_num:
                self._iter_after_end += 1

        # middle color characters starting index
        middle_color_start = self._iter_after_line_len if self._line_start < (self._line_len - tail_color_num) \
                                  else self._iter_after_line_len
        
        # preventing overflow when _col length is lower than tail_color_num
        middle_color_start = min(middle_color_start, col_len)
        # middle color characters wrapping
        if self._line_start >= 0:
            for index in range(middle_color_start, head_color_start):
                colored[index] = self.colorize(colored[index], self.MIDDLE_COLOR[0])
            if self._iter_after_line_len < tail_color_num and self._line_end >= (self._line_len - tail_color_num):
                self._iter_after_line_len += 1
        
        for index in range(0, middle_color_start):
            colored[index] = self.colorize(colored[index], self.TAIL_COLORS[-index - 1])

        return colored
    
    @staticmethod
    def colorize(str_to_color: str, color: int) -> str:
        """Wraps string in ANSI escape code corresponding
        to the provided color number

        Args:
            str_to_color (str): string to colorize
            color (int): color's integer reference

        Returns:
            str: colorized string
        """
        return f"\u001b[38;5;{color}m{str_to_color}\u001b[0m"
    
    def change_random_character(self) -> None:
        """Changes random character in column line to another character
        from CHAR_POOL
        """
        try:
            rand_index =  randint(0, len(self._col) - 1)
        except:
            raise ValueError(f"Colum does not contain any characters generated")
        self._col[rand_index] = choice(self.CHAR_POOL.replace(self._col[rand_index],""))

    def iter(self) -> bool:
        """Generates next character in column line

        If falling process has been started next character is generated, 
        if falling process did not start randon line length is set and
        first character is generated.

        Returns:
            True: If falling process is still running
            False: If falling process ends or is not started
        """
        if self._started:
            if self._line_end > self._line_len:
                del self._col[0]
                self._line_start += 1

            if self._line_end < self._end:
                self._col.append(choice(self.CHAR_POOL))
                self._line_end += 1

            if self._line_start >= self._line_end:
                self.end()

        else:
            if self._run_delay > 0:
                self._run_delay -= 1
            else:
                self.start()

        return self._started
