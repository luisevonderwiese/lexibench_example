import os
import pandas as pd


def run_inference(msa_path, model, prefix, args = ""):
    if os.path.isfile(prefix + ".raxml.bestTree"):
        return
    if msa_path != msa_path:
        print("MSA does not exist")
        return
    command = "./bin/raxml-ng"
    command += " --msa " + msa_path
    command += " --model " + model
    command += " --prefix " + prefix
    command += " --threads auto --seed 2"
    command += " " + args
    os.system(command)

lexibench_repo = "data/lexibench"
results_super_dir = "data/raxmlng"
metadata_df = pd.read_csv(os.path.join(lexibench_repo, "character_matrices_compatible/stats.tsv"), sep = "\t")
wl_df = pd.read_csv("data/lexibench/lingpy_wordlists/stats.tsv", sep = "\t")
metadata_df = metadata_df.merge(wl_df, on = "Name")

for i, row in metadata_df.iterrows():
    if row["Languages"] <= 4: #GQ distances not defined
        continue
    dataset = row["Name"]
    print(dataset)
    results_dir = os.path.join(results_super_dir, dataset)
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    print("bin.phy")
    run_inference(row["bin.phy"], "BIN+G", os.path.join(results_dir, "bin"))
    print("bin.catg")
    run_inference(row["bin.catg"], "BIN+G", os.path.join(results_dir, "bin_prob"), "--prob-msa on")
    x = row["cs_max"]
    print("multi.phy")
    run_inference(row["multi.phy"], "MULTI" + str(x) + "_MK+G", os.path.join(results_dir, "multi"))
    print("multi.catg")
    run_inference(row["multi.catg"], "MULTI" + str(x) + "_MK+G", os.path.join(results_dir, "multi_prob"), "--prob-msa on")

