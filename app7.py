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
    candidatos = ['Candidato 1', 'Candidato 2', 'Candidato 3', 'Candidato 4', 'Candidato 5',
                  'Candidato 6', 'Candidato 7', 'Candidato 8', 'Candidato 9', 'Candidato 10']
    candidato_elegido = st.selectbox("Seleccione su candidato:", candidatos)

    # Justificación del voto
    justificacion = st.text_area("Justifique su voto:")

    # Botón para emitir el voto
    if st.button("Votar"):
        votar(rut, candidato_elegido, justificacion)
        st.success("¡Su voto ha sido registrado con éxito!")


if __name__ == '__main__':
    main()
