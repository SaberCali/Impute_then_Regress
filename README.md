# Impute_then_Regress
# Requirements
```
torch     1.12.0
python    3.8
pip       22.1.2
tqdm      4.64.0
pandas    1.4.3
sklearn   0.0
scipy     1.8.1
seaborn   0.11.2
numpy     1.23.1
```
# Acknowledgment
- Code comes from marineLM https://github.com/marineLM
- This is used to directly generate small scale of data and quick plot.
- original github: https://github.com/marineLM/Impute_then_Regress
# Where the code change:
- 1. Easy to change the scale of training data and complexity of MLPs.
```
# Hyperparameter for Training and Test
n_iter = 5
n_jobs = 20
n_sizes = [200, 1e3]
n_sizes = [int(i) for i in n_sizes]
n_test = int(1e3)
n_val = int(1e3)

# Hyperparameter for MLP setting
# You can increasing the length of each hyperparameter to do Grid Search.
# Or just simply use single or double parameters for each hyperparameter 
# to decrease the time of generating data.
mlp_depths = [2]
width_factors = [1, 3]
weight_decays = [1e-5]
learning_rates = [1e-2]
neumann_depths = [20]
epoch = 50
batch_size = 50
```
- 2. No need to generate GRBT.csv, which is not need in the paper results' picture.
```
# scores_GBRT = pd.read_csv(
#     '../results/' + data_type + '_GBRT.csv', index_col=0)
#scores = scores.query('method != "GBRT"')
```
- 3. Logged out the code that made the data empty.
```
# data = data_relative.query(
#     'n == @n and prop_latent == @prop_latent')
data = data_relative
```
# How to use
- Run the lines below to get the ```.csv``` files
> ```python launch_all.py MCAR square``` (bowl)
```python launch_all.py MCAR stairs``` (wave)
```python launch_all.py MCAR discontinuous_linear``` (break)
```python launch_all.py gaussian_sm square``` (bowl)
```python launch_all.py gaussian_sm stairs``` (wave)
```python launch_all.py gaussian_sm discontinuous_linear``` (break)
- Run the lines below to get the plots in Paper:
```python plot_boxplots_neurips2021.py```
