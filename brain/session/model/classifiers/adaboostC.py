import sys
sys.path.insert(0, 'brain/session/model')
from adabooster import adaboostgen

def adaboostCgenerate(
    model,
    collection,
    payload,
    list_error,
    learning=1.0,
    estimators=50
):
    return adaboostgen(model,
                  collection,
                  payload,
                  list_error,
                  learning=learning,
                  be=None,
                  bnum=estimators)
