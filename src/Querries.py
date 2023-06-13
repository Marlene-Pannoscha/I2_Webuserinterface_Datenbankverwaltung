import time, helper
import app
import Login
from flask import jsonify


# get all institutes saved in new_tbl_institutes
def institutes_ret():
    '''
    Alle Institute, die in new_tbl_institutes gespeichert sind, holen
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    # execute stored procedure
    cur.callproc('count_agreements')
    payload = []
    # with result create an object that iterates through cur.stored_results() -> only one stored result
    for result in cur.stored_results():
        payload = return_institutes(result.fetchall())
    cur.close()
    cnxn.close()
    # convert payload to json format and send it back to server
    return jsonify(payload, {'sorting': 'a'}, {'admin': app.return_session()})


# Laden des Vertragstyp in den Filter Dropdown
def ag_type_ret():
    '''
    Die Vertragtypen in den Filter Dropdown laden
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    cur.execute('SELECT ID, deu FROM new_tbl_partnership_type ORDER BY deu')
    x = cur.fetchall()
    payload = []
    for i in x:
        content = {
            'ID': i[0],
            'ps_type': i[1]
        }
        payload.append(content)
    cur.close()
    cnxn.close()
    return jsonify(payload)


# get all country names + ID's from country table
# same logic as in institutes_ret() func
# Laden der Länderliste in den Filter Länder
def all_countries():
    '''
    Alle Länder, die in new_tbl_country gespeichert sind, für die Filterwerte holen
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    #cur.execute("SELECT de, id FROM new_tbl_country ORDER BY de")
    #cur.execute("CREATE VIEW val_coun AS SELECT de, id FROM new_tbl_country WHERE id in (SELECT id FROM auslandsamt.country) ORDER BY de ")
    #cur.execute("SELECT de, id FROM val_coun")
    cur.execute("SELECT de, id FROM new_tbl_country WHERE id in (SELECT id FROM auslandsamt.country) ORDER BY de ")
    x = cur.fetchall()
    payload = []
    for i in x:
        content = {
            'country': i[0],
            'id': i[1]
        }
        payload.append(content)
    cur.close()
    cnxn.close()
    return jsonify(payload)


# get all faculties existing in htw
# same logic as in institutes_ret() func
# Laden der Fakultäten in den Filter Fakultäten
def faculty():
    '''
    Alle Fakultäten, die in new_tbl_faculty gespeichert sind, holen
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    cur.execute("SELECT ID, deu FROM new_tbl_faculty ORDER BY deu")
    x = cur.fetchall()
    payload = []
    for i in x:
        content = {
            'id': i[0],
            'fac': i[1]
        }
        payload.append(content)
    cur.close()
    cnxn.close()
    return jsonify(payload)


# get all data needed for institut modal box; specified inst by ID given from html site
def for_institute_modal(institute_id):
    '''
    Alle Daten, die für die Bearbeitungsmodal von gewählte Hochschule
    benötigt werden, aus der Datenbank zurückgegeben
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    param_list = (institute_id,)
    cur.callproc('institute_information', param_list)
    payload = []
    for result in cur.stored_results():
        rows = result.fetchall()
        for row in rows:
            content = {
                'country': row[0],
                'eng': row[1],
                'local': row[2],
               
                #'adr': row[3],
                'website': row[4],
                'notes': row[5],
                'display': row[6],
                'ec': row[7],
                #'dep': row[8],
                #'tel': row[9],
                'mail': row[10],
                #'off_website': row[11],
               # 'function': row[12],
                #'gender': row[13],
                #'title': row[14],
                #'firstname': row[15],
                #'lastname': row[16],
               # 'pers_tel': row[17],
                #'pers_mail': row[18],
                'id': institute_id
            }
            payload.append(content)
    cur.close()
    cnxn.close()
    return jsonify(payload)


## Hier muss für das Modal Mentoren Bearbeiten eine Datenbankabfrage erstellt werden
# der Code hier darunter ist nur von for_modal (lädt Daten für Mentor Modal) kopiert.
# get all data needed for mentor modal box; specified mentor by ID given from html site
def for_mentor_modal(mentor_id):
    '''
    Alle Daten, die für die Bearbeitungsmodal von gewählte Mentor
    benötigt werden, aus der Datenbank zurückgegeben
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    param_list = (mentor_id,)
    cur.callproc('get_mentor', param_list)
    payload = []
    for result in cur.stored_results():
        rows = result.fetchall()
        for row in rows:
            content = {
                'title': row[0],
                'firstname': row[1],
                'lastname': row[2],
                'gender': row[3],
                'website': row[4],
                'mail': row[5],
                'faculty': row[6],
                'active': row[7],
                'id': mentor_id
            }
            payload.append(content)
    cur.callproc('guided_agreements', param_list)
    payload2 = []
    for result in cur.stored_results():
        rows = result.fetchall()
        for row in rows:
            content = {
                'faculty_ID': row[0],
                'institute': row[1],
                'partnership': row[2]
            }
            payload2.append(content)
    cur.close()
    cnxn.close()
    return jsonify({'modal': payload, 'agreements': payload2})


# get mobility agreements referring to institute / partnership and all course restrictions
def get_ma_and_courses(institute):
    '''
    Alle Partnerschaftsverträge und Restriktion bezüglich des Instituts aus der Datenbank holen
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    param_list = (institute,)
    cur.callproc('get_ma', param_list)
    payload = []
    for result in cur.stored_results():
        rows = result.fetchall()
        for row in rows:
            content = {
                'agreement_ID': row[0],
                'partnership_ID': row[1],
                'faculty': row[2],
                'mentor_title': row[3],
                'mentor_firstname': row[4],
                'mentor_lastname': row[5],
                'date_signature': row[6],
                'valid_since': row[7],
                'valid_until': row[8],
                'agreement_inactive': row[9],
                'in_num_mob': row[10],
                'in_num_months': row[11],
                'out_num_mob': row[12],
                'out_num_months': row[13],
                'notes': row[14],
                'mentor_ID': row[15],
                'partnership_type': row[16],
                'course_restrictions': []
            }
            agreement = (content['agreement_ID'],)
            cur.callproc('get_ma_restrictions', agreement)
            for results in cur.stored_results():
                for restriction in results:
                    content['course_restrictions'].append({
                        'restriction_ID': restriction[0],
                        'course': restriction[1],
                        'subject_area_code': restriction[2],
                        'incoming': restriction[3],
                        'sub_num_mobility': restriction[4],
                        'sub_num_months': restriction[5]
                    })
            payload.append(content)
    cur.close()
    cnxn.close()
    return jsonify(payload)


def filter_institutes(parameters):
    '''
    Die gefilterte Institute aus der Datenbank holen
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    payload = []  # empty payload to put data in later
    # 0 - country, 1 - faculty, 2 - extern, 3 - active, 4 - agreement type
    parameter_list = (parameters[0], parameters[1], parameters[2], parameters[3], parameters[4])
    print(parameter_list)
    cur.callproc('count_agreements_filter', parameter_list, )
    for result in cur.stored_results():
        payload = return_institutes(result.fetchall())
    print(payload)
    cur.close()
    cnxn.close()
    return jsonify(payload, {'sorting': parameters[5]})


def new_mentor(columns, values):
    '''
    Neue angelegte Mentor in der Datenbank speichern
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    query_parameter = helper.dynamic_querries(columns)
    query = "INSERT INTO new_tbl_mentor (" + query_parameter[0] + ") VALUES(" + query_parameter[1] + ")"
    try:
        insert = tuple(values)
        print(insert)
        #cur.execute(query, insert,)
        #cnxn.commit()
        return jsonify({'success': 'true'})
    finally:
        cur.close()
        cnxn.close()


def new_object(object_type, tuple_columns, tuple_values, inst_name=None, inst_ps_type=None):
    '''
    Neu angelegtes Objekt in der Datenbank speichern
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    state = "failed" # set initial status that is returned when it failed to set changes in db
    query_parameter = helper.dynamic_querries(tuple_columns)
    type_dict = {
        'mentor': 'new_tbl_mentor',
        'institute': 'new_tbl_institute',
        'agreement': 'new_tbl_mobility_agreement',
        'restriction': 'new_tbl_mobility_agreement_x_course',
        'faculty': 'new_tbl_faculty'        
    } 
    # define all possible tables where a new object could be created
    # create dynamic insert query
    query = f"INSERT INTO {type_dict[object_type]} ({query_parameter[0]}) VALUES ({query_parameter[1]})"
    # define tuple for parameters that need to be inserted
    parameters = tuple(tuple_values)
    try:
        # insert into new_tbl_institute
        print(query, parameters)
        cur.execute(query, parameters,)
        cnxn.commit()
        # query for insert into new_tbl_partnership
        if object_type == 'institute':
            all_parameters = (inst_name, inst_ps_type)
            cur.callproc('insert_partnership', all_parameters,)
            cnxn.commit()
        state = "successful"
    except Exception as e:
        print(e)
    finally:
        cur.close()
        cnxn.close()
        return jsonify({'result': state})


# Laden der Länder in die Tabelle auf der Seite Länderübersicht
def return_countries():
    '''
    Laden der Länder in die Tabelle auf der Seite Länderübersicht
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    #cur.execute('SELECT de, en, erasmus FROM new_tbl_country ORDER BY de')
    cur.execute("SELECT de, en, erasmus FROM new_tbl_country WHERE id in (SELECT id FROM auslandsamt.country) ORDER BY de ")
    rows = cur.fetchall()  # zusammenfassen aller Objekte der Datenbankanfrage
    payload = []
    for row in rows:
        content = {
            'de': row[0],
            'en': row[1],
            'er': row[2]
        }
        payload.append(content)
    cnxn.close()
    cur.close()
    return jsonify(payload)


# Laden der Studiengänge in die Tabelle auf der Seite Studiengänge
def return_courses():
    '''
    Laden der Studiengänge in die Tabelle auf der Seite Studiengänge 
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    cur.execute('SELECT deu, eng, ID FROM new_tbl_course ORDER BY deu')
    x = cur.fetchall()
    payload = []
    for row in x:
        content = {
            'de': row[0],
            'eng': row[1],
            'ID': row[2]
        }
        payload.append(content)
    cnxn.close()
    cur.close()
    return jsonify(payload)


# Laden der Mentoren in die Tabelle auf der Seite Mentoren
def return_mentor():  # get all mentor information and store on client storage
    '''
    Laden der Mentoren in die Tabelle auf der Seite Mentoren
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    query = """SELECT m.ID, m.faculty_ID, m.active, m.gender_ID, m.title, m.firstname, m.lastname, count(mentor_ID) 
                FROM new_tbl_mobility_agreement ma 
                RIGHT JOIN new_tbl_mentor m  
                ON ma.mentor_ID = m.ID 
                GROUP BY m.ID
                ORDER BY m.lastname"""
    cur.execute(query)
    all_mentors = cur.fetchall()
    payload = []
    for mentor in all_mentors:
        display = "Nein"
        if mentor[2] == 1:
            display = "Ja"
        content = {
            'ID': mentor[0],
            'faculty_ID': mentor[1],
            'active': display,
            'gender_ID': mentor[3],
            'title': mentor[4],
            'firstname': mentor[5],
            'lastname': mentor[6],
             #'homepage': mentor[7],
             #'email': mentor[8],
            'agreements': mentor[7]
        }
        payload.append(content)
    cnxn.close()
    cur.close()
    return jsonify(payload)


def return_faculties():
    '''
    Laden der Fakultäten in die Tabelle auf der Seite Fakultäten
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
 
    query = """SELECT f.deu, f.eng, COUNT(m.faculty_ID), f.id
                FROM new_tbl_mobility_agreement m
                JOIN new_tbl_faculty f 
                ON f.ID = m.faculty_ID
                GROUP BY m.faculty_ID
                ORDER BY f.deu"""
    cur.execute(query)
    faculties = cur.fetchall()
    payload = []
    for fac in faculties:
        content = {
            'de': fac[0],
            'eng': fac[1],
            'agreements': fac[2],
            'id': fac[3]
        }
        payload.append(content)
    cnxn.close()
    cur.close()
    return jsonify(payload)


def return_institutes(result_set):
    '''
    Die Institute in payload speichern
    '''
    payload = []
    for result in result_set:
        content = {
            'id': result[0],
            'name': result[1],
            'agreements': result[2],
            'display': result[3]
        }
        payload.append(content)
    return payload


def edit(keys, values, change_id, change_type):  # institute = institute ID
    '''
    Die geänderte Werte in der Datenbank aktualisieren
    '''
    tbl_names = {'institute': "new_tbl_institute", 'agreement': "new_tbl_mobility_agreement", 'restriction': "new_tbl_mobility_agreement_x_course", 'mentor': 'new_tbl_mentor'}
    parameter = helper.dynamic_querries(keys)
    query_string = helper.create_update_string(keys)
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    query = "UPDATE " + tbl_names[change_type] + " SET " + query_string[:-1] + " WHERE ID = " + str(change_id)
    print(query, values)
    cur.execute(query, values,)
    cnxn.commit()
    cnxn.close()
    cur.close()
    return jsonify({'status': 'success'})


def checkLength(key, object_id):
    '''
    Prüfen, ob die Institute einen bestehenden Vertrag und Einschränkung enthalten
    Prüfen, ob die Vertrag eine bestehende Einschränkung enthalten
    Falls das Objekt nichts enthaltet, es ist löschbar
    '''
    strip = object_id
    object_id = (object_id,)
    print(key, object_id)
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    dict = {
        'institute': ['agreements_for_institute', 'new_tbl_institute'],
        'agreement': ['courses_for_agreement', 'new_tbl_mobility_agreement']
    }
    if key in dict:
        procedure_name = dict[key][0]
        cur.callproc(procedure_name, object_id)
        for result in cur.stored_results():
            results = result.fetchall()
            # delete institute if there are no agreements linked to it
            if len(results) <= 0:
                delete(dict[key][1], strip)
            else:
                return {'state': 'failed'}
    else:
        delete('new_tbl_mobility_agreement_x_course', strip)
    return {'state': 'successful'}


def delete(tbl, row_id):
    '''
    Objekte (Hochschule, Vertrag) löschen
    '''
    cnxn = Login.newConnection()
    cur = cnxn.cursor()
    if tbl == 'new_tbl_institute':
        query = f"DELETE FROM new_tbl_partnership WHERE institute_ID = {row_id}"
        cur.execute(query)
        cnxn.commit()
    query = f"DELETE FROM {tbl} WHERE ID = {row_id}"
    print(query)
    cur.execute(query)
    cnxn.commit()
    cnxn.close()
    cur.close()

# pyodbc-Abfragen für Berichte

def facultyReport(faculty_id):

	cnxn = Login.newConnection()
	cur = cnxn.cursor()
        
    #(m.title + ' ' + m.firstname + ' ' + 

    # "\" benötigt um String mit Zeilenumbrüchen zu realisieren, alternativ muss die Abfrage als stored procedure angelegt werden
	cur.execute(f"SELECT c.de, i.eng, pt.deu, CONCAT(m.title, ' ',m.firstname, ' ', m.lastname) AS mentordata, ma.until_date \
				FROM new_tbl_mobility_agreement AS ma, \
					new_tbl_mentor AS m, \
					new_tbl_partnership_type AS pt, \
					new_tbl_country AS c, \
					new_tbl_partnership AS p, \
                    new_tbl_institute AS i \
				WHERE \
                    (\
					((ma.mentor_ID = m.ID) \
					AND (ma.partnership_ID = p.ID) \
					AND (p.institute_ID = i.ID) \
					AND (p.partnership_type_ID = pt.ID) \
					AND (i.country_ID = c.ID) \
                    ) \
				    AND \
					(ma.faculty_ID = {faculty_id}) \
                    ) \
                ORDER BY \
                    c.de, pt.deu, i.eng, ma.until_date, mentordata")

	x = cur.fetchall()
	payload = []
	for i in x:
		content = {
			'Land': i[0],
			'Name': i[1],
			'Vertrag': i[2],
			'Mentor': i[3],
			'Dauer (bis)': i[4]
		}
		payload.append(content)


	cur.close()
	cnxn.close()

	return payload

def erasmusReport():

    cnxn = Login.newConnection()
    cur = cnxn.cursor()    

    cur.execute("""SELECT c.de, i.eng, CONCAT(m.title, ' ',m.firstname, ' ', m.lastname) AS mentordata, ma.until_date, pt.deu
                FROM new_tbl_mobility_agreement AS ma
                JOIN new_tbl_partnership p ON p.ID = ma.partnership_ID
                JOIN new_tbl_partnership_type pt ON pt.ID = p.partnership_type_ID
                JOIN new_tbl_institute i ON i.ID = p.institute_ID
                JOIN new_tbl_country c ON c.ID = i.country_ID
                JOIN new_tbl_mentor m ON m.ID = ma.mentor_ID
                WHERE (c.erasmus = '1' AND pt.ID = '3')
                ORDER BY c.de, i.eng, ma.until_date, mentordata, pt.deu""")


    x = cur.fetchall()
    payload = []
    for i in x:
        content = {
			'Land': i[0],
			'Name': i[1],			
			'Mentor': i[2],
			'Dauer' : i[3],
            'Vertrag': i[4]
		}

        payload.append(content)


    cur.close()
    cnxn.close()

    return payload

def erasmusData():

    cnxn = Login.newConnection()
    cur = cnxn.cursor()    

    cur.execute("""SELECT c.de, i.eng, COUNT(*), COUNT(DISTINCT c.de), COUNT(DISTINCT i.eng)
                FROM new_tbl_mobility_agreement AS ma
                JOIN new_tbl_partnership p ON p.ID = ma.partnership_ID
                JOIN new_tbl_partnership_type pt ON pt.ID = p.partnership_type_ID
                JOIN new_tbl_institute i ON i.ID = p.institute_ID
                JOIN new_tbl_country c ON c.ID = i.country_ID
                WHERE (c.erasmus = '1' AND pt.ID = '3')
                ORDER BY c.de, i.eng""")


    x = cur.fetchall()
    payload = []
    for i in x:
        content = {
            'AnzahlVereinbarungen' : i[2],
            'AnzahlLaender' : i[3],
            'AnzahlPartner' : i[4]
		}

        payload.append(content)


    cur.close()
    cnxn.close()

    return payload