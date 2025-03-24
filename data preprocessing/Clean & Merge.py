from Bio import SeqIO
import os

def merge_and_clean_fasta(input_files, output_file):
    """Merge multiple FASTA files, remove duplicate sequences, and save to a new file."""
    unique_sequences = {}

    for file in input_files:
        with open(file, "r") as handle:
            for record in SeqIO.parse(handle, "fasta"):
                seq_str = str(record.seq).upper()
                if seq_str not in unique_sequences:
                    unique_sequences[seq_str] = record.description

    # Save cleaned sequences
    with open(output_file, "w") as out_handle:
        for seq, desc in unique_sequences.items():
            out_handle.write(f">{desc}\n{seq}\n")

    print(f"✅ Merged and cleaned {len(unique_sequences)} unique sequences into {output_file}")

# Define input files and outputs
data_folder = os.path.join(os.path.dirname(__file__), "..", "data")
hiv_files = [os.path.join(data_folder, "gp120_Kenya.fasta"), os.path.join(data_folder, "gp41_Kenya.fasta")]
human_files = [os.path.join(data_folder, "CCR5.fasta"), os.path.join(data_folder, "CXCR4.fasta")]

merge_and_clean_fasta(hiv_files, os.path.join(data_folder, "HIV_env_clean.fasta"))
merge_and_clean_fasta(human_files, os.path.join(data_folder, "Human_receptors_clean.fasta"))