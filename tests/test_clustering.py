import os
from pathlib import Path
import subprocess

def write_file(path, content):
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

def test_redundant_clusters(tmp_path):
    # Input files with redundancy
    queries = tmp_path / "queries.txt"
    hits = tmp_path / "hits.txt"
    fasta = tmp_path / "sequences.fasta"

    write_file(queries, "A\nC\nE")
    write_file(hits, "B\nD\nB")
    write_file(fasta, """>A
AAAAAA
>B
BBBBBB
>C
CCCCCC
>D
DDDDDD
>E
EEEEEE""")

    outdir = tmp_path / "results"
    os.makedirs(outdir, exist_ok=True)

    # Run the clustering script
    cmd = [
        "python",
        "../clustRX.py",
        "-q", str(queries),
        "-t", str(hits),
        "-f", str(fasta),
        "--min-cluster-size", "2",
        "--outdir", str(outdir)
    ]
    subprocess.run(cmd, check=True)

    # Check output directories
    clusters_dir = outdir / "clusters"
    fastas_dir = outdir / "fasta_files"
    assert clusters_dir.exists()
    assert fastas_dir.exists()

    # Two clusters expected
    txt_files = sorted(list(clusters_dir.glob("*.txt")))
    fasta_files = sorted(list(fastas_dir.glob("*.fasta")))
    assert len(txt_files) == 2
    assert len(fasta_files) == 2

    # Check that cluster 1 contains A, B, E
    with open(fasta_files[0]) as f:
        content = f.read()
        assert all(x in content for x in ["A", "B", "E"]) or all(x in content for x in ["C", "D"])


if __name__ == "__main__":

    tmp_path = Path("../temp")
    test_redundant_clusters(tmp_path)