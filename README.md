# An Exemplary Workflow using Lexibench and RAxML-NG

The Workflow is based on the data in [Lexibench](https://codeberg.org/lexibank/lexibench). [pylexibench](https://codeberg.org/lexibank/pylexibench) is used to extract character matrices and gold standard trees based on the classification in glottolog. Four different types of character matrices are used as an input for Maximum-Likelihood based Tree Searches with [RAxML-NG](https://github.com/amkozlov/raxml-ng). The inferred trees are compared the the corresponding gold standard trees by means of the Generalized Quartet (GQ) Distance.

1. Preparation 
- Download the executable for [qdist](https://birc.au.dk/software/qdist) and place it in `bin/`
- Download the executable for [RAxML-NG](https://github.com/amkozlov/raxml-ng) and place it in `bin/`
- Download the [Glottolog Repo](https://github.com/glottolog/glottolog)

2. Set up the virtual environment
```
python -m venv venv/
soucre venv/bin/activate
pip install pylexibench
pip install pandas
```
3. Create lexibench data
```
lexibench --repos data/lexibench download --upgrade
lexibench --repos data/lexibench lingpy_wordlists
lexibench --repos data/lexibench character_matrices --formats bin.phy multi.phy bin.catg multi.catg
lexibench --repos data/lexibench glottolog_trees --glottolog <your_path_to_glottlog>

```
4. Execute RAxML-NG tree searches 
```
python tree_searches.py
```
5. Calculate GQ Distances of inferred trees to the gold standard
```
python distances.py
```
