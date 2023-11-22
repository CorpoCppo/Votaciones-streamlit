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
def valida_rut(rut_completo):
    if not re.match(r'^\d+-[0-9kK]$', rut_completo, re.IGNORECASE):
        return False

    rut, digv = rut_completo.split('-')

    if digv.lower() == 'k':
        digv = 'k'

    return calcular_dv(rut) == digv

# Función para calcular el dígito verificador
def calcular_dv(rut):
    M = 0
    S = 1

    for T in reversed(list(map(int, rut))):
        S = (S + T * (9 - M % 6)) % 11
        M += 1

    return str(S - 1) if S else 'k'

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
    if not valida_rut(rut):
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

    # Mostrar resultados
    st.subheader("Resultados Parciales:")
    df_resultados = obtener_resultados()
    st.dataframe(df_resultados)

    # Visualizar gráfico del candidato más votado
    candidato_mas_votado = obtener_candidato_mas_votado()
    if candidato_mas_votado:
        st.subheader("Candidato más votado:")
        st.write(f"El candidato más votado hasta ahora es: {candidato_mas_votado}")

        # Graficar
        st.subheader("Gráfico de Votos por Candidato:")
        plt.figure(figsize=(8, 8))
        df_votos_candidato = df_resultados['candidato'].value_counts()
        plt.pie(df_votos_candidato, labels=df_votos_candidato.index, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(plt)

if __name__ == '__main__':
    main()
