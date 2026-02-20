import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN E IDENTIDAD
st.set_page_config(page_title="ECO-JUNCA | Educación Ambiental", page_icon="🧅", layout="wide")

st.markdown("""
    <style>
    .main-header {background-color: #004d40; padding: 35px; color: white; border-radius: 15px; text-align: center; margin-bottom: 25px; border-bottom: 5px solid #81c784;}
    .info-card {background-color: #f1f8e9; padding: 20px; border-radius: 10px; border-left: 10px solid #2e7d32; margin-bottom: 20px;}
    .stMetric {background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #2e7d32;}
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS TÉCNICA DE INSUMOS
insumos_db = {
    "UREA (CO(NH₂)₂)": {"uso": "Estimula el crecimiento vegetativo.", "impacto": "Transformación en nitratos; Eutrofización y pérdida de oxígeno hídrico."},
    "NITRATO DE AMONIO (NH₄NO₃)": {"uso": "Desarrollo rápido del follaje.", "impacto": "Contaminación de aguas superficiales y alteración del equilibrio trófico."},
    "FOSFATO DIAMÓNICO (DAP)": {"uso": "Desarrollo radicular.", "impacto": "Aporte de fósforo soluble; responsable de proliferación de macrófitas."},
    "CLORPIRIFOS": {"uso": "Insecticida (Control de insectos de suelo).", "impacto": "Alta toxicidad acuática; inhibe enzimas nerviosas; bioacumulable."},
    "MANCOZEB": {"tipo": "Fungicida", "uso": "Control de hongos foliares.", "impacto": "Liberación de metales pesados (Mn, Zn); daño a microbiota del suelo."},
    "CARBENDAZIM": {"uso": "Fungicida sistémico.", "impacto": "Persistencia en suelo y agua; impacto en organismos acuáticos y lombrices."},
    "GALLINAZA": {"uso": "Enmienda orgánica (Materia orgánica).", "impacto": "Riesgo de contaminación microbiológica y lixiviación de nutrientes si no es tratada."}
}

# 3. NAVEGACIÓN LATERAL
with st.sidebar:
    st.markdown("# ECO-JUNCA 🌱")
    st.write("### Educación para el Lago")
    st.divider()
    menu = st.radio("MÓDULOS DE APRENDIZAJE:", ["Contexto Territorial", "Mapa de Uso de Suelo", "Calculadora de Impacto", "Laboratorio de Encuestas", "Estrategias de Manejo"])
    st.write("---")
    st.caption("Proyecto de Grado | Ingeniería Ambiental")

# --- SECCIÓN 1: NUESTRO TERRITORIO ---
if menu == "Contexto Territorial":
    st.markdown("<div class='main-header'><h1>ECO-JUNCA: EDUCACIÓN AMBIENTAL</h1><p>Conociendo el impacto de nuestra siembra en el Lago de Tota</p></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("<div class='info-card'><h3>🌊 Importancia del Lago de Tota</h3>"
                    "<p>El Lago de Tota es un ecosistema estratégico de alta montaña, clasificado como lago por su profundidad (>60m) y red de afluentes. Suministra agua a más de 250,000 personas en Boyacá y es el soporte de la industria de la trucha arcoíris.</p></div>", unsafe_allow_html=True)
        
        st.write("### 🌱 El Cultivo de Cebolla Junca (*Allium fistulosum*) ")
        st.write("""
        Aquitania es la capital cebollera de Colombia, concentrando el **80% de la producción nacional**. 
        La cebolla junca es un cultivo de ciclo continuo que requiere una alta inversión en fertilizantes nitrogenados 
        y plaguicidas para cumplir con la demanda comercial de Corabastos. Sin embargo, su cercanía a la ronda hídrica 
        genera una presión constante por contaminación difusa.
        """)
        # Imagen de campo
        st.image("cultivo.png")
        
    with col2:
         st.markdown("<div class='edu-card'><h3>🔍 ¿Para qué sirve esta herramienta?</h3>"
                    "<p>Esta aplicación es un espacio de <b>Educación Ambiental</b> diseñado para que los agricultores de Aquitania comprendamos cómo nuestras decisiones en el cultivo de cebolla junca afectan el Lago de Tota.</p></div>", unsafe_allow_html=True)
        st.info("ECO-JUNCA surge para ofrecer soporte técnico y educación ambiental, permitiendo visualizar el impacto de las prácticas agrícolas convencionales y promover una transición sostenible.")
        # Imagen del Lago
        st.image("aquitania.png")
        st.info("El objetivo es aprender a producir sin agotar nuestros recursos naturales.")

# --- SECCIÓN 2: MAPA DE USO DE SUELO ---
elif menu == "Mapa de Uso de Suelo":
    st.markdown("<div class='main-header'><h1>ZONIFICACIÓN Y USO DE SUELO</h1></div>", unsafe_allow_html=True)
    st.write("### Cartografía de Autoría Propia")
    
    try:
        # Aquí se carga tu mapa. Recuerda subirlo a GitHub como mapa_uso_suelo.png
        st.image("mapa_uso_suelo.png", caption="Análisis geoespacial de la actividad agrícola", use_container_width=True)
        st.success("**Análisis del Mapa:** La distribución espacial evidencia la alta densidad de cultivos en áreas de protección hídrica.")
    except:
        st.error("⚠️ Sube tu archivo 'mapa_uso_suelo.png' a GitHub para visualizar tu mapa.")

# --- SECCIÓN 3: CALCULADORA ---
elif menu == "Calculadora de Impacto":
    st.subheader("🧪 Calculadora de Contaminación Difusa")
    st.write("Seleccione un insumo y la cantidad aplicada para estimar el volumen de agua pura que podría verse comprometida.")
    
    insumo = st.selectbox("Insumo químico reportado:", list(insumos_db.keys()))
    cantidad = st.number_input("Cantidad aplicada (Litros o Kg):", min_value=0.0)
    
    if cantidad > 0:
        det = insumos_db[insumo]
        agua_vol = cantidad * 100000
        st.markdown(f"<div class='info-card'><b>Uso Técnico:</b> {det['uso']}<br><b>Efecto Ambiental:</b> {det['impacto']}</div>", unsafe_allow_html=True)
        st.metric("Litros de Agua Afectada", f"{agua_vol:,.0f} L")

# --- SECCIÓN 4: ENCUESTAS ---
elif menu == "Laboratorio de Encuestas":
    st.subheader("📊 Análisis de Percepción en Campo")
    
    # Gráfico colorido para las encuestas
    df_encuesta = pd.DataFrame({
        "Variable": ["Dependencia Química", "Conciencia del Impacto", "Interés en Bioinsumos"],
        "Porcentaje": [85, 40, 70]
    })
    
    fig = px.bar(df_encuesta, x="Variable", y="Porcentaje", color="Variable", title="Resultados de Encuestas a Agricultores",
                 color_discrete_sequence=px.colors.qualitative.Dark24)
    st.plotly_chart(fig, use_container_width=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='info-card'><b>Análisis de Uso:</b> La alta dependencia de fertilizantes nitrogenados confirma la necesidad de programas de transición técnica.</div>", unsafe_allow_html=True)
    with col_b:
        st.markdown("<div class='info-card'><b>Análisis Educativo:</b> Existe una brecha entre la práctica agrícola y la percepción del daño ecosistémico al Lago.</div>", unsafe_allow_html=True)

# --- SECCIÓN 5: ESTRATEGIAS ---
elif menu == "Estrategias de Manejo":
    st.subheader("💡 Propuesta de Gestión Ambiental")
    st.success("✅ **Estrategia Sostenible:** Sustitución por biofertilizantes y respeto a la ronda hídrica.")
    st.warning("⚠️ **Estrategia Intermedia:** Manejo Integrado de Plagas (MIP) y reducción del 50% de químicos.")
    st.error("❌ **Estrategia Convencional:** Modelo actual con alta carga de insumos sintéticos.")

st.divider()
st.caption("Isabela O. | Proyecto de Grado | Ingeniería Ambiental | Universidad El Bosque")
