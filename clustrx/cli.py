import argparse
from pathlib import Path
from .clustrx import read_pairs, read_fasta, build_clusters, write_clusters

def main():
    parser = argparse.ArgumentParser(
        description="clustRX: cluster similar sequences from BLAST/HMMER outputs and generate FASTA files."
    )
    parser.add_argument("-q", "--queries", required=True, help="File with query IDs")
    parser.add_argument("-t", "--hits", required=True, help="File with target IDs")
    parser.add_argument("-f", "--fasta", required=True, help="FASTA file with all sequences")
    parser.add_argument("--min-cluster-size", type=int, default=1, help="Minimum cluster size to output")
    parser.add_argument("--outdir", default="output", help="Output directory")

    args = parser.parse_args()

    # Read input
    pairs = read_pairs(args.queries, args.hits)
    sequences = read_fasta(args.fasta)

    # Build clusters
    components = build_clusters(pairs, min_size=args.min_cluster_size)

    # Write outputs
    out_clusters = Path(args.outdir) / "clusters"
    out_fastas = Path(args.outdir) / "fasta_files"
    write_clusters(components, sequences, out_clusters, out_fastas)

    print(f"Done. {len(components)} clusters written to {args.outdir}/")