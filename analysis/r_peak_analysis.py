import pandas as pd
from scipy.signal import find_peaks


def detect_r_peaks(
    sygnal,
    threshold_rr,
    distance_rr
):

    peaks, _ = find_peaks(
        sygnal,
        distance=distance_rr,
        height=threshold_rr
    )

    return peaks


def create_rr_dataframe(
    df,
    peaks
):

    czasy_pikow = df['czas'].iloc[peaks].values

    odstepy_rr = czasy_pikow[1:] - czasy_pikow[:-1]

    df_rr = pd.DataFrame({
        '#': range(1, len(odstepy_rr) + 1),
        'rr_ms': odstepy_rr * 1000,
        'rr_s': odstepy_rr
    })

    rr_intervals = df_rr['rr_ms'].values

    return df_rr, rr_intervals