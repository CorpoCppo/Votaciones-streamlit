import streamlit as st
import sqlite3

# Conectar a la base de datos SQLite (se creará si no existe)
conn = sqlite3.connect('empleados.db')
c = conn.cursor()

# Crear tabla Departamentos si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS Departamentos (
        DepartamentoID INTEGER PRIMARY KEY,
        NombreDepartamento TEXT
    )
''')

# Crear tabla Empleados si no existe
c.execute('''
    CREATE TABLE IF NOT EXISTS Empleados (
        EmpleadoID INTEGER PRIMARY KEY,
        Nombre TEXT,
        DepartamentoID INTEGER,
        FOREIGN KEY (DepartamentoID) REFERENCES Departamentos(DepartamentoID)
    )
''')

# Función para agregar un empleado
def agregar_empleado(nombre, departamento_id):
    c.execute("INSERT INTO Empleados (Nombre, DepartamentoID) VALUES (?, ?)", (nombre, departamento_id))
    conn.commit()

# Función para obtener la lista de empleados
def obtener_empleados():
    c.execute("SELECT Empleados.Nombre, Departamentos.NombreDepartamento FROM Empleados JOIN Departamentos ON Empleados.DepartamentoID = Departamentos.DepartamentoID")
    return c.fetchall()

# Función para obtener la lista de departamentos
def obtener_departamentos():
    c.execute("SELECT * FROM Departamentos")
    return c.fetchall()

# Función para obtener el nombre de los departamentos
def obtener_nombres_departamentos():
    c.execute("SELECT NombreDepartamento FROM Departamentos")
    return [departamento[0] for departamento in c.fetchall()]

# Interfaz de usuario con Streamlit
st.title('Formulario de Empleados')

nombre = st.text_input('Nombre del Empleado:')
departamentos = obtener_nombres_departamentos()
departamento_seleccionado = st.selectbox('Departamento:', departamentos)

if st.button('Agregar Empleado'):
    # Obtener el ID del departamento seleccionado
    departamento_id = departamentos.index(departamento_seleccionado) + 1

    # Agregar el empleado a la base de datos
    agregar_empleado(nombre, departamento_id)

    st.success(f'Se ha agregado a {nombre} al departamento {departamento_seleccionado}')

# Mostrar la lista de empleados en forma de tabla con encabezados
empleados = obtener_empleados()

if empleados:
    st.subheader('Empleados Agregados:')
    st.table(empleados)
else:
    st.info('No hay empleados registrados en el sistema.')

# Cerrar la conexión a la base de datos
conn.close()
