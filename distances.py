import os
import pandas as pd
from tabulate import tabulate

def gq_dist(tree_name1, prefix):
    tree_name2 = prefix + ".raxml.bestTree"
    if tree_name1 is None or tree_name2 is None:
        return -1
    if tree_name1 != tree_name1 or tree_name2 != tree_name2:
        return -2
    os.system("./bin/qdist " + tree_name1 + " " + tree_name2 + " >out.txt")
    lines = open("out.txt").readlines()
    if len(lines) < 2: #error occurred
        return -3
    res_q = float(lines[1].split("\t")[-3])
    qdist = 1 - res_q
    os.remove("out.txt")
    return qdist


lexibench_repo = "data/lexibench"
results_super_dir = "data/raxmlng"
metadata_df = pd.read_csv(os.path.join(lexibench_repo, "character_matrices/stats.tsv"), sep = "\t")
datasets = metadata_df["Name"]
gq_distances = []

for dataset in datasets:
    row = [dataset]
    results_dir = os.path.join(results_super_dir, dataset)
    glottolog_tree_path = os.path.join(lexibench_repo, "glottolog_trees", dataset + ".tree")
    for t in ["bin", "bin_prob", "multi", "multi_prob"]:
        row.append(gq_dist(glottolog_tree_path, os.path.join(results_dir, t)))
    gq_distances.append(row)
tabulate(gq_distances, tablefmt="pipe", floatfmt=".3f", headers = ["dataset", "bin", "bin_prob", "multi", "multi_prob"])

