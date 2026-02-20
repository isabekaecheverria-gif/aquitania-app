import streamlit as st

# Configuración de página
st.set_page_config(page_title="Gestión Ambiental Aquitania", page_icon="🌱", layout="wide")

# Estilos CSS para que se vea profesional
st.markdown("""
    <style>
    .main-header {background-color: #2e7d32; padding: 20px; color: white; border-radius: 10px; text-align: center;}
    .stButton>button {background-color: #2e7d32; color: white;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-header'><h1>SISTEMA DE GESTIÓN AMBIENTAL - AQUITANIA</h1><p>Educación para la Sostenibilidad del Lago de Tota</p></div>", unsafe_allow_html=True)

# Datos técnicos sincronizados con tu Introducción
info = {
    'Sostenible (Agroecológica)': {
        'titulo': "🌱 ESTRATEGIA SOSTENIBLE (P+L)",
        [span_0](start_span)[span_1](start_span)'desc': "Basada en el programa 'Boyacá Siembra' y prácticas agroecológicas[span_0](end_span)[span_1](end_span).",
        'lago': "Bajo impacto. Protege el ecosistema del Lago de Tota (profundidad >60m, red de afluentes y efluente Upía).",
        'detalles': "Uso de bioinsumos y barreras vivas. Mercado diferenciado de cebolla junca (Allium fistulosum)."
    },
    'Intermedia (Transición)': {
        'titulo': "⚖️ ESTRATEGIA INTERMEDIA",
        [span_2](start_span)'desc': "Manejo Integrado de Plagas para reducción de carga química[span_2](end_span).",
        'lago': "Impacto Moderado. Reducción de la lixiviación de nitratos hacia el Lago.",
        'detalles': "Reducción del 50% de químicos. Optimización de costos en la producción tradicional."
    },
    'Convencional (Química)': {
        'titulo': "⚠️ ESTRATEGIA CONVENCIONAL",
        [span_3](start_span)[span_4](start_span)'desc': "Modelo intensivo con alta dependencia de pesticidas sintéticos[span_3](end_span)[span_4](end_span).",
        'lago': "Impacto Crítico. [span_5](start_span)Riesgo de eutrofización y degradación hídrica (Corpoboyacá, 2022)[span_5](end_span).",
        [span_6](start_span)[span_7](start_span)'detalles': "Abastecimiento masivo a Corabastos (80% de la oferta nacional)[span_6](end_span)[span_7](end_span)."
    }
}

with st.sidebar:
    st.header("Menú de Navegación")
    opcion = st.selectbox("Elija Escenario:", ["Inicio", "Sostenible (Agroecológica)", "Intermedia (Transición)", "Convencional (Química)"])

if opcion == "Inicio":
    st.write("### Bienvenida al Sistema de Soporte a la Decisión")
    st.info("Esta herramienta permite visualizar el impacto de la agricultura de cebolla junca en el ecosistema estratégico del Lago de Tota.")
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Lago_de_Tota_Boyac%C3%A1.jpg/800px-Lago_de_Tota_Boyac%C3%A1.jpg", caption="Vista del Lago de Tota")
else:
    data = info[opcion]
    st.subheader(data['titulo'])
    st.markdown(f"**🔍 Descripción Técnica:** {data['desc']}")
    st.markdown(f"**💧 Impacto Hídrico:** {data['lago']}")
    st.success(f"**💡 Plan de Acción:** {data['detalles']}")

st.divider()
st.caption("Proyecto de Grado | Isabela O. | Ingeniería Ambiental | Universidad El Bosque")
