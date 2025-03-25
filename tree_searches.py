import os
import pandas as pd


def run_inference(msa_path, model, prefix, args = ""):
    if os.path.isfile(prefix + ".raxml.bestTree"):
        return
    if not os.path.isfile(msa_path):
        print("MSA " + msa_path + " does not exist")
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
metadata_df = pd.read_csv(os.path.join(lexibench_repo, "character_matrices/stats.tsv"), sep = "\t")
datasets = metadata_df["Name"]

for dataset in datasets:
    msa_dir = os.path.join(lexibench_repo, "character_matrices", dataset)
    results_dir = os.path.join(results_super_dir, dataset)
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    run_inference(os.path.join(msa_dir, "bin.phy"), "BIN+G", os.path.join(results_dir, "bin"))
    run_inference(os.path.join(msa_dir, "bin.catg"), "BIN+G", os.path.join(results_dir, "bin_prob"), "--prob-msa on")
    x = list(metadata_df[metadata_df["Name"] == dataset]["cs_max"])[0]
    run_inference(os.path.join(msa_dir, "multi.phy"), "MULTI" + str(x) + "_MK+G", os.path.join(results_dir, "multi"))
    run_inference(os.path.join(msa_dir, "multi.catg"), "MULTI" + str(x) + "_MK+G", os.path.join(results_dir, "multi_prob"), "--prob-msa on")

