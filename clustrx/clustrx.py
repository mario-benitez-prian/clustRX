import os
import networkx as nx
from pathlib import Path

def read_pairs(file1, file2):
    """Read two files line by line and return pairs of IDs."""
    pairs = []
    with open(file1) as f1, open(file2) as f2:
        for id1, id2 in zip(f1, f2):
            pairs.append((id1.strip(), id2.strip()))
    return pairs

def read_fasta(fasta_file):
    """Read a FASTA file into a dictionary {id: sequence}."""
    sequences = {}
    with open(fasta_file) as f:
        seq_id = None
        seq_lines = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq_id:
                    sequences[seq_id] = "".join(seq_lines)
                seq_id = line[1:].split()[0]  # take first token as ID
                seq_lines = []
            else:
                seq_lines.append(line)
        if seq_id:
            sequences[seq_id] = "".join(seq_lines)
    return sequences

def build_clusters(pairs, min_size=1):
    """Build a graph from pairs and return connected components ≥ min_size."""
    G = nx.Graph()
    G.add_edges_from(pairs)
    components = [
        sorted(comp) for comp in nx.connected_components(G) if len(comp) >= min_size
    ]
    return components

def write_clusters(components, sequences, outdir_clusters, outdir_fastas):
    """Write cluster ID lists and FASTA files for each cluster."""
    os.makedirs(outdir_clusters, exist_ok=True)
    os.makedirs(outdir_fastas, exist_ok=True)

    for i, comp in enumerate(components, start=1):
        # Write list of IDs
        cluster_file = Path(outdir_clusters) / f"cluster_{i}.txt"
        with open(cluster_file, "w") as cf:
            cf.write("\n".join(comp) + "\n")

        # Write sequences in FASTA
        fasta_file = Path(outdir_fastas) / f"cluster_{i}.fasta"
        with open(fasta_file, "w") as ff:
            for seq_id in comp:
                seq = sequences.get(seq_id, None)
                if seq:
                    ff.write(f">{seq_id}\n{seq}\n")
                else:
                    ff.write(f">{seq_id}\nSequence_not_found\n")
                    print(f"Warning: sequence {seq_id} not found in FASTA.")
