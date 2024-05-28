# MT Exercise 5: Byte Pair Encoding, Beam Search

## Changes
- Changed `download_iwslt_2017_data.sh`. After downloading the data, it will also delete files and rename the remaining ones, given a language-pair.
- Changed `train.sh`. Only syntax changes.
- Changed `training.py` from joeynmt to allow for GPU usage.
- Changed `evaluate.sh` to use 16 CPU threads, and to use the `post_processing.py` script to detokenize the output.

## Additions
- Added `sub_sample_tokenize.py`. This script will tokenize the dev and train sets and randomly sub-sample 100k sentence pairs from the training data.
- Added `create_joint_vocab.py`. This script will join the vocabularies of the source and target languages, after a bpe model has been trained.
- Added `learn_bpe.sh`. This script will train a BPE model on the sub-sampled training data, and create a joint vocabulary. The number of operations must be set in the script.
- Added `post_processing.py`. This script will detokenize the output of the model.
- Added `run_tests.sh`. This script will create a temporary config file with increasing beam sizes, generate translations, and calculate the BLEU score for each beam size.
- Added `plot_translation_metrics.py`. This script will plot the BLEU scores and computation times for each beam size. It will run automatically at the end of `run_tests.sh`.

## Instructions
Before running the modified `download_iwslt_2017_data.sh` or `learn_bpe.sh` scripts, make sure to give them executable permission. This can be done by running `chmod +x {script_name}`.
After the given setup procedure, we have to install an additional package, `pip install mosestokenizer`. This package is used in the `sub_sample_tokenize.py` script.

To train a model, first run the `sub_sample_tokenize.py` script. Then, depending on if the model is bpe-level, run the `learn_bpe.sh` script to train a BPE model and create a joint vocabulary. Finally, set the model name and run the `train.sh` script to train a model.
After training, you can run the `run_tests.sh` script to the test the model with different beam sizes. You have to give a maximum beam size as an argument to the script.


## Results
Blue Scores (I just used greedy decoding for the first part):

|| use BPE | vocabulary size | BLEU |
|---|---|---|---|
| a | no | 2000 | 4.6 |
| b | yes | 2000 | 12.0 |
| c | yes | 8000 | 12.4 |


When looking at the graphs, there seems to be a sweet spot for the beam size around 8-12. After that, the BLEU score does not increase significantly, but the computation time increases by a lot. The best beam size for this model particularly seems to be 9.