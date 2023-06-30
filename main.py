import random
"""
MIT License

Copyright (c) 2023 Blue-Robin-Taken

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
I do not give a rats ass about variable namings
if you care, just make a PR or something
I'll probably see it
probably
"""


class Snake:
    def __init__(self, grid_size, empty_char='⬜', snake_char='😀', tail_char='😎'):
        self.running = None  # for console running
        self.grid = [[empty_char for y in range(grid_size)] for i in range(grid_size)]  # snake grid
        self.grid_size = grid_size
        self.snake_char = snake_char
        self.tail_char = tail_char
        self.empty_char = empty_char

        row = int(len(self.grid) / 2)
        self.snake_pos = [row, row]
        self.apples = 0
        self.tail_positions = []
        self.last_move = (0, 0)

    def load_grid(self):
        """
        Function to load the grid in the console via print
        """
        for x in self.grid:
            print_list = []
            for y in x:
                print_list.append(y)
            print("".join(print_list))

    def return_grid(self) -> str:
        """
        Function to return the grid in a format that's readable
        """
        end_return = []
        for x in self.grid:
            row_list = []
            for y in x:
                row_list.append(y)
            end_return.append("".join(row_list))
        return "\n".join(end_return)

    def start(self):
        """
        Start the snake game by creating the snake
        """
        self.grid[self.snake_pos[0]][self.snake_pos[1]] = self.snake_char

    def console_game(self):
        self.running = True
        controls = {
            'up': self.move_up,
            'down': self.move_down,
            'left': self.move_left,
            'right': self.move_right,
            'exit': lambda: 'stop',
        }

        while self.running:
            user_input = input()
            if user_input in controls.keys():
                controls_output = controls[user_input]()
                if controls_output == 'stop':
                    return

                self.spawn_apple()
                self.tail_handle()
                self.load_grid()

                print(self.snake_pos)
            else:
                print('False input. Use one of the following: ', end="")
                print(", ".join(controls.keys()))

    # --- Snake Movements ---

    def check_move(self, x_off, y_off) -> True | False:
        """
        This function is to stop Index errors in the grid.
        If an index error occurs, the snake DIES.
        also I named things weird for some reason
        don't think about it too much...
        IF IT WORKS, IT WORKS

        also,
        if there's an apple it adds a score

        and,
        if there's a tail it kills the snake.
        """
        x = self.snake_pos[1] + x_off  # I did this weird...
        y = self.snake_pos[0] + y_off
        if x >= self.grid_size or x < 0:
            return True  # snake died GG ez
        if y >= self.grid_size or y < 0:
            return True  # snake died GG ez

        if self.grid[y][x] == '🍎':
            self.apples += 1
        if self.grid[y][x] == self.tail_char:
            return True
        return False

    def move_right(self):  # move snake right
        if self.check_move(1, 0):
            self.running = False
            return
        self.grid[self.snake_pos[0]][self.snake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.snake_pos[0]][self.snake_pos[1] + 1] = self.snake_char  # re-add snake in new position
        self.snake_pos = [self.snake_pos[0], self.snake_pos[1] + 1]
        return 0, 1

    def move_left(self):  # move snake left
        if self.check_move(-1, 0):
            self.running = False
            return
        self.grid[self.snake_pos[0]][self.snake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.snake_pos[0]][self.snake_pos[1] - 1] = self.snake_char  # re-add snake in new position
        self.snake_pos = [self.snake_pos[0], self.snake_pos[1] - 1]
        return 0, -1

    def move_down(self):  # move snake down
        if self.check_move(0, 1):
            self.running = False
            return
        self.grid[self.snake_pos[0]][self.snake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.snake_pos[0] + 1][self.snake_pos[1]] = self.snake_char  # re-add snake in new position
        self.snake_pos = [self.snake_pos[0] + 1, self.snake_pos[1]]
        return 1, 0

    def move_up(self):  # move snake up
        if self.check_move(0, -1):
            self.running = False
            return
        self.grid[self.snake_pos[0]][self.snake_pos[1]] = self.empty_char  # remove snake from grid
        self.grid[self.snake_pos[0] - 1][self.snake_pos[1]] = self.snake_char  # re-add snake in new position
        self.snake_pos = [self.snake_pos[0] - 1, self.snake_pos[1]]
        return -1, 0

        # I hate boilerplate
        # That one o'hare youtber is cool tho

    def spawn_apple(self):
        spawn_points = []
        for x in range(self.grid_size):
            for y in range(self.grid_size):
                if self.grid[x][y] != self.snake_char and self.grid[x][y] != self.tail_char and self.grid[x][y] != '🍎':
                    spawn_points.append([x, y])
        random_choice = 0
        try:
            random_choice = random.randint(0, len(spawn_points) - 1)
        except ValueError:
            pass
        try:
            self.grid[spawn_points[random_choice][0]][spawn_points[random_choice][1]] = '🍎'
        except IndexError:
            pass

    def tail_handle(self):
        if self.apples > 0:
            self.tail_positions.append(self.snake_pos.copy())  # the copy is important
            for pos in self.tail_positions:
                if pos != self.snake_pos:
                    self.grid[pos[0]][pos[1]] = self.tail_char

            print(self.tail_positions)
            if self.apples < len(self.tail_positions) - 1:
                if self.tail_positions[0] != self.snake_pos:
                    self.grid[self.tail_positions[0][0]][
                        self.tail_positions[0][1]] = self.empty_char  # replace end tail with empty char
                    self.tail_positions.pop(0)


snake = Snake(5, '⬜')  # I'm scared
snake.start()
print(snake.return_grid())
# snake.load_grid()
snake.console_game()
