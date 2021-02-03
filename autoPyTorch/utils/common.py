import hashlib
from typing import Any, Dict, Iterable, List, NamedTuple, Optional, Type, Union

import numpy as np

import pandas as pd

import scipy.sparse

import torch
from torch.utils.data.dataloader import default_collate
from typing import NamedTuple


class ConstantKeys:
    # to avoid typo
    NUM_SPLITS, VAL_SHARE = 'num_splits', 'val_share'
    STRATIFY, STRATIFIED = 'stratify', 'stratified'


class BaseNamedTuple():
    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            raise AttributeError(f"DatasetProperties does not have the attribute name {key}")

    def keys(self):
        return self._asdict().keys()
    
    def values(self):
        return self._asdict().values()

    def items(self):
        return self._asdict().items()
    
    def _asdict(self):
        raise NotImplementedError


class FitRequirement(NamedTuple):
    """
    A class that holds inputs required to fit a pipeline. Also indicates wether
    requirements have to be user specified or are generated by the pipeline itself.

    Attributes:
    name: The name of the variable expected in the input dictionary
    supported_types: An iterable of all types that are supported
    user_defined: If false, this requirement does not have to be given to the pipeline
    """

    name: str
    supported_types: Iterable[Type]
    user_defined: bool
    dataset_property: bool

    def __str__(self) -> str:
        """
        String representation for the requirements
        """
        return "Name: %s | Supported types: %s | User defined: %s | Dataset property: %s" % (
            self.name, self.supported_types, self.user_defined, self.dataset_property)


def replace_prefix_in_config_dict(config: Dict[str, Any], prefix: str, replace: str = "") -> Dict[str, Any]:
    """
    Replace the prefix in all keys with the specified replacement string (the empty string by
    default to remove the prefix from the key). The functions makes sure that the prefix is a proper config
    prefix by checking if it ends with ":", if not it appends ":" to the prefix.

    :param config: config dictionary where the prefixed of the keys should be replaced
    :param prefix: prefix to be replaced in each key
    :param replace: the string to replace the prefix with
    :return: updated config dictionary
    """
    # make sure that prefix ends with the config separator ":"
    if not prefix.endswith(":"):
        prefix = prefix + ":"
    # only replace first occurrence of the prefix
    return {k.replace(prefix, replace, 1): v
            for k, v in config.items() if
            k.startswith(prefix)}


def custom_collate_fn(batch: List) -> List[Optional[torch.tensor]]:
    """
    In the case of not providing a y tensor, in a
    dataset of form {X, y}, y would be None.

    This custom collate function allows to yield
    None data for functions that require only features,
    like predict.

    Args:
        batch (List): a batch from a dataset

    Returns:
        List[Optional[torch.Tensor]]
    """

    items = list(zip(*batch))

    # The feature will always be available
    items[0] = default_collate(items[0])
    if None in items[1]:
        items[1] = list(items[1])
    else:
        items[1] = default_collate(items[1])
    return items


def replace_string_bool_to_bool(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Utility function to replace string-type bool to
    bool when a dict is read from json

    Args:
        dictionary (Dict[str, Any])
    Returns:
        Dict[str, Any]
    """
    for key, item in dictionary.items():
        if isinstance(item, str):
            if item.lower() == "true":
                dictionary[key] = True
            elif item.lower() == "false":
                dictionary[key] = False
    return dictionary


def hash_array_or_matrix(X: Union[np.ndarray, pd.DataFrame]) -> str:
    """
    Creates a hash for a given array.
    Used for dataset name in case none is specified
    Args:
        X: (Union[np.ndarray, pd.DataFrame])
            data

    Returns:
        (str): hash of the data as string
    """
    m = hashlib.md5()

    if hasattr(X, "iloc"):
        X = X.to_numpy()

    if scipy.sparse.issparse(X):
        m.update(X.indices)
        m.update(X.indptr)
        m.update(X.data)
        m.update(str(X.shape).encode('utf8'))
    else:
        if X.flags['C_CONTIGUOUS']:
            m.update(X.data)
            m.update(str(X.shape).encode('utf8'))
        else:
            X_tmp = np.ascontiguousarray(X.T)
            m.update(X_tmp.data)
            m.update(str(X_tmp.shape).encode('utf8'))

    hash = m.hexdigest()
    return hash
