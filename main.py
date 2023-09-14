from deep_translator import GoogleTranslator
from mod.func import timed
from re import match


def translate_to_russian(word_eng: str) -> str:
    """
    Translation of a word from English to Russian

    :param word_eng: English word
    :return: Russian word
    """
    translated = GoogleTranslator(source='auto', target='ru').translate(word_eng)
    return translated


def clear_word(word: str) -> str:
    """
    Function for clearing words

    We exclude words that:
    - are shorter than 3 characters
    - contain abbreviations in the form of apostrophes
    - contain code signs (), _, etc.
    - do not contain numbers

    :return: Purified Word
    """
    word = word.strip(',.()_!?')

    if len(word) > 3 and word.isalpha() and all(
            ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' for ch in word) and all(
            ch not in word for ch in ["'", '’', '(', ')', '_', '.']):
        return word
    else:
        # Exclude None
        return ''


def create_unique_words_set() -> set[str]:
    """
    Reads a file with text and forms a set of unique words.
    All words are converted to lower case.
    The clear_word() function clears words.

    :return: Set with words
    """
    unique_words = set()
    with open('input.txt', 'r') as infile:
        for line in infile:
            words = line.strip().split()
            # "set comprehensions"
            unique_words.update(clear_word(word.lower()) for word in words)
    return unique_words


def write_words_to_file(flag_translate: bool, unique_words_set: set) -> None:
    """
    Creating a file with unique words

    :param flag_translate: To use translation or not
    :param unique_words_set: Set with words
    :return: None
    """
    # Recording unique words and their translations(or not) into a new file
    with open('output.txt', 'w') as outfile:
        outfile.write('words count: ' + str(len(unique_words_set)) + '\n')
        for word in unique_words_set:
            if len(word) > 3:
                if flag_translate:
                    translated_word = translate_to_russian(word)
                    # print(f"{word} - {translated_word}\n")
                    outfile.write(f"{word} - {translated_word}\n")
                else:
                    outfile.write(f"{word} \n")


@timed
def main_with_translate() -> None:
    """
    Reading the source file and creating a list of unique words with translation.

    :return: None
    """
    write_words_to_file(True, create_unique_words_set())


@timed
def main_without_translate() -> None:
    """
    Reading the source file and creating a list of unique words without translation.

    :return: None
    """
    write_words_to_file(False, create_unique_words_set())


if __name__ == "__main__":

    response = input('Do you want to use word translations? [Y/N]:')
    if match("[yYдД]", response):
        main_with_translate()
    else:
        main_without_translate()



