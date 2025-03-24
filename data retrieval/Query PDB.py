import requests
import os

# List of PDB IDs for gp120, gp41, CCR5, CXCR4
pdb_ids = {
    "gp120": "6MEO",
    "gp41": "1AIK",
    "CCR5": "4MBS",
    "CXCR4": "3ODU"
}

def download_pdb(pdb_id, filename):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open(filename, "w") as file:
            file.write(response.text)
        print(f"✅ Downloaded {filename}")
    else:
        print(f"❌ Failed to download {filename}")

# Download all PDB structures
for protein, pdb_id in pdb_ids.items():
    filename = os.path.join("..", "data", f"{protein}.pdb")
    download_pdb(pdb_id, filename)