import string
from deep_translator import GoogleTranslator
from mod.func import timed
from re import match
from functools import partial


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
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


translate_into_russian = partial(translate, language='ru')


def clear_word(word):
    """
    Function for clearing words

    Clear the word of numbers and punctuation characters at the beginning and end of the word.
    A clean word is a word that's
        - is longer than 3 characters
        - does not contain digits
        - contains only ASCII characters

    :param word: (str) a word from the text
    :return: (str) a clean word
    """
    word = word.strip(string.digits)
    word = word.strip(string.punctuation)

    if len(word) > 3 and word.isalpha() and all(letter in string.ascii_letters for letter in word):
        return word
    else:
        # Exclude None
        return ''


def create_unique_words_set():
    """
    Read a file with text and forms a set of unique words.

    All words are converted to lower case.
    The clear_word() function clears words.

    :return: (set[str]) Set with words
    """
    unique_words = set()
    with open('input.txt', 'r') as infile:
        for line in infile:
            words = line.strip().split()
            # "set comprehensions"
            unique_words.update(clear_word(word.lower()) for word in words)
    return unique_words


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
        outfile.write(f"words count: {str(len(unique_words_set))}\n")
        for word in unique_words_set:
            if len(word) > 3:
                if flag_translate:
                    translated_word = translate_into_russian(word_eng=word)
                    outfile.write(f"{word} - {translated_word} \n")
                else:
                    outfile.write(f"{word} \n")


@timed
def main_without_translate(*args, **kwargs):
    """Saves unique words without translations to a new file"""
    return main_with_translate(*args, flag_translate=False, **kwargs)


if __name__ == "__main__":

    response = input('Do you want to use word translations? [Y/N]:')
    if match("[yYдД]", response):
        main_with_translate()
    else:
        main_without_translate()



