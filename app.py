import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="ECO-JUNCA | Educación Ambiental", page_icon="🌱", layout="wide")

st.markdown("""
    <style>
    .main-header {background-color: #1b5e20; padding: 35px; color: white; border-radius: 15px; text-align: center; margin-bottom: 25px; border-bottom: 5px solid #a5d6a7;}
    .edu-card {background-color: #f1f8e9; padding: 20px; border-radius: 10px; border-left: 10px solid #2e7d32; margin-bottom: 20px;}
    .stMetric {background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #2e7d32;}
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS DIDÁCTICA (INSUMOS)
insumos_db = {
    "UREA (CO(NH₂)₂)": {"clase": "Nutrición Vegetal", "leccion": "Se transforma en nitratos que 'asfixian' el lago al quitarle el oxígeno."},
    "CLORPIRIFOS": {"clase": "Control de Plagas", "leccion": "Es un veneno persistente que afecta el sistema nervioso de seres vivos en el agua."},
    "MANCOZEB": {"clase": "Protección de Cultivos", "leccion": "Deja metales pesados en el suelo que dañan los microorganismos que ayudan a la cebolla."},
    "GALLINAZA": {"clase": "Materia Orgánica", "leccion": "Si no está bien curada, lleva bacterias y exceso de sales directamente al Lago."}
}

# 3. NAVEGACIÓN
with st.sidebar:
    st.markdown("# ECO-JUNCA 🌱")
    st.write("### Educación para el Lago")
    st.divider()
    menu = st.radio("MÓDULOS DE APRENDIZAJE:", ["Nuestro Territorio", "Mapa de Uso de Suelo", "Simulador de Impacto", "Laboratorio de Percepción", "Rutas de Cambio"])
    st.divider()
    st.caption("Proyecto de Educación Ambiental | Isabela O.")

# --- SECCIÓN 1: NUESTRO TERRITORIO ---
if menu == "Nuestro Territorio":
    st.markdown("<div class='main-header'><h1>ECO-JUNCA: EDUCACIÓN AMBIENTAL</h1><p>Conociendo el impacto de nuestra siembra en el Lago de Tota</p></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("<div class='edu-card'><h3>🔍 ¿Para qué sirve esta herramienta?</h3>"
                    "<p>Esta aplicación es un espacio de <b>Educación Ambiental</b> diseñado para que los agricultores de Aquitania comprendamos cómo nuestras decisiones en el cultivo de cebolla junca afectan el Lago de Tota.</p></div>", unsafe_allow_html=True)
        
        st.write("### 🌱 La Cebolla Junca y el Lago")
        st.write("""
        En Aquitania somos orgullosamente los mayores productores de cebolla del país (80%). Sin embargo, 
        para que esta tradición siga viva, necesitamos aprender a proteger el **Lago de Tota**, nuestra fuente 
        de vida y agua para más de 250,000 personas. El Lago es un ecosistema profundo (>60m) que necesita 
        que cuidemos lo que aplicamos en la tierra.
        """)
        st.image("cultivo.png")
        
    with col2:
        st.info("El objetivo es aprender a producir sin agotar nuestros recursos naturales.")
        st.image("aquitania.png")

# --- SECCIÓN 2: MAPA DE USO DE SUELO ---
elif menu == "Mapa de Uso de Suelo":
    st.markdown("<div class='main-header'><h1>NUESTRO MAPA</h1></div>", unsafe_allow_html=True)
    st.write("### ¿Cómo estamos usando nuestra tierra?")
    st.write("Este mapa, creado específicamente para este estudio, nos muestra dónde están nuestros cultivos y qué tan cerca estamos del agua.")
    
    try:
        st.image("mapa_uso_suelo.png", caption="Zonificación de cultivos en la cuenca", use_container_width=True)
        st.success("**Lección del Mapa:** Entre más cerca sembremos de la orilla, más rápido llegan los químicos al Lago.")
    except:
        st.error("⚠️ Sube tu archivo 'mapa_uso_suelo.png' a GitHub.")

# --- SECCIÓN 3: SIMULADOR ---
elif menu == "Simulador de Impacto":
    st.subheader("🧪 Simulador de Conciencia Ambiental")
    st.write("Aprende qué sucede cuando aplicamos químicos en exceso.")
    
    insumo = st.selectbox("Elija un producto que use en su finca:", list(insumos_db.keys()))
    cantidad = st.number_input("Cantidad aplicada (Litros o Bultos):", min_value=0.0)
    
    if cantidad > 0:
        det = insumos_db[insumo]
        agua_afectada = cantidad * 100000
        st.markdown(f"<div class='edu-card'><b>Lo que debemos saber:</b> {det['leccion']}</div>", unsafe_allow_html=True)
        st.metric("Litros de agua que pierden calidad", f"{agua_afectada:,.0f} L")

# --- SECCIÓN 4: LABORATORIO DE PERCEPCIÓN (ENCUESTAS) ---
elif menu == "Laboratorio de Percepción":
    st.markdown("<div class='main-header'><h1>📊 ¿QUÉ PENSAMOS EN EL CAMPO?</h1></div>", unsafe_allow_html=True)
    st.write("Análisis de las respuestas compartidas por los agricultores de Aquitania.")
    
    df_res = pd.DataFrame({
        "Pregunta": ["Dependencia Química", "Conciencia del Daño", "Deseo de Aprender"],
        "Porcentaje": [85, 40, 75]
    })
    
    fig = px.bar(df_res, x="Pregunta", y="Porcentaje", color="Pregunta", 
                 title="Percepción sobre Prácticas Agrícolas",
                 color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<div class='edu-card'><b>Análisis Educativo:</b> Aunque el 85% depende de químicos, un 75% quiere aprender nuevas formas de siembra. ¡Ahí está nuestra oportunidad!</div>", unsafe_allow_html=True)
    st.image("https://img.freepik.com/foto-gratis/agricultor-sosteniendo-plantas-suelo_23-2148580000.jpg", caption="Educación para el futuro del campo")

# --- SECCIÓN 5: RUTAS DE CAMBIO (ESTRATEGIAS) ---
elif menu == "Rutas de Cambio":
    st.subheader("💡 Rutas hacia una Siembra Sostenible")
    st.write("La educación ambiental nos propone tres caminos:")
    st.success("🌱 **Ruta de la Naturaleza:** Sustitución por abonos orgánicos y respeto a la orilla del lago.")
    st.warning("⚖️ **Ruta del Equilibrio:** Usar menos químicos y solo cuando sea necesario.")
    st.error("⚠️ **Ruta Tradicional:** El modelo que debemos transformar para no perder el Lago.")

st.divider()
st.caption("Isabela O. | Tesis de Educación Ambiental | Universidad El Bosque")
