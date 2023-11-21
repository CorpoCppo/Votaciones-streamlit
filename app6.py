import streamlit as st
import pandas as pd

# Crear un DataFrame para almacenar los votos
df_votos = pd.DataFrame(columns=['RUT', 'Candidato', 'Justificacion'])

# Lista de candidatos
candidatos = ['Candidato 1', 'Candidato 2', 'Candidato 3', 'Candidato 4', 'Candidato 5',
              'Candidato 6', 'Candidato 7', 'Candidato 8', 'Candidato 9', 'Candidato 10']

# Función para votar
def votar(rut, candidato, justificacion):
    global df_votos
    nuevo_voto = pd.DataFrame({'RUT': [rut], 'Candidato': [candidato], 'Justificacion': [justificacion]})
    df_votos = pd.concat([df_votos, nuevo_voto], ignore_index=True)

# Aplicación Streamlit
def main():
    st.title("Aplicación de Votación")

    # Obtener RUT del usuario
    rut = st.text_input("Ingrese su RUT chileno:")

    # Verificar si el RUT ya ha votado
    if rut in df_votos['RUT'].values:
        st.warning("Usted ya ha votado. Solo se permite un voto por RUT.")
        st.stop()

    # Mostrar lista de candidatos
    candidato_elegido = st.selectbox("Seleccione su candidato:", candidatos)

    # Justificación del voto
    justificacion = st.text_area("Justifique su voto:")

    # Botón para emitir el voto
    if st.button("Votar"):
        votar(rut, candidato_elegido, justificacion)
        st.success("¡Su voto ha sido registrado con éxito!")

    # Mostrar resultados
    st.subheader("Resultados Parciales:")
    st.dataframe(df_votos)

if __name__ == '__main__':
    main()
