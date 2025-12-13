# Importamos 'Annotated' desde el módulo 'typing'.
# 'Annotated' se utiliza para dar información extra sobre un tipo de dato.
# En términos simples: sirve para "decorar" o etiquetar un tipo (por ejemplo, una lista)
# con metadatos que otras herramientas pueden usar.
from typing import Annotated 

# Importamos 'TypedDict' desde 'typing_extensions'.
# 'TypedDict' nos permite definir "diccionarios con forma fija".
# Es decir, estructuras de datos que se parecen a un objeto con campos definidos.
# Por ejemplo:
#   {
#       "messages": [...]
#   }
# y podemos decir de qué tipo es cada campo.
from typing_extensions import TypedDict

# Importamos 'add_messages' desde langgraph.graph.message.
# Esta función se usa como anotación especial para indicar a LangGraph
# cómo debe manejar la lista de mensajes (por ejemplo, cómo agregar nuevos mensajes
# al estado de la conversación).
from langgraph.graph.message import add_messages


# Definimos una clase llamada 'State' que hereda de 'TypedDict'.
# En palabras sencillas:
#   - Estamos definiendo la "forma" del estado de la conversación.
#   - Es como decir: "nuestro estado será un diccionario con ciertas llaves".
class State(TypedDict):
    # Definimos un campo llamado 'messages' dentro de State.
    #
    # 'messages' va a ser una lista (list) de mensajes.
    # Pero además usamos 'Annotated[list, add_messages]' para decir:
    #   - Es una lista.
    #   - Y LangGraph debe aplicar la lógica de 'add_messages' cuando
    #     se agreguen nuevos mensajes a este campo.
    #
    # En la práctica, esto le dice a LangGraph:
    #   "Este campo guarda el historial de mensajes de la conversación,
    #    y cada vez que devuelvas nuevos mensajes, añádelos a esta lista."
    messages: Annotated[list, add_messages]
