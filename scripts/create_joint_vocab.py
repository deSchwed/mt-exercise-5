import os
import argparse
from collections import defaultdict


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Create a joint vocabulary from source and target language files.")
    parser.add_argument('--src_lang', type=str, required=True,
                        help="Source language code (e.g., 'en')")
    parser.add_argument('--trg_lang', type=str, required=True,
                        help="Target language code (e.g., 'de')")
    parser.add_argument('--vocab_size', type=int,
                        required=True, help="Vocabulary size")
    return parser.parse_args()


def read_tokens(file_path):
    tokens = set()
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            tokens.update(line.strip().split())
    return tokens


def write_joint_vocab(vocab, vocab_size, output_file):
    sorted_vocab = sorted(vocab)
    with open(output_file, 'w', encoding='utf-8') as f:
        for token in sorted_vocab:
            f.write(f"{token}\n")


print("Joint vocabulary written to 'joint_vocab.txt'.")


def main():
    args = parse_arguments()

    data_dir = 'data'
    shared_models_dir = 'shared_models'
    joint_vocab_file = os.path.join(
        shared_models_dir, f'joint_vocab{args.vocab_size}.txt')

    # File paths for source and target language files
    src_file = os.path.join(data_dir, f'train.BPE.{args.src_lang}')
    trg_file = os.path.join(data_dir, f'train.BPE.{args.trg_lang}')

    # Read tokens
    src_tokens = read_tokens(src_file)
    trg_tokens = read_tokens(trg_file)

    # Combine tokens
    joint_vocab = src_tokens.union(trg_tokens)

    # Write to file
    write_joint_vocab(joint_vocab, args.vocab_size, joint_vocab_file)

    print(f"Joint vocabulary written to '{joint_vocab_file}'.")


if __name__ == '__main__':
    main()
