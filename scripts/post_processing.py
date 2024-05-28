import sys
from mosestokenizer import MosesDetokenizer


def main():
    if not sys.argv[1]:
        raise ValueError("No File path provided")

    translation_file = sys.argv[1]

    detokenized_lines = []

    # Open the translations
    with open(translation_file, 'r', encoding='utf-8') as input_f:
        tokenized_lines = input_f.readlines()

    # Detokenize
    with MosesDetokenizer() as detokenize:
        for line in tokenized_lines:
            detokenized_lines.append(detokenize(
                line.rstrip('\n').split()) + '\n')

    # Write back to file
    with open(translation_file, 'w', encoding='utf-8') as output_f:
        output_f.writelines(detokenized_lines)


if __name__ == '__main__':
    main()
