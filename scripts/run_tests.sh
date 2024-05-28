#!/bin/bash

scripts=$(dirname "$0")
base=$scripts/..
data=$base/data
configs=$base/configs

# models=$base/models

temp_configs=$base/temp_configs
translations=$base/translations


mkdir -p "$temp_configs"
mkdir -p "$translations"


# Set the model name
model_name="transformer_bpe8000"
# Set the max beam size
max_beam_size=$1

src="nl"
trg="de"

num_threads=16
device=0

# Set file paths to config and temporary config files
config_file="$configs"/"$model_name".yaml
temp_config_file="$temp_configs"/"$model_name".yaml

# Create folder for the output of the model
translations_sub=$translations/$model_name

mkdir -p "$translations_sub"

# Create the CSV file and write the header
csv_file="$translations_sub"/translation_metrics.csv
echo "beam_size,bleu_score,duration" > "$csv_file"

for beam_size in $(seq 1 "$max_beam_size"); do
    # Create a temporary config file with the modified beam_size
    sed "s/beam_size: [0-9]\+/beam_size: $beam_size/" "$config_file" > "$temp_config_file"

    # Start the timer
    start_time=$(date +%s)

    # Generate translations
    CUDA_VISIBLE_DEVICES=$device OMP_NUM_THREADS=$num_threads python -m joeynmt translate "$temp_config_file" < "$data"/test.$src > "$translations_sub"/test"$beam_size".$model_name.$trg

    # Stop the timer
    end_time=$(date +%s)
    
    # Calculate the duration
    duration=$((end_time - start_time))

    echo "Running translation with beam_size=$beam_size took $duration seconds"

    # Detokenize the output
    python "$scripts"/post_processing.py "$translations_sub"/test"$beam_size".$model_name.$trg
    # compute case-sensitive BLEU 
    bleu_output=$(cat "$translations_sub"/test"$beam_size".$model_name.$trg | sacrebleu "$data"/test.$trg)
    bleu_score=$(echo "$bleu_output" | grep -oP '"score": \K[0-9.]+')

    # Append the results to the csv file
    echo "$beam_size,$bleu_score,$duration" >> "$csv_file"
done

# Cleanup temporary files
rm "$temp_config_file"

echo "Completed running tests for beam sizes from 1 to $max_beam_size"
echo "Plotting translation metrics"

python "$scripts"/plot_translation_metrics.py "$model_name"

echo "Finished plotting translation metrics"