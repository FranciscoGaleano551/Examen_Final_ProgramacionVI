import flet as ft
from datetime import datetime

# Contraseña fija
CONTRASENA_CORRECTA = "Fran12345"

# Lista global para almacenar nombres, edades, y fechas
lista_entradas = []


class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "Examen Final"
        self.page.bgcolor = "#EAF6F6"
        self.styles = {
            "titulo": {"size": 30, "color": "#333333"},
            "texto": {"size": 20, "color": "#666666"},
            "boton": {"color": "white", "bgcolor": "#007BFF"}
        }
        self.main_view()

    def main_view(self):
        """Vista principal de inicio de sesión."""
        self.page.clean()
        usuario_input = ft.TextField(label="Usuario", width=250)
        contrasena_input = ft.TextField(label="Contraseña", width=250, password=True)
        mensaje_error = ft.Text(value="", color="red")

        # Imagen del logo
        logo = ft.Image(
            src="C:\\Users\\TOSHIBA\\P6 Python - Francisco Galeano\\Logo.JPG",
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN,
        )

        # Botón para iniciar sesión
        boton_iniciar = ft.ElevatedButton(
            text="Iniciar",
            style=ft.ButtonStyle(
                color=self.styles["boton"]["color"], bgcolor=self.styles["boton"]["bgcolor"]
            ),
            on_click=lambda e: self.verificar_contrasena(
                contrasena_input.value, mensaje_error
            ),
        )

        contenido = ft.Column(
            controls=[
                logo,
                ft.Text("Iniciar Sesión", **self.styles["titulo"]),
                usuario_input,
                contrasena_input,
                ft.Row(
                    controls=[ft.Checkbox(label="Recordar contraseña")],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                boton_iniciar,
                mensaje_error,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        )
        self.page.add(contenido)

    def verificar_contrasena(self, contrasena, mensaje_error):
        """Verifica la contraseña ingresada por el usuario."""
        if contrasena == CONTRASENA_CORRECTA:
            mensaje_error.value = ""
            self.verificacion_edad_view()
        else:
            mensaje_error.value = "Contraseña incorrecta. Intenta nuevamente."
            mensaje_error.update()

    def verificacion_edad_view(self):
        """Vista para verificar edad."""
        self.page.clean()

        nombre_input = ft.TextField(label="Nombre", width=200)
        edad_input = ft.TextField(label="Edad", width=200)
        resultado = ft.Text(value="", color="black")

        def procesar_datos(e):
            """Procesa y valida los datos ingresados."""
            nombre = nombre_input.value.strip()
            edad = edad_input.value.strip()
            if not nombre or not edad:
                resultado.value = "Por favor, llena todos los campos."
            else:
                try:
                    edad = int(edad)
                    if edad < 0:
                        resultado.value = "Por favor, ingresa una edad válida (no negativa)."
                    else:
                        fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if edad >= 18:
                            mensaje = f"Hola {nombre}, eres mayor de edad."
                        else:
                            mensaje = f"Hola {nombre}, eres menor de edad."
                        lista_entradas.append(
                            {"Nombre": nombre, "Edad": edad, "Fecha y Hora": fecha_hora}
                        )
                        actualizar_lista()
                        resultado.value = mensaje
                except ValueError:
                    resultado.value = "Por favor, ingresa una edad válida (número)."
            resultado.update()

        def actualizar_lista():
            """Actualiza la tabla de entradas."""
            tabla_entradas.controls.clear()
            for i, entrada in enumerate(lista_entradas):
                fila = ft.Row(
                    controls=[
                        ft.TextField(value=entrada["Nombre"], on_change=lambda e, i=i: editar_nombre(i, e.control.value)),
                        ft.TextField(value=str(entrada["Edad"]), on_change=lambda e, i=i: editar_edad(i, e.control.value)),
                        ft.Text(value=entrada["Fecha y Hora"]),
                        ft.IconButton(icon=ft.icons.DELETE, on_click=lambda e, i=i: eliminar_entrada(i))
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
                tabla_entradas.controls.append(fila)
            tabla_entradas.update()

        def editar_nombre(indice, nuevo_nombre):
            lista_entradas[indice]["Nombre"] = nuevo_nombre

        def editar_edad(indice, nueva_edad):
            try:
                lista_entradas[indice]["Edad"] = int(nueva_edad)
            except ValueError:
                pass  # Ignorar valores inválidos temporalmente

        def eliminar_entrada(indice):
            lista_entradas.pop(indice)
            actualizar_lista()

        def exportar_datos(e):
            with open("historial_usuarios.txt", "w") as archivo:
                archivo.writelines(
                    f"{entrada['Nombre']} - {entrada['Edad']} años - {entrada['Fecha y Hora']}\n"
                    for entrada in lista_entradas
                )
            resultado.value = "Historial exportado a historial_usuarios.txt"
            resultado.update()

        def limpiar_campos(e):
            nombre_input.value = ""
            edad_input.value = ""
            resultado.value = ""
            nombre_input.update()
            edad_input.update()
            resultado.update()

        tabla_entradas = ft.Column()

        formulario = ft.Column(
            controls=[
                ft.Text("Verificación de Edad", **self.styles["titulo"]),
                nombre_input,
                edad_input,
                ft.Row(controls=[
                    ft.ElevatedButton(text="Procesar", on_click=procesar_datos),
                    ft.ElevatedButton(text="Limpiar", on_click=limpiar_campos),
                    ft.ElevatedButton(text="Exportar Historial", on_click=exportar_datos),
                    ft.ElevatedButton(text="Salir", on_click=lambda e: self.main_view()),
                ]),
                resultado,
            ],
        )

        self.page.add(
            ft.Column(
                controls=[
                    formulario,
                    ft.Text("Historial de Entradas:", **self.styles["texto"]),
                    tabla_entradas,
                ]
            )
        )


# Ejecutar la aplicación
ft.app(target=lambda page: App(page))

