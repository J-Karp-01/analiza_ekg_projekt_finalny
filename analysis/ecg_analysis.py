from scipy.signal import savgol_filter


def filter_ecg(
    surowy_wektor,
    window_length,
    polyorder
):

    ecg_filtrowany = savgol_filter(
        surowy_wektor,
        window_length,
        polyorder
    )

    return ecg_filtrowany