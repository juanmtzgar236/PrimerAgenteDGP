# Esta línea dice:
# "Toma (importa) del archivo llamado 'chat.py' una función que se llama 'run_chat_loop'."
#
# En otras palabras:
# - Existe otro archivo de código llamado 'chat.py'.
# - Dentro de ese archivo hay una función que ya programamos antes,
#   llamada 'run_chat_loop', que se encarga de manejar la conversación
#   con el usuario (el ciclo del chat en la terminal).
from chat import run_chat_loop


# Esta parte es una forma estándar en Python de decir:
# "Si este archivo se está ejecutando directamente (no como parte de otro),
# entonces haz lo siguiente..."
if __name__ == "__main__":
    # Llamamos a la función 'run_chat_loop()'.
    # Esto inicia el chat interactivo en la consola:
    # - Aparece el prompt "User: "
    # - El usuario puede escribir mensajes
    # - El chatbot responde usando toda la lógica que ya definimos antes.
    run_chat_loop()
