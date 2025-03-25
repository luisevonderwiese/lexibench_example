import os
import pandas as pd
from tabulate import tabulate

def gq_dist(tree_name1, prefix):
    tree_name2 = prefix + ".raxml.bestTree"
    if not os.path.isfile(tree_name1) or not os.path.isfile(tree_name2):
        return float("nan")
    os.system("./bin/qdist " + tree_name1 + " " + tree_name2 + " >out.txt")
    lines = open("out.txt").readlines()
    if len(lines) < 2: #error occurred
        #print(lines)
        return float("nan") 
    res_q = float(lines[1].split("\t")[-3])
    qdist = 1 - res_q
    os.remove("out.txt")
    #if qdist != qdist:
       # print(lines)
    return qdist


lexibench_repo = "data/lexibench"
results_super_dir = "data/raxmlng"
metadata_df = pd.read_csv(os.path.join(lexibench_repo, "character_matrices/stats.tsv"), sep = "\t")
datasets = metadata_df["Name"]
gq_distances = []
matrix_types = ["bin", "bin_prob", "multi", "multi_prob"]

for dataset in datasets:
    row = [dataset]
    print(dataset)
    results_dir = os.path.join(results_super_dir, dataset)
    glottolog_tree_path = os.path.join(lexibench_repo, "glottolog_trees", dataset + ".tree")
    for t in matrix_types:
        row.append(gq_dist(glottolog_tree_path, os.path.join(results_dir, t)))
    gq_distances.append(row)
headers = ["dataset"] + matrix_types
print(tabulate(gq_distances, tablefmt="pipe", floatfmt=".3f", headers = headers))
with open("data/distances.tsv", "w+", encoding="utf-8") as outfile:
    outfile.write(tabulate(gq_distances, tablefmt="tsv", floatfmt=".3f", headers = headers))
with open("data/distances.md", "w+", encoding="utf-8") as outfile:
    outfile.write(tabulate(gq_distances, tablefmt="github", floatfmt=".3f", headers = headers))


