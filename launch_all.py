'''
Defines:
 - the paramaters of data simulations, 
 - the list of methods to compare and their hyperparameters,
And launches all experiments.
'''

import pandas as pd
import argparse
from run_all import run

parser = argparse.ArgumentParser()
parser.add_argument('mdm', help='missing data mechanism',
                    choices=['MCAR', 'MAR', 'gaussian_sm'])
parser.add_argument('link', help='type of link function for the outcome',
                    choices=['linear', 'square', 'stairs','discontinuous_linear'])
print(parser.parse_args())
args = parser.parse_args()
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

if args.link == 'square':
    curvature = 1
elif args.link == 'stairs':
    curvature = 20
else:
    curvature = None

# First fill in data_desc with all default values.
if args.mdm == 'MCAR':
    if args.link:
        filename = 'MCAR_' + args.link
    else:
        filename = 'MCAR'

    default_values = {'n_features': 50, 'missing_rate': 0.5,
                      'prop_latent': 0.3, 'snr': 10, 'masking': 'MCAR',
                      'prop_for_masking': None, 'link': args.link,
                      'curvature': curvature}

    # Define the list of parameters that should be tested and their range of
    # values
    other_values = {'prop_latent': [0.7]}

elif args.mdm == 'gaussian_sm':
    if args.link:
        filename = 'gaussian_sm_' + args.link
    else:
        filename = 'gaussian_sm'

    default_values = {'n_features': 50, 'missing_rate': 0.5,
                      'prop_latent': 0.3, 'sm_type': 'gaussian',
                      'sm_param': 2, 'snr': 10, 'perm': False,
                      'link': args.link, 'curvature': curvature}

    # Define the list of parameters that should be tested and their range of
    # values
    other_values = {'prop_latent': [0.7]}

# Then vary parameters one by one while the other parameters remain constant,
# and equal to their default values.
data_descs = [pd.DataFrame([default_values])]
for param, vals in other_values.items():
    n = len(vals)
    data = pd.DataFrame([default_values]*n)
    data.loc[:, param] = vals
    data_descs.append(data)
data_descs = pd.concat(data_descs, axis=0)


# Define the methods that will be compared
methods_params = []

methods_params.append({'method': 'BayesPredictor', 'order0': False})
methods_params.append({'method': 'BayesPredictor_order0', 'order0': True})

for max_leaf_nodes in [50, 100, 200]:
    for max_iter in [100]:
        for min_samples_leaf in [10, 20]:
            methods_params.append({'method': 'GBRT',
                                   'n_iter_no_change': 10,
                                   'max_leaf_nodes': max_leaf_nodes,
                                   'max_iter': max_iter,
                                   'min_samples_leaf': min_samples_leaf
                                   })


for add_mask in [True, False]:
    for mlp_d in mlp_depths:
        for wf in width_factors:
            for wd in weight_decays:
                for lr in learning_rates:
                    if add_mask:
                        name = 'oracleMLPPytorch_mask'
                    else:
                        name = 'oracleMLPPytorch'
                    methods_params.append({'method': name,
                                           'add_mask': add_mask,
                                           'mdm': args.mdm,
                                           'n_epochs': epoch,
                                           'batch_size': batch_size,
                                           'lr': lr,
                                           'weight_decay': wd,
                                           'early_stopping': True,
                                           'optimizer': 'adam',
                                           'width_factor': wf,
                                           'mlp_depth': mlp_d,
                                           'init_type': 'uniform',
                                           'verbose': False})


for add_mask in [True, False]:
    for imp_type in ['mean', 'MICE']:
        for mlp_d in mlp_depths:
            for wf in width_factors:
                for wd in weight_decays:
                    for lr in learning_rates:
                        if add_mask:
                            name = imp_type + 'MLPPytorch_mask'
                        else:
                            name = imp_type + 'MLPPytorch'
                        methods_params.append({'method': name,
                                               'add_mask': add_mask,
                                               'imputation_type': imp_type,
                                               'n_epochs': epoch,
                                               'batch_size': batch_size,
                                               'lr': lr,
                                               'weight_decay': wd,
                                               'early_stopping': True,
                                               'optimizer': 'adam',
                                               'mlp_depth': mlp_d,
                                               'width_factor': wf,
                                               'init_type': 'uniform',
                                               'verbose': False})


for init in ['uniform']:
    name = 'NeuMiss_' + init + '_'
    for mlp_d in mlp_depths:
        for wf in width_factors:
            for d in neumann_depths:
                for wd in weight_decays:
                    for lr in learning_rates:
                        methods_params.append({'method': name,
                                               'mode': 'shared',
                                               'depth': d,
                                               'n_epochs': epoch,
                                               'batch_size': batch_size,
                                               'lr': lr,
                                               'weight_decay': wd,
                                               'early_stopping': True,
                                               'optimizer': 'adam',
                                               'residual_connection': True,
                                               'mlp_depth': mlp_d,
                                               'width_factor': wf,
                                               'init_type': init,
                                               'add_mask': False,
                                               'verbose': False})


run_params = {
        'n_iter': n_iter,
        'n_sizes': n_sizes,
        'n_test': n_test,
        'n_val': n_val,
        'mdm': args.mdm,
        'data_descs': data_descs,
        'methods_params': methods_params,
        'filename': filename,
        'n_jobs': n_jobs}

run(**run_params)
