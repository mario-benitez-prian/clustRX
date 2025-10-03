import argparse
from pathlib import Path
from .clustrx import read_pairs, read_fasta, build_clusters, write_clusters

def main():
    parser = argparse.ArgumentParser(
        description=(
        "clustRX: Cluster sequences from BLAST/HMMER outputs and generate FASTA groups.\n\n"
        "Author: Mario Benítez-Prián | Please cite clustRX if used in your research.\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-q", "--queries", required=True, help="File with query IDs")
    parser.add_argument("-hi", "--hits", required=True, help="File with hit IDs")
    parser.add_argument("-f", "--fasta", required=True, help="FASTA file with all sequences")
    parser.add_argument("-min", "--min-cluster-size", type=int, default=2, help="Minimum cluster size to output (default=2). Note: clusters are built from pairs, so the minimum possible size is 2.")
    parser.add_argument("--outdir", default="clustrx_output", help="Output directory")

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