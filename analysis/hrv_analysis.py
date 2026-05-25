def calculate_hrv_statistics(
    df_rr
):

    srednie_rr = df_rr['rr_ms'].mean()

    sdnn = df_rr['rr_ms'].std()

    max_rr = df_rr['rr_ms'].max()

    min_rr = df_rr['rr_ms'].min()

    liczba_R = df_rr.shape[0]

    return (
        srednie_rr,
        sdnn,
        max_rr,
        min_rr,
        liczba_R
    )