import itertools
from typing import Union, List

import torch
from more_itertools import chunked
from torch.nn import functional as F

import numpy as np
from tqdm import tqdm
from transformers import AutoTokenizer, AutoModelForSequenceClassification, PreTrainedTokenizerFast, \
    PreTrainedModel

from commentsearch.config import COLIBERT_BATCH_SIZE


class TextPairClassificationModel:
    def __init__(self, model_name: str):
        self.device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        self.tokenizer: PreTrainedTokenizerFast = AutoTokenizer.from_pretrained(model_name, use_fast=True)
        self.model: PreTrainedModel = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.model.to(self.device)

    def get_pairwise_scores(self, texts_a: List[str], texts_b: List[str]) -> np.ndarray:
        text_pairs = itertools.product(texts_a, texts_b)
        batch_preds = []
        for pair_batch in chunked(tqdm(text_pairs, total=len(texts_a) * len(texts_b)), n=COLIBERT_BATCH_SIZE):
            tokens = self.tokenizer(*list(zip(*pair_batch)), padding=True, truncation='longest_first', max_length=128, return_tensors='pt').to(self.device)
            outputs, = self.model(**tokens)
            batch_preds.append(F.softmax(outputs.cpu(), dim=-1)[:, 1].detach().numpy())
        return np.concatenate(batch_preds).reshape((len(texts_a), len(texts_b)))


colibert: Union[None, TextPairClassificationModel] = None


def get_colibert() -> TextPairClassificationModel:
    global colibert
    if colibert is None:
        colibert = TextPairClassificationModel("ietz/comment-linking-distilbert-base-german-cased")
    return colibert
