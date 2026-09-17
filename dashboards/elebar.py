from dashboards.common import render_dashboard
from config.config import BRANDS

def render(df): render_dashboard(df, BRANDS['ELEBAR'])
