import win32print

def label_print(message):
    font_file = open("font_data.txt", "rb")
    print_data = font_file.read()
    font_file.close()

    printer_settings = f"""ZT
N
Q100,0
q135
A128,0,1,a,2,2,N,\"         {message}         \"
P1
"""
    printer_settings_bytes = bytes(printer_settings, "utf-8")

    print_data = print_data + printer_settings_bytes

    output = open("output.txt", "wb")
    output.write(print_data)
    output.close()
    
    printer_name = win32print.GetDefaultPrinter()
    printer = win32print.OpenPrinter(printer_name)
    
    try:
        printjob = win32print.StartDocPrinter(printer, 1, ("ribbon", None, "RAW"))
        try:
            win32print.StartPagePrinter(printer)
            win32print.WritePrinter(printer, print_data)
            win32print.EndPagePrinter(printer)
        finally:
            win32print.EndDocPrinter(printer)
            
    finally:
        win32print.ClosePrinter(printer)
    

    
