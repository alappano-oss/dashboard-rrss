def fmt(v):
    if v is None:return '—'
    try:return f'{v:,.0f}'.replace(',','.')
    except:return str(v)
