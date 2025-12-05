import flet as ft
from core.functions import send_text, line_break
from core.variables import *


#UI Ejemplo para poner en práctica las funciones de la impresora
#UI Example to try the printer functions



def main(page: ft.Page):
    page.window.height= 700
    page.window.width= 600
    page.window.maximizable = False
    page.window.resizable = False
    
    # Diccionario de reemplazos (palabra clave: valor a reemplazar)
    def procesar_texto(e):
        printer_name = "posnet"
        # Obtener texto original
        texto_original = tf_texto.value
        
        # Reemplazar palabras clave#
        # Replace words
        texto_procesado = texto_original
        for clave, valor in acciones.items():
            texto_procesado = texto_procesado.replace(clave, valor)
        texto_formateado = line_break(texto_procesado)
        terminado = (f"\x1B\x40"                     
                    f"{texto_formateado}\n\n\n\n\n")
        # Actualizar el texto de salida
        # Refresh the text
        send_text(printer_name, terminado)
        texto_salida.value = texto_formateado
        page.update()
        
    def includeFormat(e):
        data = e.control.data
        tf_texto.value += data
        page.update()
    # Componentes de la UI
    # UI components
    tf_texto = ft.TextField(label="Ingresa tu texto", multiline=True, height=300)
    boton_procesar = ft.ElevatedButton("Imprimir", on_click=procesar_texto)
    texto_salida = ft.Text(width=200)
    column1 = ft.Column(
        [
        ft.Text("Herramienta para imprimir texto en posnet"),
        tf_texto, boton_procesar, 
        ft.Row([
               ft.Column([texto_salida],
                         scroll="Always")
               ],
                height=200)
        ],
        height=600,
        width=400,
        alignment=ft.MainAxisAlignment.START,
        
    )
    column2 = ft.Column([
        ft.ElevatedButton(text="Font A", icon=ft.Icons.FONT_DOWNLOAD, data="#F", on_click=includeFormat),
        ft.ElevatedButton(text="Font B", icon=ft.Icons.FONT_DOWNLOAD_OUTLINED, data="#f", on_click=includeFormat),
        ft.ElevatedButton(text="Bold", icon=ft.Icons.FORMAT_BOLD, icon_color="green", data="**", on_click=includeFormat),        
        ft.ElevatedButton(text="Bold Off", icon=ft.Icons.FORMAT_BOLD, icon_color="red", data="/*", on_click=includeFormat),        
        ft.ElevatedButton(text="Underline", icon=ft.Icons.FORMAT_UNDERLINE, icon_color="green", data="__", on_click=includeFormat),
        ft.ElevatedButton(text="Under Off", icon=ft.Icons.FORMAT_UNDERLINE, icon_color="red", data="/_", on_click=includeFormat),
        ft.ElevatedButton(text="Align left", icon=ft.Icons.ALIGN_HORIZONTAL_LEFT, data="<=", on_click=includeFormat),        
        ft.ElevatedButton(text="Align center", icon=ft.Icons.ALIGN_HORIZONTAL_CENTER, data="||", on_click=includeFormat),        
        ft.ElevatedButton(text="Align right", icon=ft.Icons.ALIGN_HORIZONTAL_RIGHT, data="=>", on_click=includeFormat),
        ft.ElevatedButton(text="Biggest", icon=ft.Icons.EXPAND, data="#+", on_click=includeFormat),
        ft.ElevatedButton(text="Little", icon=ft.Icons.COMPRESS, data="#-", on_click=includeFormat),        
        ft.ElevatedButton(text="Double high", icon=ft.Icons.EXPAND, data="*+", on_click=includeFormat),        
        ft.ElevatedButton(text="Double wide", icon=ft.Icons.SWITCH_LEFT_SHARP, data="*-", on_click=includeFormat)      
    ])
      
    page.add(
             ft.Row(
                 [
                     column1,
                     column2
                 ],
                 alignment=ft.MainAxisAlignment.CENTER
             ))

ft.app(target=main)