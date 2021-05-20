"""
======================
Tabular Classification
======================

The following example shows how to fit a sample classification model
with AutoPyTorch
"""
import os
import tempfile as tmp
import warnings

os.environ['JOBLIB_TEMP_FOLDER'] = tmp.gettempdir()
os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'

warnings.simplefilter(action='ignore', category=UserWarning)
warnings.simplefilter(action='ignore', category=FutureWarning)

import sklearn.datasets
import sklearn.model_selection

from autoPyTorch.api.tabular_classification import TabularClassificationTask


if __name__ == '__main__':

    ############################################################################
    # Data Loading
    # ============

    import openml
    import time
    import gc
    ids = {
        'higgs': 23512,
        'poker-hand': 1567,
        'covertype': 1596
    }

    time.sleep(0.3)
    print(f'import module {time.time()}')
    time.sleep(0.3)

    name = list(ids.keys())[2]
    print(name)
    id = ids[name]
    dataset = openml.datasets.get_dataset(id)
    X, y, _, _ = dataset.get_data(target=dataset.default_target_attribute)

    # X, y = sklearn.datasets.fetch_openml(data_id=40981, return_X_y=True, as_frame=True)
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(
        X,
        y,
        random_state=1,
    )

    del X, y
    gc.collect()
    time.sleep(0.3)
    print(f'Complete dataset {time.time()}')
    time.sleep(0.3)

    ############################################################################
    # Build and fit a classifier
    # ==========================
    api = TabularClassificationTask(
        temporary_directory='./tmp/autoPyTorch_example_tmp_01',
        output_directory='./tmp/autoPyTorch_example_out_01',
        # To maintain logs of the run, set the next two as False
        delete_tmp_folder_after_terminate=True,
        delete_output_folder_after_terminate=True
    )

    ############################################################################
    # Search for an ensemble of machine learning algorithms
    # =====================================================
    api.search(
        X_train=X_train,
        y_train=y_train,
        X_test=X_test,
        y_test=y_test,
        optimize_metric='accuracy',
        total_walltime_limit=300,
        func_eval_time_limit_secs=50
    )

    ############################################################################
    # Print the final ensemble performance
    # ====================================
    print(api.run_history, api.trajectory)
    y_pred = api.predict(X_test)
    score = api.score(y_pred, y_test)
    print(score)
    # Print the final ensemble built by AutoPyTorch
    print(api.show_models())
