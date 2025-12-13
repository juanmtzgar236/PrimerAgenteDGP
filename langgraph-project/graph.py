# Importamos StateGraph y START desde langgraph.
# StateGraph:
#   - Es como un "mapa de flujo" que define los pasos que va a seguir nuestro chatbot.
# START:
#   - Es el punto de inicio de ese flujo (dónde empieza la conversación en el gráfico).
from langgraph.graph import StateGraph, START

# Importamos componentes ya hechos (prebuilt) para trabajar con herramientas:
# - ToolNode: un tipo de "nodo" que se encarga de ejecutar herramientas externas (como búsquedas).
# - tools_condition: una función que decide si el modelo necesita usar una herramienta o no.
from langgraph.prebuilt import ToolNode, tools_condition

# Importamos desde nuestro archivo config:
# - tools: lista de herramientas disponibles (por ejemplo, TavilySearch).
# - memory: el sistema de memoria para recordar lo que pasa en la conversación.
# - llm_with_tools: el modelo de IA ya conectado con esas herramientas.
from config import tools, memory, llm_with_tools

# Importamos el tipo State, que define cómo se ve el "estado" de la conversación.
# Normalmente incluye cosas como:
#   - los mensajes intercambiados entre usuario y chatbot.
from state import State

# Definimos una función que construye el gráfico (el flujo del chatbot)
def build_graph() -> StateGraph:
    # Creamos el "constructor" del gráfico y le decimos que usaremos el tipo State
    # para representar el estado de la conversación.
    graph_builder = StateGraph(State)

    # Definimos una función interna llamada "chatbot".
    # Esta función será un "nodo" del gráfico.
    def chatbot(state: State):
        # Aquí le pedimos al modelo de IA (llm_with_tools) que responda,
        # usando los mensajes que ya hay en el estado de la conversación.
        # - state["messages"] es la lista de mensajes previos (usuario + chatbot).
        message = llm_with_tools.invoke(state["messages"])
        
        # Devolvemos un diccionario con la clave "messages".
        # LangGraph entiende que estamos agregando un nuevo mensaje a la conversación.
        return {"messages": [message]}

    # Agregamos el nodo "chatbot" al gráfico, usando la función que acabamos de definir.
    graph_builder.add_node("chatbot", chatbot)

    # Creamos un nodo de herramientas:
    # ToolNode se encarga de ejecutar las herramientas (por ejemplo, búsquedas en internet)
    # que tengamos definidas en la lista "tools".
    tool_node = ToolNode(tools)
    graph_builder.add_node("tools", tool_node)

    # Aquí definimos conexiones "condicionales" desde el nodo "chatbot".
    # ¿Qué significa esto?
    # - Después de que el chatbot responda, LangGraph usará "tools_condition"
    #   para decidir a dónde ir:
    #   - Si el modelo pidió usar una herramienta, irá al nodo "tools".
    #   - Si no, puede quedarse en el flujo normal del chatbot.
    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
    )

    # Esta línea indica que:
    # Cada vez que se termina de usar una herramienta (nodo "tools"),
    # volvemos al "chatbot" para que decida cuál es el siguiente paso.
    graph_builder.add_edge("tools", "chatbot")

    # Indicamos que el flujo (el gráfico) comienza en el nodo "chatbot".
    # START es el punto inicial del gráfico.
    graph_builder.add_edge(START, "chatbot")
    
    # Finalmente, "compilamos" el gráfico.
    # - checkpointer=memory significa que usaremos "memory" para guardar
    #   el estado de la conversación, de modo que se pueda retomar después.
    return graph_builder.compile(checkpointer=memory)
