import requests
import os

# UniProt IDs for CCR5 & CXCR4
uniprot_ids = {
    "CCR5": "P51681",
    "CXCR4": "P61073"
}

def download_uniprot_sequence(protein_name, uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    response = requests.get(url)
    
    if response.status_code == 200:
        filename = os.path.join("..", "data", f"{protein_name}.fasta")
        with open(filename, "w") as file:
            file.write(response.text)
        print(f"✅ Downloaded {filename}")
    else:
        print(f"❌ Failed to download {protein_name}")

# Download sequences
for protein, uniprot_id in uniprot_ids.items():
    download_uniprot_sequence(protein, uniprot_id)