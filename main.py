import string

from functools import partial, wraps
from re import match
from time import perf_counter
from deep_translator import GoogleTranslator


def timed(func):
    """
    (ru) Функция декоратор, которая при вызове декорируемой функции измеряет время ее выполнения
    (en) Decorator which measures the execution time of the wrapped function
    """
    @wraps(func)
    def wrap(*args, **kwargs):
        t1 = perf_counter()
        result = func(*args, **kwargs)
        t2 = perf_counter()
        print(f"Calling {func.__name__} took {t2-t1} second, ", end="")
        print(f"(with parameters {args}, {kwargs})")
        return result
    return wrap


def translate(word_eng, language):
    """
    Translate a word from English to the target language

    :param language: (str) Target language e.g. "ru" for Russian
    :param word_eng: (str) English word
    :return: (str) Translated word
    """
    try:
        if word_eng is None:
            raise ValueError("The word to translate cannot be None")
        translated = GoogleTranslator(source='auto', target=language).translate(word_eng)
        return translated
    except ValueError as ve:
        print(f"An error occurred: {ve}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return


translate_into_russian = partial(translate, language='ru')


def clear_word(word):
    """
    Clear the word of numbers and punctuation characters at the beginning and end of the word.

    A clean word:
      - is longer than 3 characters
      - does not contain digits
      - contains only ASCII characters

    :param word: (str) a word from the text
    :return: (str) a clean word
    """
    word = word.strip(string.digits).strip(string.punctuation)
    if all([
        len(word) > 3,
        word.isalpha(),
        all(letter in string.ascii_letters for letter in word)
    ]):
        return word


def create_unique_words_set():
    """
    Load a text file and create a set of unique words.

    Convert all words to lower case.
    Clear words with clear_word().

    :return: (set[str]) Set with words
    """
    unique_words = set()
    with open('input.txt', 'r') as infile:
        for line in infile:
            unique_words.update(
                clear_word(word.lower()) for word in line.strip().split()
            )
    return {word for word in unique_words if word}


@timed
def main_with_translate(flag_translate=True, unique_words_set=None):
    """
    Save unique words and (optionally) their translations to a new file

    :param flag_translate: (bool) use translation if True
    :param unique_words_set: (set) unique words
    :return: None
    """
    if unique_words_set is None:
        unique_words_set = create_unique_words_set()
    with open('output.txt', 'w') as outfile:
        outfile.write(f"Word count: {str(len(unique_words_set))}\n")
        for word in unique_words_set:
            if len(word) > 3:
                if flag_translate:
                    translated_word = translate_into_russian(word_eng=word)
                    outfile.write(f"{word} - {translated_word}\n")
                else:
                    outfile.write(f"{word}\n")


def main_without_translate(unique_words_set=None):
    """Save unique words without translations to a new file"""
    return main_with_translate(
        flag_translate=False,
        unique_words_set=unique_words_set
    )


if __name__ == "__main__":
    response = input('Do you want to use word translations? [Y/N]: ')
    if match("[yYдД]", response):
        main_with_translate()
    else:
        main_without_translate()
