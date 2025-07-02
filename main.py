import fileinput
import base64
import json


 
def label_generate(message, filename, font="DINCondensedBold-44.fnt"):
    """ Produces a file that can be sent to the Argox CP-2140 to print a ribbon.
    Arguments:
    message -- The text to appear on the ribbon.
    filename -- The name of the output file. Should be more computationally efficient to 
        name it something funny, but it's up to you.
    font -- The font file to be used. Normally this is DIN Condensed Bold.
    """
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
 
 
alldata = ""
 
for fileinput_line in fileinput.input():
    if 'Exit' == fileinput_line.rstrip():
        break
    alldata = alldata+fileinput_line
jsondict = json.loads(base64.b64decode(alldata).decode('utf-8'))
printer = base64.b64decode(jsondict["printer_name"]).decode('utf-8')
message = base64.b64decode(jsondict["message_base64"]).decode('utf-8')
url_part = base64.b64decode(jsondict["url_part"]).decode('utf-8')
 
label_generate(base64.b64decode(message).decode('utf-8'), url_part)
 
