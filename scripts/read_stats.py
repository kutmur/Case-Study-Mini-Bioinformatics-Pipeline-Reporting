#!/usr/bin/env python3
"""
Calculate per-read statistics from a FASTQ file:
  - GC content (%)
  - Read length (bp)
  - Mean Phred quality score
"""

import argparse
import csv
import sys


def phred_score(char):
    """Convert ASCII quality character to Phred score (Phred+33)."""
    return ord(char) - 33


def process_fastq(input_path, output_path):
    """Parse FASTQ and compute per-read stats."""
    with open(input_path, "r") as fq, open(output_path, "w", newline="") as out:
        writer = csv.writer(out)
        writer.writerow(["read_id", "read_length", "gc_content", "mean_quality"])

        while True:
            header = fq.readline().rstrip("\n")
            if not header:
                break
            sequence = fq.readline().rstrip("\n")
            fq.readline()  # + line
            quality = fq.readline().rstrip("\n")

            read_id = header.split()[0].lstrip("@")
            read_len = len(sequence)

            if read_len == 0:
                continue

            gc_count = sequence.upper().count("G") + sequence.upper().count("C")
            gc_pct = round((gc_count / read_len) * 100, 2)

            mean_qual = round(
                sum(phred_score(ch) for ch in quality) / len(quality), 2
            )

            writer.writerow([read_id, read_len, gc_pct, mean_qual])

    print(f"Read statistics saved to {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute per-read FASTQ statistics")
    parser.add_argument("-i", "--input", required=True, help="Input FASTQ file")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file")
    args = parser.parse_args()

    process_fastq(args.input, args.output)
