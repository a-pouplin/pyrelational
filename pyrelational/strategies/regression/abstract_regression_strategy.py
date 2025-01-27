from abc import ABC, abstractmethod
from typing import Any, List

import torch
from torch import Tensor

from pyrelational.data_managers import DataManager
from pyrelational.model_managers import ModelManager
from pyrelational.strategies.abstract_strategy import Strategy


class RegressionStrategy(Strategy, ABC):
    """A base active learning strategy class for regression in which the top n indices,
    according to user-specified scoring function, are queried at each iteration"""

    def __init__(self) -> None:
        super(RegressionStrategy, self).__init__()

    def __call__(
        self, num_annotate: int, data_manager: DataManager, model_manager: ModelManager[Any, Any]
    ) -> List[int]:
        output = self.train_and_infer(data_manager=data_manager, model_manager=model_manager)
        scores = self.scoring_function(output).squeeze(-1)
        ixs = torch.argsort(scores, descending=True).tolist()
        return [data_manager.u_indices[i] for i in ixs[:num_annotate]]

    @abstractmethod
    def scoring_function(self, predictions: Tensor) -> Tensor:
        """
        Compute score of each sample.

        :param predictions: model predictions for each sample
        :return: scores for each sample
        """
