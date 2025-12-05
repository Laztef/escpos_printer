iniciar = "\x1B\x40"
grande = "\x1d\x21\x11"
pequeño= "\x1d\x21\x00"
doble_ancho = "\x1d\x21\x10"
doble_alto = "\x1d\x21\x01"
doble_ancho_alto = "\x1d\x21\x22"
condensado_on = "\x0f"
condensado_off = "\x12"
subrayado_doble = "\x1b\x2d\x02"
ancho_normal = "\x1b\x57\x00"
negrita_on = "\x1b\x45\x01"
negrita_off = "\x1b\x45\x00"
subrayado_simple_on = "\x1b\x2d\x01"
subrayado_simple_off = "\x1b\x2d\x00"
subrayado_doble_on = "\x1b\x2d\x02"
subrayado_doble_off = "\x1b\x2d\x00"
invertir_color_on = "\x1d\x42\x01"
invertir_color_off = "\x1d\x42\x00"
fuente_a = "\x1b\x4d\x00"
fuente_b = "\x1b\x4d\x01"
izquierda = "\x1b\x61\x00"
centro = "\x1b\x61\x01"
derecha = "\x1b\x61\x02"
avanzar_papel_1_línea = "\x1b\x64\x01"  
avanzar_papel_2_línea = "\x1b\x64\x02"  
avanzar_papel_3_línea = "\x1b\x64\x03"  
avanzar_papel_5_línea = "\x1b\x64\x05"  
avanzar_papel_10_línea = "\x1b\x64\x10"  
corte_parcial = "\x1b\x69"
corte_total = "\x1b\x70"
avance_línea = "\x1b\x4a\x01" 
avance_2_línea = "\x1b\x4a\x02" 
avance_3_línea = "\x1b\x4a\x03" 
avance_5_línea = "\x1b\x4a\x05" 
avance_10_línea = "\x1b\x4a\x10" 
fuente_frac_1 = "\x1b\x21\x01"
fuente_frac_2 = "\x1b\x21\x02"
fuente_mediana = "\x1b\x21\x12"

acciones = {
    "iniciar" : iniciar,
    "#F" : fuente_a,
    "#f" : fuente_b,
    "**" : negrita_on,
    "/*" : negrita_off,
    "__" : subrayado_simple_on,
    "/_" : subrayado_simple_off,
    "==" : subrayado_doble,
    "/=" : subrayado_doble_off,
    "<=" : izquierda,
    "||" : centro,
    "=>" : derecha,
    "#+" : grande,
    "*+" : doble_alto,
    "#-" : pequeño,
    "*-" : doble_ancho,
    "\n" : "\x0A"
}

# Seleccionar el tipo de código de barras
code128 = "\x1d\x6b\x49"
cod_barras_upc_a = "\x1d\x6b\x00"
cod_barras_upc_e = "\x1d\x6b\x01"
cod_barras_ean13 = "\x1d\x6b\x02"
cod_barras_code39 = "\x1d\x6b\x04"
# Especificar el contenido del código de barras entre paréntesis 
# contenido_code128 = "\x1d\x6b\x49{longitud}{contenido_code128}" 
# "{longitud}" es la longitud del contenido (de 1 a 255) 
# "{contenido_code128}" es el contenido del código de barras en sí 
# ejemplo_code128 = "\x1d\x6b\x49\x0cABCDEFGHIJKL" # Ejemplo de texto "ABCDEFGHIJKL" en Code 128
