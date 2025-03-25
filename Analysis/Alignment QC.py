from Bio import AlignIO
import numpy as np

# Define input files
aligned_files = {
    "HIV_env": "data/HIV_env_aligned.fasta",
    "Human_receptors": "data/Human_receptors_aligned.fasta"
}

# Function to calculate gap percentage
def calculate_gap_percentage(alignment):
    total_positions = alignment.get_alignment_length()
    total_gaps = sum(record.seq.count("-") for record in alignment)
    return (total_gaps / (total_positions * len(alignment))) * 100

# Function to calculate average conservation score (basic)
def calculate_conservation_score(alignment):
    conservation_scores = []
    for i in range(alignment.get_alignment_length()):
        column = [record.seq[i] for record in alignment]
        unique_residues = set(column) - {"-"}
        score = len(unique_residues) / len(column)  # Simplicity: fewer unique = more conserved
        conservation_scores.append(1 - score)  # Closer to 1 means high conservation
    return np.mean(conservation_scores)

# Perform QC on each file
for key, file in aligned_files.items():
    try:
        alignment = AlignIO.read(file, "fasta")
        num_sequences = len(alignment)
        alignment_length = alignment.get_alignment_length()
        gap_percentage = calculate_gap_percentage(alignment)
        conservation_score = calculate_conservation_score(alignment)

        # QC Report
        print(f"\n
