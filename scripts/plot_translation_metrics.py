import sys
import matplotlib.pyplot as plt
import pandas as pd


def main():
    model_name = sys.argv[1]

    df = pd.read_csv(f'translations/{model_name}/translation_metrics.csv')

    plt.figure(figsize=(14, 6))

    # BLEU Score vs Beam Size
    plt.subplot(1, 2, 1)
    plt.plot(df['beam_size'], df['bleu_score'], marker='o', linestyle='-')
    plt.xlabel('Beam Size')
    plt.ylabel('BLEU Score')
    plt.title('Impact of Beam Size on BLEU Score')
    plt.xticks(df['beam_size'][::2])
    plt.grid(True)

    # Translation Time vs Beam Size
    plt.subplot(1, 2, 2)
    plt.plot(df['beam_size'], df['duration'], marker='o', linestyle='-')
    plt.xlabel('Beam Size')
    plt.ylabel('Translation Time (seconds)')
    plt.title('Impact of Beam Size on Translation Time')
    plt.xticks(df['beam_size'][::2])
    plt.grid(True)

    # Adjust layout and save the plot
    plt.tight_layout()
    plt.savefig(f'translations/{model_name}/metrics_plot.png')
    return


if __name__ == '__main__':
    main()
