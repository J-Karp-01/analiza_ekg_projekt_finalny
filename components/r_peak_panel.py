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
        <hr style="
            margin-top: 10px;
            height:5px;
            border:none;
            background-color:#0092ff;
        " />
    """, unsafe_allow_html=True)

    st.markdown(
        '<p style="font-size: 18px; font-weight: bold; color: #0092ff;">Identyfikacja załamków R i tworzenie szeregu RR</p>',
        unsafe_allow_html=True
    )

    col_left, col_center, col_right = st.columns([1, 2.3, 2])

    with col_left:

        with st.container(border=True):

            st.markdown(
                '<div style="margin-top:20px;"></div>',
                unsafe_allow_html=True
            )

            threshold_rr = st.slider(
                "Próg dla pików R:",
                min_value=0.0,
                max_value=2.0,
                value=float(threshold_rr),
                step=0.01
            )

            distance_rr = st.slider(
                "Dystans między RR:",
                min_value=0.0,
                max_value=2000.0,
                value=float(distance_rr),
                step=10.0
            )

            st.markdown("</div>", unsafe_allow_html=True)

    with col_center:

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=df['czas'],
            y=df['ecg_filtrowany'],
            mode='lines',
            name='Sygnał EKG',
            line=dict(
                color="#C5E0F1",
                width=1.5
            )
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
                line=dict(
                    color='white',
                    width=1
                )
            )
        ))

        fig.add_hline(
            y=threshold_rr,
            line_dash="dash",
            line_color="rgba(255,255,255,0.3)"
        )

        fig.update_layout(
            height=500,
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            template="plotly_dark",
            hovermode="x unified",
            xaxis_title="Czas [s]",
            yaxis_title="Amplituda [mV]",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col_right:

        st.markdown(
            '<p style="font-size: 18px; font-weight: bold; color: #0092ff;">Szereg RR</p>',
            unsafe_allow_html=True
        )

        st.dataframe(
            df_rr,
            height=220,
            use_container_width=True
        )

        fig_rr = go.Figure()

        fig_rr.add_trace(go.Scatter(
            x=df['czas'].iloc[peaks[1:]],
            y=df_rr['rr_ms'].values,
            mode='lines+markers',
            name='Odstępy RR',
            line=dict(
                color=bialy,
                width=2
            ),
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
            margin=dict(l=20, r=20, t=20, b=20),
            height=260
        )

        st.plotly_chart(
            fig_rr,
            use_container_width=True
        )

    st.markdown("""
        <hr style="
            margin-top: 30px;
            height:5px;
            border:none;
            background-color:#444444;
        " />
    """, unsafe_allow_html=True)

    return col_right, threshold_rr, distance_rr, df_rr