# Importamos la función 'build_graph' desde el archivo 'graph'.
# Esta función se encarga de construir el "cerebro" del chatbot:
# es decir, el flujo de la conversación con los nodos de LangGraph.
from graph import build_graph

# Importamos la configuración 'graph_config' desde el archivo 'config'.
# Ahí se suelen definir cosas como el identificador de la conversación (thread_id),
# y otros parámetros de cómo se comporta el gráfico.
from config import graph_config


# Definimos una función llamada 'stream_graph_updates' que recibe como parámetro
# el texto que escribió el usuario (user_input).
def stream_graph_updates(user_input: str):
    # 1) Construimos el gráfico de conversación (chatbot + herramientas + memoria, etc.)
    graph = build_graph()
    
    # 2) Iniciamos un "stream" (flujo continuo) de actualizaciones desde el gráfico.
    #    Es como decir: "graph, toma este mensaje del usuario y ve generando
    #    los pasos y respuestas poco a poco".
    for event in graph.stream(
        # Este es el estado inicial que le enviamos al gráfico:
        # Una lista de mensajes donde:
        #   - "role": "user" indica que el mensaje lo escribió el usuario.
        #   - "content": user_input es el texto que el usuario tecleó.
        {"messages": [{"role": "user", "content": user_input}]}, 
        
        # 'config' indica que usamos la configuración definida en 'graph_config'
        # (por ejemplo, el thread_id, memoria, etc.).
        config=graph_config,
        
        # 'stream_mode="values"' le dice a LangGraph que nos vaya enviando
        # los "valores" del estado conforme se va actualizando.
        stream_mode="values"
    ):
        # 'event' representa el estado de la conversación en ese momento.
        # 'event["messages"]' es la lista de mensajes acumulados.
        # '[-1]' significa "el último mensaje" (normalmente la respuesta más reciente).
        #
        # 'pretty_print()' muestra ese mensaje en pantalla de forma más amigable.
        event["messages"][-1].pretty_print()


# Definimos una función llamada 'run_chat_loop' que se encarga de
# mantener un ciclo de conversación con el usuario en la terminal/console.
def run_chat_loop():
    # 'while True' significa: repetir para siempre hasta que rompamos el ciclo.
    while True:
        try:
            # Pedimos al usuario que escriba un mensaje.
            # 'input("User: ")' muestra "User: " y espera que la persona teclee algo.
            user_input = input("User: ")
            
            # Si el usuario escribe "quit", "exit" o "q" (en cualquier combinación de mayúsculas/minúsculas),
            # entendemos que quiere terminar la conversación.
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break  # 'break' sale del ciclo y termina la función.
            
            # Si no escribió ninguna palabra de salida, llamamos a 'stream_graph_updates'
            # para que el gráfico procese el mensaje y genere respuestas.
            stream_graph_updates(user_input)
        
        # 'except:' captura cualquier error que ocurra dentro del bloque 'try'.
        # Aquí se usa para manejar fallos de forma sencilla.
        except:
            # Si ocurre un error, en lugar de mostrar un fallo técnico,
            # el sistema usa una pregunta por defecto:
            user_input = "What do you know about LangGraph?"
            print("User: " + user_input)
            
            # Llamamos otra vez a 'stream_graph_updates' pero ahora con esa pregunta fija.
            stream_graph_updates(user_input)
            
            # Después de eso, rompemos el ciclo y terminamos el chat.
            break
