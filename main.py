import os
import sqlite3


def obtener_ultimas_busquedas(history_db_path, output_file_path):
    # Conectar a la base de datos
    conn = sqlite3.connect(history_db_path)
    cursor = conn.cursor()

    # Consulta SQL para obtener las últimas 10 búsquedas
    query = """
        SELECT term
        FROM keyword_search_terms
        ORDER BY last_visit_time DESC
        LIMIT 10;
    """

    # Ejecutar la consulta
    cursor.execute(query)

    # Obtener los resultados
    search_terms = [row[0] for row in cursor.fetchall()]

    # Cerrar la conexión a la base de datos
    conn.close()

    # Guardar las búsquedas en un archivo de texto
    with open(output_file_path, 'w') as f:
        f.write("Últimas 10 búsquedas en Microsoft Edge:\n")
        for i, term in enumerate(search_terms, start=1):
            f.write(f"{i}. {term}\n")

    print("Las últimas 10 búsquedas han sido guardadas en el archivo:", output_file_path)


if __name__ == "__main__":
    # Determinar la ubicación del perfil de Microsoft Edge según el sistema operativo
    if os.name == "posix":  # macOS
        edge_profile_path = os.path.expanduser("~/Library/Application Support/Microsoft Edge/Default")
    elif os.name == "nt":  # Windows
        edge_profile_path = os.path.join(os.getenv("APPDATA"), "Local", "Microsoft", "Edge", "User Data", "Default")
    else:
        raise NotImplementedError("Este sistema operativo no es compatible")

    # Ruta a la base de datos del historial de búsqueda de Edge
    history_db_path = os.path.join(edge_profile_path, "History")

    # Ruta de salida para el archivo de texto
    output_file_path = 'ultimas_busquedas_edge.txt'

    obtener_ultimas_busquedas(history_db_path, output_file_path)
