import Querries
import pdfkit
import os
import datetime
from flask import Flask, send_from_directory

path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtmltopdf)

def make_pdf(id):

    data = Querries.facultyReport(id)

    return querry_to_html(data, id)    


def querry_to_html(data, faculty_id):
    
    start = f"""
    <html>
      <head>

        <meta name="pdfkit-page-size" content="Legal"/>
        <meta name="pdfkit-orientation" content="Landscape"/>

      </head>

      <body>
      <h2>Fakultät {faculty_id}</h2>
      <table  id="report_table">
      <tr>
        <th>Land</th>
        <th>Name</th>
        <th>Vertragsart</th>
        <th>Programmbeauftragter</th>
        <th>Dauer</th>
      </tr> """
    

    result = start

    for dictionary in data:

        loop = """<tr>"""

        for dicotionary_item in dictionary:

            loop_item = f""" <td>
            {dictionary[dicotionary_item]}
            </td>
            """ 
            loop+= loop_item
        
        loop+= """</tr>"""

        result+= loop

    result += """</table>"""

    style = """<style>
    table, th, td {
    border: 1px solid;
    border-collapse: collapse;
    }
    th, td {
    padding: 10px;
    }
    </style>"""

    result += style

    closingtag = """
    createPDF();
    </body>
    </html>
    """

    result += closingtag 

    #result_encoded = result.encode("utf-8")
    #result_decoded = result_encoded.decode()

    #path = "../../reports/"
    naming = f"reports/FacultyReport_{faculty_id}_" + getPDFName() + ".pdf"
    #path+= naming

    workingdir = os.path.abspath(os.getcwd())
    pdfkit.from_string(result, output_path=naming, configuration=config)
   
    #filename = "../" + naming

    #path = workingdir + 
    return send_from_directory(workingdir, naming)

    #return result

def getPDFName():
    date = datetime.datetime.now().date()
    return str(date)