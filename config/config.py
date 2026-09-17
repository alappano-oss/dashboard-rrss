from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / 'data'
RAW_DIR = DATA_DIR / 'raw'
PROCESSED_DIR = DATA_DIR / 'processed'

BRANDS = {
    'ELEBAR': {
        'slug': 'elebar',
        'primary': '#FBBA00', 'secondary': '#571744', 'tertiary': '#6B4B63',
        'display_name': 'Elebar',
    },
    'PUNTO BLU': {
        'slug': 'blu',
        'primary': '#0760f7', 'secondary': '#024099', 'tertiary': '#FBBA00',
        'display_name': 'Punto Blu',
    },
}

CANONICAL_COLUMNS = [
    'date','time','platform','account','post_id','url','format','content_type','copy',
    'reach','impressions','video_views','likes','comments','shares','saves','clicks',
    'profile_visits','followers_gained','followers_lost','interactions','er_reach',
    'er_impressions','video_duration_seconds','source_file','source_row','brand',
]

NUMERIC_COLUMNS = [
    'reach','impressions','video_views','likes','comments','shares','saves','clicks',
    'profile_visits','followers_gained','followers_lost','interactions',
    'er_reach','er_impressions','video_duration_seconds',
]

REQUIRED_ANY = {
    'date': ['date','published_at','publication_date','post_date','date_published'],
    'platform': ['platform','network','social_network','channel'],
}

COLUMN_ALIASES = {
    'date': ['date','published_at','publication_date','post_date','date_published','fecha'],
    'time': ['time','published_time','publication_time','hora'],
    'platform': ['platform','network','social_network','channel','plataforma','red'],
    'account': ['account','account_name','profile','page','page_name','cuenta'],
    'post_id': ['post_id','postid','id','content_id','publication_id','id_publicacion'],
    'url': ['url','permalink','post_url','link','enlace'],
    'format': ['format','type','media_type','post_type','content_format','formato','tipo'],
    'content_type': ['content_type','content_category','topic','tipo_contenido'],
    'copy': ['copy','caption','message','text','post_text','description','texto'],
    'reach': ['reach','accounts_reached','people_reached','alcance'],
    'impressions': ['impressions','views','impressions_total','impresiones'],
    'video_views': ['video_views','reels_plays','video_plays','plays','reproducciones','reproducciones_de_video'],
    'likes': ['likes','reactions','post_reactions','me_gusta','reacciones'],
    'comments': ['comments','comentarios'],
    'shares': ['shares','shared','compartidos'],
    'saves': ['saves','saved','guardados'],
    'clicks': ['clicks','link_clicks','post_clicks','clics'],
    'profile_visits': ['profile_visits','profile_views','visits_to_profile','visitas_al_perfil'],
    'followers_gained': ['followers_gained','follows','new_followers','seguidores_ganados'],
    'followers_lost': ['followers_lost','unfollows','lost_followers','seguidores_perdidos'],
    'interactions': ['interactions','engagements','total_interactions','interacciones'],
    'video_duration_seconds': ['video_duration_seconds','video_duration','duration_seconds','duracion_video'],
}

FORMAT_MAP = {
    'reel':'Reel','reels':'Reel','video reel':'Reel','instagram reel':'Reel','reel video':'Reel',
    'carousel':'Carrusel','carrousel':'Carrusel','carousel post':'Carrusel','carrusel':'Carrusel',
    'post':'Post','feed post':'Post','photo':'Imagen','image':'Imagen','imagen':'Imagen',
    'video':'Video','videos':'Video','video post':'Video',
}

PLATFORM_MAP = {
    'instagram':'Instagram','ig':'Instagram','facebook':'Facebook','fb':'Facebook',
}
