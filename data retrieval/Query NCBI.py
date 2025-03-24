import os
import ssl
import certifi
from Bio import Entrez

# Set email (required by NCBI)
Entrez.email = "johnadams9644@gmail.com"

# Manually set SSL certificate file
os.environ['SSL_CERT_FILE'] = certifi.where()

# Force SSL context to use updated certificates
ssl._create_default_https_context = ssl._create_unverified_context

def fetch_ncbi_sequences(gene_name, organism="HIV-1", location="Kenya", max_results=10):
    """
    Fetches HIV protein sequences from NCBI GenBank for a specific gene/protein in a specific location.
    Saves the results in a FASTA file.

    Args:
        gene_name (str): Name of the gene/protein to search (e.g., "gp120").
        organism (str): Target organism (default: "HIV-1").
        location (str): Location filter (default: "Kenya").
        max_results (int): Number of sequences to retrieve (default: 10).
    """
    search_query = f"{gene_name} AND {organism} AND {location}"
    
    try:
        # Step 1: Search NCBI
        print(f"🔎 Searching for {gene_name} sequences in {location}...")
        handle = Entrez.esearch(db="nucleotide", term=search_query, retmax=max_results)
        record = Entrez.read(handle)
        handle.close()

        # Step 2: Retrieve Sequence IDs
        ids = record["IdList"]
        if not ids:
            print(f"⚠ No results found for {gene_name} in {location}.")
            return
        
        print(f"✅ Found {len(ids)} sequences for {gene_name}. Fetching data...")

        # Step 3: Fetch Sequences
        handle = Entrez.efetch(db="nucleotide", id=ids, rettype="fasta", retmode="text")
        sequences = handle.read()
        handle.close()

        # Step 4: Save to FASTA File
        filename = f"{gene_name}_Kenya.fasta"
        with open(filename, "w") as f:
            f.write(sequences)
        
        print(f"✅ {gene_name} sequences saved to {filename}")

    except Exception as e:
        print(f"❌ Error fetching {gene_name}: {e}")

# Fetch sequences for gp120 and gp41 from Kenya
fetch_ncbi_sequences("gp120")
fetch_ncbi_sequences("gp41")