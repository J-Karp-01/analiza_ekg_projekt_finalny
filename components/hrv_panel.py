import streamlit as st
import plotly.express as px

from analysis.hrv_analysis import (
    calculate_hrv_statistics
)

import plotly.graph_objects as go



def render_hrv_panel(
    col2,
    df_rr,
    rr_intervals,
    niebieski,
    lekki_szary
):

    st.markdown(
        '<p style="font-size: 18px; font-weight: bold; color: #0092ff;">Histogram odstępów RR</p>',
        unsafe_allow_html=True
    )

    histogram_bins = st.slider(
        'Liczba binów',
        min_value=20,
        max_value=300,
        value=180,
        step=1
)

    fig_hist = px.histogram(
        df_rr,
        x="rr_ms",
        nbins=histogram_bins,
        labels={'rr_ms': 'Odstęp RR [ms]'},
        color_discrete_sequence=[niebieski],
        marginal="rug"
    )

    fig_hist.update_layout(
        height=520,
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title="Czas trwania [ms]",
        yaxis_title="Częstość",
        bargap=0.1,
        template="plotly_dark"
    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )

    (
        srednie_rr,
        sdnn,
        max_rr,
        min_rr,
        liczba_R

    ) = calculate_hrv_statistics(df_rr)

    st.markdown(f"""
        <hr style="
            margin-top: 20px;
            height:5px;
            border:none;
            background-color:{niebieski};
        " />
    """, unsafe_allow_html=True)

    cola, colb, colc, cold, cole = st.columns([1,1,1,1,2])

    with cola:
        st.metric("Średnie RR", f"{srednie_rr:.0f} ms")

    with colb:
        st.metric("Std RR", f"{sdnn:.0f} ms")

    with colc:
        st.metric("Max RR", f"{max_rr:.0f} ms")

    with cold:
        st.metric("Min RR", f"{min_rr:.0f} ms")

    with cole:
        st.metric(
            "Liczba zidentyfikowanych załamków R",
            f"{liczba_R:.0f}"
        )

    st.markdown(f"""
        <hr style="
            margin-top: 20px;
            height:5px;
            border:none;
            background-color:#0092ff;
        " />
    """, unsafe_allow_html=True)