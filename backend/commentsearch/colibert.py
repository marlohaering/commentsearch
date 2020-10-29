import itertools
from typing import Union, List
import torch
from torch.nn import functional as F

import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification, PreTrainedTokenizerFast, \
    PreTrainedModel


class TextPairClassificationModel:
    def __init__(self, model_name: str):
        self.tokenizer: PreTrainedTokenizerFast = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.model: PreTrainedModel = AutoModelForSequenceClassification.from_pretrained(model_name)

    def get_pairwise_scores(self, texts_a: List[str], texts_b: List[str]) -> np.ndarray:
        text_pairs = itertools.product(texts_a, texts_b)
        tokens = self.tokenizer(*list(zip(*text_pairs)), padding=True, truncation='longest_first', max_length=128, return_tensors='pt')
        outputs, = self.model(**tokens)
        preds = F.softmax(outputs, dim=-1)
        return torch.reshape(preds[:, 1], (len(texts_a), len(texts_b))).detach().numpy()


colibert: Union[None, TextPairClassificationModel] = None


def get_colibert() -> TextPairClassificationModel:
    global colibert
    if colibert is None:
        colibert = TextPairClassificationModel("ietz/comment-linking-distilbert-base-german-cased")
    return colibert
