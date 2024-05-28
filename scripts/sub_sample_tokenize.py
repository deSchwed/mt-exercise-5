import os
import random
from mosestokenizer import MosesTokenizer

# Paths to the 'data' directory
data_dir = 'data'
file_train_nl = os.path.join(data_dir, 'train.nl')
file_train_de = os.path.join(data_dir, 'train.de')


# Function to read lines from a file
def read_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()


# Function to write lines to a file
def write_lines(file_path, lines):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)


# Function to tokenize a list of lines
def tokenize_lines(lines):
    tokenized_lines = []
    with MosesTokenizer() as tokenizer:
        for line in lines:
            tokenized_lines.append(' '.join(tokenizer(line.strip())) + '\n')
    return tokenized_lines


# Read and subsample from train.en and train.de
lines_train_nl = read_lines(file_train_nl)
lines_train_de = read_lines(file_train_de)

# Check that the files have the same number of lines
assert len(lines_train_nl) == len(
    lines_train_de), "The files must have the same number of lines"

# Randomly select 100,000 line pairs
num_lines = len(lines_train_nl)
num_samples = min(100000, num_lines)
selected_indices = random.sample(range(num_lines), num_samples)

selected_lines_nl = [lines_train_nl[i] for i in selected_indices]
selected_lines_de = [lines_train_de[i] for i in selected_indices]

# Tokenize the selected lines
tokenized_lines_nl = tokenize_lines(selected_lines_nl)
tokenized_lines_de = tokenize_lines(selected_lines_de)

# Write the tokenized selected lines back to the train files
write_lines(file_train_nl, tokenized_lines_nl)
write_lines(file_train_de, tokenized_lines_de)


# Function to tokenize and write back files starting with 'test' and ending with .en or .de
def tokenize_and_write_test_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if (file.startswith('dev') and (file.endswith('.nl') or file.endswith('.de'))):
                file_path = os.path.join(root, file)
                lines = read_lines(file_path)
                tokenized_lines = tokenize_lines(lines)
                write_lines(file_path, tokenized_lines)


# Tokenize and write back test files in the directory
tokenize_and_write_test_files(data_dir)

print("Tokenization complete for 'dev' files. Randomly selected and tokenized 100,000 line pairs for train files.")
