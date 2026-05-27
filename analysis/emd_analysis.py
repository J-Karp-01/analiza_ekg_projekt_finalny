import streamlit as st
from PyEMD import EMD
import pandas as pd
import numpy as np


@st.cache_data
def compute_emd(signal):

    emd = EMD()

    imfs = emd.emd(signal)

    df_imfs = pd.DataFrame(imfs.T)

    df_imfs.columns = [
        f"IMF_{i+1}" for i in range(df_imfs.shape[1])
    ]

    return df_imfs

def reconstruct_signal(df_imfs, wybrane_imf):

    sygnal_rekonstrukcja = np.zeros(len(df_imfs))

    for imf in wybrane_imf:

        sygnal_rekonstrukcja += df_imfs[imf].values

    return sygnal_rekonstrukcja

def compute_imf_energy(df_imfs):

    energie = {}

    for col in df_imfs.columns:

        energie[col] = (df_imfs[col] ** 2).sum()

    return energie