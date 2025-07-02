import win32print
import base64
import json
import urllib.request
import zipfile
import sys
import os
import glob


def label_print(b64Params):
    
    decoded_params = base64.b64decode(b64Params)
    param_dict = json.loads(decoded_params)
    
    file_url = "http://charger2.tpsuk.local/ribbon/getribbons.php?ribbon=" + param_dict["URL"]
    printer_name = param_dict["printer"]
    
    ## Get the ribbon data zip
    try:
        urllib.request.urlretrieve(file_url, "tempfiles/ribbondata.zip")
    except urllib.error.URLError:
        server_name = file_url.split(".")[0].split("//")[1]
        print(f"Could not reach server {server_name}. Is it offline?")
    
    ## unzip to a temporary file
    try:
        with zipfile.ZipFile("tempfiles/ribbondata.zip", 'r') as zip_ref:
            zip_ref.extractall("tempfiles")
    except zipfile.BadZipFile:
        print("Downloaded file is empty. Check the \"?ribbon=\" parameter is correct.")
    except FileNotFoundError:
        print("ribbondata.zip not found. Did it fail to download?")
    
    ## get data from unzipped file, move it to print_data variable
    print_data = b""
    try:
        ribbon_file = param_dict["URL"] ## ribbon file is named the same as the URL end
        print("ribbon_file_name: ", ribbon_file)
        f = open("./tempfiles/" + ribbon_file, "rb")
        
        print_data = f.read()
        f.close()        
    except FileNotFoundError:
        print("Ribbon file not found. Was it unzipped from ribbondata.zip successfully?")
    
    ## delete temporary files
    files = glob.glob("tempfiles/*")
    for f in files:
        os.remove(f)
        
    
    ## send to printer
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
        
label_print(sys.argv[1])

