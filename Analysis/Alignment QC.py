from Bio import AlignIO
import numpy as np
import os

# Define input aligned files
aligned_files = {
    "HIV_env": "data/HIV_env_aligned.fasta",
    "Human_receptors": "data/Human_receptors_aligned.fasta"
}

def calculate_gap_percentage(alignment):
    """Calculate the percentage of gaps ('-') in an alignment."""
    total_positions = alignment.get_alignment_length() * len(alignment)
    gap_count = sum(record.seq.count('-') for record in alignment)
    return (gap_count / total_positions) * 100

def compute_conservation_score(alignment):
    """Estimate sequence conservation using simple frequency-based scoring."""
    alignment_length = alignment.get_alignment_length()
    consensus_score = []

    for i in range(alignment_length):
        column = [record.seq[i] for record in alignment]
        most_common = max(set(column), key=column.count)
        score = column.count(most_common) / len(column)
        consensus_score.append(score)

    return np.mean(consensus_score)

def qc_report(filepath):
    """Run QC on an alignment file."""
    if os.path.exists(filepath):
        alignment = AlignIO.read(filepath, "fasta")
        num_sequences = len(alignment)
        alignment_length = alignment.get_alignment_length()
        gap_percentage = calculate_gap_percentage(alignment)
        conservation_score = compute_conservation_score(alignment)

        print(f"\n📌 QC Report for {filepath}")
        print(f"📏 Number of Sequences: {num_sequences}")
        print(f"📐 Alignment Length: {alignment_length} bp")
        print(f"⚠️ Gap Percentage: {gap_percentage:.2f}%")
        print(f"🧬 Average Conservation Score: {conservation_score:.2f}")
        print("✅ QC Completed.\n")
    else:
        print(f"⚠️ File not found: {filepath} (Skipping...)")

# Run QC for each aligned file
for key in aligned_files:
    qc_report(aligned_files[key])

print("🚀 QC analysis complete!")
