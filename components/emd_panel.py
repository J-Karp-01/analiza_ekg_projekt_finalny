import streamlit as st
import plotly.graph_objects as go
from analysis.emd_analysis import reconstruct_signal
from analysis.emd_analysis import compute_imf_energy
import pandas as pd

def render_emd_panel(
    df_view,
    df_imfs,
    fioletowy,
):

    st.markdown(f"""
    <p style="
        color:{fioletowy};
        font-size:18px;
        font-weight:700;
        margin-bottom:5px;
    ">
    Dekompozycja sygnału EMD
    </p>

    <hr style="
        height:5px;
        border:none;
        background-color:{fioletowy};
        margin-bottom:25px;
    ">
    """, unsafe_allow_html=True)

    imf_names = df_imfs.columns.tolist()

    wybrany_imf = st.selectbox(
        "Wybierz składową IMF:",
        imf_names
    )

    wybrane_imf = st.multiselect(
    "Wybierz IMF do rekonstrukcji:",
    imf_names,
    default=imf_names[:2]
    )

    sygnal_rekonstrukcja = reconstruct_signal(
        df_imfs,
        wybrane_imf
    )

    energie_imf = compute_imf_energy(df_imfs)

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_view['czas'],
        y=df_imfs[wybrany_imf],
        mode='lines',
        name=wybrany_imf,
        line=dict(
            color=fioletowy,
            width=2
        )
    ))

    fig.update_layout(
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Czas [s]",
        yaxis_title="Amplituda",
        margin=dict(
            l=0,
            r=0,
            t=20,
            b=0
        )
    )

    st.plotly_chart(
    fig,
    use_container_width=True,
    key="emd_imf_plot"
)

    st.markdown("""
    <hr style="
        margin-top:25px;
        margin-bottom:25px;
        height:4px;
        border:none;
        background-color:#444444;
    ">
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <p style="
        color:{fioletowy};
        font-size:18px;
        font-weight:700;
        margin-top:30px;
        margin-bottom:10px;
    ">
    Rekonstrukcja sygnału
    </p>
    """, unsafe_allow_html=True)

    fig_rek = go.Figure()

    fig_rek.add_trace(go.Scatter(
        x=df_view['czas'][:len(sygnal_rekonstrukcja)],
        y=sygnal_rekonstrukcja,
        mode='lines',
        name='Rekonstrukcja',
        line=dict(
            color='#ffffff',
            width=2
        )
    ))

    fig_rek.update_layout(
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Czas [s]",
        yaxis_title="Amplituda",
        margin=dict(
            l=0,
            r=0,
            t=20,
            b=0
        )
    )
    
    st.plotly_chart(
    fig_rek,
    use_container_width=True,
    key="emd_reconstruction_plot"
)
    
    st.markdown("""
    <hr style="
        margin-top:25px;
        margin-bottom:25px;
        height:4px;
        border:none;
        background-color:#444444;
    ">
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <p style="
        color:{fioletowy};
        font-size:18px;
        font-weight:700;
        margin-top:10px;
        margin-bottom:15px;
    ">
    Energia składowych IMF
    </p>
    """, unsafe_allow_html=True)

    df_energia = pd.DataFrame({
        "IMF": list(energie_imf.keys()),
        "Energia": list(energie_imf.values())
    })

    st.dataframe(
        df_energia,
        use_container_width=True,
        hide_index=True
    )

    