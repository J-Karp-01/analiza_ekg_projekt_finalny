import streamlit as st
import plotly.graph_objects as go
from analysis.respiration_analysis import detect_resp_cycles,compute_resp_phase,build_synchrogram_dataframe
from scipy.signal import find_peaks
import numpy as np
import plotly.express as px

def render_respiration_panel(
    df_view,
    czerwony,
    żółty,
    cyjan,
    neon_yellow,
    neon_pink,
    neon_green,
    neon_orange,
    neon_purple
):

    st.markdown(f"""
    <p style="
        color:{żółty};
        font-size:18px;
        font-weight:700;
        margin-bottom:10px;
    ">
    Synchronizacja sercowo oddechowa
    </p>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <hr style="
        height:4px;
        border:none;
        background-color:{żółty};
        margin-bottom:25px;
    ">
    """, unsafe_allow_html=True)

    resp_signal = df_view['resp'].values

    resp_peaks = detect_resp_cycles(
        resp_signal
    )

    ecg_signal = df_view['ecg'].values

    r_peaks, _ = find_peaks(
        ecg_signal,
        distance=500,
        height=np.mean(ecg_signal)
    )

    phases, cycle_numbers = compute_resp_phase(
        r_peaks,
        resp_peaks
    )
    df_sync = build_synchrogram_dataframe(
        r_peaks,
        phases,
        cycle_numbers
    )

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df_view['czas'],
        y=df_view['ecg'],
        mode='lines',
        name='EKG',
        line=dict(
            color=czerwony,
            width=2
        )
    ))

    fig.add_trace(go.Scatter(
        x=df_view['czas'],
        y=df_view['resp'],
        mode='lines',
        name='Oddech',
        line=dict(
            color=żółty,
            width=2
        ),
        yaxis='y2'
    ))

    fig.update_layout(
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',

        xaxis=dict(
            title='Czas [s]'
        ),

        yaxis=dict(
            title='EKG'
        ),

        yaxis2=dict(
            title='Oddech',
            overlaying='y',
            side='right'
        ),

        legend=dict(
            orientation='h',
            y=1.02
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        key="resp_plot"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(f"""
        <p style="
            font-size:14px;
            color:white;
            text-align:center;
        ">
        Cykle oddechowe<br>
        <span style="
            color:#dfff4f;
            font-weight:700;
            font-size:30px;
        ">
        {len(resp_peaks)}
        </span>
        </p>
        """, unsafe_allow_html=True)



    with col2:

        st.markdown(f"""
        <p style="
            font-size:14px;
            color:white;
            text-align:center;
        ">
        R-peaki<br>
        <span style="
            color:#dfff4f;
            font-weight:700;
            font-size:30px;
        ">
        {len(r_peaks)}
        </span>
        </p>
        """, unsafe_allow_html=True)



    with col3:

        st.markdown(f"""
        <p style="
            font-size:14px;
            color:white;
            text-align:center;
        ">
        Obliczone fazy<br>
        <span style="
            color:#dfff4f;
            font-weight:700;
            font-size:30px;
        ">
        {len(phases)}
        </span>
        </p>
        """, unsafe_allow_html=True)



    st.markdown("""
    <hr style="
        margin-top:10px;
        margin-bottom:30px;
        height:3px;
        border:none;
        background-color:#5c5c5c;
    ">
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <p style="
        color:#ffdd00;
        font-size:18px;
        font-weight:700;
        margin-bottom:25px;
    ">
    Synchrogram liniowy
    </p>
    """, unsafe_allow_html=True)

    col_left, col_right = st.columns([4, 1.3])

    with col_right:

        liczba_cykli = st.slider(
            "Liczba cykli",
            1,
            int(df_sync['cykl'].max()) + 1,
            10
        )

        df_sync_filtered = df_sync[
            df_sync['cykl'] < liczba_cykli
        ]

        st.markdown("<br>", unsafe_allow_html=True)

        st.dataframe(

            df_sync_filtered[[
                'czas',
                'faza_deg',
                'cykl'
            ]].head(10),

            use_container_width=True,
            height=350
        )

    with col_left:
            
        fig_sync = go.Figure()

        fig_sync.add_trace(go.Scatter(

            x=df_sync_filtered['czas'],

            y=df_sync_filtered['faza_deg'],

            mode='lines+markers',

            line=dict(
            width=2
        ),

            marker=dict(
                size=8,
                color=df_sync_filtered['cykl'],
                colorscale='Turbo',
                showscale=False
            ),

            name='Faza oddechu'
        ))

        fig_sync.update_layout(

            height=500,

            paper_bgcolor='rgba(0,0,0,0)',

            plot_bgcolor='rgba(0,0,0,0)',

            xaxis=dict(
                title='Czas [s]'
            ),

            yaxis=dict(
                title='Faza oddechu [°]',
                range=[0, 360]
            )
        )

        st.plotly_chart(
            fig_sync,
            use_container_width=True,
            key='linear_sync'
        )

    st.markdown("""
    <hr style="
        margin-top:10px;
        margin-bottom:30px;
        height:3px;
        border:none;
        background-color:#5c5c5c;
    ">
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <p style="
        color:#ffdd00;
        font-size:18px;
        font-weight:700;
        margin-bottom:25px;
    ">
    Synchrogram kołowy
    </p>
    """, unsafe_allow_html=True)

    fig_polar = go.Figure()

    colors = [
    cyjan,
    neon_yellow,
    neon_pink,
    neon_green,
    neon_orange,
    neon_purple
]

    for i, beat in enumerate(sorted(df_sync_filtered['beat'].unique())):

        df_beat = df_sync_filtered[
            df_sync_filtered['beat'] == beat
        ]

        color = colors[i % len(colors)]

        for _, row in df_beat.iterrows():

            fig_polar.add_trace(
                go.Scatterpolar(
                    r=[0, row['cykl']],
                    theta=[row['faza_deg'], row['faza_deg']],
                    mode='lines',
                    line=dict(color=color, width=2.5),
                    opacity=0.65,
                    showlegend=False,
                    hoverinfo='skip'
                )
            )

        fig_polar.add_trace(
            go.Scatterpolar(
                r=df_beat['cykl'],
                theta=df_beat['faza_deg'],
                mode='markers',
                marker=dict(
                    size=12,
                    color=color,
                    line=dict(color='rgba(255,255,255,0.9)', width=2)
                ),
                name=f'Beat {beat}',
                hovertemplate=
                    "<b>Beat:</b> %{text}<br>" +
                    "<b>Cykl:</b> %{r}<br>" +
                    "<b>Faza:</b> %{theta:.1f}°<extra></extra>",
                text=[beat] * len(df_beat)
            )
        )

    fig_polar.update_layout(
        height=680,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,

        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(color='white', size=12),
            bgcolor='rgba(255,255,255,0.3)',
            bordercolor='rgba(255,255,255,0.8)',
            borderwidth=1
        ),

        margin=dict(l=40, r=40, t=40, b=40),

        polar=dict(
            bgcolor='rgba(0,0,0,0)',

            radialaxis=dict(
                range=[0, df_sync_filtered['cykl'].max() + 1],
                color='white',
                gridcolor='rgba(255,255,255,0.28)',
                linecolor='rgba(255,255,255,0.3)',
                tickfont=dict(color='white', size=12),
                gridwidth=1
            ),

            angularaxis=dict(
                color='white',
                gridcolor='rgba(255,255,255,0.28)',
                linecolor='rgba(255,255,255,0.3)',
                tickfont=dict(color='white', size=14),
                direction='clockwise',
                rotation=90
            )
        )
    )

    st.plotly_chart(
        fig_polar,
        use_container_width=True,
        key='polar_sync'
    )