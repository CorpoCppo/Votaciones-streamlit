import streamlit as st
import sqlite3
import pandas as pd

# Conectar a la base de datos SQLite (se crea si no existe)
conn = sqlite3.connect('votacion.db')
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS votos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rut TEXT,
        candidato TEXT,
        justificacion TEXT
    )
''')
conn.commit()

# Función para votar
def votar(rut, candidato, justificacion):
    cursor.execute('''
        INSERT INTO votos (rut, candidato, justificacion) VALUES (?, ?, ?)
    ''', (rut, candidato, justificacion))
    conn.commit()

# Función para obtener resultados
def obtener_resultados():
    df = pd.read_sql_query('SELECT * FROM votos', conn)
    return df

# Aplicación Streamlit
def main():
    st.title("Aplicación de Votación")

    # Obtener RUT del usuario
    rut = st.text_input("Ingrese su RUT chileno:")

    # Verificar si el RUT ya ha votado
    cursor.execute('SELECT rut FROM votos WHERE rut = ?', (rut,))
    if cursor.fetchone():
        st.warning("Usted ya ha votado. Solo se permite un voto por RUT.")
        st.stop()

    # Mostrar lista de candidatos
    candidatos = ['Alejandra Rojas Alfaro', 'Carlos Carrasco Varas', 'Carlos Flores Zuñiga ', 'Daniel Caminada Cortez', 'Daniela Aróstica Salinas',
                  'Daniela Castillo Morales', 'David Villarroel Esteban', 'Delia Carmona Durán', 'Eduardo López Pizarro', 'Ericko Carvajal Barrera',
                  'Evelyn Jara Varas','Felipe Castillo Manquecoy','Felipe Guerrero Tabilo','Franco Espinoza Lobos','Leonardo Piñones Castillo',
                  'Lissette Borja Soto','Lorena Miranda Arrocet','Luis Olivares Cano','María Eugenia Herrera Campusano','Maylin Rivera Escobar',
                  'Rodrigo Leyton Araya','Vanessa Millacheo Acuna','Victor Quevedo Araya','Ximena Zenteno Aguirre']
    candidato_elegido = st.selectbox("Seleccione su candidato:", candidatos)

    # Justificación del voto
    justificacion = st.text_area("Justifique su voto:")

    # Botón para emitir el voto
    if st.button("Votar"):
        votar(rut, candidato_elegido, justificacion)
        st.success("¡Su voto ha sido registrado con éxito!")


if __name__ == '__main__':
    main()
