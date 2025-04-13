import functools
import pathlib

import tqdm


_MODULE_DIR = pathlib.Path(__file__).parent
_OFFENSIVE_WORDS_FILE = _MODULE_DIR / "offensive_words.txt"
_ALL_ENGLISH_WORDS = _MODULE_DIR / "all_english_words.txt"
CHECK_FOR_OTHER_WORDS = _OFFENSIVE_WORDS_FILE.is_file() or _ALL_ENGLISH_WORDS.is_file()

ROOT_CHAR = object()
WORD_END = object()


class WordPointer:
    """A character in a map of words."""

    def __init__(self, char: str):
        self._direct_children = set()
        self.char = char
        self.next = []

    def add_child(self, char: str) -> "WordPointer":
        result = None
        if char not in self._direct_children:
            result = WordPointer(char)
            self._direct_children.add(char)
            self.next.append(result)
            return result
        for child in self.next:
            if child.char == char:
                return child

    def word_finished(self):
        """Mark the end of a word."""
        if WORD_END not in self._direct_children:
            self._direct_children.add(WORD_END)

    def find_word(self, word: str) -> bool:
        """Check if a word is in the trie."""
        current = self
        for c in word.lower():
            if c not in current._direct_children:
                return False
            current = next(child for child in current.next if child.char == c)
        return WORD_END in current._direct_children

    def find_start_of_word(self, word: str) -> bool:
        """Check if a word is in the trie -> does NOT need to have an ending after it."""
        current = self
        for c in word.lower():
            if c not in current._direct_children:
                return False
            current = next(child for child in current.next if child.char == c)
        return True


_ROOT = WordPointer(ROOT_CHAR)


def _load_words_from_file(file: pathlib.Path, minimum_length=1):
    with file.open(encoding="utf-8") as f:
        for line in f:
            word = line.strip()
            if not word or word.startswith("#") or len(word) < minimum_length:
                continue
            current = _ROOT
            for c in word.lower():
                current = current.add_child(c)
            current.word_finished()


@functools.lru_cache(maxsize=1)
def load_in_all_words() -> None:
    """Load all words from the file into the trie."""
    if _ALL_ENGLISH_WORDS:
        print(
            "Loading all words from list of English words, this takes a minute or so..."
        )
        _load_words_from_file(_ALL_ENGLISH_WORDS, minimum_length=2)
    if _OFFENSIVE_WORDS_FILE:
        print("Loading words from list of offensive words...")
        _load_words_from_file(_OFFENSIVE_WORDS_FILE)

    return _ROOT
