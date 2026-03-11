#!/usr/bin/env python3
"""
Generate distribution plots and summary statistics from read_stats CSV output.
Produces:
  - GC content histogram
  - Read length histogram
  - Mean quality histogram
  - Summary statistics printed to stdout and saved to a text file
"""

import argparse
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def load_data(csv_path):
    df = pd.read_csv(csv_path)
    required = {"read_length", "gc_content", "mean_quality"}
    if not required.issubset(df.columns):
        sys.exit(f"CSV missing required columns: {required - set(df.columns)}")
    return df


def summary_statistics(df, output_path):
    """Calculate and save summary statistics for the three metrics."""
    metrics = {
        "Read Length (bp)": df["read_length"],
        "GC Content (%)": df["gc_content"],
        "Mean Quality (Phred)": df["mean_quality"],
    }

    lines = [f"Total reads: {len(df):,}", ""]
    for name, series in metrics.items():
        lines.append(f"--- {name} ---")
        lines.append(f"  Mean:   {series.mean():.2f}")
        lines.append(f"  Median: {series.median():.2f}")
        lines.append(f"  Std:    {series.std():.2f}")
        lines.append(f"  Min:    {series.min():.2f}")
        lines.append(f"  Max:    {series.max():.2f}")
        lines.append(f"  N50:    {compute_n50(series):.0f}" if name == "Read Length (bp)" else "")
        lines.append("")

    text = "\n".join(lines)
    print(text)
    with open(output_path, "w") as f:
        f.write(text + "\n")
    print(f"\nSummary statistics saved to {output_path}")


def compute_n50(lengths):
    """Calculate N50 from a series of read lengths."""
    sorted_lengths = sorted(lengths, reverse=True)
    total = sum(sorted_lengths)
    cumulative = 0
    for length in sorted_lengths:
        cumulative += length
        if cumulative >= total / 2:
            return length
    return 0


def plot_gc_content(df, output_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["gc_content"], bins=50, kde=True, color="steelblue", ax=ax)
    ax.axvline(df["gc_content"].mean(), color="red", linestyle="--", label=f'Mean: {df["gc_content"].mean():.1f}%')
    ax.axvline(df["gc_content"].median(), color="orange", linestyle="--", label=f'Median: {df["gc_content"].median():.1f}%')
    ax.set_xlabel("GC Content (%)")
    ax.set_ylabel("Number of Reads")
    ax.set_title("Distribution of GC Content per Read")
    ax.legend()
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"GC content plot saved to {output_path}")


def plot_read_lengths(df, output_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["read_length"], bins=50, kde=True, color="forestgreen", ax=ax)
    ax.axvline(df["read_length"].mean(), color="red", linestyle="--", label=f'Mean: {df["read_length"].mean():.0f} bp')
    ax.axvline(df["read_length"].median(), color="orange", linestyle="--", label=f'Median: {df["read_length"].median():.0f} bp')
    ax.set_xlabel("Read Length (bp)")
    ax.set_ylabel("Number of Reads")
    ax.set_title("Distribution of Read Lengths")
    ax.legend()
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Read length plot saved to {output_path}")


def plot_mean_quality(df, output_path):
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df["mean_quality"], bins=50, kde=True, color="darkorange", ax=ax)
    ax.axvline(df["mean_quality"].mean(), color="red", linestyle="--", label=f'Mean: {df["mean_quality"].mean():.1f}')
    ax.axvline(df["mean_quality"].median(), color="blue", linestyle="--", label=f'Median: {df["mean_quality"].median():.1f}')
    ax.axvline(7, color="gray", linestyle=":", alpha=0.6, label="Q7 threshold")
    ax.set_xlabel("Mean Phred Quality Score")
    ax.set_ylabel("Number of Reads")
    ax.set_title("Distribution of Mean Read Quality Scores")
    ax.legend()
    plt.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)
    print(f"Quality score plot saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize read statistics")
    parser.add_argument("-i", "--input", required=True, help="Input CSV from read_stats.py")
    parser.add_argument("-o", "--outdir", required=True, help="Output directory for plots")
    args = parser.parse_args()

    import os
    os.makedirs(args.outdir, exist_ok=True)

    df = load_data(args.input)

    summary_statistics(df, os.path.join(args.outdir, "summary_statistics.txt"))
    plot_gc_content(df, os.path.join(args.outdir, "gc_content_distribution.png"))
    plot_read_lengths(df, os.path.join(args.outdir, "read_length_distribution.png"))
    plot_mean_quality(df, os.path.join(args.outdir, "mean_quality_distribution.png"))

    print("\nAll plots and statistics generated successfully.")
