import pandas as pd
from src.data_cleaner import normalize_format,normalize_platform,deduplicate

def test_format_normalization():
    assert normalize_format('REEL')=='Reel'
    assert normalize_format('Video Reel')=='Reel'
    assert normalize_format('Carousel')=='Carrusel'

def test_duplicate_detection():
    a=pd.DataFrame({'_record_key':['id:1'],'post_id':['1']})
    b=pd.DataFrame({'_record_key':['id:1','id:2'],'post_id':['1','2']})
    out,dups=deduplicate(a,b)
    assert dups==1 and len(out)==2
