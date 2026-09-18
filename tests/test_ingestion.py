import pandas as pd
from src.data_cleaner import normalize_dataframe
from src.data_validator import validate_raw
def test_fb():
 r=pd.DataFrame({'identificador de la publicación':['1'],'Nombre de la página':['Tarjeta Elebar'],'Descripción':['Texto'],'Hora de publicación':['01/02/2026 11:30'],'Enlace permanente':['x'],'Tipo de publicación':['Fotos'],'Fecha':['Total'],'Visualizaciones':[1667],'Alcance':[1150],'Reacciones':[15],'Comentarios':[3],'Veces que se ha compartido':[2]})
 assert validate_raw(r).valid
 o=normalize_dataframe(r,'FB-01 ENERO 2026.csv','ELEBAR','Facebook');assert o.loc[0,'date'].isoformat()=='2026-01-02';assert o.loc[0,'format']=='Imagen';assert o.loc[0,'video_views']==1667;assert pd.isna(o.loc[0,'impressions'])
def test_ig():
 r=pd.DataFrame({'identificador de la publicación':['2'],'Nombre de usuario de la cuenta':['tarjeta.elebar'],'Nombre de la cuenta':['Tarjeta Elebar'],'Descripción':['Texto'],'Hora de publicación':['02/05/2026 12:00'],'Enlace permanente':['x'],'Tipo de publicación':['Reel de Instagram'],'Fecha':['Total'],'Visualizaciones':[2000],'Alcance':[1500],'Me gusta':[100],'Veces que se ha compartido':[10],'Seguidores':[2],'Comentarios':[5],'Veces guardado':[20]})
 o=normalize_dataframe(r,'IG-02 FEBRERO 2026.csv','ELEBAR','Instagram');assert o.loc[0,'format']=='Reel';assert o.loc[0,'interactions']==135;assert o.loc[0,'followers']==2
