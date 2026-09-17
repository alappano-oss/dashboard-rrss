import pandas as pd
from src.metrics import kpis

def test_engagement():
    df=pd.DataFrame({'reach':[1000],'impressions':[2000],'likes':[50],'comments':[10],'shares':[20],'saves':[20],'interactions':[80]})
    assert kpis(df)['er_reach']==8
    assert kpis(df)['er_impressions']==4

def test_missing_metric_is_nan():
    df=pd.DataFrame({'reach':[100]})
    assert pd.isna(kpis(df)['impressions_total'])
