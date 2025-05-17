import copy
import enum
import math
import pathlib
import pprint
import random
import re
import typing
import string

import click

from wordsearch import _english_words

_MODULE_DIR = pathlib.Path(__file__).parent
_CHECK_FOR_OTHER_WORDS = _english_words.CHECK_FOR_OTHER_WORDS


class _Direction(enum.Enum):
    """Direction of word placement."""

    FORWARD = 0
    REVERSE = enum.auto()
    DOWN = enum.auto()
    UP = enum.auto()
    RIGHT_DOWN = enum.auto()
    RIGHT_UP = enum.auto()
    LEFT_DOWN = enum.auto()
    LEFT_UP = enum.auto()


def _print_grid(grid: typing.List[typing.List[str]], file=None):
    """Print the grid to the console."""
    print(" " * 3, end=" ", file=file)
    for i in range(len(grid[0])):
        print(chr(ord("A") + i), end=" ", file=file)
    print("", file=file)

    for i, row in enumerate(grid):
        print(f"{i+1:> 3}", " ".join([ch or " " for ch in row]), file=file)


def _make_grid(width: int, height: int) -> typing.List[typing.List[str]]:
    """Create a grid of the given width and height."""
    return [["" for _ in range(width)] for _ in range(height)]


def _place_word(grid: typing.List[typing.List[str]], word: str, direction: _Direction):
    """Place a word in the grid in the given direction."""
    word_length = len(word)
    grid_height = len(grid)
    grid_width = len(grid[0])

    if all(
        [
            word_length > grid_width,
            word_length > grid_height,
            (
                word_length > math.hypot(grid_width, grid_height)
                and direction
                in {
                    _Direction.RIGHT_DOWN,
                    _Direction.RIGHT_UP,
                    _Direction.LEFT_DOWN,
                    _Direction.LEFT_UP,
                }
            ),
        ]
    ):
        raise ValueError("Word is too long for grid.")

    attempts = 500
    for _ in range(attempts):
        if direction == _Direction.FORWARD:
            start_x = random.randint(0, grid_width - 1 - word_length)
            start_y = random.randint(0, grid_height - 1)
            for i, c in enumerate(word):
                current_char = grid[start_y][start_x + i]
                space_available = current_char == "" or current_char == c
                if not space_available:
                    break
            else:
                for i, c in enumerate(word):
                    grid[start_y][start_x + i] = c
                break

        elif direction == _Direction.REVERSE:
            start_x = random.randint(word_length, grid_width - 1)
            start_y = random.randint(0, grid_height - 1)
            for i, c in enumerate(word):
                current_char = grid[start_y][start_x - i]
                space_available = current_char == "" or current_char == c
                if not space_available:
                    break
            else:
                for i, c in enumerate(word):
                    grid[start_y][start_x - i] = c
                break
        elif direction == _Direction.DOWN:
            start_x = random.randint(0, grid_width - 1)
            start_y = random.randint(0, grid_height - 1 - word_length)
            for i, c in enumerate(word):
                current_char = grid[start_y + i][start_x]
                space_available = current_char == "" or current_char == c
                if not space_available:
                    break
            else:
                for i, c in enumerate(word):
                    grid[start_y + i][start_x] = c
                break
        elif direction == _Direction.UP:
            start_x = random.randint(0, grid_width - 1)
            start_y = random.randint(word_length - 1, grid_height - 1)
            for i, c in enumerate(word):
                current_char = grid[start_y - i][start_x]
                space_available = current_char == "" or current_char == c
                if not space_available:
                    break
            else:
                for i, c in enumerate(word):
                    grid[start_y - i][start_x] = c
                break
        elif direction == _Direction.RIGHT_DOWN:
            start_x = random.randint(0, grid_width - 1 - word_length)
            start_y = random.randint(0, grid_height - 1 - word_length)
            # break
            for i, c in enumerate(word):
                current_char = grid[start_y + i][start_x + i]
                space_available = current_char == "" or current_char == c
                if not space_available:
                    break
            else:
                for i, c in enumerate(word):
                    grid[start_y + i][start_x + i] = c
                break
        elif direction == _Direction.RIGHT_UP:
            start_x = random.randint(0, grid_width - 1 - word_length)
            start_y = random.randint(word_length - 1, grid_height - 1)
            # break
            for i, c in enumerate(word):
                current_char = grid[start_y - i][start_x + i]
                space_available = current_char == "" or current_char == c
                if not space_available:
                    break
            else:
                for i, c in enumerate(word):
                    grid[start_y - i][start_x + i] = c
                break
        elif direction == _Direction.LEFT_DOWN:
            start_x = random.randint(word_length, grid_width - 1)
            start_y = random.randint(0, grid_height - 1 - word_length)
            for i, c in enumerate(word):
                current_char = grid[start_y + i][start_x - i]
                space_available = current_char == "" or current_char == c
                if not space_available:
                    break
            else:
                for i, c in enumerate(word):
                    grid[start_y + i][start_x - i] = c
                break
        elif direction == _Direction.LEFT_UP:
            start_x = random.randint(word_length - 1, grid_width - 1)
            start_y = random.randint(word_length - 1, grid_height - 1)
            for i, c in enumerate(word):
                current_char = grid[start_y - i][start_x - i]
                space_available = current_char == "" or current_char == c
                if not space_available:
                    break
            else:
                for i, c in enumerate(word):
                    grid[start_y - i][start_x - i] = c
                break
    else:
        raise ValueError(
            f"Could not place word in grid after {attempts} attempts ☹. Word: {word}, Direction: {direction}"
        )

    return start_x, start_y


@click.command()
@click.option(
    "--output",
    type=click.Path(exists=False, path_type=pathlib.Path),
    default=_MODULE_DIR / "wordsearch.txt",
    help="Output file name.",
)
@click.option(
    "--word",
    # name="words",
    "words",
    type=str,
    multiple=True,
    help="Word to include in the word search. (repeat for multiple)",
)
@click.option(
    "--wordlist-file",
    type=click.Path(exists=True, path_type=pathlib.Path),
    help="File containing words to include in the word search.",
)
@click.option(
    "--hardness-level",
    type=click.Choice(["easy", "medium", "hard"], case_sensitive=False),
    default="medium",
    help="Hardness level of the word search. Easy has all words left to right; medium adds backwards, down, and right-down; hard adds right-up and left-(up/down). (default: medium)",
)
@click.option(
    "--random-seed",
    type=int,
    help="This is fancy computer speak for 'the staring point of the random numbers'. If you want to be able to reproduce the same word search, use this option. If you don't care, just leave it off (we will print the seed that is chosen so you can recreate later if you want).",
)
@click.option(
    "--height",
    type=int,
    help="Height of the word search. If nothing is provided, will default to longest word + 2",
)
@click.option(
    "--width",
    type=int,
    help="Width of the word search. If nothing is provided, will default to longest word + 2",
)
def main(
    output: typing.Optional[pathlib.Path],
    words: typing.Tuple[str, ...],
    wordlist_file: typing.Optional[pathlib.Path],
    random_seed: typing.Optional[int],
    hardness_level: str,
    height: typing.Optional[int],
    width: typing.Optional[int],
) -> None:
    """Generate word searches."""
    if random_seed is None:
        random_seed = random.randint(0, 2**10 - 1)
    random.seed(random_seed)

    if not words and not wordlist_file:
        raise click.UsageError("Please provide at least one word or a wordlist file.")
    if words and wordlist_file:
        raise click.UsageError(
            "Please provide either words or a wordlist file, not both."
        )

    if wordlist_file:
        with wordlist_file.open("r") as f:
            words = tuple(line.strip() for line in f if line.strip())
    
    numbers_in_wordlist = set()
    for word in words:
        numbers_in_wordlist.update([str(find) for find in re.findall(r"\d", word)])

    if any(" " in word for word in words):
        print("Removing spaces from within words, as that prints funny")
        words = tuple(word.replace(" ", "") for word in words)

    click.echo(f"Using random seed: {random_seed}")

    if not height:
        height = max(len(word) for word in words) + 2
    if not width:
        width = max(len(word) for word in words) + 2

    direction_options = {
        "easy": [_Direction.FORWARD],
        "medium": [
            _Direction.FORWARD,
            _Direction.REVERSE,
            _Direction.DOWN,
            _Direction.RIGHT_DOWN,
        ],
        "hard": list(_Direction),
    }

    grid = _make_grid(width, height)
    word_coords = _fill_in_grid(
        words, hardness_level, height, width, grid, direction_options
    )

    _safe_random_fill(words, height, width, grid, word_coords, numbers_to_include=numbers_in_wordlist)

    pprint.pprint(word_coords)

    # Write the grid to the output file
    with output.open("w") as f:
        _print_grid(grid, file=f)


def _safe_random_fill(words, height, width, grid, coords, numbers_to_include=()):
    """Fill the grid with random letters, avoiding the words already placed."""

    used_coords = set()
    for word, (word_x, word_y, direction) in coords.items():
        if direction == _Direction.FORWARD:
            for i in range(len(word)):
                used_coords.add((word_x + i, word_y))
        elif direction == _Direction.REVERSE:
            for i in range(len(word)):
                used_coords.add((word_x - i, word_y))
        elif direction == _Direction.DOWN:
            for i in range(len(word)):
                used_coords.add((word_x, word_y + i))
        elif direction == _Direction.UP:
            for i in range(len(word)):
                used_coords.add((word_x, word_y - i))
        elif direction == _Direction.RIGHT_DOWN:
            for i in range(len(word)):
                used_coords.add((word_x + i, word_y + i))
        elif direction == _Direction.RIGHT_UP:
            for i in range(len(word)):
                used_coords.add((word_x + i, word_y - i))
        elif direction == _Direction.LEFT_DOWN:
            for i in range(len(word)):
                used_coords.add((word_x - i, word_y + i))
        elif direction == _Direction.LEFT_UP:
            for i in range(len(word)):
                used_coords.add((word_x - i, word_y - i))
        

    answer_key = copy.deepcopy(grid)

    # Fill in the rest of the grid with random letters
    alphabet = string.ascii_uppercase + string.ascii_uppercase + "".join(numbers_to_include)
    for y in range(height):
        for x in range(width):
            if grid[y][x] == "":
                grid[y][x] = random.choice(alphabet)

    if _CHECK_FOR_OTHER_WORDS:
        used_coordinates = set()
        changed_coordinates = set()
        while coords_to_change := _are_other_words_in_grid(
            grid, words, ignored_coords=used_coordinates
        ):
            for x, y in coords_to_change:
                if (x, y) not in used_coords and (x, y) not in changed_coordinates:
                    grid[y][x] = random.choice([o for o in alphabet if o != grid[y][x]])
                    changed_coordinates.add((x, y))
                    break
            else:
                used_coordinates.update(
                    coords_to_change
                )  # they're all used, don't keep checking

    for y in range(height):
        for x in range(width):
            if answer_key[y][x] != "" and answer_key[y][x] != grid[y][x]:
                raise ValueError(f"Ah!!! We changed a letter in the answer key! -> ({x}, {y}) {answer_key[y][x]} -> {grid[y][x]}")
    
    _print_grid(answer_key)

def _are_other_words_in_grid(grid, words, ignored_coords=None):
    """Check if any other words are in the grid."""
    # for each coordinate, check if is start of a word in the trie but not in words
    # if so, return True
    _english_words.load_in_all_words()
    height = len(grid)
    width = len(grid[0])
    for y in range(height):
        for x in range(width):
            if (x, y) in ignored_coords:
                continue

            for direction in list(_Direction):
                word = grid[y][x]
                if direction == _Direction.FORWARD:
                    for i in range(width - x - 1):
                        char = grid[y][x + i + 1]
                        if not (_english_words._ROOT.find_start_of_word(word + char)):
                            break
                        word += char
                        if _is_word_and_not_ok(words, word):
                            print(_Direction.FORWARD, word, x, y)
                            return [(x + i, y) for i in range(len(word))]

                    if _is_word_and_not_ok(words, word):
                        print(_Direction.FORWARD, word, x, y)
                        return [(x + i, y) for i in range(len(word))]
                elif direction == _Direction.REVERSE:
                    for i in range(x, 0, -1):
                        if i - 1 < 0:
                            break
                        char = grid[y][i - 1]
                        if not (_english_words._ROOT.find_start_of_word(word + char)):
                            break
                        word += char

                        if _is_word_and_not_ok(words, word):
                            print(_Direction.REVERSE, word, x, y)
                            return [(x - i, y) for i in range(len(word))]
                    if _is_word_and_not_ok(words, word):
                        print(_Direction.REVERSE, word, x, y)
                        return [(x - i, y) for i in range(len(word))]

                elif direction == _Direction.DOWN:
                    for i in range(height - y - 1):
                        char = grid[y + i + 1][x]
                        if not (_english_words._ROOT.find_start_of_word(word + char)):
                            break
                        word += char

                        if _is_word_and_not_ok(words, word):
                            print(_Direction.DOWN, word, x, y)
                            return [(x, y + i) for i in range(len(word))]
                    if _is_word_and_not_ok(words, word):
                        print(_Direction.DOWN, word, x, y)
                        return [(x, y + i) for i in range(len(word))]
                elif direction == _Direction.UP:
                    for i in range(y, 0, -1):
                        if y - i - 1 < 0:
                            break
                        char = grid[y - i - 1][x]
                        if not (_english_words._ROOT.find_start_of_word(word + char)):
                            break
                        word += char
                        if _is_word_and_not_ok(words, word):
                            print(_Direction.UP, word, x, y)
                            return [(x, y - i) for i in range(len(word))]
                    if _is_word_and_not_ok(words, word):
                        print(_Direction.UP, word, x, y)
                        return [(x, y - i) for i in range(len(word))]
                elif direction == _Direction.RIGHT_DOWN:
                    for i in range(min(width - x - 1, height - y - 1)):
                        char = grid[y + i + 1][x + i + 1]
                        if not (_english_words._ROOT.find_start_of_word(word + char)):
                            break
                        word += char
                        if _is_word_and_not_ok(words, word):
                            print(_Direction.RIGHT_DOWN, word, x, y)
                            return [(x + i, y + i) for i in range(len(word))]
                    if _is_word_and_not_ok(words, word):
                        print(_Direction.RIGHT_DOWN, word, x, y)
                        return [(x + i, y + i) for i in range(len(word))]
                elif direction == _Direction.RIGHT_UP:
                    for i in range(min(width - x - 1, y)):
                        if y - i - 1 < 0:
                            break
                        char = grid[y - i - 1][x + i + 1]
                        if not (_english_words._ROOT.find_start_of_word(word + char)):
                            break
                        word += char
                        if _is_word_and_not_ok(words, word):
                            print(_Direction.RIGHT_UP, word, x, y)
                            return [(x + i, y - i) for i in range(len(word))]

                    if _is_word_and_not_ok(words, word):
                        print(_Direction.RIGHT_UP, word, x, y)
                        return [(x + i, y - i) for i in range(len(word))]
                elif direction == _Direction.LEFT_DOWN:
                    debug_coords = []
                    for i in range(min(x, height - y - 1)):
                        if (x - i - 1) < 0:
                            break
                        coord = (y + i + 1, x - i - 1)
                        debug_coords.append(coord)
                        char = grid[coord[0]][coord[1]]
                        if not (_english_words._ROOT.find_start_of_word(word + char)):
                            break
                        word += char
                        if _is_word_and_not_ok(words, word):
                            print(_Direction.LEFT_DOWN, word, x, y)
                            return [(x - i, y + i) for i in range(len(word))]

                    if _is_word_and_not_ok(words, word):
                        print(_Direction.LEFT_DOWN, word, x, y)
                        return [(x - i, y + i) for i in range(len(word))]
                elif direction == _Direction.LEFT_UP:
                    for i in range(min(x, y)):
                        if (x - i - 1) < 0 or (y - i - 1) < 0:
                            break
                        char = grid[y - i - 1][x - i - 1]
                        if not (_english_words._ROOT.find_start_of_word(word + char)):
                            break
                        word += char
                        if _is_word_and_not_ok(words, word):
                            print(_Direction.LEFT_UP, word, x, y)
                            return [(x - i, y - i) for i in range(len(word))]

                    if _is_word_and_not_ok(words, word):
                        print(_Direction.LEFT_UP, word, x, y)
                        return [(x - i, y - i) for i in range(len(word))]
    return False


def _is_word_and_not_ok(words, word):
    result = (
        _english_words._ROOT.find_word(word)
        and word not in words
        and not any(search_word.upper().startswith(word) for search_word in words)
    )
    return result


def _fill_in_grid(words, hardness_level, height, width, grid, direction_options):
    result = {}
    for word in words:
        direction = random.choice(direction_options[hardness_level])
        result[word] = *_place_word(grid, word.upper(), direction), direction

    return result


if __name__ == "__main__":
    main()
