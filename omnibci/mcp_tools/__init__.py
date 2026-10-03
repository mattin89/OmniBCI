"""
Paper2Agent MCP Tools Catalog for Brain-Computer Interfaces (BCI).
Exposes validated scientific tools extracted from peer-reviewed publications.
"""

from .riemannian_ea_mcp import train_and_eval_riemannian_ea, align_euclidean, project_tangent_space
from .eegnet_mcp import train_and_eval_eegnet
from .shallow_fbcsp_mcp import train_and_eval_shallow_fbcsp
from .intertwined_mcp import train_and_eval_intertwined

MCP_REGISTRY = {
    "intertwined_nn": {
        "title": "Intertwined Neural Network (tdFC + sdConv)",
        "reference": "Duggento, De Lorenzo, et al. (2022) arXiv:2208.08860",
        "description": "Intertwined time-distributed spatial projections (tdFC) and space-distributed temporal convolutions (sdConv) for robust multi-scale spatio-temporal EEG decoding.",
        "runner": train_and_eval_intertwined,
        "category": "Deep Learning / Spatio-Temporal Intertwining"
    },
    "riemannian_ea": {
        "title": "Euclidean Alignment + Riemannian Tangent Space",
        "reference": "He & Wu (2019) IEEE TBME; Barachant et al. (2012) IEEE TBME",
        "description": "Aligns subject covariance matrices in Riemannian manifold to eliminate cross-subject domain shift.",
        "runner": train_and_eval_riemannian_ea,
        "category": "DSP / Riemannian Geometry"
    },
    "eegnet": {
        "title": "EEGNet Compact Convolutional Neural Network",
        "reference": "Lawhern et al. (2018) J. Neural Engineering",
        "description": "Temporal and depthwise spatial convolutions tailored for low-channel sensorimotor EEG.",
        "runner": train_and_eval_eegnet,
        "category": "Deep Learning / End-to-End"
    },
    "shallow_fbcsp": {
        "title": "ShallowFBCSPNet",
        "reference": "Schirrmeister et al. (2017) Human Brain Mapping",
        "description": "Convolutional architecture designed to mimic Filter Bank Common Spatial Patterns with bandpower pooling.",
        "runner": train_and_eval_shallow_fbcsp,
        "category": "Deep Learning / Energy Pooling"
    }
}
