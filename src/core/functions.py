import ctypes
import ctypes.wintypes
from core.variables import *
from PIL import Image as pimg
import unicodedata

# Declare dlls
winspool = ctypes.WinDLL("WINSPOOL.DRV")
kernel32 = ctypes.WinDLL("KERNEL32")

# Types 
HANDLE = ctypes.wintypes.HANDLE
LPBYTE = ctypes.POINTER(ctypes.c_ubyte)
DWORD = ctypes.wintypes.DWORD
LPCWSTR = ctypes.wintypes.LPCWSTR

# StartDocPrinter required structure
class DOC_INFO_1(ctypes.Structure):
    _fields_ = [("pDocName", LPCWSTR),
                ("pOutputFile", LPCWSTR),
                ("pDatatype", LPCWSTR)]
    
def open_printer(printer_name):
        printer_handle = HANDLE()
        winspool.OpenPrinterW(printer_name, ctypes.byref(printer_handle), None)
        return printer_handle

def close_printer(printer_handle):
    winspool.ClosePrinter(printer_handle)

# Start printer work
def start_doc_printer(printer_handle, doc_name):
    doc_info = DOC_INFO_1()
    doc_info.pDocName = doc_name
    doc_info.pOutputFile = None
    doc_info.pDatatype = "RAW"
    winspool.StartDocPrinterW(printer_handle, 1, ctypes.byref(doc_info))

# Finish printer work
def end_doc_printer(printer_handle):
    winspool.EndDocPrinter(printer_handle)

# Writing data in printer
def write_printer(printer_handle, data):
    bytes_written = DWORD()
    success = winspool.WritePrinter(printer_handle, data, len(data), ctypes.byref(bytes_written))
    if not success:
        raise ctypes.WinError()
    return bytes_written.value

# Send POS
def send_text(printer_name, escpos_data):    
    printer_handle = open_printer(printer_name)
    try:
        
        start_doc_printer(printer_handle, "pos-ticket")
        config = b'\x1B\x74\x12'
        write_printer(printer_handle, config)
        
        textoSinTildes = clear_accent_marks(escpos_data)
        if isinstance(textoSinTildes,str):
            raw_data = textoSinTildes.encode("CP852", errors='ignore')
        else:
            raw_data = textoSinTildes
        
        write_printer(printer_handle, raw_data)
    finally:
        end_doc_printer(printer_handle)
        close_printer(printer_handle)
       
def image_to_escpos(image_path, max_width=300): #The recommended width is 200 for practicality and compatiblity.
                                                #It can be wider, but you need adjust regard your printer limit.
                                                #If you pass the printer's limit, your printer maybe restart
    
    img = pimg.open(image_path).convert("L")  # Gray scale
    img_width, img_height = img.size

    # convert to mono
    img = img.convert("1")

    # Rasterize esc/pos
    escpos = bytearray()
    escpos += b"\x1B\x40"  # Reset printer
    escpos += b"\x1B\x61\x01"  # align
    escpos += b"_" * 32
    escpos += b"\x1D\x76\x30\x00"  # Raster bit image
    width_bytes = (img.width + 7) // 8  # width in bytes
    escpos += (width_bytes & 0xFF).to_bytes(1, 'little')
    escpos += (width_bytes >> 8).to_bytes(1, 'little')
    escpos += (img.height & 0xFF).to_bytes(1, 'little')
    escpos += (img.height >> 8).to_bytes(1, 'little')

    # Process the image line to line
    pixels = img.load()
    for y in range(img.height):
        row_data = bytearray()
        for x in range(0, img.width, 8):
            byte = 0
            for bit in range(8):
                if x + bit < img.width and pixels[x + bit, y] == 0:
                    byte |= (1 << (7 - bit))
            row_data.append(byte)
        escpos += row_data
    escpos += b"\n"
    return bytes(escpos)

    
        
def send_image(printer_name, imgpath):
    printer_handle = open_printer(printer_name)
    img = image_to_escpos(imgpath)
    try:
        start_doc_printer(printer_handle, "pos-ticket")
        write_printer(printer_handle, img)
    finally:
        end_doc_printer(printer_handle)
        close_printer(printer_handle)

#Create spaces if you need fill out the line      
def spacing_generator(left_text, right_text, max_chars=32):
        center = " " * (max_chars - len(right_text) - len(left_text))
        return f"{left_text}{center}{right_text}"

#Create middle dash if you need fill out the line
def dash_generator(max_chars=32):
    dash = "─" * (max_chars)
    return f"{dash}"

#This break the line regarding the "max_chars" limit. The choice depends
#on your printer's limits
def line_break(text, max_chars=32):
    import textwrap
    original_lines = text.split('\n')
    process = [
        textwrap.fill(line, max_chars)
        for line in original_lines
    ]
    result = '\n'.join(process)
    return result

#Clear all accent marks of the text
def clear_accent_marks(text):
    sin_tildes = unicodedata.normalize("NFD", text)
    return ''.join(
        c for c in sin_tildes
        if not unicodedata.combining(c)
    )

if __name__ == "__main__":
    printer_name = "posnet"
    direccion = "Tu dirección 1234"
    contacto = "1123871936"
    condiciones = """
La empresa solo se responsabiliza de la reparacion dentro del tiempo de gerantia correspondiente y unicamente por la reparacion realizada al dispositivo que se detalla en dicho ticket. Los equipos solo seran validos para garantia si los sellos de garantia no fueron violados.
"""
    bloque = dash_generator()
    text_example = ( 
            f"\x1B\x40" # Init printer 
            f"{negrita_on}{grande}{fuente_b}{centro}Ticket\n{negrita_off}"                              
            f"{pequeño}{izquierda}{fuente_a}{bloque}\n"
            f"{pequeño}{negrita_on}{centro}Servicio\n"            
            f"{negrita_off}{bloque}"
            f"{doble_ancho}{centro}Informacion del\n cliente\n"
            f"{pequeño}{izquierda}{bloque}"
            f"{spacing_generator("Nombre", "Cliente")}\n"
            f"{spacing_generator("Celular", "Numero")}\n"            
            f"{bloque}\n"
            f"{doble_ancho}{centro}Informacion del dispositivo\n"
            f"{pequeño}{izquierda}{bloque}\n"
            f"{spacing_generator("Marca", "Samsung")}\n"
            f"{spacing_generator("Modelo", "A04s")}\n"
            f"{spacing_generator("Color", "Cyan")}\n"
            f"{spacing_generator("IMEI", "350000000000000")}\n"
            f"{spacing_generator("Reparacion", "Sistema / full")}\n"            
            f"{spacing_generator("Reparacion", "Instalar apps")}\n"  
            f"CUENTA DNI - UALA - MERCADOPAGO\n - MI ARGENTINA\n"          
            f"{bloque}\n"            
            f"\n\n\n\n\n"
            f"{corte_parcial}"
        )          
    path = "your_image_in_grayscale.bmp"
    # send_image(printer_name, path)
    send_text(printer_name, text_example)