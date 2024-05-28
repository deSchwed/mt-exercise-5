#! /bin/bash

scripts=$(dirname "$0")
base=$scripts/..

data=$base/data
vocab_dir=$base/shared_models

mkdir -p "$vocab_dir"

vocab_size=8000
lang1="nl"
lang2="de"

# Measure time
SECONDS=0

# Learn the BPE model
subword-nmt learn-joint-bpe-and-vocab --input "$data"/train."$lang1" "$data"/train."$lang2" -s $vocab_size -o "$data"/codes"$vocab_size".bpe --write-vocabulary "$vocab_dir"/vocab."$lang1" "$vocab_dir"/vocab."$lang2" --total-symbols

# Apply bpe with vocab filter
subword-nmt apply-bpe -c "$data"/codes"$vocab_size".bpe --vocabulary "$vocab_dir"/vocab."$lang1" < "$data"/train."$lang1" > "$data"/train.BPE."$lang1"
subword-nmt apply-bpe -c "$data"/codes"$vocab_size".bpe --vocabulary "$vocab_dir"/vocab."$lang2" < "$data"/train."$lang2" > "$data"/train.BPE."$lang2"

# Create the joint vocabulary file
python "$scripts"/create_joint_vocab.py --src_lang nl --trg_lang de --vocab_size "$vocab_size"

echo "time taken:"
echo "$SECONDS seconds"
