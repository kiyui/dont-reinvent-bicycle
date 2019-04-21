Title: the unix paradigm
Date: 2019-04-19 15:00
Modified: 2019-04-21 12:17
Tags: programming, unix, musing
Slug: the-unix-paradigm
Summary: how was software for the UNIX paradigm written?

If you're a learned programmer or computer nerd, you may have heard of the UNIX philosophy;- A set of guidelines to developing minimalist and modular software. The premise of this design pattern was fundamentally opposed to software designed in a monolithic fashion. We've all seen those crazy bash liners for doing a myriad of tasks. There's even an [entire site](http://www.bashoneliners.com/) dedicated to it. Here's one I have aliased and use frequently:
```bash
fd -t f 2> /dev/null | fzy | xsel -b

# fd -t f       Find all files in the current directory
# 2> /dev/null  Pipe errors to /dev/null so we don't see them
# fzy           Fuzzy search program
# xsel -b       Copy the output to clipboard
```
I'm not going to go too deep into the UNIX philosophy, though if you are interested, AT&T has made available [this great video](https://www.youtube.com/watch?v=tc4ROCJYbm0) on YouTube. The UNIX design philosophy was designed not only with composability in mind, but with the limitations that the machines had. Writing monolith software took more memory as the software had to take on more responsibilities. Software was designed to do one thing, and one thing only. We have today come to know this as "the functional approach" to programming;- Writing composable functions easy to test and piece together.
```javascript
users
  .filter(ageMoreThan(18))
  .reduce(sortByAge) // If you think about it, pipes are all reduce statements!
  .map(prop('name'))
```

With the [TC39 pipeline operator](https://tc39.github.io/proposal-pipeline-operator/) for ECMAScript in place and libraries like RxJS introducing [pipeable operators](https://github.com/ReactiveX/rxjs/blob/91088dae1df097be2370c73300ffa11b27fd0100/doc/pipeable-operators.md), we are seeing large code ecosystems adopt ever more functional programming ideas. That said, while functional programming and composable functions are great and all, what did it mean to the original UNIX developers? What was it to this idea that was so fundamentally different? I had to see for myself;- By building a program that relies on pipes. Naturally, I settled upon writing the 2048 game, using UNIX principles.

## unix 2048

Let's consider the components of the game 2048. It is build by a 4x4 grid as so:
```
-----------------
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 0 |
-----------------
```
Parsing this in an application would be hard, so let's break it down into a single 1x16 CSV string:
```
0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```
The game starts off with a single `2` randomly on the board, as well as one added per move in the game. As such, we would a need a function that takes a board and replaces an empty space, represented by a `0`, with a `2`. I decided to go with Python for this program since it is stupidly simple programming language for getting anything done. The following details a hacked together way to add a number `2` to an array of length 16:
```python
def add_random(board):
    game_board = list(board).copy()

    random_added = False
    while not random_added:
        add_at = randint(0, len(game_board) - 1)

        # Replace the value if it is a 2
        if game_board[add_at] == 0:
            game_board[add_at] = 2
            random_added = True

    return game_board
```
Great! Let's call this program `add_program.py`. It will read a board of `1x16` from STDIN (or from a provided argument) and print out a board of `1x16` to STDOUT with a 2 added to it.
```bash
./add_random.py --help

# usage: add_random.py [-h] [--board BOARD]
# 
# Randomly populates an empty tile in a 2048 board string with a 2.
# 
# optional arguments:
#   -h, --help     show this help message and exit
#   --board BOARD  The 2048 game board as a CSV string
```
This works out to something like this:
```bash
echo 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 | ./src/add_random.py #=> 0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0
```
Now, we need a program to help us shift the values on the board according to the values swiped. In the game 2048, one can swipe from top to bottom, left to right, and vice-versa. For example, a swipe right on the following board:
```
-----------------
| 0 | 0 | 0 | 0 |
| 0 | 2 | 2 | 0 |
| 0 | 0 | 0 | 4 |
| 0 | 2 | 4 | 4 |
-----------------
```
would result in the following:
```
-----------------
| 0 | 0 | 0 | 0 |
| 0 | 0 | 0 | 4 |
| 0 | 0 | 0 | 4 |
| 0 | 0 | 2 | 8 |
-----------------
```
Playing the game would do more justice than any explanation could. Values are added row by row, adding same values and shifting populated values over empty values. Simplified, this only requires that we deal with every board row by row from left to right, such as the following:
```
-----------------
| 0 | 0 | 0 | 0 |
| 0 | 2 | 2 | 0 |
| 0 | 0 | 0 | 4 |
| 0 | 2 | 4 | 4 |
-----------------

# 4th row, right to left: 4,4,2,0
# 4th column, top to bttom: 0,0,4,4
```
Assuming we could write a function that would shift these values in the order left to right, we could break any 4x4 matrix into a 1x4 array in any direction and have it dealt with row by row. Let's write a function in a separate program to do just that:
```python
def slide_values(value_row):
    output_row = value_row.copy()

    i = len(output_row) - 1
    while i >= 0:
        current = output_row[i]
        ii = i - 1
        while ii >= 0:
            before = output_row[ii]

            if current == 0:
                output_row[i] = before
                output_row[ii] = 0
                current = before
            elif current == before:
                output_row[i] = current * 2
                output_row[ii] = 0
                break
            elif before != 0:
                break

            ii -= 1
        i -= 1

    return output_row
```
Putting that in a test case, we can assert that exact behaviour:
```python
from game import slide_values, play_game

def test_slide_values():
    # etc...
    assert slide_values([2, 0, 4, 2]) == [0, 2, 4, 2]
    assert slide_values([2, 4, 0, 4]) == [0, 0, 2, 8]
    assert slide_values([2, 4, 2, 0]) == [0, 2, 4, 2]
    assert slide_values([2, 4, 2, 2]) == [0, 2, 4, 4]
    # etc...
```
Great, now from a 1x16 CSV input, we can simply convert it into a 4x4 matrix and rotate it such that our rows can always result in a 1x4 input to be parsed by the `slide_values` function. Packaging this as another program, we now have a `game.py` program. We can now have the program composed as so, the first argument to `game.py` being the direction:
```bash
./game.py --help

# usage: game.py [-h] [--board BOARD] direction
# 
# Creates an output 2048 board based on the provided direction and input board.
# 
# positional arguments:
#   direction      0: Up, 1: Down, 2: Left, 3: Right
# 
# optional arguments:
#   -h, --help     show this help message and exit
#   --board BOARD  The 2048 game board as a CSV string
```
Using the program works out to the following:
```bash
echo 0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0 | ./src/game.py 0 #=> 2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```

## putting it all together

The game now being composed, we can try playing it! The following details an example game-play of `unix-2048`:
```
$ echo "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0" | ./src/add_random.py
#=> 0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0

$ echo "0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0" | ./src/game.py 3 | ./src/add_random.py
#=> 0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,2

$ echo "0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,2" | ./src/game.py 1 | ./src/add_random.py
#=> 0,0,2,0,0,0,0,0,0,0,0,0,0,2,0,2

$ echo "0,0,2,0,0,0,0,0,0,0,0,0,0,2,0,2" | ./src/game.py 3 | ./src/add_random.py
#=> 0,2,0,2,0,0,0,0,0,0,0,0,0,0,0,4
```
The UX of that was pretty bad, so I coded up a `view.py` that prints a 1x16 input string as a 4x4 table. Piecing that as a script, I managed to come up with a full-on game!
```bash
while true
do
  function update_view () {
    clear
    ./src/view.py --board $board
  }

  if [[ $direction -eq 4 ]]; then
    >&2 echo "Invalid direction:" 
    >&2 echo "w: up, a: left, s: down, r: right" 
  elif [[ -z $board ]]; then
    board=$(./src/add_random.py --board "0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    update_view
  else
    board=$(./src/game.py "$direction" --board "$board" | ./src/add_random.py)
    update_view
  fi

  # Get input
  read -s -n1 key

  case "$key" in
    "w") direction=0;;
    "a") direction=2;;
    "s") direction=1;;
    "d") direction=3;;
    *) direction=4;;
  esac
done
```
Check out the end result [on GitHub](https://github.com/kiyui/unix-2048). Cheers, and enjoy your musing.
