import Querries
import pdfkit
import os
import datetime
from flask import Flask, send_from_directory

path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf = path_to_wkhtmltopdf)

def make_faculty_pdf(id):
  '''
  Daten für den Bericht zur Fakultät der gewünschten id holen
  '''

  faculty_data = Querries.facultyReport(id)
  return faculty_querry_to_html(faculty_data, id)  


def make_erasmus_pdf():
  '''
  Daten für den Bericht zu Erasmuspartnerschafen holen
  '''
    
  erasmus_report_data = Querries.erasmusReport()
  erasmus_data = Querries.erasmusData()


  return erasmus_querry_to_html(erasmus_report_data, erasmus_data)

  
def make_institute_pdf():
  '''
  Daten für den Bericht über alle Hochschulpartnerschaften holen
  '''
  
  institute_report_data = Querries.instituteReport()
  institute_data = Querries.instituteReportData()
  
  return institute_querry_to_html(institute_report_data, institute_data)


def institute_querry_to_html(report, data):
  '''
  Erzeugt eine html-Seite, gefüllt mit den Daten zu Hochschulpartnerschaften, wandelt diese in eine pdf-Datei um, welche dann zurückgegeben wird
  '''
  
  start = f"""
    <html> 
    <head>

      <meta charset="utf-8">
      <meta name="pdfkit-page-size" content="Legal"/>
      <meta name="pdfkit-orientation" content="Landscape"/>

    </head>

    <body>
    <h2>Hochschulpartnerschaften</h2>

    <table id="report_table">
    <tr>
      <th>Land</th>
      <th>Name</th>
      <th>Programmbeauftragter</th>
      <th>Dauer</th>
      <th>Vertragsart</th>
    </tr>
    """
      
  result = start

  agreement_count = 0
  country_count = 0
  partner_count = 0

  for dictionary in report:

    loop = """<tr>"""
    loop_item = f"""<td>{dictionary["Name"]}</td>"""
    loop_item+= f"""<td>{dictionary["Land"]}</td>"""
    loop_item+= f"""<td>{dictionary["Vertrag"]}</td>"""
    loop_item+= f"""<td>{dictionary["Mentor"]}</td>"""
    loop_item+= f"""<td>{dictionary["Dauer"]}</td>"""
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

  for dataset in data:
        
    agreement_count = dataset["AnzahlVereinbarungen"]
    country_count = dataset["AnzahlLaender"]
    partner_count = dataset["AnzahlPartner"]

  closingtag = f"""
    <br>
    <p>Anzahl Vereinbarungen : {agreement_count} <br>
    Anzahl Länder : {country_count} <br>
    Anzahl Partnerhochschulen: {partner_count} <br>
    </p>
    </body>
    </html>
    """

  result += closingtag

  naming = f"reports/InstituteReport_" + get_date_as_str() + ".pdf"

  workingdir = os.path.abspath(os.getcwd())
  pdfkit.from_string(result, output_path=naming, configuration=config)

  return send_from_directory(workingdir, naming)
  return result

def erasmus_querry_to_html(report, data):
  '''
  Erzeugt eine html-Seite, gefüllt mit den Daten zu Erasmuspartnerschaften, wandelt diese in eine pdf-Datei um, welche dann zurückgegeben wird
  '''          
  start = f"""
    <html>
      <head>

        <meta charset="utf-8">
        <meta name="pdfkit-page-size" content="Legal"/>
        <meta name="pdfkit-orientation" content="Landscape"/>

      </head>

      <body>
      <h2>Erasmuspartnerschaften</h2>

      <table id="report_table">
      <tr>
        <th>Land</th>
        <th>Name</th>
        <th>Programmbeauftragter</th>
        <th>Dauer</th>
        <th>Vertragsart</th>
      </tr>
      """
    
  result = start

  agreement_count = 0
  country_count = 0
  partner_count = 0

  for dictionary in report:

    loop = """<tr>"""
    loop_item = f"""<td>{dictionary["Land"]}</td>"""
    loop_item+= f"""<td>{dictionary["Name"]}</td>"""
    loop_item+= f"""<td>{dictionary["Mentor"]}</td>"""
    loop_item+= f"""<td>{dictionary["Dauer"]}</td>"""
    loop_item+= f"""<td>{dictionary["Vertrag"]}</td>"""
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

  for dataset in data:
        
    agreement_count = dataset["AnzahlVereinbarungen"]
    country_count = dataset["AnzahlLaender"]
    partner_count = dataset["AnzahlPartner"]

  closingtag = f"""
    <br>
    <p>Anzahl Vereinbarungen : {agreement_count} <br>
    Anzahl Länder : {country_count} <br>
    Anzahl Partnerhochschulen: {partner_count} <br>
    </p>
    </body>
    </html>
    """

  result += closingtag

  naming = f"reports/ErasmusReport_" + get_date_as_str() + ".pdf"

  workingdir = os.path.abspath(os.getcwd())
  pdfkit.from_string(result, output_path=naming, configuration=config)

  return send_from_directory(workingdir, naming)


def faculty_querry_to_html(data, faculty_id):
  '''
  Erzeugt eine html-Seite, gefüllt mit den Daten zur Fakutltät mit facutlty_id, wandelt diese in eine pdf-Datei um, welche dann zurückgegeben wird
  '''  
  start = f"""
    <html>
      <head>

        <meta charset="utf-8">
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

      for dictotionary_item in dictionary:

          loop_item = f""" <td>
          {dictionary[dictotionary_item]}
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
    </body>
    </html>
    """

  result += closingtag

  #result_encoded = result.encode("utf-8")
  #result_decoded = result_encoded.decode()

  naming = f"reports/FacultyReport_{faculty_id}_" + get_date_as_str() + ".pdf"

  workingdir = os.path.abspath(os.getcwd())
  pdfkit.from_string(result, output_path=naming, configuration=config)
   

  return send_from_directory(workingdir, naming)

def get_date_as_str():
  '''
  Gibt das aktuelle Datum (im Format yyyy/mm/dd) zurück
  '''
  
  date = datetime.datetime.now().date()
  return str(date)