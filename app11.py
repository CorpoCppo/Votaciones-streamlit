import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# Configuración de estilo para seaborn
sns.set(style="whitegrid")

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

# Función para validar RUT chileno
def validar_rut(rut):
    patron_rut = re.compile(r'^\d{7,8}[-][0-9kK]$')
    if not patron_rut.match(rut):
        return False

    rut_numero, verificador = rut.split('-')
    rut_numero = int(rut_numero)

    suma = 0
    multiplo = 2

    for digito in reversed(str(rut_numero)):
        suma += int(digito) * multiplo
        multiplo = multiplo + 1 if multiplo < 7 else 2

    resto = suma % 11
    digito_verificador_esperado = str(11 - resto) if resto != 0 else '0'

    return digito_verificador_esperado == verificador.upper()

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

# Función para obtener el candidato más votado
def obtener_candidato_mas_votado():
    df = obtener_resultados()
    if not df.empty:
        candidato_mas_votado = df['candidato'].value_counts().idxmax()
        return candidato_mas_votado
    return None

# Aplicación Streamlit
def main():
    st.title("Aplicación de Votación 🗳️")

    # Obtener RUT del usuario
    st.markdown("## El rut debe ser en formato 9780133-1 ")
    rut = st.text_input("Ingrese su RUT:")

    # Validar el RUT
    if not validar_rut(rut):
        st.warning("El formato del RUT no es válido.")
        st.stop()

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
