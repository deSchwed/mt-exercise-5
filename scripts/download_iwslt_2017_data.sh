#! /bin/bash

scripts=$(dirname "$0")
base=$scripts/..

data=$base/data

# download preprocessed data

wget https://files.ifi.uzh.ch/cl/archiv/2020/mt20/data.ex5.tar.gz -P "$base"
tar -xzvf "$base"/data.ex5.tar.gz

rm "$base"/data.ex5.tar.gz


# set langauge pair
language_pair="nl-de"
# Remove files that don't contain the language pair
find "$data" -type f ! -name "*$language_pair*" -exec rm -f {} +

# Rename remaining files by removing the language pair from the filename
for file in "$data"/*"$language_pair"*; do
  mv "$file" "${file%"$language_pair"*}${file##*.}"
done


# sizes
echo "Sizes of data files:"
wc -l "$data"/*

# sanity checks
echo "At this point, please make sure that 1) number of lines are as expected, 2) language suffixes are correct and 3) files are parallel"
