import streamlit as st
import plotly.graph_objects as go


def render_r_peak_panel(
    df,
    peaks,
    threshold_rr,
    distance_rr,
    df_rr,
    niebieski,
    lekki_szary,
    bialy
):

    st.markdown("""
        <hr style="margin-top: 10px;height:5px; border:none; color:#444444; background-color:#444444;" />
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4, 4.5])

    with col1:

        st.markdown(
            '<p style="margin-top: px; font-size: 18px; font-weight: bold; color: #0092ff;"> Identyfikacja załamków R i tworzenie szeregu RR</p>',
            unsafe_allow_html=True
        )

        col_left, col_right = st.columns([1, 4])

        with col_left:

            st.markdown(f"""
                <div style="background-color: {niebieski};
                    border-radius: 10px;
                    padding: 40px;
                    margin-bottom: -1820px;
                    height: 230px;
                    border: 0px solid rgba(100,100,100,1);
                ">
                </div>
            """, unsafe_allow_html=True)

            lewy, srodek, prawy = st.columns([0.1, 0.9, 0.1])

            with srodek:

                st.markdown(
                    '<div style="margin-top: 20px;"></div>',
                    unsafe_allow_html=True
                )

                st.slider(
                    "Próg dla pików R:",
                    min_value=0.0,
                    max_value=2.0,
                    value=float(threshold_rr),
                    step=0.01,
                    disabled=True
                )

                st.slider(
                    "Dystans między RR:",
                    min_value=0.0,
                    max_value=2000.0,
                    value=float(distance_rr),
                    step=10.0,
                    disabled=True
                )

        with col_right:

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=df['czas'],
                y=df['ecg_filtrowany'],
                mode='lines',
                name='Sygnał EKG',
                line=dict(color='#C3E5FF', width=1.5)
            ))

            fig.add_trace(go.Scatter(
                x=df['czas'].iloc[peaks],
                y=df['ecg_filtrowany'].iloc[peaks],
                mode='markers',
                name='Piki R',
                marker=dict(
                    color=niebieski,
                    size=8,
                    symbol='circle',
                    line=dict(color='white', width=1)
                )
            ))

            fig.add_hline(
                y=threshold_rr,
                line_dash="dash",
                line_color="rgba(255,255,255,0.3)"
            )

            fig.update_layout(
                height=200,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0
                ),
                xaxis_title="Czas [s]",
                yaxis_title="Amplituda [mV]"
            )

            with st.container(border=True):

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

        st.markdown(f"""
            <div style="background-color: {lekki_szary};
                border-radius: 10px;
                padding: 40px;
                margin-bottom: -1820px;
                height: 300px;
                border: 0px solid rgba(100,100,100,1);
            ">
            </div>
        """, unsafe_allow_html=True)

        lewy, srodek, prawy = st.columns([0.02, 0.9, 0.02])

        with srodek:

            fig_rr = go.Figure()

            fig_rr.add_trace(go.Scatter(
                x=df['czas'].iloc[peaks[1:]],
                y=df_rr['rr_ms'].values,
                mode='lines+markers',
                name='Odstępy RR',
                line=dict(color=bialy, width=2),
                marker=dict(
                    size=6,
                    color=niebieski,
                    symbol='circle'
                )
            ))

            fig_rr.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Czas badania [s]",
                yaxis_title="Odstęp RR [ms]",
                template="plotly_dark",
                hovermode="x unified",
                margin=dict(l=30, r=20, t=30, b=90),
                height=300
            )

            st.plotly_chart(
                fig_rr,
                use_container_width=True
            )

    return col2