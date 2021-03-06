from util.experiment import Experiment
from util.data import Data
import traceback
from sklearn.model_selection import ParameterGrid

datasets = ['FB15k', 'WN18', 'WN18RR', 'FB15k-237', 'YAGO3-10', 'UMLS', 'Kinship']
models = ['QMult', 'OMult', 'ConvQ', 'ConvO']
for kg_root in datasets:
    for model_name in models:
        data_dir = 'KGs/' + kg_root + '/'
        config = {
            'num_of_epochs': [2000],  # no tuning
            'batch_size': [1024],  # no tuning.
            'learning_rate': [.001],  # no tuning.
            'label_smoothing': [0.1],  # no tuning.
            'decay_rate': [None],  # no tuning.
            'scoring_technique': ['KvsAll'],  # no tuning.
            'train_plus_valid': [True],
            'num_workers': [32],  # depends on the machine available.
        }
        if model_name in ['ConvQ']:  # Convolutional Quaternion Knowledge Graph Embeddings
            config.update({'embedding_dim': [100],
                           'input_dropout': [.3],
                           'hidden_dropout': [.3],
                           'feature_map_dropout': [.4],
                           'num_of_output_channels': [16],
                           'norm_flag': [False], 'kernel_size': [3]})
        elif model_name in ['ConvO']:  # Convolutional Octonion Knowledge Graph Embeddings
            config.update({'embedding_dim': [50],
                           'input_dropout': [.3],
                           'hidden_dropout': [.3],
                           'feature_map_dropout': [.4],
                           'num_of_output_channels': [16],
                           'norm_flag': [False], 'kernel_size': [3]})
        elif model_name in ['QMult']:  # Quaternion Knowledge Graph Embeddings
            config.update({'embedding_dim': [100],
                           'input_dropout': [.3],
                           'hidden_dropout': [.3], 'norm_flag': [False]})
        elif model_name in ['OMult']:  # Octonion Knowledge Graph Embeddings
            config.update({'embedding_dim': [50],
                           'input_dropout': [.3],
                           'hidden_dropout': [.3], 'norm_flag': [False]})
        else:
            print(model_name)
            raise ValueError

        for th, setting in enumerate(ParameterGrid(config)):
            dataset = Data(data_dir=data_dir, train_plus_valid=setting['train_plus_valid'])
            experiment = Experiment(dataset=dataset,
                                    model=model_name,
                                    parameters=setting, ith_logger='_' + str(th) + '_' + kg_root,
                                    store_emb_dataframe=False)
            try:
                experiment.train_and_eval()
            except RuntimeError as re:
                traceback.print_exc()
                print('Exit.')
                exit(1)
