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
    # Expresión regular para validar RUT chileno
    patron_rut = re.compile(r'^[0-9]+-[0-9kK]{1}$')
    if not patron_rut.match(rut):
        return False

    # Separar el número y el dígito verificador
    rut_numero, verificador = rut[:-1], rut[-1]

    # Reemplazar puntos y convertir a entero
    rut_numero = int(rut_numero)

    # Calcular el dígito verificador esperado
    suma = 0
    multiplo = 2

    for digito in reversed(str(rut_numero)):
        suma += int(digito) * multiplo
        multiplo = multiplo + 1 if multiplo < 7 else 2

    resto = suma % 11
    digito_verificador_esperado = str(11 - resto) if resto != 0 else '0'

    # Comparar el dígito verificador
    return digito_verificador_esperado.upper() == verificador.upper()

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
    st.title("Aplicación de Votación")

    # Obtener RUT del usuario
    rut = st.text_input("Ingrese su RUT chileno:")

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
    candidatos = ['Candidato 1', 'Candidato 2', 'Candidato 3', 'Candidato 4', 'Candidato 5',
                  'Candidato 6', 'Candidato 7', 'Candidato 8', 'Candidato 9', 'Candidato 10']
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
