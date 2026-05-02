import streamlit as st
import datetime
import io

# ─────────────────────────────────────────────────────────────────────────────
# 1. CONFIGURACIÓN GENERAL
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SAT ECO-JUNCA | Sistema de Alerta Temprana",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# 2. ESTILOS — Paleta Eco-Junca (verde oliva / lima / teal)
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fondo general ── */
.stApp { background-color: #F7F8F5; }

/* ── Header principal ── */
.main-header {
    background: linear-gradient(135deg, #2D4A1E 0%, #3A6B28 100%);
    padding: 28px 30px 22px 30px;
    color: white;
    border-radius: 12px;
    text-align: center;
    margin-bottom: 28px;
    border-bottom: 5px solid #6AAF18;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}
.main-header h1 { font-size: 1.8rem; margin: 0 0 6px 0; letter-spacing: 1px; }
.main-header p  { font-size: 0.95rem; margin: 0; opacity: 0.88; }

/* ── Tarjeta técnica neutra ── */
.tech-card {
    background-color: #FFFFFF;
    padding: 18px 22px;
    border-radius: 10px;
    border-left: 8px solid #2D4A1E;
    margin-bottom: 18px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.07);
}

/* ── Alertas del semáforo ── */
.alert-red {
    background-color: #FFEBEE;
    padding: 22px 24px;
    border-radius: 10px;
    border-left: 10px solid #C62828;
    color: #7F0000;
    box-shadow: 0 3px 8px rgba(198,40,40,0.15);
}
.alert-yellow {
    background-color: #FFFDE7;
    padding: 22px 24px;
    border-radius: 10px;
    border-left: 10px solid #F9A825;
    color: #5D4037;
    box-shadow: 0 3px 8px rgba(249,168,37,0.15);
}
.alert-green {
    background-color: #E8F5E9;
    padding: 22px 24px;
    border-radius: 10px;
    border-left: 10px solid #2E7D32;
    color: #1B5E20;
    box-shadow: 0 3px 8px rgba(46,125,50,0.15);
}

/* ── Badges de estado fenológico ── */
.fenol-badge {
    display: inline-block;
    background-color: #2D4A1E;
    color: white;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: bold;
    margin-top: 4px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] { background-color: #2D4A1E; }
[data-testid="stSidebar"] * { color: white !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 0.93rem; }

/* ── Separador visual ── */
.divider-green {
    border: none;
    height: 3px;
    background: linear-gradient(to right, #6AAF18, #026E7A);
    border-radius: 2px;
    margin: 18px 0;
}

/* ── Nota de pie ── */
.nota-pie {
    font-size: 0.78rem;
    color: #666;
    font-style: italic;
    margin-top: 6px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# 3. BASES DE DATOS TÉCNICAS
# ─────────────────────────────────────────────────────────────────────────────

# Insumos y sus factores de riesgo hídrico
# Factor de dilución: volumen de agua (L) que se requiere para diluir 1 kg/L
# de insumo hasta concentración de referencia de inocuidad según literatura
INSUMOS_DB = {
    "UREA (Nitrógeno al 46%)": {
        "clase": "Fertilizante nitrogenado sintético",
        "cat_toxicologica": "No aplica (nutriente)",
        "riesgo_hidrico": "Aporte directo de nitratos (NO₃⁻). Riesgo alto de eutrofización acelerada "
                          "en ecosistemas lénticos. La concentración crítica de N-NO₃ para "
                          "eutrofización es ≥ 0.3 mg/L [Ref. IDEAM, 2022].",
        "factor_disolucion": 3333,   # litros/kg para llegar a 0.3 mg/L (46% N → 460 g N/kg)
        "unidad": "kg",
        "accion_preventiva": "Fraccionar la dosis en 3 aplicaciones. Nunca aplicar antes de lluvia. "
                             "Incorporar al suelo para minimizar escorrentía."
    },
    "FOSFATO DIAMÓNICO (DAP)": {
        "clase": "Fertilizante fosforado-nitrogenado",
        "cat_toxicologica": "No aplica (nutriente)",
        "riesgo_hidrico": "Aporte de fósforo (P). Detonante principal de floración algal (buchón de agua) "
                          "por escorrentía superficial. Concentración crítica P-total ≥ 0.025 mg/L [POMCA, 2022].",
        "factor_disolucion": 18000,  # litros/kg (46% P₂O₅ → ~200 g P/kg; límite 0.025 mg/L)
        "unidad": "kg",
        "accion_preventiva": "Aplicar en banda, no al voleo. Respetar distancia mínima de 30 m de la ronda hídrica."
    },
    "CLORPIRIFOS": {
        "clase": "Insecticida organofosforado (Cat. II — Moderadamente peligroso)",
        "cat_toxicologica": "Categoría II",
        "riesgo_hidrico": "Alta toxicidad aguda para macroinvertebrados acuáticos (LC₅₀ = 0.003 µg/L "
                          "en trucha arcoíris). Alta persistencia en sedimento bentónico (t½ = 30-60 días). "
                          "USO RESTRINGIDO bajo Res. ICA 30021.",
        "factor_disolucion": 2_000_000,  # LC50 ~0.003 µg/L → factor enorme
        "unidad": "litros",
        "accion_preventiva": "⚠️ PROHIBIDO en Escenario B. Sustituir por extractos de neem o rotación "
                             "con productos Cat. III. Nunca aplicar a menos de 100 m del lago."
    },
    "MANCOZEB": {
        "clase": "Fungicida ditiocarbamato (Cat. III — Ligeramente peligroso)",
        "cat_toxicologica": "Categoría III",
        "riesgo_hidrico": "Contiene Manganeso (Mn) y Zinc (Zn). Riesgo de bioacumulación en microfauna "
                          "edáfica y lixiviación freática. Límite Zn en agua: 0.5 mg/L [Res. 2115/2007].",
        "factor_disolucion": 6250,   # 80% Mancozeb, ~5% Zn → 50 g Zn/kg; límite 0.5 mg/L
        "unidad": "kg",
        "accion_preventiva": "Rotar con fungicidas biológicos (Trichoderma spp.). Respetar período de "
                             "carencia de 7 días. Usar con EPP completo (Cat. III)."
    },
    "GALLINAZA CRUDA": {
        "clase": "Enmienda orgánica sin compostaje",
        "cat_toxicologica": "No aplica (residuo orgánico)",
        "riesgo_hidrico": "Aporte crítico de coliformes totales, DBO (Demanda Biológica de Oxígeno) y "
                          "patógenos entéricos si hay lavado pluvial. Nitrógeno amoniacal (NH₄⁺) "
                          "disponible para lixiviación inmediata.",
        "factor_disolucion": 500,    # 30% MO húmeda → DBO elevada; factor conservador
        "unidad": "kg",
        "accion_preventiva": "Sustituir por compost maduro (mínimo 60 días). Si se usa, incorporar "
                             "inmediatamente al suelo y no aplicar con pronóstico de lluvia."
    },
    "IPRODIONE (Fungicida)": {
        "clase": "Fungicida dicarboximida (Cat. III)",
        "cat_toxicologica": "Categoría III",
        "riesgo_hidrico": "Moderada persistencia en suelo (t½ = 14-21 días). Posible disrupción endocrina "
                          "en organismos acuáticos a concentraciones > 0.1 µg/L.",
        "factor_disolucion": 10000,
        "unidad": "litros",
        "accion_preventiva": "Aplicar solo al superar UDE. Respetar carencia de 14 días antes de cosecha."
    },
    "METAMIDOFOS": {
        "clase": "Insecticida organofosforado (Cat. I — Altamente peligroso)",
        "cat_toxicologica": "Categoría I — USO PROHIBIDO (Res. ICA 970/2010)",
        "riesgo_hidrico": "⚠️ PROHIBIDO en Colombia. Extremadamente tóxico para fauna acuática y "
                          "humanos. DL₅₀ oral = 20 mg/kg. No debe usarse bajo ninguna circunstancia.",
        "factor_disolucion": 5_000_000,
        "unidad": "litros",
        "accion_preventiva": "NO USAR. Reportar a ICA si se detecta uso en el territorio. "
                             "Sustituir por productos Cat. III autorizados."
    }
}

# Estados fenológicos de Allium fistulosum L.
ESTADOS_FENOLOGICOS = {
    "Germinación / Plántula (0 – 15 días)": {
        "descripcion": "La planta está en su etapa más vulnerable. El sistema radicular es superficial "
                       "y la capacidad de tolerar estrés químico es mínima.",
        "riesgo_extra": "ALTO",
        "recomendacion": "Evitar cualquier aplicación fitosanitaria. Priorizar condiciones "
                         "de humedad estable y control mecánico de arvenses.",
        "umbral_ajuste": 0.5   # multiplica el UDE (más sensible)
    },
    "Desarrollo vegetativo (15 – 60 días)": {
        "descripcion": "Fase de crecimiento activo del pseudotallo. Mayor demanda nutricional "
                       "y susceptibilidad a Mildiu velloso y Trips.",
        "riesgo_extra": "MEDIO",
        "recomendacion": "Monitorear semanalmente. Aplicar solo si se supera el UDE. "
                         "Priorizar Cat. III y biopreparados.",
        "umbral_ajuste": 1.0
    },
    "Maduración / Pre-cosecha (60 – 90 días)": {
        "descripcion": "El pseudotallo está en engrosamiento final. Período crítico para "
                       "el cumplimiento de períodos de carencia.",
        "riesgo_extra": "CRÍTICO",
        "recomendacion": "Respetar estrictamente los períodos de carencia de todos los "
                         "productos aplicados. Prohibir Cat. I y II.",
        "umbral_ajuste": 1.5   # más tolerante, pero carencia es prioritaria
    },
    "Cosecha inminente (< 15 días)": {
        "descripcion": "Período de carencia activo. Cualquier aplicación residual representa "
                       "riesgo directo para el consumidor y viola la Res. ICA 30021.",
        "riesgo_extra": "CRÍTICO — PERÍODO DE CARENCIA",
        "recomendacion": "SUSPENSIÓN ABSOLUTA de aplicaciones químicas. Solo control manual.",
        "umbral_ajuste": 2.0
    }
}


# ─────────────────────────────────────────────────────────────────────────────
# 4. BARRA LATERAL
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌱 SAT ECO-JUNCA")
    st.markdown("**Sistema de Alerta Temprana**")
    st.markdown("*Producción Más Limpia · Lago de Tota*")
    st.markdown("---")
    menu = st.radio(
        "MÓDULOS DE GESTIÓN:",
        [
            "🚦  1. Alerta Temprana (Semáforo)",
            "⚗️  2. Modelación de Cargas",
            "🗺️  3. Zonificación de Riesgo",
            "📊  4. Escenarios de Transición",
        ],
        label_visibility="visible"
    )
    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.78rem; opacity:0.75;'>"
        "Prototipo de Ingeniería Ambiental<br>"
        "Isabela Orozco Echeverría<br>"
        "Dir: Viviana Osorno<br>"
        "Universidad El Bosque · 2026"
        "</div>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────────────────
# ── MÓDULO 1: ALERTA TEMPRANA (SEMÁFORO AMBIENTAL) ──────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
if "1." in menu:
    st.markdown(
        "<div class='main-header'>"
        "<h1>🚦 MÓDULO DE ALERTA TEMPRANA</h1>"
        "<p>Protocolo Semáforo Ambiental · Evaluación de Riesgo de Escorrentía y Lixiviación · "
        "Cuenca Lago de Tota [Res. ICA 30021 / POMCA Corpoboyacá 2022]</p>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown("### ⚙️ Parametrización del Entorno — Ingreso de las 4 Variables")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("**1. Variable Meteorológica**")
        lluvia = st.radio(
            "Pronóstico de precipitación (24 h):",
            ["No (Clima seco)", "Sí (Lluvia inminente)"],
            help="Consultar el IDEAM o la aplicación del SNIRH para el pronóstico local."
        )

    with col2:
        st.markdown("**2. Variable Agronómica**")
        dias_cosecha = st.number_input(
            "Días para el corte (cosecha):",
            min_value=0, max_value=120, value=30,
            help="Período de carencia crítico: < 15 días activa automáticamente Alerta Roja [Res. ICA 30021]."
        )

    with col3:
        st.markdown("**3. Variable Biológica**")
        plaga = st.radio(
            "Incidencia de plaga respecto al UDE:",
            ["Bajo (no supera el UDE)", "Alto (supera el UDE)"],
            help="UDE: Umbral de Daño Económico. Aplicar solo si la plaga lo supera (Principio MIP)."
        )

    with col4:
        st.markdown("**4. Estado Fenológico** *(Allium fistulosum L.)*")
        fenologia = st.selectbox(
            "Etapa actual del cultivo:",
            list(ESTADOS_FENOLOGICOS.keys()),
            help="La vulnerabilidad de la planta varía según su etapa de desarrollo. "
                 "Ajusta la sensibilidad del protocolo [Bornacelli, 2025]."
        )

    st.markdown("<hr class='divider-green'>", unsafe_allow_html=True)

    # ── Información del estado fenológico seleccionado ──
    fenol_info = ESTADOS_FENOLOGICOS[fenologia]
    st.markdown(
        f"<div class='tech-card'>"
        f"<b>📌 Estado fenológico seleccionado:</b> {fenologia}<br>"
        f"<b>Descripción:</b> {fenol_info['descripcion']}<br>"
        f"<b>Riesgo adicional:</b> <span class='fenol-badge'>{fenol_info['riesgo_extra']}</span><br>"
        f"<b>Recomendación específica:</b> {fenol_info['recomendacion']}"
        f"</div>",
        unsafe_allow_html=True
    )

    ejecutar = st.button("🔍 EJECUTAR EVALUACIÓN DE RIESGO AMBIENTAL", use_container_width=True)

    if ejecutar:
        st.markdown("### 📊 Resultado de la Evaluación:")

        # ── Lógica del semáforo (4 variables) ──────────────────────────────
        carencia_activa      = dias_cosecha < 15
        fenol_critica        = fenologia == "Cosecha inminente (< 15 días)"
        lluvia_activa        = lluvia == "Sí (Lluvia inminente)"
        plaga_supera_ude     = plaga == "Alto (supera el UDE)"
        fenol_plantula       = fenologia == "Germinación / Plántula (0 – 15 días)"

        # ROJO: lluvia o carencia activa o fenología de cosecha inminente
        if lluvia_activa or carencia_activa or fenol_critica:
            causas = []
            if lluvia_activa:
                causas.append("pronóstico de precipitación en las próximas 24 h")
            if carencia_activa or fenol_critica:
                causas.append(f"período de carencia activo ({dias_cosecha} días para cosecha)")
            causas_txt = " + ".join(causas).capitalize()

            st.markdown(
                f"<div class='alert-red'>"
                f"<h2>🛑 ALERTA ROJA: RIESGO CRÍTICO</h2>"
                f"<b>INSTRUCCIÓN: SUSPENSIÓN ABSOLUTA DE ASPERSIÓN QUÍMICA.</b><br><br>"
                f"<b>Causas activadas:</b> {causas_txt}.<br><br>"
                f"<b>Justificación técnica:</b> El pronóstico de precipitación generará "
                f"escorrentía superficial y lixiviación directa de ingredientes activos hacia la "
                f"ronda hídrica del Lago de Tota. Aplicar con período de carencia &lt; 15 días "
                f"vulnera la normatividad sanitaria vigente (Res. ICA 30021 / POMCA 2022) y "
                f"representa un riesgo directo para el consumidor final.<br><br>"
                f"<b>Acciones permitidas:</b> control manual de arvenses, revisión de infraestructura "
                f"de drenaje, instalación de trampas cromáticas."
                f"</div>",
                unsafe_allow_html=True
            )

        # AMARILLO: clima seco, carencia no activa, PERO plaga no supera UDE
        # O fenología de plántula (demasiado vulnerable aunque no haya plaga)
        elif not plaga_supera_ude or fenol_plantula:
            razon = ("la población de plaga no ha superado el Umbral de Daño Económico (UDE)"
                     if not plaga_supera_ude
                     else "el cultivo se encuentra en etapa de plántula (máxima vulnerabilidad)")
            st.markdown(
                f"<div class='alert-yellow'>"
                f"<h2>⚠️ ALERTA AMARILLA: RIESGO CONTROLADO</h2>"
                f"<b>INSTRUCCIÓN: NO APLICAR QUÍMICOS. ACTIVAR CONTROL FÍSICO Y CULTURAL.</b><br><br>"
                f"<b>Justificación técnica:</b> El clima es seco y el período de carencia no está "
                f"activo, sin embargo {razon}. Introducir carga química al sistema suelo-agua "
                f"es innecesario e ineficiente en estas condiciones [MIP — Principio del UDE].<br><br>"
                f"<b>Acciones recomendadas:</b> instalación o mantenimiento de trampas cromáticas "
                f"(amarillas para trips, azules para minadores), monitoreo de plantas centinela, "
                f"aplicación de caldos biológicos preventivos (Trichoderma, Bacillus subtilis)."
                f"</div>",
                unsafe_allow_html=True
            )

        # VERDE: clima seco + carencia no activa + plaga supera UDE
        else:
            st.markdown(
                "<div class='alert-green'>"
                "<h2>✅ ALERTA VERDE: VENTANA DE INTERVENCIÓN RACIONAL</h2>"
                "<b>INSTRUCCIÓN: APLICACIÓN AUTORIZADA CON RESTRICCIÓN A CATEGORÍA III.</b><br><br>"
                "<b>Justificación técnica:</b> Las condiciones climáticas minimizan el riesgo de "
                "transporte de contaminantes. La superación del Umbral de Daño Económico (UDE) "
                "justifica la intervención fitosanitaria. Se aplica el Principio de Manejo Integrado "
                "de Plagas (MIP) [Res. ICA 30021 / Rodríguez-Robayo et al., 2022].<br><br>"
                "<b>Restricciones obligatorias:</b><br>"
                "• Utilizar exclusivamente moléculas de baja toxicidad (Categoría III).<br>"
                "• Respetar dosificaciones de etiqueta — no sobredosificar.<br>"
                "• Uso completo de EPP (traje, guantes, careta, botas).<br>"
                "• Respetar el período de carencia del producto seleccionado.<br>"
                "• No mezclar más de 2 productos en la misma jornada."
                "</div>",
                unsafe_allow_html=True
            )

        # ── Generar reporte descargable ──────────────────────────────────────
        st.markdown("<hr class='divider-green'>", unsafe_allow_html=True)
        fecha_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

        if lluvia_activa or carencia_activa or fenol_critica:
            nivel = "ROJA — RIESGO CRÍTICO"
        elif not plaga_supera_ude or fenol_plantula:
            nivel = "AMARILLA — RIESGO CONTROLADO"
        else:
            nivel = "VERDE — INTERVENCIÓN AUTORIZADA"

        reporte_txt = f"""
SAT ECO-JUNCA — REPORTE DE EVALUACIÓN AMBIENTAL
================================================
Fecha y hora : {fecha_hora}
Generado por : SAT Eco-Junca (Prototipo v2.0)
               Programa Ingeniería Ambiental | Universidad El Bosque

─── PARÁMETROS INGRESADOS ─────────────────────
1. Variable meteorológica   : {lluvia}
2. Días para cosecha        : {dias_cosecha} días
3. Incidencia de plaga      : {plaga}
4. Estado fenológico        : {fenologia}

─── RESULTADO ─────────────────────────────────
NIVEL DE ALERTA: {nivel}

─── RECOMENDACIÓN FENOLÓGICA ──────────────────
{fenol_info['recomendacion']}

─── FUNDAMENTO NORMATIVO ──────────────────────
• Res. ICA 30021/2017 (BPA — Períodos de Carencia)
• POMCA Corpoboyacá 2022 (Ronda hídrica — 30 m)
• Decreto 1072 SGSST (EPP obligatorio)
• Principios MIP (Umbral de Daño Económico)

Este reporte fue generado automáticamente.
Consúltelo con su asistente técnico agropecuario.
"""
        buffer = io.BytesIO(reporte_txt.encode("utf-8"))
        st.download_button(
            label="📥 Descargar reporte de esta evaluación (.txt)",
            data=buffer,
            file_name=f"EcoJunca_Reporte_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
            use_container_width=True
        )


# ─────────────────────────────────────────────────────────────────────────────
# ── MÓDULO 2: MODELACIÓN DE CARGAS CONTAMINANTES ─────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
elif "2." in menu:
    st.markdown(
        "<div class='main-header'>"
        "<h1>⚗️ MODELACIÓN DE CARGAS CONTAMINANTES</h1>"
        "<p>Estimación del volumen hídrico comprometido por ingrediente activo aplicado · "
        "Cuenca Lago de Tota</p>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='tech-card'>"
        "<b>Fundamento metodológico:</b> El <i>volumen de agua comprometido</i> se estima a partir "
        "del factor de dilución de cada insumo: volumen de agua (L) necesario para diluir 1 kg o 1 L "
        "del ingrediente activo hasta su concentración de referencia de inocuidad según normativa "
        "vigente (Res. 2115/2007 — criterios de calidad de agua; límites de ecotoxicidad acuática "
        "IDEAM 2022). Este modelo es una proyección simplificada de carga potencial; no reemplaza "
        "un estudio de caracterización fisicoquímica en campo."
        "</div>",
        unsafe_allow_html=True
    )

    colA, colB = st.columns([1.1, 1])

    with colA:
        insumo_sel = st.selectbox(
            "Seleccione el ingrediente activo / insumo:",
            list(INSUMOS_DB.keys())
        )
        det = INSUMOS_DB[insumo_sel]

        cantidad = st.number_input(
            f"Cantidad aplicada ({det['unidad']}):",
            min_value=0.0, step=0.5,
            help="Ingrese el volumen o peso total del insumo aplicado en el ciclo de aspersión."
        )

        area_ha = st.number_input(
            "Área de aplicación (hectáreas):",
            min_value=0.1, max_value=10.0, value=1.0, step=0.1
        )

        coef_escorrentia = st.slider(
            "Coeficiente de escorrentía estimado (0.0 – 1.0):",
            min_value=0.0, max_value=1.0, value=0.35,
            help="0.0 = sin escorrentía (suelo muy absorbente). "
                 "1.0 = escorrentía total. "
                 "Para suelos de ladera compactados en Aquitania se recomienda 0.30–0.45."
        )

    with colB:
        st.markdown(
            f"<div class='tech-card'>"
            f"<b>Insumo:</b> {insumo_sel}<br>"
            f"<b>Clasificación:</b> {det['clase']}<br>"
            f"<b>Categoría toxicológica:</b> {det['cat_toxicologica']}<br><br>"
            f"<b>Riesgo hídrico:</b> {det['riesgo_hidrico']}<br><br>"
            f"<b>Acción preventiva recomendada:</b><br>{det['accion_preventiva']}"
            f"</div>",
            unsafe_allow_html=True
        )

    if cantidad > 0:
        st.markdown("<hr class='divider-green'>", unsafe_allow_html=True)
        st.markdown("### 📈 Resultados del modelo")

        # Cálculo: solo la fracción que escurre llega al cuerpo de agua
        carga_total_kg      = cantidad                             # kg o L aplicados
        fraccion_escorrentia = carga_total_kg * coef_escorrentia  # kg/L que escurren
        vol_agua_riesgo     = fraccion_escorrentia * det["factor_disolucion"]

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric(
                label=f"Carga aplicada ({det['unidad']})",
                value=f"{carga_total_kg:.1f} {det['unidad']}"
            )
        with col_m2:
            st.metric(
                label=f"Fracción en escorrentía ({coef_escorrentia:.0%})",
                value=f"{fraccion_escorrentia:.2f} {det['unidad']}"
            )
        with col_m3:
            st.metric(
                label="Volumen de agua comprometido (L)",
                value=f"{vol_agua_riesgo:,.0f} L",
                delta=f"≈ {vol_agua_riesgo/1000:,.1f} m³",
                delta_color="inverse"
            )

        # Equivalencia visual
        equiv_piscinas = vol_agua_riesgo / 2_500_000  # piscina olímpica ≈ 2,500 m³ = 2,500,000 L
        equiv_cisternas = vol_agua_riesgo / 1100      # cisterna estándar ≈ 1,100 L

        st.markdown(
            f"<div class='tech-card'>"
            f"<b>Equivalencia orientativa:</b> El volumen de agua que requeriría dilución representa "
            f"aproximadamente <b>{equiv_piscinas:.4f} piscinas olímpicas</b> o "
            f"<b>{equiv_cisternas:,.0f} cisternas domésticas</b>.<br>"
            f"<span class='nota-pie'>Nota: Modelo simplificado basado en factor de dilución hasta "
            f"concentración de referencia de inocuidad. Datos reales dependen de pendiente, "
            f"textura del suelo y condiciones hidrometeorológicas locales.</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        # Nivel de riesgo semafórico
        if vol_agua_riesgo > 10_000_000:
            st.error(f"🛑 **Riesgo CRÍTICO**: el volumen comprometido supera 10,000,000 L. "
                     f"Reducir dosis o sustituir el insumo inmediatamente.")
        elif vol_agua_riesgo > 1_000_000:
            st.warning(f"⚠️ **Riesgo ALTO**: el volumen comprometido supera 1,000,000 L. "
                       f"Revisar dosificación y condiciones de aplicación.")
        else:
            st.success(f"✅ **Riesgo MODERADO a BAJO**: volumen comprometido dentro de rangos "
                       f"manejables con prácticas adecuadas.")


# ─────────────────────────────────────────────────────────────────────────────
# ── MÓDULO 3: ZONIFICACIÓN DE RIESGO ─────────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
elif "3." in menu:
    st.markdown(
        "<div class='main-header'>"
        "<h1>🗺️ ZONIFICACIÓN DE VULNERABILIDAD HÍDRICA</h1>"
        "<p>Análisis de presión territorial del monocultivo sobre la ronda hídrica del Lago de Tota</p>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='tech-card'>"
        "<b>Marco conceptual:</b> El monocultivo intensivo en la ronda hídrica elimina la zona de "
        "amortiguación (buffer) natural. Esto convierte las prácticas agronómicas tradicionales en "
        "un vector directo de carga contaminante (N, P y plaguicidas sintéticos) hacia el lago. "
        "El POMCA de Corpoboyacá (2022) restringe actividades agrícolas en los primeros <b>30 metros</b> "
        "de la ronda hídrica; sin embargo, el diagnóstico de campo evidenció ocupación sistemática "
        "de esta franja de protección [POMCA 2022; Informante 5, entrevista semiestructurada]."
        "</div>",
        unsafe_allow_html=True
    )

    # ── Calculadora interactiva de riesgo por posición del predio ──────────
    st.markdown("### 📐 Calculadora de Riesgo por Posición del Predio")

    col1, col2 = st.columns(2)
    with col1:
        distancia_m = st.number_input(
            "Distancia del predio al espejo de agua del Lago de Tota (metros):",
            min_value=0, max_value=500, value=50,
            help="Medir desde el borde del cultivo hasta el nivel normal del lago."
        )
        pendiente_pct = st.slider(
            "Pendiente del terreno (%):",
            min_value=0, max_value=60, value=15,
            help="A mayor pendiente, mayor velocidad de escorrentía y menor infiltración."
        )
        cobertura_suelo = st.selectbox(
            "Cobertura vegetal entre el predio y el lago:",
            [
                "Sin cobertura (suelo desnudo o laboreo intensivo)",
                "Cobertura parcial (rastrojos, arvenses)",
                "Franja vegetada establecida (≥ 3 m de ancho)",
                "Franja riparia en buen estado (≥ 10 m)"
            ]
        )

    with col2:
        # Índice de riesgo territorial (0–100)
        # Factor distancia: < 30m = máximo riesgo
        if distancia_m < 30:
            factor_dist = 1.0
        elif distancia_m < 100:
            factor_dist = 0.7
        elif distancia_m < 200:
            factor_dist = 0.4
        else:
            factor_dist = 0.15

        factor_pendiente = min(pendiente_pct / 60, 1.0)

        cobertura_factor = {
            "Sin cobertura (suelo desnudo o laboreo intensivo)": 1.0,
            "Cobertura parcial (rastrojos, arvenses)": 0.65,
            "Franja vegetada establecida (≥ 3 m de ancho)": 0.35,
            "Franja riparia en buen estado (≥ 10 m)": 0.10
        }
        factor_cob = cobertura_factor[cobertura_suelo]

        indice_riesgo = round((factor_dist * 0.50 + factor_pendiente * 0.30 + factor_cob * 0.20) * 100)

        st.markdown("#### Índice de Riesgo Territorial (IRT)")
        if indice_riesgo >= 70:
            st.error(f"**IRT = {indice_riesgo} / 100 — RIESGO CRÍTICO**")
            estado_zona = "ZONA ROJA — Alta vulnerabilidad. El predio tiene alta probabilidad de "
            "aportar carga contaminante directa al lago por escorrentía superficial."
        elif indice_riesgo >= 40:
            st.warning(f"**IRT = {indice_riesgo} / 100 — RIESGO MODERADO**")
            estado_zona = "ZONA AMARILLA — Vulnerabilidad intermedia. Se recomienda establecer "
            "franja vegetada de amortiguación y reducir dosis de insumos."
        else:
            st.success(f"**IRT = {indice_riesgo} / 100 — RIESGO BAJO**")
            estado_zona = "ZONA VERDE — Vulnerabilidad controlada. Mantener las prácticas de "
            "cobertura y distancia establecidas."

        st.markdown(
            "<div class='tech-card'>"
            "<b>Composición del índice:</b><br>"
            f"• Distancia al lago: {factor_dist:.0%} de riesgo relativo<br>"
            f"• Pendiente del terreno: {factor_pendiente:.0%} de riesgo relativo<br>"
            f"• Factor de cobertura: {factor_cob:.0%} de riesgo relativo<br><br>"
            "<b>Fuente normativa:</b> POMCA Corpoboyacá 2022 — Ronda hídrica 30 m; "
            "Ecología de cuencas (zonas de amortiguación como filtros biológicos)."
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown("<hr class='divider-green'>", unsafe_allow_html=True)

    # ── Mapa conceptual de zonas ──────────────────────────────────────────
    st.markdown("### 🗂️ Zonificación de referencia — Cuenca Lago de Tota")

    col_z1, col_z2, col_z3 = st.columns(3)
    with col_z1:
        st.markdown(
            "<div style='background:#FFEBEE; border-left:8px solid #C62828; padding:16px; border-radius:8px;'>"
            "<b>🔴 ZONA ROJA (0–30 m)</b><br><br>"
            "Ronda hídrica protegida por POMCA. Prohibición de actividades agrícolas intensivas. "
            "Cualquier aplicación de agroquímicos genera escorrentía directa al lago. "
            "<br><br><b>Porcentaje de predios en esta zona según diagnóstico: ~35 %</b>"
            "</div>",
            unsafe_allow_html=True
        )
    with col_z2:
        st.markdown(
            "<div style='background:#FFFDE7; border-left:8px solid #F9A825; padding:16px; border-radius:8px;'>"
            "<b>🟡 ZONA AMARILLA (30–100 m)</b><br><br>"
            "Zona de transición. La escorrentía puede alcanzar el lago en eventos de lluvia intensa. "
            "Se recomienda franja vegetada de amortiguación de mínimo 10 m y reducción del 50 % "
            "en dosis de insumos nitrogenados."
            "</div>",
            unsafe_allow_html=True
        )
    with col_z3:
        st.markdown(
            "<div style='background:#E8F5E9; border-left:8px solid #2E7D32; padding:16px; border-radius:8px;'>"
            "<b>🟢 ZONA VERDE (> 100 m)</b><br><br>"
            "Zona con menor riesgo de contaminación directa. Sin embargo, la lixiviación "
            "vertical puede contaminar el nivel freático. Aplicar Semáforo Ambiental "
            "y protocolo de triple lavado de RESPEL."
            "</div>",
            unsafe_allow_html=True
        )

    st.markdown(
        "<div class='nota-pie' style='margin-top:14px;'>Fuente: POMCA Corpoboyacá (2022); "
        "Jaramillo-García et al. (2020); diagnóstico de campo Orozco Echeverría (2026).</div>",
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────────────────────────────────────
# ── MÓDULO 4: ESCENARIOS DE TRANSICIÓN ───────────────────────────────────────
# ─────────────────────────────────────────────────────────────────────────────
elif "4." in menu:
    st.markdown(
        "<div class='main-header'>"
        "<h1>📊 EVALUACIÓN DE ESCENARIOS AGRONÓMICOS DE TRANSICIÓN</h1>"
        "<p>Análisis comparativo de alternativas de manejo PML · Cuenca Lago de Tota · "
        "Basado en evaluación multicriterio + juicio de expertos [Orozco Echeverría, 2026]</p>"
        "</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "Seleccione un escenario para evaluar su viabilidad técnica, "
        "impacto financiero y carga contaminante proyectada."
    )

    tab1, tab2, tab3 = st.tabs([
        "🔴  Escenario A — Convencional (Línea Base)",
        "🟢  Escenario B — Manejo Integrado ★ Priorizado",
        "🌿  Escenario C — Agroecológico (Proyección futura)"
    ])

    # ── ESCENARIO A ──────────────────────────────────────────────────────────
    with tab1:
        st.markdown("### 🔴 Escenario A: Manejo Convencional (Línea Base)")
        st.markdown(
            "**Enfoque:** Netamente químico / preventivo — aplicación *'por calendario'*. "
            "Este escenario describe el modelo actual identificado en el diagnóstico territorial. "
            "La sobreaplicación responde a la aversión al riesgo económico documentada en las "
            "entrevistas semiestructuradas [Orozco Echeverría, 2026]."
        )

        col1, col2 = st.columns(2)
        with col1:
            st.error("**Protocolo operativo:**")
            st.write("• Aplicación fija cada 7–8 días sin monitoreo previo.")
            st.write("• Mezcla indiscriminada de moléculas Cat. I, II y III ('fumigación cóctel').")
            st.write("• Dosificación empírica delegada a vendedores de insumos.")
            st.write("• Sobredosis de gallinaza cruda para lograr 'cebolla verde oscura'.")
            st.write("• Uso nulo o mínimo de EPP.")
            st.write("• Disposición inadecuada de envases RESPEL.")
        with col2:
            st.metric(
                label="Reducción de carga contaminante vs. línea base",
                value="0 %",
                delta="Referencia — máxima contaminación",
                delta_color="inverse"
            )
            st.metric(label="Ciclos de aspersión por cosecha", value="~20 ciclos")
            st.metric(label="Ahorro en costos operativos", value="0 %", delta_color="off")
            st.metric(label="Riesgo de intoxicación ocupacional", value="ALTO", delta_color="off")

        st.info(
            "**Viabilidad social:** Alta inercia cultural. El productor percibe esta práctica "
            "como la única garantía contra la pérdida de cosecha. Sin embargo, es ambiental y "
            "económicamente insostenible a mediano plazo [UPRA, 2023]."
        )

    # ── ESCENARIO B ──────────────────────────────────────────────────────────
    with tab2:
        st.markdown("### 🟢 Escenario B: Manejo Integrado (Ruta Priorizada por Eco-Junca)")
        st.markdown(
            "**Enfoque:** Híbrido — químico racional + control cultural + biológico. "
            "Estrategia de transición diseñada y validada en este proyecto. Opera a través del "
            "**Semáforo Ambiental** y las herramientas duales Eco-Junca. Validado por juicio de "
            "3 expertos en ingeniería ambiental, agronomía y desarrollo rural (Likert 5 puntos)."
        )

        col1, col2 = st.columns(2)
        with col1:
            st.success("**Protocolo operativo:**")
            st.write("• **Regla fundamental:** aplicar SOLO si la plaga supera el UDE.")
            st.write("• Monitoreo semanal de plantas centinela antes de cualquier intervención.")
            st.write("• Restricción absoluta de aplicaciones con lluvia inminente o en período de carencia.")
            st.write("• Rotación de moléculas Cat. III alternadas con biopreparados (neem, Trichoderma).")
            st.write("• Reducción gradual de NPK e introducción de compostaje básico.")
            st.write("• EPP obligatorio en toda intervención química.")
            st.write("• Protocolo de triple lavado y perforación de envases RESPEL.")
        with col2:
            st.metric(
                label="Reducción de ciclos de aspersión",
                value="−40 %",
                delta="De 20 a 12 ciclos/cosecha",
                delta_color="normal"
            )
            st.metric(
                label="Ahorro neto en costos operativos",
                value="~30 %",
                delta="Proyección sobre estructura UPRA 2023",
                delta_color="normal"
            )
            st.metric(
                label="Reducción de carga contaminante",
                value="~40 %",
                delta="Proyección teórica (validación pendiente en parcelas)",
                delta_color="normal"
            )
            st.metric(label="Riesgo de intoxicación ocupacional", value="REDUCIDO", delta_color="off")

        st.success(
            "**Viabilidad (óptimo técnico-social):** Equilibrio entre protección del recurso hídrico "
            "y viabilidad económica del productor. Es la única trayectoria socialmente viable para "
            "Aquitania en el corto plazo. Mantiene la red de seguridad financiera mientras demuestra "
            "que reducir la dosificación es más rentable."
        )

        st.markdown(
            "<div class='nota-pie'>"
            "Nota metodológica: Los porcentajes de ahorro y reducción de carga son proyecciones "
            "teóricas basadas en la frecuencia de aspersión declarada en las entrevistas, cruzada "
            "con la estructura de costos UPRA 2023 para cebolla junca en la región andina. "
            "La validación experimental en parcelas demostrativas es la principal recomendación "
            "de investigación futura."
            "</div>",
            unsafe_allow_html=True
        )

    # ── ESCENARIO C ──────────────────────────────────────────────────────────
    with tab3:
        st.markdown("### 🌿 Escenario C: Manejo Agroecológico (Proyección a Largo Plazo)")
        st.markdown(
            "**Enfoque:** Netamente sostenible / orgánico. Escenario ideal proyectado para la "
            "restauración total de la cuenca. Técnicamente deseable pero **socialmente inviable "
            "a corto plazo** en el contexto actual de Aquitania por la aversión al riesgo "
            "económico documentada en el diagnóstico [Orozco Echeverría, 2026]."
        )

        col1, col2 = st.columns(2)
        with col1:
            st.warning("**Protocolo operativo:**")
            st.write("• Cero síntesis química de cualquier categoría.")
            st.write("• Control exclusivo con alelopatía (ajo, ají) y biocontroladores.")
            st.write("• Insectos benéficos como agentes de control biológico.")
            st.write("• Nutrición 100 % con compost maduro (mínimo 60 días) y microorganismos eficientes.")
            st.write("• Certificación agroecológica progresiva (AGROSAVIA, 2022).")
        with col2:
            st.metric(
                label="Eliminación de carga química",
                value="100 %",
                delta="Protección total del ecosistema léntico",
                delta_color="normal"
            )
            st.metric(
                label="Riesgo financiero a corto plazo",
                value="ALTO",
                delta="Posible choque productivo por degradación del suelo",
                delta_color="inverse"
            )

        st.error(
            "**Viabilidad:** Inviable a corto plazo por la degradación actual del suelo y la "
            "profunda aversión al riesgo económico del productor. Imponer esta transición de "
            "forma abrupta generaría un choque frontal con la cultura de manejo local y "
            "aumentaría la percepción de riesgo de pérdida [Orozco Echeverría, 2026]. "
            "Se recomienda como meta de largo plazo (5–10 años) tras estabilizar el Escenario B."
        )
