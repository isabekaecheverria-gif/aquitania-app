import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CONFIGURACIÓN E IDENTIDAD VISUAL
st.set_page_config(page_title="Gestión Ambiental Aquitania", page_icon="🧅", layout="wide")

st.markdown("""
    <style>
    .main-header {background-color: #1b5e20; padding: 30px; color: white; border-radius: 15px; text-align: center; margin-bottom: 20px;}
    .section-card {background-color: #ffffff; padding: 20px; border-radius: 10px; border-left: 8px solid #2e7d32; border-right: 1px solid #e0e0e0; border-top: 1px solid #e0e0e0; border-bottom: 1px solid #e0e0e0; margin-bottom: 20px;}
    .metric-box {background-color: #f1f8e9; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #2e7d32;}
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS TÉCNICA DE INSUMOS (Lo que me diste)
insumos_db = {
    "UREA (CO(NH₂)₂)": {"tipo": "Fertilizante Nitrogenado", "uso": "Estimula crecimiento vegetativo.", "impacto": "Transformación en nitratos (NO₃⁻); Eutrofización y pérdida de oxígeno en el Lago."},
    "NITRATO DE AMONIO (NH₄NO₃)": {"tipo": "Fertilizante Nitrogenado", "uso": "Desarrollo rápido del cultivo.", "impacto": "Contaminación de aguas superficiales y alteración del equilibrio trófico."},
    "FOSFATO DIAMÓNICO (DAP)": {"tipo": "Fertilizante Fosfatado", "uso": "Desarrollo radicular.", "impacto": "Aporte de fósforo soluble; principal responsable de macrófitas y sedimentación."},
    "CLORPIRIFOS": {"tipo": "Insecticida (Organofosforado)", "uso": "Control de insectos de suelo.", "impacto": "Alta toxicidad acuática; inhibe enzimas nerviosas; bioacumulable."},
    "MANCOZEB": {"tipo": "Fungicida (Ditiocarbamato)", "uso": "Control de hongos foliares.", "impacto": "Liberación de metales pesados (Mn, Zn); daño a la microbiota del suelo."},
    "CARBENDAZIM": {"tipo": "Fungicida Sistémico", "uso": "Control de hongos.", "impacto": "Persistencia en suelo y agua; impacto en lombrices y organismos acuáticos."},
    "GALLINAZA": {"tipo": "Enmienda Orgánica", "uso": "Aporte de materia orgánica.", "impacto": "Riesgo de contaminación microbiológica y lixiviación si no hay compostaje previo."}
}

# 3. MENÚ LATERAL INTERACTIVO
with st.sidebar:
    st.image("https://drive.google.com/file/d/1Ouq7ehVjaHQbNyOKYXMy1AAdMihOX9wB/view?usp=drivesdk")
    st.header("📌 PANEL DE CONTROL")
    menu = st.radio("Seleccione Módulo:", ["Contexto Territorial", "Mapa de Uso de Suelo", "Calculadora de Insumos", "Resultados de Encuestas", "Estrategias de Gestión"])
    st.divider()
    st.info("Objetivo: Generar estrategias que permitan la coexistencia entre producción y conservación.")

# --- MÓDULO 1: CONTEXTO ---
if menu == "Contexto Territorial":
    st.markdown("<div class='main-header'><h1>AQUITANIA Y EL LAGO DE TOTA</h1></div>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.write("### ¿Por qué esta Aplicación?")
        st.write("""
        Esta herramienta se crea para mitigar la presión ambiental sobre el **Lago de Tota**, el cuerpo de agua dulce más grande de Colombia. 
        Aquitania produce el 80% de la cebolla junca del país, pero el uso de agroquímicos pone en riesgo el agua que abastece a 250,000 personas (incluyendo Sogamoso) 
        y la industria de la trucha arcoíris.
        """)
        st.markdown("**Características Técnicas del Lago:**")
        st.write("- Profundidad > 60m (Clasificación: Lago).\n- Red de afluentes y efluente principal (Río Upía).\n- Ecosistema estratégico de alta montaña.")
    with col2:
        st.image("https://porelparamo.org/sites/default/files/styles/noticia_detalle/public/2021-03/Aquitania_Cebolla_Tota.jpg", caption="Ribera del Lago de Tota")

# --- MÓDULO 2: TU MAPA ---
elif menu == "Mapa de Uso de Suelo":
    st.markdown("<div class='main-header'><h1>MAPA DE USO DE SUELO</h1></div>", unsafe_allow_html=True)
    st.write("### Cartografía Elaborada por el Autor")
    st.write("Este mapa identifica las áreas de cultivo y la zonificación de impacto directo sobre la cuenca.")
    
    # REEMPLAZA 'mapa.png' por el nombre real de tu archivo subido a GitHub
    try:
        st.image("mapa_uso_suelo.png", caption="Mapa de Uso de Suelo - Cuenca del Lago de Tota", use_container_width=True)
    except:
        st.warning("⚠️ El archivo de imagen 'mapa_uso_suelo.png' no se encuentra en el repositorio de GitHub. Por favor, súbelo.")

# --- MÓDULO 3: CALCULADORA ---
elif menu == "Calculadora de Insumos":
    st.markdown("<div class='main-header'><h1>🧪 CALCULADORA DE IMPACTO</h1></div>", unsafe_allow_html=True)
    insumo = st.selectbox("Seleccione el insumo químico reportado:", list(insumos_db.keys()))
    cantidad = st.number_input("Cantidad aplicada (Litros o Kg):", min_value=0.0)
    
    if cantidad > 0:
        det = insumos_db[insumo]
        agua_vol = cantidad * 100000
        st.markdown(f"<div class='section-card'><b>Uso:</b> {det['uso']}<br><b>Impacto Hídrico:</b> {det['impacto']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='metric-box'><h3>Impacto Potencial: {agua_vol:,.0f} Litros de agua degradada</h3></div>", unsafe_allow_html=True)

# --- MÓDULO 4: ENCUESTAS ---
elif menu == "Resultados de Encuestas":
    st.markdown("<div class='main-header'><h1>📊 LABORATORIO DE ENCUESTAS</h1></div>", unsafe_allow_html=True)
    
    # Gráfico colorido de ejemplo
    df = pd.DataFrame({
        "Pregunta": ["Uso de Químicos", "Conciencia Ambiental", "Dispuesto a Cambiar", "Uso de Bioinsumos"],
        "Si (%)": [85, 40, 70, 25],
        "No (%)": [15, 60, 30, 75]
    })
    
    fig = px.bar(df, x="Pregunta", y=["Si (%)", "No (%)"], title="Percepción del Agricultor en Aquitania", 
                 barmode='group', color_discrete_sequence=['#2e7d32', '#d32f2f'])
    st.plotly_chart(fig, use_container_width=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='section-card'><b>Análisis de Uso:</b> El 85% depende de la Urea, lo que confirma la necesidad de estrategias de transición.</div>", unsafe_allow_html=True)
        st.image("https://img.freepik.com/foto-gratis/agricultor-sosteniendo-plantas-suelo_23-2148580000.jpg", caption="Labor de campo en Aquitania")
    with c2:
        st.markdown("<div class='section-card'><b>Análisis de Educación:</b> Solo el 40% asocia la pérdida de oxígeno del lago con sus fertilizantes.</div>", unsafe_allow_html=True)

# --- MÓDULO 5: ESTRATEGIAS ---
elif menu == "Estrategias de Gestión":
    st.markdown("<div class='main-header'><h1>💡 ESTRATEGIAS DE MANEJO</h1></div>", unsafe_allow_html=True)
    st.write("Estrategias propuestas según el nivel de uso de insumos:")
    st.success("✅ **Sostenible:** Sustitución por bioinsumos y manejo agroecológico.")
    st.warning("⚠️ **Intermedia:** Manejo integrado y reducción del 50% de carga química.")
    st.error("❌ **Convencional:** Uso intensivo (Modelo actual a transformar).")

st.divider()
st.caption("Isabela O. | Ingeniería Ambiental | Universidad El Bosque")
