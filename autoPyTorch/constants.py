"""Constant numbers for this package

TODO:
    * Makes this file nicer
    * transfer to proper locations e.g. create task directory?
"""

from enum import Enum
from autoPyTorch.pipeline.image_classification import ImageClassificationPipeline
from autoPyTorch.pipeline.tabular_classification import TabularClassificationPipeline
from autoPyTorch.pipeline.tabular_regression import TabularRegressionPipeline
import abc
from typing import Union


SupportedPipelines = Union[ImageClassificationPipeline,
                           TabularClassificationPipeline,
                           TabularRegressionPipeline]


class BaseTaskTypes(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def is_supported(self) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def task_name(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def dataset_type(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def pipeline(self) -> SupportedPipelines:
        raise NotImplementedError


class RegressionTypes(Enum, BaseTaskTypes):
    tabular = TabularRegressionPipeline
    image = None
    time_series = None

    def is_supported(self) -> bool:
        return self.value is not None

    def task_name(self) -> str:
        return 'regressor'

    def dataset_type(self) -> str:
        return self.name

    def pipeline(self) -> SupportedPipelines:
        if not self.is_supported():
            raise ValueError(f"{self.name} is not supported pipeline.")

        return self.value


class ClassificationTypes(Enum, BaseTaskTypes):
    tabular = TabularClassificationPipeline
    image = ImageClassificationPipeline
    time_series = None

    def is_supported(self) -> bool:
        return self.value is not None

    def task_name(self) -> str:
        return 'classifier'

    def dataset_type(self) -> str:
        return self.name

    def pipeline(self) -> SupportedPipelines:
        if not self.is_supported():
            raise ValueError(f"{self.name} is not supported pipeline.")

        return self.value


SupportedTaskTypes = (RegressionTypes, ClassificationTypes)


"""TODO: remove these variables
TABULAR_CLASSIFICATION = 1
IMAGE_CLASSIFICATION = 2
TABULAR_REGRESSION = 3
IMAGE_REGRESSION = 4
TIMESERIES_CLASSIFICATION = 5
TIMESERIES_REGRESSION = 6

REGRESSION_TASKS = [TABULAR_REGRESSION, IMAGE_REGRESSION, TIMESERIES_REGRESSION]
CLASSIFICATION_TASKS = [TABULAR_CLASSIFICATION, IMAGE_CLASSIFICATION, TIMESERIES_CLASSIFICATION]

TABULAR_TASKS = [TABULAR_CLASSIFICATION, TABULAR_REGRESSION]
IMAGE_TASKS = [IMAGE_CLASSIFICATION, IMAGE_REGRESSION]
TASK_TYPES = REGRESSION_TASKS + CLASSIFICATION_TASKS

TASK_TYPES_TO_STRING = \
    {TABULAR_CLASSIFICATION: 'tabular_classification',
     IMAGE_CLASSIFICATION: 'image_classification',
     TABULAR_REGRESSION: 'tabular_regression',
     IMAGE_REGRESSION: 'image_regression',
     TIMESERIES_CLASSIFICATION: 'time_series_classification',
     TIMESERIES_REGRESSION: 'time_series_regression'}

STRING_TO_TASK_TYPES = \
    {'tabular_classification': TABULAR_CLASSIFICATION,
     'image_classification': IMAGE_CLASSIFICATION,
     'tabular_regression': TABULAR_REGRESSION,
     'image_regression': IMAGE_REGRESSION,
     'time_series_classification': TIMESERIES_CLASSIFICATION,
     'time_series_regression': TIMESERIES_REGRESSION}
"""


# Output types have been defined as in scikit-learn type_of_target
# (https://scikit-learn.org/stable/modules/generated/sklearn.utils.multiclass.type_of_target.html)
BINARY = 10
CONTINUOUSMULTIOUTPUT = 11
MULTICLASS = 12
CONTINUOUS = 13
MULTICLASSMULTIOUTPUT = 14

OUTPUT_TYPES = [BINARY, CONTINUOUSMULTIOUTPUT, MULTICLASS, CONTINUOUS]

OUTPUT_TYPES_TO_STRING = \
    {BINARY: 'binary',
     CONTINUOUSMULTIOUTPUT: 'continuous-multioutput',
     MULTICLASS: 'multiclass',
     CONTINUOUS: 'continuous',
     MULTICLASSMULTIOUTPUT: 'multiclass-multioutput'}

STRING_TO_OUTPUT_TYPES = \
    {'binary': BINARY,
     'continuous-multioutput': CONTINUOUSMULTIOUTPUT,
     'multiclass': MULTICLASS,
     'continuous': CONTINUOUS,
     'multiclass-multioutput': MULTICLASSMULTIOUTPUT}

CLASSIFICATION_OUTPUTS = [BINARY, MULTICLASS, MULTICLASSMULTIOUTPUT]
REGRESSION_OUTPUTS = [CONTINUOUS, CONTINUOUSMULTIOUTPUT]
