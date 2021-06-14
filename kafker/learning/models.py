from typing import Set

import faust

from kafker.app import app


class Bigram(faust.Record, coerce=True):
    lhs: str
    rhs: str


new_texts = app.topic("new_texts", internal=True, value_type=str)
new_bigrams = app.topic("new_bigrams", internal=True, value_type=Bigram)
bigrams = app.SetGlobalTable("bigrams", key_type=str, value_type=str, default=set)
bigram_weights = app.GlobalTable("bigram_weights", value_type=int, default=int)
