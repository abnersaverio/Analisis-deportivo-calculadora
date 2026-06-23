import math
import streamlit as st

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(
    page_title="Calculadora de Pronósticos Deportivos",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Encabezado principal y botón de reinicio
col_titulo, col_reset = st.columns([4, 1])
with col_titulo:
    st.title("⚽ Motor de Pronósticos Avanzado v2.5")
    st.write("Análisis estadístico profesional con mercados Over/Under combinados, Hándicap y validación anti-errores.")
with col_reset:
    st.write("") 
    if st.button("🔄 Reiniciar Datos", use_container_width=True):
        st.rerun()

st.divider()

# --- PESTAÑAS DE ENTRADA DE DATOS ---
tab_datos, tab_h2h = st.tabs([
    "📋 Rendimiento de Local / Visitante", 
    "⚔️ Historial Directo (H2H)"
])

with tab_datos:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🏠 Datos del Local (Solo en CASA)")
        nombre_l = st.text_input("Nombre Equipo Local", value="Barcelona SC", key="nl")
        pj_l = st.number_input("Partidos de Local Analizados", min_value=1, value=5, key="pjl")
        v_l = st.number_input("Victorias de Local", min_value=0, value=3, key="vl")
        e_l = st.number_input("Empates de Local", min_value=0, value=1, key="el")
        goles_l = st.number_input("Goles a Favor en Casa (Total)", min_value=0, value=8, key="gl")
        goles_1t_l = st.number_input("⚽ Goles en 1er Tiempo en Casa (Total)", min_value=0, value=3, key="g1tl")
        corners_l = st.number_input("🚩 Corners Totales en Casa", min_value=0, value=25, key="cl")
        tarjetas_l = st.number_input("🟨 Tarjetas Totales en Casa", min_value=0, value=12, key="tl")

        st.markdown("**🎯 Frecuencias de Mercado (Partidos que cumplieron)**")
        f_goles_l = st.number_input("Partidos con +1.5 Goles Totales", min_value=0, value=3, key="fgl")
        f_goles25_l = st.number_input("Partidos con +2.5 Goles Totales", min_value=0, value=2, key="fg25l")
        f_corners_l = st.number_input("Partidos con +7.5 Corners Totales", min_value=0, value=3, key="fcl")

    with col2:
        st.markdown("### ✈️ Datos del Visitante (Solo FUERA)")
        nombre_v = st.text_input("Nombre Equipo Visitante", value="LDU Quito", key="nv")
        pj_v = st.number_input("Partidos de Visitante Analizados", min_value=1, value=5, key="pjv")
        v_v = st.number_input("Victorias de Visitante", min_value=0, value=2, key="vv")
        e_v = st.number_input("Empates de Visitante", min_value=0, value=2, key="ev")
        goles_v = st.number_input("Goles a Favor Fuera (Total)", min_value=0, value=5, key="gv")
        goles_1t_v = st.number_input("⚽ Goles en 1er Tiempo Fuera (Total)", min_value=0, value=2, key="g1tv")
        corners_v = st.number_input("🚩 Corners Totales Fuera", min_value=0, value=20, key="cv")
        tarjetas_v = st.number_input("🟨 Tarjetas Totales Fuera", min_value=0, value=15, key="tv")

        st.markdown("**🎯 Frecuencias de Mercado (Partidos que cumplieron)**")
        f_goles_v = st.number_input("Partidos con +1.5 Goles Totales ", min_value=0, value=3, key="fgv")
        f_goles25_v = st.number_input("Partidos con +2.5 Goles Totales ", min_value=0, value=1, key="fg25v")
        f_corners_v = st.number_input("Partidos con +7.5 Corners Totales ", min_value=0, value=2, key="fcv")

with tab_h2h:
    st.markdown("### ⚔️ Historial de Enfrentamientos Directos (H2H Recientes)")
    pj_h2h = st.number_input("Partidos H2H analizados", min_value=1, value=1, key="pjh2h")
    v_l_h2h = st.number_input(f"Victorias de {nombre_l}", min_value=0, value=0, key="vlh2h")
    e_h2h = st.number_input("Empates entre ambos", min_value=0, value=1, key="eh2h")
    v_v_h2h = int(pj_h2h) - int(v_l_h2h) - int(e_h2h)

st.divider()

# --- PROCESAMIENTO MATEMÁTICO ---
if st.button("🚀 CORRER SIMULACIÓN AVANZADA", use_container_width=True):
    
    # SISTEMA DE VALIDACIÓN CONTROLADA (Anti-Colapsos)
    errores = []
    if (v_l + e_l) > pj_l:
        errores.append(f"La suma de Victorias ({v_l}) y Empates ({e_l}) del Local supera los partidos jugados ({pj_l}).")
    if (v_v + e_v) > pj_v:
        errores.append(f"La suma de Victorias ({v_v}) y Empates ({e_v}) del Visitante supera los partidos jugados ({pj_v}).")
    if v_l_h2h + e_h2h > pj_h2h:
        errores.append(f"En la pestaña H2H, la suma de victorias y empates supera el total de partidos ({pj_h2h}).")
    if goles_1t_l > goles_l:
        errores.append(f"Los goles del 1er Tiempo del Local ({goles_1t_l}) superan sus goles totales ({goles_l}).")
    if goles_1t_v > goles_v:
        errores.append(f"Los goles del 1er Tiempo del Visitante ({goles_1t_v}) superan sus goles totales ({goles_v}).")

    if errores:
        for err in errores:
            st.warning(f"⚠️ {err}")
        st.error("Por favor, corrige los datos arriba antes de continuar.")
        st.stop()

    # Cálculos de Probabilidades Principales
    win_rate_l, draw_rate_l = v_l / pj_l, e_l / pj_l
    win_rate_v, draw_rate_v = v_v / pj_v, e_v / pj_v
    h2h_win_l, h2h_draw, h2h_win_v = v_l_h2h / pj_h2h, e_h2h / pj_h2h, v_v_h2h / pj_h2h

    prob_final_l = int(((win_rate_l * 0.7) + (h2h_win_l * 0.3)) * 100)
    prob_final_v = int(((win_rate_v * 0.7) + (h2h_win_v * 0.3)) * 100)
    prob_final_e = int((((draw_rate_l + draw_rate_v) / 2 * 0.7) + (h2h_draw * 0.3)) * 100)

    total_p = prob_final_l + prob_final_v + prob_final_e
    if total_p != 100 and total_p > 0:
        prob_final_l = int((prob_final_l / total_p) * 100)
        prob_final_v = int((prob_final_v / total_p) * 100)
        prob_final_e = 100 - prob_final_l - prob_final_v

    # Promedios y Proyecciones Aritméticas
    prom_g_l, prom_g_v = goles_l / pj_l, goles_v / pj_v
    total_goles = round(prom_g_l + prom_g_v, 2)

    prom_1t_l, prom_1t_v = goles_1t_l / pj_l, goles_1t_v / pj_v
    total_goles_1t = round(prom_1t_l + prom_1t_v, 2)

    prom_c_l, prom_c_v = corners_l / pj_l, corners_v / pj_v
    total_corners = round(prom_c_l + prom_c_v, 2)

    prom_t_l, prom_t_v = tarjetas_l / pj_l, tarjetas_v / pj_v
    total_tarjetas = round(prom_t_l + prom_t_v, 2)

    # Cálculo de Frecuencias de Mercado Empíricas (Over y Under)
    freq_over15 = int(((f_goles_l / pj_l) + (f_goles_v / pj_v)) / 2 * 100)
    freq_under15 = 100 - freq_over15

    freq_over25 = int(((f_goles25_l / pj_l) + (f_goles25_v / pj_v)) / 2 * 100)
    freq_under25 = 100 - freq_over25

    # Cambiado con éxito a la línea de +7.5 Corners
    freq_over75_c = int(((f_corners_l / pj_l) + (f_corners_v / pj_v)) / 2 * 100)
    freq_under75_c = 100 - freq_over75_c

    # Distribución de Poisson para Ambos Marcan y 1er Tiempo
    def poisson_pmf(lmbda, k):
        if lmbda == 0: return 1.0 if k == 0 else 0.0
        return (lmbda**k * math.exp(-lmbda)) / math.factorial(k)

    prob_l_cero = poisson_pmf(prom_g_l, 0)
    prob_v_cero = poisson_pmf(prom_g_v, 0)
    prob_ambos_marcan = int(((1 - prob_l_cero) * (1 - prob_v_cero)) * 100)
    prob_no_ambos_marcan = 100 - prob_ambos_marcan

    # Poisson para Goles en el 1er Tiempo
    prob_1t_cero = poisson_pmf(total_goles_1t, 0) * 100
    prob_1t_over05 = 100 - prob_1t_cero
    prob_1t_over15 = (1 - poisson_pmf(total_goles_1t, 0) - poisson_pmf(total_goles_1t, 1)) * 100
    prob_1t_under15 = 100 - prob_1t_over15

    # Marcadores Exactos
    resultados_exactos = []
    for i in range(5):  
        for j in range(5):  
            prob_marcador = poisson_pmf(prom_g_l, i) * poisson_pmf(prom_g_v, j) * 100
            resultados_exactos.append((f"{i} - {j}", prob_marcador))
    resultados_exactos.sort(key=lambda x: x[1], reverse=True)
    top_3_marcadores = resultados_exactos[:3]

    # Sugerencia de Hándicap Asiático
    margen_goles = prom_g_l - prom_g_v
    if margen_goles > 0.65: handicap_sugerido = f"{nombre_l} -0.5 o -1"
    elif margen_goles > 0.20: handicap_sugerido = f"{nombre_l} Hándicap Asiático 0 (DNB)"
    elif margen_goles < -0.65: handicap_sugerido = f"{nombre_v} -0.5 o -1"
    elif margen_goles < -0.20: handicap_sugerido = f"{nombre_v} Hándicap Asiático 0 (DNB)"
    else: handicap_sugerido = "Línea muy ajustada (Hándicap Asiático 0 / DNB)"

    # --- DESPLIEGUE EN INTERFAZ ---
    st.header(f"📊 Reporte de Inteligencia: {nombre_l} vs {nombre_v}")
    
    st.markdown("### 🏆 Predicción de Desenlace (Forma de Campo + H2H)")
    c1, c2, c3 = st.columns(3)
    c1.metric(f"Gana {nombre_l} (1)", f"{prob_final_l}%")
    c2.metric("Empate (X)", f"{prob_final_e}%")
    c3.metric(f"Gana {nombre_v} (2)", f"{prob_final_v}%")

    st.markdown("#### 🛡️ Mercados de Seguridad")
    am1, am2, am3, am4 = st.columns(4)
    am1.metric(f"1X ({nombre_l} o X)", f"{prob_final_l + prob_final_e}%")
    am2.metric(f"X2 ({nombre_v} o X)", f"{prob_final_v + prob_final_e}%")
    am3.metric("Ambos Marcan: SÍ", f"{prob_ambos_marcan}%")
    am4.metric("Ambos Marcan: NO", f"{prob_no_ambos_marcan}%")

    st.info(f"🎯 **Hándicap Sugerido:** {handicap_sugerido} | Margen de Goles: {round(margen_goles, 2)}")
    st.divider()

    # --- TOTALES + OVER/UNDER SIMULTÁNEOS ---
    st.markdown("### 📈 Análisis de Mercados Secundarios (Detalle Equipo + Over / Under)")
    
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    
    with col_m1:
        st.info("⚽ Goles Totales (90 Min)")
        st.write(f"Promedio {nombre_l} (Casa): **{prom_g_l:.1f}**")
        st.write(f"Promedio {nombre_v} (Fuera): **{prom_g_v:.1f}**")
        st.write(f"**Total Proyectado:** {total_goles}")
        st.write("---")
        st.metric("🟢 Over +1.5 Goles", f"{freq_over15}%")
        st.metric("🔴 Under -1.5 Goles", f"{freq_under15}%")
        st.metric("🟢 Over +2.5 Goles", f"{freq_over25}%")
        st.metric("🔴 Under -2.5 Goles", f"{freq_under25}%")

    with col_m2:
        st.success("⏱️ Goles 1er Tiempo")
        st.write(f"Promedio {nombre_l} (Casa): **{prom_1t_l:.1f}**")
        st.write(f"Promedio {nombre_v} (Fuera): **{prom_1t_v:.1f}**")
        st.write(f"**Total Proyectado 1T:** {total_goles_1t}")
        st.write("---")
        st.metric("🟢 Over +0.5 Goles 1T", f"{prob_1t_over05:.1f}%", help="Probabilidad estadística de gol antes del descanso")
        st.metric("🔴 Under -0.5 Goles 1T", f"{prob_1t_cero:.1f}%")
        st.metric("🟢 Over +1.5 Goles 1T", f"{prob_1t_over15:.1f}%")
        st.metric("🔴 Under -1.5 Goles 1T", f"{prob_1t_under15:.1f}%")

    with col_m3:
        st.warning("🚩 Tiros de Esquina")
        st.write(f"Promedio {nombre_l} (Casa): **{prom_c_l:.1f}**")
        st.write(f"Promedio {nombre_v} (Fuera): **{prom_c_v:.1f}**")
        st.write(f"**Total Proyectado:** {total_corners}")
        st.write("---")
        st.metric("🟢 Over +7.5 Corners", f"{freq_over75_c}%")
        st.metric("🔴 Under -7.5 Corners", f"{freq_under75_c}%")

    with col_m4:
        st.error("🟨 Tarjetas Amarillas")
        st.write(f"Promedio {nombre_l} (Casa): **{prom_t_l:.1f}**")
        st.write(f"Promedio {nombre_v} (Fuera): **{prom_t_v:.1f}**")
        st.write(f"**Total Proyectado:** {total_tarjetas}")
        st.write("---")
        if total_tarjetas < 4.5:
            st.metric("📉 Línea Sugerida", "Menos de 5.5", delta="Under Seguro")
        elif total_tarjetas < 5.5:
            st.metric("📉 Línea Sugerida", "Menos de 6.5", delta="Under Regular")
        else:
            st.metric("📈 Línea Sugerida", "Más de 4.5", delta="Alta Fricción", delta_color="inverse")

    st.divider()

    # Bloque: Marcadores Exactos
    st.markdown("### 🧮 Modelado de Poisson (Marcadores Exactos)")
    m1, m2, m3 = st.columns(3)
    m1.success(f"🥇 Opción 1: {top_3_marcadores[0][0]} ({round(top_3_marcadores[0][1], 1)}%)")
    m2.success(f"🥈 Opción 2: {top_3_marcadores[1][0]} ({round(top_3_marcadores[1][1], 1)}%)")
    m3.success(f"🥉 Opción 3: {top_3_marcadores[2][0]} ({round(top_3_marcadores[2][1], 1)}%)")