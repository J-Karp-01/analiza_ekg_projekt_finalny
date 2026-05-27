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

def compute_imf_energy(df_imfs):

    energie = {}

    for col in df_imfs.columns:

        energie[col] = (df_imfs[col] ** 2).sum()

    return energie