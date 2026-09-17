from __future__ import annotations
import numpy as np
import pandas as pd


def safe_sum(df, col): return df[col].sum(min_count=1) if col in df else np.nan

def safe_mean(df, col): return df[col].mean() if col in df and df[col].notna().any() else np.nan

def kpis(df: pd.DataFrame) -> dict:
    interactions = safe_sum(df, 'interactions')
    reach = safe_sum(df, 'reach')
    impressions = safe_sum(df, 'impressions')
    followers_gained = safe_sum(df, 'followers_gained')
    followers_lost = safe_sum(df, 'followers_lost')
    return {
        'reach_total': reach, 'reach_avg': safe_mean(df,'reach'),
        'reach_max': df['reach'].max() if 'reach' in df else np.nan,
        'reach_min': df['reach'].min() if 'reach' in df else np.nan,
        'impressions_total': impressions, 'impressions_avg': safe_mean(df,'impressions'),
        'frequency': impressions/reach if pd.notna(impressions) and pd.notna(reach) and reach else np.nan,
        'interactions_total': interactions, 'interactions_avg': safe_mean(df,'interactions'),
        'er_reach': interactions/reach*100 if pd.notna(interactions) and pd.notna(reach) and reach else np.nan,
        'er_impressions': interactions/impressions*100 if pd.notna(interactions) and pd.notna(impressions) and impressions else np.nan,
        'posts': len(df),
        'video_views_total': safe_sum(df,'video_views'), 'video_views_avg': safe_mean(df,'video_views'),
        'followers_gained': followers_gained, 'followers_lost': followers_lost,
        'followers_net': followers_gained-followers_lost if pd.notna(followers_gained) and pd.notna(followers_lost) else np.nan,
    }


def relative_performance(df: pd.DataFrame, metric='reach') -> pd.Series:
    if metric not in df or df[metric].dropna().empty: return pd.Series(np.nan, index=df.index)
    avg = df[metric].mean()
    return df[metric] / avg if avg else pd.Series(np.nan, index=df.index)
