"""Representative sampling based active learning strategy
"""
from typing import Any, List, Optional, Union

import torch
from sklearn.base import ClusterMixin

from pyrelational.data import GenericDataManager
from pyrelational.informativeness import representative_sampling
from pyrelational.models import GenericModel
from pyrelational.strategies.generic_al_strategy import GenericActiveLearningStrategy


class RepresentativeSamplingStrategy(GenericActiveLearningStrategy):
    """Representative sampling based active learning strategy"""

    def __init__(
        self,
        clustering_method: Union[str, ClusterMixin] = "KMeans",
        **clustering_kwargs: Any,
    ):
        super(RepresentativeSamplingStrategy, self).__init__()
        self.clustering_method = clustering_method
        self.clustering_kwargs = clustering_kwargs

    def active_learning_step(
        self,
        data_manager: GenericDataManager,
        num_annotate: Optional[int] = None,
    ) -> List[int]:
        unlabelled_features = torch.stack(data_manager.get_sample_feature_vectors(data_manager.u_indices))
        representative_samples = representative_sampling(
            unlabelled_features,
            num_annotate=num_annotate,
            clustering_method=self.clustering_method,
            **self.clustering_kwargs,
        )
        return [data_manager.u_indices[i] for i in representative_samples]
