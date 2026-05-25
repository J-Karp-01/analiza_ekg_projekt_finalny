import streamlit as st
import plotly.express as px

from analysis.hrv_analysis import (
    calculate_hrv_statistics
)


def render_hrv_panel(
    col2,
    df_rr,
    rr_intervals,
    niebieski,
    lekki_szary
):

    with col2:

        st.markdown(
            f'<p style="margin-top: 0px; font-size: 18px; font-weight: bold; color:#0092ff;">Histogram</p>',
            unsafe_allow_html=True
        )

        st.markdown(f"""
            <div style="background-color: {lekki_szary};
                border-radius: 10px;
                padding: 40px;
                margin-bottom: -1820px;
                height: 550px;
                border: 0px solid rgba(100,100,100,1);
            ">
            </div>
        """, unsafe_allow_html=True)

        lewy, srodek, prawy = st.columns([0.02, 0.9, 0.02])

        with srodek:

            col_rr1, col_rr2 = st.columns([1., 1.8])

            with col_rr1:

                st.dataframe(
                    df_rr,
                    height=310,
                    use_container_width=True
                )

            with col_rr2:

                histogram_bins = st.slider(
                    'Histogram',
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
                    height=250,
                    margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    xaxis_title="Czas trwania [ms]",
                    yaxis_title="Częstość",
                    bargap=0.1
                )

                with st.container(border=True):

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
                <hr style="margin-top: 10px;height:5px; border:none; color: {niebieski}; background-color:{niebieski};" />
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
                <hr style="margin-top: 10px;height:5px; border:none; color: {niebieski}; background-color:{niebieski};" />
            """, unsafe_allow_html=True)