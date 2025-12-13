# Importamos una función que nos permite leer variables guardadas en un archivo llamado ".env" (por ejemplo claves o contraseñas).
from dotenv import load_dotenv 

# Importamos el modelo de Google Gemini para poder usar inteligencia artificial a través de la librería LangChain.
from langchain_google_genai import ChatGoogleGenerativeAI

# Importamos una herramienta llamada TavilySearch, que sirve para hacer búsquedas en internet y traer información actualizada.
from langchain_tavily import TavilySearch

# Importamos MemorySaver, que sirve para guardar el "recuerdo" de la conversación, es decir, para que el sistema pueda recordar lo que se habló antes.
from langgraph.checkpoint.memory import MemorySaver

# 1) Cargar las variables de entorno / Esta línea lee las variables que tengamos en un archivo .env (por ejemplo, claves de API de Google, Tavily, etc.).  
# Así no las escribimos directamente en el código.
load_dotenv()

# 2) Inicializar la memoria de la conversación
# Creamos un objeto de tipo "MemorySaver" que se encargará de guardar el contexto y el historial de la conversación con el usuario.
memory = MemorySaver()

# 3) Configurar las herramientas (tools)
# Creamos una herramienta de búsqueda en internet utilizando Tavily. "max_results=2" significa que cuando haga una búsqueda, devolverá como máximo 2 resultados.
tavily_tool = TavilySearch(max_results=2)

# Guardamos la herramienta en una lista. Más adelante, el modelo de IA podrá usar esta lista de herramientas cuando lo necesite.
tools = [tavily_tool]

# 4) Inicializar el modelo de IA (LLM) ANTES se usaba un modelo de OpenAI (por ejemplo, gpt-4.1).
# Ahora se cambia a un modelo de Google llamado "gemini-2.5-flash".
# "temperature=0" significa que el modelo será más "serio" y predecible, es decir, dará respuestas más estables y menos creativas/aleatorias.
llm = ChatGoogleGenerativeAI( model="gemini-2.5-flash", temperature=0 )

# 5) Conectar el modelo de IA con las herramientas
# Aquí "unimos" el modelo de IA con las herramientas de búsqueda. 
# De esta forma, cuando el modelo vea que necesita información extra, podrá llamar a TavilySearch para buscar en internet.
llm_with_tools = llm.bind_tools(tools)

# 6) Configurar el "hilo" o sesión de conversación
# "graph_config" es una configuración donde indicamos, por ejemplo,un identificador de conversación (thread_id).
# Esto sirve para que el sistema sepa que todos los mensajes pertenecen al mismo hilo o sesión.
graph_config = {  "configurable": { "thread_id": "1" }}
