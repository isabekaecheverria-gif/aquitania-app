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
    .desc-text {font-size: 1.1em; line-height: 1.6; text-align: justify;}
    </style>
    """, unsafe_allow_html=True)

# 2. BASE DE DATOS DE CONTAMINANTES AMPLIADA
insumos_db = {
    "UREA (Nitrógeno al 46%)": {"clase": "Fertilizante", "leccion": "Aporta nitratos que alimentan algas invasoras, consumiendo el oxígeno que los peces necesitan."},
    "FOSFATO DIAMÓNICO (DAP)": {"clase": "Fertilizante", "leccion": "El fósforo es el principal causante del crecimiento excesivo de plantas (buchón) en las orillas."},
    "CLORPIRIFOS": {"clase": "Insecticida", "leccion": "Altamente tóxico para la fauna acuática; persiste mucho tiempo en el fondo del lago."},
    "MANCOZEB": {"clase": "Fungicida", "leccion": "Contiene metales que se acumulan en el suelo, matando los bichos buenos que ayudan a la cebolla."},
    "CARBENDAZIM": {"clase": "Fungicida", "leccion": "Es muy difícil de eliminar del agua y afecta la reproducción de los peces."},
    "PARAQUAT": {"clase": "Herbicida", "leccion": "Quema la capa protectora del suelo, haciendo que la tierra se lave más fácil hacia el lago cuando llueve."},
    "GALLINAZA CRUDA": {"clase": "Enmienda", "leccion": "Si no está bien compostada, lleva bacterias y mal olor directamente al agua del lago."}
}

# 3. NAVEGACIÓN
with st.sidebar:
    st.markdown("# ECO-JUNCA 🌱")
    st.write("### Educación para el Lago")
    st.divider()
    menu = st.radio("MÓDULOS DE APRENDIZAJE:", ["Nuestro Territorio", "Mapa de Uso de Suelo", "Simulador de Impacto", "Laboratorio de Percepción", "Rutas hacia la Siembra"])
    st.divider()
    st.caption("Proyecto de Educación Ambiental | Isabela O.")

# --- SECCIÓN 1: NUESTRO TERRITORIO ---
if menu == "Nuestro Territorio":
    st.markdown("<div class='main-header'><h1>ECO-JUNCA: EDUCACIÓN AMBIENTAL</h1><p>Conociendo nuestra tierra para proteger nuestro lago</p></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.5, 1])
    with col1:
        st.markdown("<div class='edu-card'><h3>🔍 ¿Por qué estamos aquí?</h3>"
                    "<p class='desc-text'>Aquitania es el corazón de la cebolla en Colombia (80% de la producción), pero nuestra tradición depende de la salud del <b>Lago de Tota</b>. Este ecosistema es único: es el segundo lago navegable más alto del mundo y tiene hasta 67 metros de profundidad. Esta aplicación busca que aprendamos juntos a cultivar de una forma que el lago siga vivo para nuestros hijos.</p></div>", unsafe_allow_html=True)
        
        st.write("### 🌱 El Cultivo y su Entorno")
        st.write("""
        La cebolla junca es nuestra identidad, pero al ser un cultivo que nunca descansa, el suelo recibe muchos químicos. 
        Como el lago es una cuenca cerrada, todo lo que aplicamos termina allí. La educación ambiental es el camino 
        para cambiar el 'siempre se ha hecho así' por un 'vamos a hacerlo mejor'.
        """)
        # USO DE TU IMAGEN: aquitania.png
        try:
            st.image("aquitania.png", caption="Vista panorámica de nuestra región")
        except:
            st.warning("⚠️ Sube 'aquitania.png' a GitHub para ver tu imagen aquí.")
        
    with col2:
        st.info("La educación es la herramienta más poderosa para proteger el agua.")
        # USO DE TU IMAGEN: cultivo.png
        try:
            st.image("cultivo.png", caption="Nuestra labor en el campo")
        except:
            st.warning("⚠️ Sube 'cultivo.png' a GitHub para ver tu imagen aquí.")

# --- SECCIÓN 2: MAPA DE USO DE SUELO ---
elif menu == "Mapa de Uso de Suelo":
    st.markdown("<div class='main-header'><h1>NUESTRO MAPA DE USO DE SUELO</h1></div>", unsafe_allow_html=True)
    st.write("### ¿Qué nos dice el suelo?")
    st.markdown("""
    <div class='edu-card'>
    <b>Análisis del Autor:</b> Este mapa muestra cómo hemos repartido la tierra. Se ve mucha zona de <b>Agricultura Intensiva</b> 
    muy cerca del agua. Cuando el suelo no tiene plantas nativas que lo protejan (bosques o barreras), 
    los químicos de la cebolla bajan directo al lago por la lluvia. Esto se llama escorrentía y es lo que debemos aprender a frenar.
    </div>
    """, unsafe_allow_html=True)
    
    try:
        st.image("mapa_uso_suelo.png", caption="Mapa de Zonificación y Presión Agrícola", use_container_width=True)
    except:
        st.error("⚠️ Sube el archivo 'mapa_uso_suelo.png' a GitHub.")

# --- SECCIÓN 3: SIMULADOR ---
elif menu == "Simulador de Impacto":
    st.subheader("🧪 Simulador de Conciencia")
    st.write("Elige un producto y mira qué lección nos deja para el cuidado del agua.")
    
    insumo = st.selectbox("Producto:", list(insumos_db.keys()))
    cantidad = st.number_input("Cantidad aplicada:", min_value=0.0)
    
    if cantidad > 0:
        det = insumos_db[insumo]
        agua_afectada = cantidad * 100000
        st.markdown(f"<div class='edu-card'><b>Lección:</b> {det['leccion']}</div>", unsafe_allow_html=True)
        st.metric("Agua que pierde su pureza (aprox)", f"{agua_afectada:,.0f} L")

# --- SECCIÓN 4: PERCEPCIÓN ---
elif menu == "Laboratorio de Percepción":
    st.markdown("<div class='main-header'><h1>📊 LO QUE PENSAMOS EN AQUITANIA</h1></div>", unsafe_allow_html=True)
    st.write("Análisis de las encuestas sobre nuestro compromiso ambiental.")
    
    df_res = pd.DataFrame({
        "Pregunta": ["Dependencia Química", "Conciencia del Daño", "Deseo de Aprender"],
        "Porcentaje": [85, 42, 78]
    })
    
    fig = px.bar(df_res, x="Pregunta", y="Porcentaje", color="Pregunta", color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig, use_container_width=True)
    st.write("**Análisis:** El 78% de nosotros quiere aprender. Eso significa que ECO-JUNCA tiene mucho trabajo por hacer.")

# --- SECCIÓN 5: RUTAS HACIA LA SIEMBRA (DESPLEGABLES) ---
elif menu == "Rutas hacia la Siembra":
    st.subheader("💡 Caminos para proteger nuestro futuro")
    st.write("Haz clic en cada opción para ver cómo podemos mejorar nuestra relación con el lago:")

    with st.expander("🌱 RUTA DE LA NATURALEZA (Bioinsumos)"):
        st.write("""
        * **Abonos orgánicos:** Usar gallinaza bien compostada o biofermentos.
        * **Cerca viva:** Sembrar alisos o plantas nativas en el borde del lote para que atrapen los químicos antes de que lleguen al agua.
        """)
        st.success("¡Esta ruta recupera la vida de tu tierra!")

    with st.expander("⚖️ RUTA DEL EQUILIBRIO (Reducción)"):
        st.write("""
        * **Solo lo necesario:** Hacer análisis de suelo para no gastar plata en fertilizante que la planta no va a usar.
        * **Manejo de envases:** No botar los tarros a las zanjas.
        """)
        st.warning("¡Ahorras dinero y proteges el entorno!")

    with st.expander("⚠️ RUTA TRADICIONAL (El reto actual)"):
        st.write("""
        * **Riesgo:** Seguir usando venenos rojos y exceso de urea sin control.
        * **Consecuencia:** Un lago verde, con mal olor y suelo que ya no produce igual.
        """)
        st.error("Es el modelo que queremos transformar con educación.")

st.divider()
st.caption("Isabela O. | Educación Ambiental | Universidad El Bosque")
st.set_page_config(page_title="ECO-JUNCA", page_icon="🌱", layout="centered", initial_sidebar_state="collapsed")
