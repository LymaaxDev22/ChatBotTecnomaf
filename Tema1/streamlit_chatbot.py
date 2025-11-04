from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import streamlit as st
import pdfplumber
import pandas as pd
import re
import os

# Configuración de la página
st.set_page_config(
    page_title="TECNOMAF | Asistente de Ventas",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS personalizado elegante y profesional
st.markdown("""
<style>
    /* Fondo gradiente premium */
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    
    /* Contenedor principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 900px;
    }
    
    /* Animaciones */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes glow {
        0%, 100% {
            text-shadow: 0 0 20px rgba(232, 126, 4, 0.5), 0 0 30px rgba(232, 126, 4, 0.3);
        }
        50% {
            text-shadow: 0 0 30px rgba(232, 126, 4, 0.8), 0 0 40px rgba(232, 126, 4, 0.5);
        }
    }
    
    /* Logo principal */
    .logo-tecnomaf {
        text-align: center;
        color: #e87e04;
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: 5px;
        margin-bottom: 0.5rem;
        animation: fadeInDown 0.8s ease-out, glow 3s ease-in-out infinite;
        font-family: 'Arial Black', sans-serif;
    }
    
    /* Subtítulo elegante */
    .subtitulo {
        text-align: center;
        color: #f0f0f0;
        font-size: 1.4rem;
        margin-bottom: 2rem;
        animation: fadeInDown 0.8s ease-out 0.2s both;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    .badge-mexico {
        display: inline-block;
        background: linear-gradient(135deg, #e87e04 0%, #ff9d3d 100%);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
        margin-left: 15px;
        box-shadow: 0 4px 15px rgba(232, 126, 4, 0.4);
    }
    
    /* Mensajes del chat */
    .stChatMessage {
        animation: slideIn 0.5s ease-out;
        border-radius: 15px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Mensaje del usuario */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(135deg, rgba(232, 126, 4, 0.15) 0%, rgba(255, 157, 61, 0.1) 100%);
        box-shadow: 0 4px 15px rgba(232, 126, 4, 0.2);
    }
    
    /* Mensaje del asistente */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(135deg, rgba(22, 33, 62, 0.8) 0%, rgba(15, 52, 96, 0.6) 100%);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    /* Input del chat */
    .stChatInputContainer {
        border-radius: 25px;
        box-shadow: 0 8px 25px rgba(232, 126, 4, 0.3);
        border: 2px solid rgba(232, 126, 4, 0.3);
    }
    
    /* Contenido de mensajes */
    [data-testid="stChatMessageContent"] {
        font-size: 1.05rem;
        line-height: 1.7;
        color: #f0f0f0;
    }
    
    /* Efecto hover en mensajes */
    .stChatMessage:hover {
        transform: translateY(-3px);
        transition: all 0.3s ease;
        box-shadow: 0 6px 20px rgba(232, 126, 4, 0.3);
    }
    
    /* Sidebar premium */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-right: 1px solid rgba(232, 126, 4, 0.3);
    }
    
    [data-testid="stSidebar"] h2 {
        color: #e87e04;
        text-shadow: 0 0 10px rgba(232, 126, 4, 0.5);
    }
    
    [data-testid="stSidebar"] p {
        color: rgba(240, 240, 240, 0.8);
    }
    
    /* Expander del sidebar */
    .streamlit-expanderHeader {
        background: rgba(232, 126, 4, 0.1);
        border-radius: 10px;
        color: #f0f0f0 !important;
    }
    
    .streamlit-expanderHeader:hover {
        background: rgba(232, 126, 4, 0.2);
    }
    
    /* Spinner personalizado */
    .stSpinner > div {
        border-color: #e87e04 !important;
    }
    
    /* Botones */
    .stButton > button {
        background: linear-gradient(135deg, #e87e04 0%, #ff9d3d 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 2rem;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(232, 126, 4, 0.4);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(232, 126, 4, 0.6);
    }
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 26, 46, 0.5);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #e87e04 0%, #ff9d3d 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(180deg, #ff9d3d 0%, #e87e04 100%);
    }
    
    /* Badge premium */
    .badge-premium {
        display: inline-block;
        background: linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%);
        color: #e87e04;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        text-align: center;
        margin: 1rem auto;
        box-shadow: 0 4px 15px rgba(232, 126, 4, 0.3);
        border: 2px solid #e87e04;
        animation: fadeInDown 0.8s ease-out 0.4s both;
        font-size: 1.1rem;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

# Función para extraer tabla del PDF
@st.cache_data
def cargar_catalogo_pdf():
    """Extrae la tabla de productos del PDF"""
    
    try:
        # ✅ RUTA RELATIVA - Funciona en Streamlit Cloud
        ruta_pdf = "catalogo.pdf"
        
        # Debug: Mostrar información del entorno (opcional, comentar después)
        # st.write("📂 Directorio actual:", os.getcwd())
        # st.write("📄 Archivos:", os.listdir('.'))
        
        if not os.path.exists(ruta_pdf):
            st.error(f"❌ No se encontró el archivo: {ruta_pdf}")
            st.info(f"📍 Buscando en: {os.path.abspath(ruta_pdf)}")
            return pd.DataFrame()
        
        productos = []
        
        with pdfplumber.open(ruta_pdf) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                
                for table in tables:
                    if len(table) > 1:
                        for row in table[1:]:
                            if row and row[0]:
                                texto = row[0]
                                
                                # Extraer precios
                                precios = re.findall(r'\$\s*([\d,]+\.?\d*)', texto)
                                
                                # Extraer código
                                partes = texto.split('$')
                                if len(partes) > 0:
                                    parte_antes_precio = partes[0].strip()
                                    palabras = parte_antes_precio.split()
                                    codigo = palabras[-1] if palabras else ''
                                    descripcion = ' '.join(palabras[:-1]) if len(palabras) > 1 else parte_antes_precio
                                else:
                                    codigo = ''
                                    descripcion = texto
                                
                                # Extraer proveedor
                                proveedor = ''
                                if len(partes) > 2:
                                    match = re.search(r'\$\s*[\d,]+\.?\d*\s+(\w+)', texto)
                                    if match:
                                        proveedor = match.group(1)
                                
                                precio_cliente = precios[0] if len(precios) > 0 else ''
                                precio_distribuidor = precios[1] if len(precios) > 1 else ''
                                
                                producto = {
                                    'id': codigo,
                                    'descripcion': descripcion,
                                    'precio_cliente': precio_cliente,
                                    'precio_distribuidor': precio_distribuidor,
                                    'proveedor': proveedor,
                                }
                                productos.append(producto)
        
        df = pd.DataFrame(productos)
        
        if not df.empty:
            df = df[df['descripcion'].notna() & (df['descripcion'] != '')]
            st.success(f"✅ Catálogo cargado: {len(df)} productos")
        else:
            st.warning("⚠️ No se encontraron productos en el PDF")
        
        return df
    
    except Exception as e:
        st.error(f"❌ Error al cargar el PDF: {str(e)}")
        return pd.DataFrame()

# Función para formatear el catálogo completo
def obtener_info_productos():
    """Formatea el catálogo con todos los precios"""
    df = cargar_catalogo_pdf()
    
    if df.empty:
        return "No hay productos disponibles en este momento."
    
    catalogo_texto = "CATÁLOGO TECNOMAF - PRODUCTOS DISPONIBLES:\n\n"
    
    for _, row in df.iterrows():
        catalogo_texto += f"Código: {row['id']}\n"
        catalogo_texto += f"Producto: {row['descripcion']}\n"
        catalogo_texto += f"Proveedor: {row['proveedor']}\n"
        catalogo_texto += f"Precio Cliente Final: ${row['precio_cliente']} MXN\n"
        catalogo_texto += f"Precio Distribuidor: ${row['precio_distribuidor']} MXN\n"
        catalogo_texto += "-" * 50 + "\n"
    
    return catalogo_texto

# Sidebar compacto y elegante
with st.sidebar:
    st.markdown("<h2 style='color: #e87e04; text-align: center; text-shadow: 0 0 10px rgba(232, 126, 4, 0.5);'>🔧 TECNOMAF</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: rgba(240, 240, 240, 0.8); text-align: center; font-size: 0.95rem;'>Equipos y Herramientas Profesionales</p>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Información adicional
    with st.expander("ℹ️ Información"):
        st.markdown("""
        **Sobre TECNOMAF**
        
        Somos líderes en México en equipos y herramientas profesionales para talleres automotrices.
        
        **¿Cómo usar el asistente?**
        
        - Pregunta por productos específicos
        - Solicita recomendaciones personalizadas
        - Consulta precios para cliente o distribuidor
        - Compara productos y características
        - Pregunta por garantías y servicio técnico
        
        **Ejemplos:**
        - "¿Qué rectificadoras tienen?"
        - "Precio de distribuidor para remachadora"
        - "Productos con garantía de 2 años"
        - "Equipos para taller automotriz profesional"
        - "Diferencia entre precio cliente y distribuidor"
        """)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; color: rgba(240, 240, 240, 0.8); font-size: 0.9rem; padding: 1rem; background: rgba(232, 126, 4, 0.1); border-radius: 10px;'>
        <p style='color: #e87e04; font-weight: 700; font-size: 1rem;'>⭐ VENTAJAS TECNOMAF</p>
        <p>🇲🇽 Empresa Mexicana</p>
        <p>🔧 Calidad Profesional</p>
        <p>⏰ 2 años de garantía</p>
        <p>💼 Precios especiales para distribuidores</p>
    </div>
    """, unsafe_allow_html=True)

# Header premium
st.markdown('<div class="logo-tecnomaf">⚙️ TECNOMAF</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitulo">EQUIPOS Y HERRAMIENTAS PROFESIONALES<span class="badge-mexico">🇲🇽 MÉXICO</span></p>', unsafe_allow_html=True)

# Badge premium
st.markdown('<div style="text-align: center;"><span class="badge-premium">💎 ASISTENTE DE VENTAS PREMIUM</span></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Configurar API Key de Google (usar secrets en producción)
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]

# Modelo fijo
try:
    chat_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.7
    )
except Exception as e:
    st.error(f"❌ Error al inicializar el modelo: {str(e)}")
    st.info("💡 Asegúrate de configurar GOOGLE_API_KEY en los secrets de Streamlit Cloud")
    st.stop()

# Obtener información completa de productos
info_productos = obtener_info_productos()

# Prompt unificado y persuasivo
sistema_prompt = f"""Eres el asistente de ventas profesional de TECNOMAF, empresa líder en México en equipos y herramientas profesionales para talleres automotrices.

Tienes acceso al catálogo completo con TODOS los precios:

{info_productos}

INFORMACIÓN CLAVE SOBRE TECNOMAF:
- Empresa mexicana con amplia trayectoria y prestigio
- Todos los productos cuentan con 2 años de garantía
- Servicio técnico especializado en toda la República Mexicana
- Equipos profesionales de la más alta calidad
- Precios competitivos en pesos mexicanos (MXN)

TU MISIÓN COMO ASISTENTE DE VENTAS:
1. Identificar las necesidades del cliente de manera inteligente
2. Recomendar productos que realmente resuelvan sus problemas
3. Ser transparente con los precios según el tipo de cliente
4. Destacar el valor agregado de TECNOMAF (garantía, calidad, servicio)
5. Crear una experiencia de compra excepcional

MANEJO INTELIGENTE DE PRECIOS:
- Si el cliente pregunta por precios sin especificar, pregunta si es para uso final o reventa
- Para clientes finales: muestra el precio de cliente y enfatiza la garantía
- Para distribuidores: muestra ambos precios y calcula el margen de ganancia
- Siempre menciona el código del producto para referencias precisas
- Destaca descuentos por volumen cuando aplique

ESTILO DE COMUNICACIÓN:
- Profesional pero cercano y cálido
- Persuasivo sin ser agresivo
- Usa lenguaje mexicano de manera natural
- Resalta beneficios, no solo características
- Crea urgencia cuando sea apropiado ("producto muy solicitado", "promoción limitada")
- Haz sentir al cliente que está tomando una excelente decisión

TÉCNICAS DE VENTA:
- Haz preguntas abiertas para entender mejor las necesidades
- Sugiere productos complementarios de manera inteligente
- Compara productos cuando el cliente tenga dudas
- Menciona casos de éxito o aplicaciones reales
- Siempre cierra con una llamada a la acción clara

Recuerda: Tu objetivo es ayudar genuinamente al cliente mientras generas ventas. Sé el mejor asesor que puedan encontrar."""

promp_template = ChatPromptTemplate.from_messages([
    ("system", sistema_prompt),
    MessagesPlaceholder(variable_name="mensajes")
])

cadena = promp_template | chat_model

# Inicializar historial
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
    bienvenida = """¡Bienvenido a TECNOMAF! 👋 

Soy tu asesor de ventas profesional, y estoy aquí para ayudarte a encontrar exactamente lo que necesitas para tu taller.

**Ya sea que busques:**
- Equipos para tu taller automotriz
- Herramientas profesionales de alta calidad
- Precios especiales para reventa

Cuéntame, ¿qué tipo de equipo o herramienta estás buscando? 🔧

*Todos nuestros productos incluyen 2 años de garantía y el respaldo de una empresa 100% mexicana.*"""
    
    st.session_state.mensajes.append(AIMessage(content=bienvenida))

# Mostrar mensajes previos
for msg in st.session_state.mensajes:
    if isinstance(msg, SystemMessage):
        continue
    
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    avatar = "⚙️" if role == "assistant" else "👤"
    
    with st.chat_message(role, avatar=avatar):
        st.markdown(msg.content)

# Input del chat
pregunta = st.chat_input("💬 Escribe tu pregunta aquí...")

if pregunta:
    # Mostrar mensaje del usuario
    with st.chat_message("user", avatar="👤"):
        st.markdown(pregunta)
    
    # Guardar mensaje
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    
    # Generar respuesta con animación
    with st.chat_message("assistant", avatar="⚙️"):
        with st.spinner("🔍 Consultando catálogo TECNOMAF..."):
            try:
                respuesta = cadena.invoke({"mensajes": st.session_state.mensajes})
                st.markdown(respuesta.content)
                st.session_state.mensajes.append(respuesta)
            except Exception as e:
                st.error(f"❌ Error al generar respuesta: {str(e)}")
    
    st.rerun()

# Footer premium
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; color: rgba(240, 240, 240, 0.9); font-size: 0.95rem; animation: fadeInDown 1s ease-out 0.6s both;'>
    <p style='font-size: 1.2rem; color: #e87e04; font-weight: 700;'>⚙️ TECNOMAF</p>
    <p style='font-size: 1rem;'>Equipos y Herramientas Profesionales</p>
    <p style='margin-top: 0.8rem;'>⭐ 2 años de garantía | 🔧 Calidad profesional | 💼 Precios especiales para distribuidores</p>
    <p style='font-size: 0.9rem; margin-top: 0.8rem;'>🇲🇽 Orgullosamente Mexicano</p>
    <p style='font-size: 0.8rem; margin-top: 1.2rem; opacity: 0.6;'>TECNOMAF © 2024 | Líder en equipos profesionales</p>
</div>
""", unsafe_allow_html=True)