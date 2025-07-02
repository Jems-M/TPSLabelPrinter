import fileinput
import base64
import json

## Produces a file that can be sent to the Argox CP-2140 to print a ribbon.
# Outputs its junk into /tempfiles/.
# message: The text to appear on the ribbon.
# filename: The name of the output file. Should be more computationally efficient to 
    # name it something funny, but it's up to you.
# font: The font file to be used. Normally this is DIN Condensed Bold. TODO: Explainer
    # on how to make font files.
 
def label_generate(message, filename, font="DINCondensedBold-44.fnt"):
    font_file = open("./fonts/" + font, "rb")
    print_data = font_file.read()
 
    font_file.close()
 
    printer_settings = f"""ZT
N
Q100,0
q135
A128,0,1,a,1,1,N,\"         {message}         \"
P1
"""
    printer_settings_bytes = bytes(printer_settings, "utf-8")
 
    print_data = print_data + printer_settings_bytes
 
    output = open("./tempfiles/" + filename, "wb")
    output.write(print_data)
    output.close()
