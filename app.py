import streamlit as st

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="SAT ECO-JUNCA | Gestión de Riesgo", page_icon="🚦", layout="wide")

# ESTILOS CSS
st.markdown("""
    <style>
    .main-header {background-color: #0D47A1; padding: 25px; color: white; border-radius: 10px; text-align: center; margin-bottom: 25px; border-bottom: 5px solid #1976D2;}
    .tech-card {background-color: #F5F5F5; padding: 20px; border-radius: 8px; border-left: 8px solid #424242; margin-bottom: 20px;}
    .alert-red {background-color: #FFEBEE; padding: 20px; border-radius: 8px; border-left: 10px solid #D32F2F; color: #B71C1C;}
    .alert-yellow {background-color: #FFFDE7; padding: 20px; border-radius: 8px; border-left: 10px solid #FBC02D; color: #F57F17;}
    .alert-green {background-color: #E8F5E9; padding: 20px; border-radius: 8px; border-left: 10px solid #388E3C; color: #1B5E20;}
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS TÉCNICA
insumos_db = {
    "UREA (Nitrógeno al 46%)": {"clase": "Fertilizante Sintético", "riesgo": "Aporte directo de nitratos. Riesgo alto de eutrofización acelerada en ecosistemas lénticos."},
    "FOSFATO DIAMÓNICO (DAP)": {"clase": "Fertilizante", "riesgo": "Aporte de fósforo. Detonante principal de floración algal (Buchón de agua) por escorrentía superficial."},
    "CLORPIRIFOS": {"clase": "Insecticida (Cat. I/II)", "riesgo": "Alta toxicidad aguda para macroinvertebrados acuáticos. Alta persistencia en sedimento bentónico."},
    "MANCOZEB": {"clase": "Fungicida (Cat. III)", "riesgo": "Contiene Manganeso y Zinc. Riesgo de bioacumulación en microfauna edáfica y lixiviación a nivel freático."},
    "GALLINAZA CRUDA": {"clase": "Enmienda Orgánica", "riesgo": "Aporte de coliformes totales y DBO (Demanda Biológica de Oxígeno) crítica si hay lavado pluvial."}
}

# 3. NAVEGACIÓN LATERAL
with st.sidebar:
    st.markdown("# 🚦 SAT ECO-JUNCA")
    st.write("### Sistema de Alerta Temprana")
    st.divider()
    menu = st.radio("MÓDULOS DE GESTIÓN:", [
        "1. Alerta Temprana (Semáforo)", 
        "2. Modelación de Cargas", 
        "3. Zonificación de Riesgo",
        "4. Escenarios de Transición"
    ])
    st.divider()
    st.caption("Prototipo de Ingeniería Ambiental | Isabela Orozco E.")

# --- MÓDULO 1: ALERTA TEMPRANA ---
if menu == "1. Alerta Temprana (Semáforo)":
    st.markdown("<div class='main-header'><h1>MÓDULO DE ALERTA TEMPRANA</h1><p>Evaluación de Riesgo de Escorrentía y Lixiviación</p></div>", unsafe_allow_html=True)
    
    st.write("### ⚙️ Parametrización del Entorno (Ingreso de Datos)")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**1. Variable Meteorológica**")
        lluvia = st.radio("Pronóstico de precipitación (24h):", ["No (Clima Seco)", "Sí (Lluvia inminente)"])
    with col2:
        st.markdown("**2. Variable Agronómica**")
        dias_cosecha = st.number_input("Días para el corte (Cosecha):", min_value=0, max_value=120, value=30)
    with col3:
        st.markdown("**3. Variable Biológica**")
        plaga = st.radio("Incidencia de plaga (Umbral):", ["Bajo (No supera UDE)", "Alto (Supera UDE)"])

    st.divider()
    
    if st.button("EJECUTAR EVALUACIÓN DE RIESGO AMBIENTAL", use_container_width=True):
        st.write("### 📊 Resultado de la Evaluación:")
        if lluvia == "Sí (Lluvia inminente)" or dias_cosecha < 15:
            st.markdown("<div class='alert-red'><h2>🛑 ALERTA ROJA: RIESGO CRÍTICO</h2><b>INSTRUCCIÓN: SUSPENSIÓN ABSOLUTA DE ASPERSIÓN QUÍMICA.</b><br><br><b>Justificación Técnica:</b> El pronóstico de precipitación generará escorrentía superficial y lixiviación directa de ingredientes activos hacia la ronda hídrica del Lago de Tota. Aplicar con periodo de carencia < 15 días vulnera la normatividad sanitaria (Res. ICA 30021).</div>", unsafe_allow_html=True)
        elif plaga == "Bajo (No supera UDE)":
            st.markdown("<div class='alert-yellow'><h2>⚠️ ALERTA AMARILLA: RIESGO CONTROLADO</h2><b>INSTRUCCIÓN: NO APLICAR QUÍMICOS. USO DE CONTROL FÍSICO.</b><br><br><b>Justificación Técnica:</b> La población plaga no ha superado el Umbral de Daño Económico (UDE). Introducir carga química al ecosistema es innecesario. Se recomienda instalación o mantenimiento de trampas cromáticas.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='alert-green'><h2>✅ ALERTA VERDE: VENTANA SEGURA</h2><b>INSTRUCCIÓN: APLICACIÓN AUTORIZADA (RESTRICCIÓN A CAT. III).</b><br><br><b>Justificación Técnica:</b> Condiciones secas que minimizan el riesgo de transporte de contaminantes. La superación del UDE justifica la intervención. Utilice exclusivamente moléculas de baja toxicidad, respete dosificación y garantice uso de EPP.</div>", unsafe_allow_html=True)

# --- MÓDULO 2: MODELACIÓN DE CARGAS ---
elif menu == "2. Modelación de Cargas":
    st.markdown("<div class='main-header'><h1>MODELACIÓN DE CARGAS CONTAMINANTES</h1></div>", unsafe_allow_html=True)
    st.write("Evaluación proyectada del impacto residual en el ecosistema léntico (Lago de Tota).")
    
    colA, colB = st.columns([1, 1])
    with colA:
        insumo = st.selectbox("Seleccione el Ingrediente Activo / Insumo:", list(insumos_db.keys()))
        cantidad = st.number_input("Volumen de aplicación (Kg o Litros):", min_value=0.0, step=1.0)
    
    with colB:
        if cantidad > 0:
            det = insumos_db[insumo]
            volumen_riesgo = cantidad * 1500
            st.markdown(f"<div class='tech-card'><b>Clasificación:</b> {det['clase']}<br><br><b>Riesgo Ambiental:</b> {det['riesgo']}</div>", unsafe_allow_html=True)
            st.metric(label="Volumen de Agua en Riesgo de Alteración (Litros)", value=f"{volumen_riesgo:,.0f} L")

# --- MÓDULO 3: ZONIFICACIÓN DE RIESGO ---
elif menu == "3. Zonificación de Riesgo":
    st.markdown("<div class='main-header'><h1>ZONIFICACIÓN DE VULNERABILIDAD</h1></div>", unsafe_allow_html=True)
    st.markdown("<div class='tech-card'><b>Análisis de Presión Territorial:</b> El monocultivo intensivo en la ronda hídrica elimina la zona de amortiguación o 'buffer' natural. Esto maximiza la vulnerabilidad del Lago de Tota ante eventos de escorrentía superficial, convirtiendo las prácticas agronómicas tradicionales en un vector directo de carga contaminante (N, P y plaguicidas sintéticos).</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Área de Estudio (Cuenca)**")
        try:
            st.image("aquitania.png", caption="Lago de Tota - Zona de influencia directa")
        except:
            st.warning("⚠️ Imagen 'aquitania.png' no encontrada.")
    with col2:
        st.write("**Presión Agrícola**")
        try:
            st.image("cultivo.png", caption="Invasión de ronda hídrica por cultivo")
        except:
            st.warning("⚠️ Imagen 'cultivo.png' no encontrada.")
            
    try:
        st.image("mapa_uso_suelo.png", caption="Mapa de Zonificación y Presión Agrícola", use_container_width=True)
    except:
        pass

# --- MÓDULO 4: ESCENARIOS DE TRANSICIÓN ---
elif menu == "4. Escenarios de Transición":
    st.markdown("<div class='main-header'><h1>EVALUACIÓN DE ESCENARIOS AGRONÓMICOS</h1></div>", unsafe_allow_html=True)
    st.markdown("### Análisis Técnico de Alternativas de Manejo en la Cuenca del Lago de Tota")
    st.write("Seleccione un escenario para evaluar su viabilidad técnica, impacto financiero y carga contaminante proyectada.")

    tab1, tab2, tab3 = st.tabs(["🔴 Escenario A: Convencional", "🟢 Escenario B: Manejo Integrado (Eco-Junca)", "🌿 Escenario C: Agroecológico"])

    with tab1:
        st.markdown("### Estrategia 1: Manejo Convencional (Línea Base)")
        st.markdown("**Enfoque:** Netamente Químico / Preventivo ('Por Calendario').\nEsta estrategia describe el modelo actual identificado en el diagnóstico territorial. Es un sistema altamente ineficiente e insostenible a largo plazo.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.error("**Protocolo Operativo:**")
            st.write("• Aplicación de moléculas Cat. I y II cada 7-8 días.")
            st.write("• Dosificación empírica ('al ojo').")
            st.write("• Nutrición basada en gallinaza cruda y NPK sintético.")
        with col2:
            st.metric(label="Reducción de Carga Contaminante", value="0%", delta="- Crítico (Alto Lixiviado)", delta_color="inverse")
            st.metric(label="Frecuencia de Aplicación", value="20 ciclos/cosecha")
            
        st.info("**Viabilidad:** Alta inercia cultural (zona de confort del agricultor), pero insostenible ambientalmente por eutrofización del cuerpo léntico.")

    with tab2:
        st.markdown("### Estrategia 2: Manejo Integrado (Ruta Priorizada)")
        st.markdown("**Enfoque:** Híbrido (Químico Racional + Cultural + Biológico).\nEs la estrategia de transición diseñada para este proyecto. Combina la seguridad del control racionalizado con prácticas sostenibles, operada a través del Semáforo Ambiental.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.success("**Protocolo Operativo:**")
            st.write("• **Monitoreo:** Aplicación exclusiva al superar el Umbral de Daño Económico (UDE).")
            st.write("• **Rotación:** Moléculas de baja toxicidad (Cat. III) alternadas con biopreparados.")
            st.write("• **Restricción:** Cero aplicaciones bajo pronóstico de precipitación (Lluvia).")
        with col2:
            st.metric(label="Reducción de Costos Operativos", value="30%", delta="Ahorro en insumos", delta_color="normal")
            st.metric(label="Reducción de Carga Tóxica", value="40%", delta="-8 ciclos de fumigación", delta_color="normal")
            
        st.info("**Viabilidad (Óptimo Técnico-Social):** Equilibrio perfecto. Protege la ronda hídrica sin exponer al agricultor al riesgo de pérdida económica total.")

    with tab3:
        st.markdown("### Estrategia 3: Manejo Agroecológico (Sostenible Radical)")
        st.markdown("**Enfoque:** Netamente Sostenible / Orgánico.\nEscenario ideal de sostenibilidad proyectado a futuro para la restauración total de la cuenca.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.warning("**Protocolo Operativo:**")
            st.write("• Cero uso de síntesis química.")
            st.write("• Control exclusivo con alelopatía y biocontroladores.")
            st.write("• Nutrición 100% con compost maduro y microorganismos eficientes.")
        with col2:
            st.metric(label="Eliminación de Carga Química", value="100%", delta="Protección Total del Lago", delta_color="normal")
            st.metric(label="Riesgo Financiero a Corto Plazo", value="Alto", delta="Posible choque productivo", delta_color="inverse")
            
        st.info("**Viabilidad:** Inviable a corto plazo debido a la alta degradación actual del suelo y la barrera de aversión al riesgo por parte del productor.")
