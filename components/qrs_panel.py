import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


def render_qrs_panel(
    df,
    peaks,
    df_qrs,
    zielony,
    niebieski
):

    st.markdown(
        f'<p style="margin-top: 0px; font-size: 18px; font-weight: bold; color:{zielony};">Segmentacja zespołu QRS</p>',
        unsafe_allow_html=True
    )

    st.markdown(f"""
        <hr style="margin-top: 10px;height:5px; border:none; color:{niebieski}; background-color:{zielony};" />
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([4,4.5])

    with col1:

        col_left, col_right = st.columns([1, 1])

        with col_left:

            window = st.slider(
                "Próg dla pików R:",
                min_value=100,
                max_value=1000,
                value=250,
                step=10
            )

        with col_right:

            idx_segmentu = st.slider(
                "Wybierz numer zespołu QRS:",
                0,
                len(peaks)-1,
                2
            )

            r_center = peaks[idx_segmentu]

            start_idx = max(0, r_center - window)
            stop_idx = min(len(df), r_center + window)

            fig_seg = go.Figure()

            fig_seg.add_trace(go.Scatter(
                x=df['czas'],
                y=df['ecg_filtrowany'],
                mode='lines',
                line=dict(color='rgba(150, 150, 150, 0.5)', width=1),
                name='Pełny sygnał'
            ))

            fig_seg.add_trace(go.Scatter(
                x=df['czas'].iloc[start_idx:stop_idx],
                y=df['ecg_filtrowany'].iloc[start_idx:stop_idx],
                mode='lines',
                line=dict(color=zielony, width=3),
                name='Wybrany segment'
            ))

            fig_seg.add_vrect(
                x0=df['czas'].iloc[start_idx],
                x1=df['czas'].iloc[stop_idx],
                fillcolor=zielony,
                opacity=0.2,
                layer="below",
                line_width=0,
            )

            fig_seg.update_layout(
                title=f"Podgląd segmentu nr {idx_segmentu + 1} (R w {df['czas'].iloc[r_center]:.2f} s)",
                xaxis_title="Czas [s]",
                yaxis_title="Amplituda",
                template="plotly_dark",
                height=300,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0
                ),
            )

            fig_seg.update_layout(
                title_font=dict(
                    color="#c8ff4a",
                    size=18
                ),
                title_x=0.02
            )

            st.plotly_chart(
                fig_seg,
                use_container_width=True
            )

    with col2:

        lewy, prawy = st.columns([1, 1])

        with lewy:

            df_qrs['SREDNI_QRS'] = df_qrs.mean(axis=1)

            y_min_sredni = df_qrs['SREDNI_QRS'].min()
            y_max_sredni = df_qrs['SREDNI_QRS'].max()

            margines = (y_max_sredni - y_min_sredni) * 0.15

            fig_qrs = px.line(
            df_qrs,
            labels={
                'index': 'Próbki względem R',
                'value': 'Amplituda'
            },

            title="Nałożone segmenty QRS z uśrednionym profilem",

            template="plotly_dark"
        )

            fig_qrs.update_layout(
                title_font=dict(
                    color="#c8ff4a",
                    size=18
                ),
                title_x=0.02
            )
            
            fig_qrs.update_traces(
                line=dict(
                    width=1,
                    color="#c8ff4a"
                ),
                opacity=0.4
            )

            fig_qrs.update_layout(
                yaxis=dict(
                    range=[
                        y_min_sredni - margines,
                        y_max_sredni + margines
                    ],
                    fixedrange=False
                ),
                template="plotly_dark",
                uirevision='constant'
            )

            fig_qrs.for_each_trace(
                lambda trace: trace.update(
                    line=dict(color=zielony, width=4),
                    opacity=1
                )
                if trace.name == 'SREDNI_QRS' else ()
            )

            fig_qrs.data = (
                [t for t in fig_qrs.data if t.name != 'SREDNI_QRS']
                +
                [t for t in fig_qrs.data if t.name == 'SREDNI_QRS']
            )

            st.plotly_chart(
                fig_qrs,
                use_container_width=True
            )

        with prawy:

            wybrana_kolumna = f'QRS_{idx_segmentu + 1:02d}'

            y_values = df_qrs[wybrana_kolumna].values
            x_values = df_qrs.index

            fig_single = go.Figure()

            fig_single.add_trace(go.Scatter(
                x=list(x_values),
                y=list(y_values),
                mode='lines',
                line=dict(color=zielony, width=4),
                name=wybrana_kolumna,
                fill='tozeroy',
                fillcolor='rgba(46, 204, 113, 0.2)'
            ))

            fig_single.update_layout(
                title=dict(
                    text=f"Analiza morfologii: {wybrana_kolumna}",
                    font=dict(
                        color="#c8ff4a",
                        size=18
                    ),
                    x=0.02
                ),
                xaxis_title="Próbki względem załamka R [n]",
                yaxis_title="Amplituda [mV]",
                template="plotly_dark",
                height=400,
                showlegend=False,
                shapes=[dict(
                    type='line',
                    yref='y',
                    y0=0,
                    y1=0,
                    xref='x',
                    x0=x_values.min(),
                    x1=x_values.max(),
                    line=dict(
                        color="#00ff88",
                        width=1,
                        dash="dot"
                    )
                )]
            )

            st.plotly_chart(
                fig_single,
                use_container_width=True
            )

    z_data = df_qrs.drop(
        columns=['SREDNI_QRS'],
        errors='ignore'
    ).values.T

    x_axis = df_qrs.index
    y_axis = np.arange(z_data.shape[0])

    fig_3d = go.Figure(data=[go.Surface(
        z=z_data,
        x=x_axis,
        y=y_axis,
        colorscale='Rainbow',
        colorbar=dict(title="Amplituda"),
        opacity=0.9
    )])

    st.markdown("""
        <hr style="
            margin-top: 30px;
            height:5px;
            border:none;
            background-color:#444444;
        " />
    """, unsafe_allow_html=True)

    fig_3d.update_layout(
        title=dict(
            text='Trójwymiarowa segmentacja zespołów QRS',
            font=dict(
                color="#c8ff4a",
                size=18
            ),
            x=0.02
        ),
        scene=dict(
            xaxis_title='Czas wewnątrz QRS [n]',
            yaxis_title='Numer uderzenia',
            zaxis_title='Amplituda',
            camera=dict(
                eye=dict(
                    x=1.5,
                    y=1.5,
                    z=1.2
                )
            ),
        ),
        template="plotly_dark",
        margin=dict(l=0, r=0, b=0, t=40),
        height=700
    )

    st.plotly_chart(
        fig_3d,
        use_container_width=True
    )

    styled_df = df_qrs.style.map(
        lambda x: f"color: {zielony}; font-weight: bold;"
    )

    wybrana_kolumna = f'QRS_{idx_segmentu + 1:02d}'

    def highlight_selected(x):
        return 'color: #2ecc71; font-weight: bold; background-color: rgba(46, 284, 113, 0.1);'

    st.dataframe(
    df_qrs,
    use_container_width=True
)