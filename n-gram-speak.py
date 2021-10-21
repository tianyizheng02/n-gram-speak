from os.path import isfile
from random import choice
from textwrap import wrap

from nltk import ConditionalFreqDist, ngrams


def build_ngrams(file: str, n: int) -> zip:
    with open(file) as f:
        text = f.read()
    return ngrams(text.split(), n)


def build_cfd(ngrams: zip) -> ConditionalFreqDist:
    return ConditionalFreqDist([(ngram[:-1], ngram[-1]) for ngram in ngrams])


def generate(cfd: ConditionalFreqDist, words: list[str], length: int) \
        -> list[str]:
    speak = words.copy()
    for i in range(length - len(words)):
        fd = cfd[tuple(words)]
        if len(fd) == 0:
            print('Ran out of selections. Stopping generation early...\n')
            return speak
        selection = choice(fd.most_common(20))[0]
        words.append(selection)
        words.pop(0)
        speak.append(selection)
    return speak


def get_file() -> str:
    while True:
        file = input('Enter a file name, or enter "q" to quit: ').lower()
        if file == 'q' or isfile(file):
            return file
        print('File not found.')


def get_n() -> int:
    while True:
        n = input('Enter an n-gram size: ')
        if not n.isnumeric():
            print('Size must be a positive integer.')
        elif int(n) < 2:
            print('N-gram size must be greater than 1.')
        else:
            return int(n)


def get_starting_words(cfd: ConditionalFreqDist, num: int) -> list[str]:
    while True:
        start = input(f'Enter {num} starting '
                      f'{"words" if num > 1 else "word"}: ').split()
        if len(start) != num:
            print('Wrong number of starting words.')
        elif tuple(start) not in cfd:
            print('Your starting words were not found in the text.')
        else:
            return start


def get_length(n: int) -> int:
    while True:
        length = input('Enter the length of text to be generated: ')
        if not length.isnumeric():
            print('Length must be a positive integer.')
        elif int(length) < n:
            print(f'Length must be greater than {n - 1}.')
        else:
            return int(length)


def run() -> None:
    print('Welcome to N-Gram Speak!\n')
    while True:
        file_name = get_file()
        if file_name == 'q':
            return
        print()

        n = get_n()
        print('\nGenerating n-grams...\n')
        file_cfd = build_cfd(build_ngrams(file_name, n))

        while True:
            start = get_starting_words(file_cfd, n - 1)
            print()

            length = get_length(n)
            print()

            generated = generate(file_cfd, start, length)
            print('Generated Text:')
            print('\n'.join(wrap(' '.join(generated), 80)))
            print()

            if input('Would you like to try again? (y/n) ').lower() != 'y':
                break
            print()
        print()


if __name__ == '__main__':
    run()
