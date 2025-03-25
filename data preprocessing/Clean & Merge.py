from Bio import SeqIO
import numpy as np
import os

# Define input and output file paths
input_files = {
    "HIV_env": ["data/gp120_Kenya.fasta", "data/gp41_Kenya.fasta"],
    "Human_receptors": ["data/CCR5.fasta", "data/CXCR4.fasta"]
}

output_files = {
    "HIV_env": "data/HIV_env_raw.fasta",
    "Human_receptors": "data/Human_receptors_raw.fasta"
}

trimmed_output_files = {
    "HIV_env": "data/HIV_env_trimmed.fasta",
    "Human_receptors": "data/Human_receptors_trimmed.fasta"
}


def merge_fasta(input_list, output_fasta):
    """Merges multiple FASTA files into one."""
    sequences = []
    for file in input_list:
        if os.path.exists(file):
            sequences.extend(list(SeqIO.parse(file, "fasta")))
        else:
            print(f"⚠️ Warning: File not found -> {file}")

    if sequences:
        SeqIO.write(sequences, output_fasta, "fasta")
        print(f"✅ Merged {len(sequences)} sequences into {output_fasta}")
    else:
        print(f"⚠️ No valid sequences found for {output_fasta}")

    return sequences


def compute_qc(sequences, label):
    """Generates a QC report for the dataset."""
    lengths = [len(seq.seq) for seq in sequences]
    min_len = min(lengths) if lengths else 0
    max_len = max(lengths) if lengths else 0
    avg_len = np.mean(lengths) if lengths else 0
    median_len = np.median(lengths) if lengths else 0
    total_seqs = len(lengths)

    print(f"\n📌 QC Report for {label}")
    print(f"📏 Number of Sequences: {total_seqs}")
    print(f"📐 Sequence Lengths: Min = {min_len} bp, Max = {max_len} bp, Avg = {avg_len:.2f} bp, Median = {median_len:.2f} bp")

    return median_len


def trim_sequences(sequences, median_len, output_fasta):
    """Trims sequences to the median length and filters out short ones."""
    trimmed_seqs = [seq for seq in sequences if len(seq.seq) >= median_len * 0.5]
    
    for seq in trimmed_seqs:
        seq.seq = seq.seq[:int(median_len)]  # Trim to median length
    
    SeqIO.write(trimmed_seqs, output_fasta, "fasta")
    print(f"✅ Trimmed {len(trimmed_seqs)} sequences and saved to {output_fasta}")

    return trimmed_seqs


# Run the merging and trimming process
for dataset in input_files:
    merged_sequences = merge_fasta(input_files[dataset], output_files[dataset])
    median_length = compute_qc(merged_sequences, output_files[dataset])
    
    # Trim to median length and filter short sequences
    trimmed_sequences = trim_sequences(merged_sequences, median_length, trimmed_output_files[dataset])

    # Final QC after trimming
    compute_qc(trimmed_sequences, trimmed_output_files[dataset])

print("\n🚀 Data merging and preprocessing complete!\n")
