# ─────────────────────────────────────────────
# Mini-Bioinformatics Pipeline: Long-Read QC
# ─────────────────────────────────────────────

SAMPLE = "barcode77"
FASTQ  = f"data/{SAMPLE}.fastq"

rule all:
    input:
        f"results/nanoplot/{SAMPLE}/NanoStats.txt",
        f"results/{SAMPLE}_read_stats.csv",
        "results/plots/summary_statistics.txt",
        "results/plots/gc_content_distribution.png",
        "results/plots/read_length_distribution.png",
        "results/plots/mean_quality_distribution.png",

# ── Step 1: Long-read QC with NanoPlot ──────
rule nanoplot_qc:
    input:
        FASTQ,
    output:
        f"results/nanoplot/{SAMPLE}/NanoStats.txt",
    params:
        outdir = f"results/nanoplot/{SAMPLE}",
    shell:
        "NanoPlot --fastq {input} --outdir {params.outdir} --no_static"

# ── Step 2: Custom per-read statistics ──────
rule read_stats:
    input:
        FASTQ,
    output:
        f"results/{SAMPLE}_read_stats.csv",
    shell:
        "python scripts/read_stats.py -i {input} -o {output}"

# ── Step 3: Visualization & summary stats ───
rule visualize:
    input:
        f"results/{SAMPLE}_read_stats.csv",
    output:
        "results/plots/summary_statistics.txt",
        "results/plots/gc_content_distribution.png",
        "results/plots/read_length_distribution.png",
        "results/plots/mean_quality_distribution.png",
    shell:
        "python scripts/visualize.py -i {input} -o results/plots"
