from datetime import datetime
import sqlite3
connection = sqlite3.connect('competency_info.db')
cursor = connection.cursor()
t_date = datetime.today()
d_string = t_date.strftime("%Y-%m-%d")



'''-----------------------------------
Universal Methods
--------------------------------------
'''
def date_test(date):
    date_list = []
    final_string = ""
    for i in date:
        date_list.append(i)

    year = [0, 1, 2, 3]
    month = [5, 6]
    day = [8, 9]
    for i, v in enumerate(date_list):
        if i in year:
            date_list[i] = "y"
        
        elif i in month:
            date_list[i] = "m"

        elif i in day:
            date_list[i] = "d"

    for i in date_list:
        final_string += i

    if final_string == ("yyyy/mm/dd"):
        return True
    else:
        return False



def edit_user(user_email, user_password, u_id):
    exited = False
    users = cursor.execute("SELECT u_fname, u_lname, u_email, u_password, u_phone FROM Users WHERE u_email=? AND u_password=?;", (user_email, user_password)).fetchall()

    print(f'{"NAME":^21} | {"PHONE":^15} | {"EMAIL":^20} | {"PASSWORD":^14}')
    print(f'---------------------------------------------------------------------------')

    for user in users:
        u_fname, u_lname, u_phone, u_email, u_password = user
        u_fname = u_fname if u_fname != None else ''
        u_lname = u_lname if u_lname != None else ''
        u_phone = u_phone if u_phone != None else ''
        u_email = u_email if u_email != None else ''
        u_password = u_password if u_password != None else ''

        print(f"{u_fname:>10} {u_lname:<10} | {u_phone:^15} | {u_email:^20} | {u_password:^20}")

    while True:
        options = ['', 'e']
        user_continue = input('\nYou are about to enter the user update screen. Type (e) to abort, or press (enter) to continue.\n>>>>')
        if user_continue not in options:
            print("\n<!Please enter one of the options above!>")
            continue

        elif user_continue == 'e':
            exited = True
            break

        else:
            break

    if exited == True:
        print('\nExited.')
        
    else:
        valid_options = ['f', 'l', 'p', 'e', 'u']
        print('\nEnter the first letter of the field you wish to edit:')
        print('(F)irst Name\n(L)ast Name\n(P)hone\n(E)mail\n(U)ser Password')
        while True:
            field_to_edit = input('>>>>')
            if field_to_edit == '':
                print('\n<!Please enter a field to edit!>')
                continue

            elif field_to_edit.lower() not in valid_options:
                print('\n<!Please choose from the options displayed above!>')
                continue
            

            elif field_to_edit.lower() == 'f':
                while True:
                    new_fname = input('\nPlease enter the new first name.\n>>>>')
                    if new_fname == '':
                        print('\n<!The user must contain a first name!>')
                        continue
                    else:
                        cursor.execute("UPDATE Users SET u_fname=? WHERE user_id=?;", (new_fname), (u_id))
                        print("\nFirst name updated successfully.")
                        break

            
            elif field_to_edit.lower() == 'l':
                while True:
                    new_lname = input('\nPlease enter the new last name.\n>>>>')
                    if new_lname == '':
                        print('\n<!The user must contain a last name!>')
                        continue
                    else:
                        cursor.execute("UPDATE Users SET u_lname=? WHERE user_id=?;", (new_lname), (u_id))
                        print("\nLast name updated succesfully.")
                        break

            
            elif field_to_edit.lower() == 'p':
                while True:
                    new_phone = input('\nPlease enter the new phone number excluding special characters (enter to remove phone number).\n>>>>')
                    if new_phone == "":
                        print("\nExited.")
                        continue

                    if not new_phone.isnumeric():
                        print("\n<!Please exclude all special characters!>")
                        continue
                    else:
                        cursor.execute("UPDATE Users SET u_phone=? WHERE user_id=?;", (new_phone, u_id))
                        print("\nPhone number updated successfully.")
                        break


            elif field_to_edit.lower() == 'e':
                email_valid = True
                taken_emails = cursor.execute("SELECT u_email FROM Users").fetchall()
                while True:
                    new_email = input('\nPlease enter the new email.\n>>>>')
                    if new_email == '':
                        print('\n<!A user email is required!>')
                        continue
                    for email in taken_emails:
                        if new_email in email:
                            email_valid = False
                            break
                    if not email_valid:
                        print('\n<!The email must be unique!>')
                        continue
                    else:
                        cursor.execute("UPDATE Users SET u_email=? WHERE user_id=?;", (new_email, u_id))
                        print("\nUser email updated successfully.")


            elif field_to_edit == 'u':
                pass_valid = True
                taken_passwords = cursor.execute("SELECT u_password FROM Users").fetchall()
                while True:
                    new_pass = input('\nPlease enter the new password.\n>>>>')
                    if new_pass == '':
                        print('\n<!A password is required!>')
                        continue
                    u_password = str(u_password)
                    for password in taken_passwords:
                        if u_password == password:
                            pass_valid = False
                            break
                    if not pass_valid:
                        print('\n<!The user password must be unique!>')
                        continue
                    else:
                        cursor.execute("UPDATE Users SET u_password=? WHERE user_id=?;", (u_password, u_id))
                        print("\nPassword updated successfully")
                        break

            break
        connection.commit()
# To do non-manager view, use view all but supply the user email and password
# To do non-manager ctr, use ctr function and supply only user id



'''-----------------------------------------------------------
Manager VIEW Methods
--------------------------------------------------------------
'''
def view_all_users(email="", password=""):
    if email=="" and password=="":
        users = cursor.execute("SELECT * FROM Users;").fetchall()
    else:
        users = cursor.execute("SELECT * FROM Users WHERE u_email=? AND u_password=?", (email, password))

    print(f'{"USER ID":^7} | {"NAME":^21} | {"PHONE":^15} | {"EMAIL":^20} | {"PASSWORD":^20} | {"ACTIVE STATUS":^13} | {"DATE CREATED":^12} | {"DATE HIRED":^10} | {"USER TYPE":^9}')
    print(f'-------------------------------------------------------------------------------------------------------------------------------------------------------------')

    for user in users:
        user_id, u_fname, u_lname, u_phone, u_email, u_password, is_active, date_created, date_hired, is_manager = user
        user_id = user_id if user_id != None else ''
        u_fname = u_fname if u_fname != None else ''
        u_lname = u_lname if u_lname != None else ''
        u_phone = u_phone if u_phone != None else ''
        u_email = u_email if u_email != None else ''
        u_password = u_password if u_password != None else ''
        is_active = is_active if is_active != None else ''
        date_created = date_created if date_created != None else ''
        date_hired = date_hired if date_hired != None else ''
        is_manager = is_manager if is_manager != None else ''
        if is_manager == 1:
            user_status = 'Manager'
        else:
            user_status = 'User'
        if is_active == 1:
            user_active = 'Active'
        else:
            user_active = 'Inactive'


        print(f"{user_id:^7} | {u_fname:>10} {u_lname:<10} | {u_phone:^15} | {u_email:^20} | {u_password:^20} | {user_active:^13} | {date_created:^12} | {date_hired:^10} | {user_status:^9}")



def search_user(f_name='', l_name=''):
    neither = False
    first_last = False
    first = False
    last = False
    results = cursor.execute("SELECT * FROM Users")

    if f_name != '' and l_name != '':
        first_last = True
    elif f_name != '':
        first = True
    elif l_name != '':
        last = True
    else:
        neither = True

    print(f'{"USER ID":^7} | {"NAME":^21} | {"PHONE":^15} | {"EMAIL":^20} | {"PASSWORD":^14} | {"ACTIVE STATUS":^13} | {"DATE CREATED":^12} | {"DATE HIRED":^10} | {"USER TYPE":^9}')
    print(f'------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

    for user in results:
        user_id, u_fname, u_lname, u_phone, u_email, u_password, is_active, date_created, date_hired, is_manager = user
        user_id = user_id if user_id != None else ''
        u_fname = u_fname if u_fname != None else ''
        u_lname = u_lname if u_lname != None else ''
        u_phone = u_phone if u_phone != None else ''
        u_email = u_email if u_email != None else ''
        u_password = u_password if u_password != None else ''
        is_active = is_active if is_active != None else ''
        date_created = date_created if date_created != None else ''
        date_hired = date_hired if date_hired != None else ''
        is_manager = is_manager if is_manager != None else ''

        if is_manager == 1:
            user_status = 'Manager'
        else:
            user_status = 'User'

        if is_active == 1:
            user_active = 'Active'
        else:
            user_active = 'Inactive'

        if first == True:
            if (str(u_fname.lower()) == f_name.lower()):
                print(f"{user_id:^7} | {u_fname:>10} {u_lname:<10} | {u_phone:^15} | {u_email:^20} | {u_password:^20} | {user_active:^13} | {date_created:^12} | {date_hired:^10} | {user_status:^9}")
        elif last == True:
            if (u_lname.lower() == l_name.lower()):
                print(f"{user_id:^7} | {u_fname:>10} {u_lname:<10} | {u_phone:^15} | {u_email:^20} | {u_password:^20} | {user_active:^13} | {date_created:^12} | {date_hired:^10} | {user_status:^9}")
        elif first_last == True or neither == True:
            print(f"{user_id:^7} | {u_fname:>10} {u_lname:<10} | {u_phone:^15} | {u_email:^20} | {u_password:^20} | {user_active:^13} | {date_created:^12} | {date_hired:^10} | {user_status:^9}")



def competency_assessment_results(assessment_id='', user_id=''):
    user_names = cursor.execute("SELECT u_fname, u_lname FROM Users").fetchall()

    if user_id == '' and assessment_id == '':
        results = cursor.execute("SELECT * FROM Competency_Assessment_Results")
    elif user_id == '' and assessment_id != '':
        results = cursor.execute("SELECT * FROM Competency_Assessment_Results WHERE assessment=?", (assessment_id,))
    elif user_id != '' and assessment_id == '':
        results = cursor.execute("SELECT * FROM Competency_Assessment_Results WHERE user=?", (user_id,))
    else:
        results = cursor.execute("SELECT * FROM Competency_Assessment_Results WHERE assessment=? AND user=?", (assessment_id, user_id))

    print(f"{'RESULT ID':^10} | {'USER':^29} | {'ASSESSMENT':^10} | {'SCORE':^5} | {'DATE TAKEN':^10} | {'MANAGER':^29}")
    print(f"--------------------------------------------------------------------------------------------------------------")

    for result in results:
        counter = 0
        car_id, user, assessment, score, date_taken, manager = result
        car_id = car_id if car_id != None else ''
        user = user if user != None else ''
        assessment = assessment if assessment != None else ''
        score = score if score != None else ''
        date_taken = date_taken if date_taken != None else ''
        manager = manager if manager != None else ''

        print(f"{car_id:^10} | {user_names[counter][0]:>14} {user_names[counter][1]:<14} | {assessment:^10} | {score:^5} | {date_taken:^10} | {user_names[counter][0]:>14} {user_names[counter][1]:<14}")

        counter += 1



'''----------------------------------------
Manager ADD Methods
-------------------------------------------
'''
def add_user():
    uid_valid = True
    uemail_valid = True
    upassword_valid = True
    taken_fields = cursor.execute("SELECT user_id, u_email, u_password FROM Users;").fetchall()

    while True:
        u_id = input("\nPlease enter a unique ID for the user to be added.\n>>>>")
        if u_id == '':
            print('\n<!The user must have an ID!>')
            continue
        u_id = int(u_id)
        if not u_id.isnumeric():
            print('\n<!The user id must be a numeric value!>')
            continue
        for thing in taken_fields:
            if u_id in thing:
                uid_valid = False
                break
        if uid_valid == False:
            print('\n<!The user ID must be unique!>')
            continue
        else:
            break

    while True:
        u_fname = input("\nPlease enter the user's first name.\n>>>>")
        u_fname = str(u_fname)
        if u_fname == '':
            print('\n<!The user must have a first name!>')
            continue
        else:
            u_fname = u_fname.title()
            break

    while True:
        u_lname = input("\nPlease enter the user's last name.\n>>>>")
        u_lname = str(u_lname)
        if u_lname == '':
            print('\n<!The user must have a last name!>')
            continue
        else:
            u_lname = u_lname.title()
            break

    u_phone = input("\nPlease enter the user's phone number.\n>>>>")
    u_phone = str(u_phone)

    while True:
        u_email = input("\nPlease enter a unique email for the user to be added.\n>>>>")
        if u_email == '':
            print('\n<!The user must have an email!>')
            continue
        u_email = str(u_email)
        for thing in taken_fields:
            if u_email in thing:
                uemail_valid = False
                break
        if uemail_valid == False:
            print('\n<!The user email must be unique!>')
            continue
        else:
            break

    while True:
        u_password = input("\nPlease enter a unique password for the user to be added.\n>>>>")
        if u_password == '':
            print('\n<!The user must have a password!>')
            continue
        u_password = str(u_password)
        for thing in taken_fields:
            if u_password in thing:
                upassword_valid = False
                break
        if upassword_valid == False:
            print('\n<!The user password must be unique!>')
            continue
        else:
            break
    
    while True:
        date_hired = input("\nPlease enter the date the user was hired (yyyy/mm/dd) (enter if n/a).\n>>>>")

        if date_hired == "":
            print("\nExited.")
            break

        if len(date_hired) < 10:
            print("\n<!Please enter the date in the format specified above!>")
            break

        if date_test(date_hired):
            print("\nDate updated successfully.")
            break
        
        else:
            print("\n<!Please enter the date in the format specified above!>")
            continue

    while True:
        options = [1, 0]
        is_manager = input('\nPlease enter (1) if the user is a manager or enter (0) if the user is not a manager.\n>>>>')
        if not is_manager.isnumeric():
            print("\n<!Please enter a numeric value!>")
            continue
        manager = int(manager)
        if manager not in options:
            print("\n<!Please enter a (1) or a (0)!>")
            continue
        else:
            break

    query = ("INSERT INTO Users (user_id, u_fname, u_lname, u_phone, u_email, u_password, date_created, date_hired, is_manager) VALUES (?,?,?,?,?,?,?,?,?)")
    values = (u_id, u_fname, u_lname, u_phone, u_email, u_password, d_string, date_hired, is_manager)
    cursor.execute(query, values)
    connection.commit()

    print('\nUser Created!')



def add_competency():
    taken_fields = cursor.execute('SELECT comp_id, comp_name FROM Competencies;').fetchall()


    while True:
        compid_valid = True
        comp_id = input("\nPlease enter a unique ID for the competency.\n>>>>")
        if comp_id == '':
            print("\n<!The competency must have an ID!>")
            continue

        if not comp_id.isnumeric():
            print("\n<!The competency ID must be numeric!>")
            continue

        comp_id = int(comp_id)
        for thing in taken_fields:
            if comp_id == thing[0]:
                compid_valid = False
                break

        if not compid_valid:
            print("\n<!The competency ID must be unique!>")
            continue
        else:
            break


    while True:
        compname_valid = True
        comp_name = input("\nPlease enter a unique name for the competency.\n>>>>")
        if comp_name == '':
            print('\n<!The competency must have a name!>')
            continue

        for thing in taken_fields:
            if comp_name.lower() == thing[1].lower():
                compname_valid = False
                break

        if not compname_valid:
            print("\n<!The competency name must be unique!>")
            continue
        else:
            break

    query = ("INSERT INTO Competencies (comp_id, comp_name, date_created) VALUES (?,?,?)")
    values = (comp_id, comp_name, d_string)
    cursor.execute(query, values)
    connection.commit()

    print('\nCompetency Created!')



def add_assessment():
    comp_ids = cursor.execute("SELECT comp_id FROM Competencies;").fetchall()
    comp_names = cursor.execute("SELECT comp_name FROM Competencies").fetchall()
    taken_fields = cursor.execute("SELECT assessment_id, assessment_name from Assessments;").fetchall()

    print(taken_fields)


    while True:
        asmtid_valid = True
        asmt_id = input("\nPlease enter a unique ID for the assessment.\n>>>>")
        if asmt_id == '':
            print('\n<!The assessment must have an ID!>')
            continue

        if not asmt_id.isnumeric():
            print("\n<!The assessment ID must be numeric!>")
            continue

        # asmt_id = int(asmt_id)
        for field in taken_fields:
            if int(asmt_id) == field[0]:
                asmtid_valid = False
                break

        if asmtid_valid == False:
            print('\n<!The assessment ID must be unique!>')
            continue
        else:
            break


    while True:
        asmtname_valid = True
        asmt_name = input("\nPlease enter a unique name for the assessment.\n>>>>")
        if asmt_name == '':
            print('\n<!The assessment must have an name!>')
            continue

        for field in taken_fields:
            if asmt_name.lower() == field[1].lower():
                asmtname_valid = False
                break

        if asmtname_valid == False:
            print('\n<!The assessment name must be unique!>')
            continue
        else:
            break


    while True:
        compt_valid = False
        print("")
        for i, v in enumerate(comp_ids):
            print(f'| {v[0]}, "{comp_names[i][0]}" ')

        comp_tested = input('\nPlease enter the ID of the competency being tested.\n>>>>')
        if comp_tested == '':
            print('\n<!The assessment must include the tested competency!>')
            continue

        if not comp_tested.isnumeric():
            print('\n<!The competency ID must be numeric!>')
            continue

        comp_tested = int(comp_tested)
        for id in comp_ids:
            if comp_tested == id[0]:
                compt_valid = True
                break

        if not compt_valid:
            print('\n<!The ID must be in the list of competencies!>')
            continue
        else:
            break


    query = ("INSERT INTO Assessments (assessment_id, assessment_name, date_created, comp_tested) VALUES (?,?,?,?)")
    values = (asmt_id, asmt_name, d_string, comp_tested)
    cursor.execute(query, values)
    connection.commit()

    print('\nAssessment Created!')



def add_assessment_result():
    score_values = [1, 2, 3, 4]
    user_ids = cursor.execute("SELECT user_id FROM Users WHERE is_active=1;").fetchall()
    taken_fields = cursor.execute("SELECT car_id FROM Competency_Assessment_Results;").fetchall()
    man_ids = cursor.execute("SELECT user_id FROM Users WHERE is_manager=1 AND is_active=1;").fetchall()
    asmt_ids = cursor.execute("SELECT assessment_id FROM Assessments;").fetchall()


    while True:
        carid_valid = True
        car_id = input("\nPlease enter the ID for the assessment result.\n>>>>")
        if car_id == '':
            print("\n<!The assessment result must have an ID!>")
            continue

        if not car_id.isnumeric():
            print("\n<!The assessment result ID must be numeric!!>")
            continue

        car_id = int(car_id)
        for field in taken_fields:
            if car_id == field[0]:
                carid_valid = False
                break

        if not carid_valid:
            print("\n<!The assessment result ID must be unique!>")
            continue
        else:
            break


    while True:
        assessmentid_valid = False
        assessment_id = input("\nPlease enter the assessment ID.\n>>>>")
        if assessment_id == '':
            print("\n<!An assessment ID must be included!>")
            continue
        if not assessment_id.isnumeric():
            print("\n<!The assessment ID must be a numeric value!>")
            continue
        assessment_id = int(assessment_id)
        for field in asmt_ids:
            if assessment_id == field[0]:
                assessmentid_valid = True
                break
        if not assessmentid_valid:
            print('\n<!The assessment ID must be an existing assessment!>')
            continue
        else:
            break


    while True:
        userid_valid = False
        user_id = input("\nPlease enter the ID of the user.\n>>>>")
        if user_id == '':
            print('\n<!The assessment record must have a user ID!>')
            continue

        if not user_id.isnumeric():
            print('\n<!The user ID must be numeric!>')
            continue

        user_id = int(user_id)
        for id in user_ids:
            if user_id in id:
                userid_valid = True
                break

        if not userid_valid:
            print('\n<!The user ID must be in the list of user IDs!>')
            continue
        else:
            break


    while True:
        score = input('\nPlease enter the score that the person received (1-4).\n>>>>')
        if score == '':
            print("\n<!The user's score must be included!>")
            continue

        if not score.isnumeric():
            print("\n<!The score must be numeric!>")
            continue

        score = int(score)
        if score not in score_values:
            print("\n<!The person's score must be from 1-4!>")
            continue
        else:
            break


    while True:
        manid_valid = False
        man_id = input("\nPlease enter the ID of the manager (if none, press enter).\n>>>>")
        if man_id == '':
            break

        if not man_id.isnumeric():
            print('\n<!The manager ID must be numeric!>')
            continue

        man_id = int(man_id)
        for id in man_ids:
            if man_id == id[0]:
                manid_valid = True
                break

        if not manid_valid:
            print('\n<!The manager ID must be in the list of user IDs!>')
            continue
        else:
            break


    query = ("INSERT INTO Competency_Assessment_Results (car_id, user, assessment, score, date_taken, manager) VALUES (?,?,?,?,?,?)")
    values = (car_id, user_id, assessment_id, score, d_string, man_id)
    cursor.execute(query, values)
    connection.commit()

    print('\nAssessment Created!')



'''--------------------------------------------------------------
Manager Edit Methods
-----------------------------------------------------------------
'''
def man_edit_user():
    exited = False
    user_ids = []
    users = cursor.execute("SELECT * FROM Users;").fetchall()

    print(f'{"USER ID":^7} | {"NAME":^21} | {"PHONE":^15} | {"EMAIL":^20} | {"PASSWORD":^14} | {"ACTIVE STATUS":^13} | {"DATE CREATED":^12} | {"DATE HIRED":^10} | {"USER TYPE":^9}')
    print(f'------------------------------------------------------------------------------------------------------------------------------------------------------------------------')

    for user in users:
        user_id, u_fname, u_lname, u_phone, u_email, u_password, is_active, date_created, date_hired, is_manager = user
        user_id = user_id if user_id != None else ''
        u_fname = u_fname if u_fname != None else ''
        u_lname = u_lname if u_lname != None else ''
        u_phone = u_phone if u_phone != None else ''
        u_email = u_email if u_email != None else ''
        u_password = u_password if u_password != None else ''
        is_active = is_active if is_active != None else ''
        date_created = date_created if date_created != None else ''
        date_hired = date_hired if date_hired != None else ''
        is_manager = is_manager if is_manager != None else ''
        if is_manager == 1:
            user_status = 'Manager'
        else:
            user_status = 'User'
        if is_active == 1:
            user_active = 'Active'
        else:
            user_active = 'Inactive'

        user_ids.append(int(user_id))

        print(f"{user_id:^7} | {u_fname:>10} {u_lname:<10} | {u_phone:^15} | {u_email:^20} | {u_password:^20} | {user_active:^13} | {date_created:^12} | {date_hired:^10} | {user_status:^9}")


    while True:
        user_to_edit = input('\nPlease enter the ID of the user you wish to edit (enter to exit).\n>>>>')
        if user_to_edit == '':
            exited = True
            break
        if not user_to_edit.isnumeric():
            print('\n<!The user ID must be numeric!>')
            continue
        user_to_edit = int(user_to_edit)
        if user_to_edit not in user_ids:
            print('\n<!The user ID must be from an existing user!>')
            continue
        else:
            break

    if exited == True:
        print('\nExited.')
    else:
        valid_options = ['i', 'f', 'l', 'p', 'e', 'u', 'a', 'd', 'm']
        print('\nEnter the first letter of the field you wish to edit:')
        print('(I)D\n(F)irst Name\n(L)ast Name\n(P)hone\n(E)mail\n(U)ser Password\n(A)ctive Status\n(D)ate Hired\n(M)anager Status')
        while True:
            field_to_edit = input('>>>>')
            if field_to_edit == '':
                print('\n<!Please enter a field to edit!>')
                continue

            elif field_to_edit.lower() not in valid_options:
                print('\n<!Please choose from the options displayed above!>')
                continue


            elif field_to_edit.lower() == 'i':
                newid_valid = True
                taken_ids = cursor.execute("SELECT user_id FROM Users;").fetchall()

                new_id = input('\nPlease enter the new ID.\n>>>>')
                if new_id == '':
                    print('\n<!Please enter an ID!>')
                    continue
                if not new_id.isnumeric():
                    print('\n<!The user ID must be a numeric value!>')
                    continue
                new_id = int(new_id)
                for id in taken_ids:
                    if new_id in id:
                        newid_valid = False
                        break
                if not newid_valid:
                    print('\n<!The new ID must be unique!>')
                    continue
                else:
                    cursor.execute("UPDATE Users SET user_id=? WHERE user_id=?;", (new_id, user_to_edit))
                    print("\nUser ID updated successfully.")
            

            elif field_to_edit.lower() == 'f':
                while True:
                    new_fname = input('\nPlease enter the new first name.\n>>>>')
                    if new_fname == '':
                        print('\n<!The user must contain a first name!>')
                        continue
                    else:
                        cursor.execute("UPDATE Users SET u_fname=? WHERE user_id=?;", (new_fname), (user_to_edit))
                        print("\nFirst name updated successfully.")
                        break

            
            elif field_to_edit.lower() == 'l':
                while True:
                    new_lname = input('\nPlease enter the new last name.\n>>>>')
                    if new_lname == '':
                        print('\n<!The user must contain a last name!>')
                        continue
                    else:
                        cursor.execute("UPDATE Users SET u_lname=? WHERE user_id=?;", (new_lname), (user_to_edit))
                        print("\nLast name updated succesfully.")
                        break

            
            elif field_to_edit.lower() == 'p':
                while True:
                    new_phone = input('\nPlease enter the new phone number excluding special characters (enter to remove phone number).\n>>>>')
                    if new_phone == "":
                        print("\nExited.")
                        continue

                    if not new_phone.isnumeric():
                        print("\n<!Please exclude all special characters!>")
                        continue
                    else:
                        cursor.execute("UPDATE Users SET u_phone=? WHERE user_id=?;", (new_phone, user_to_edit))
                        print("\nPhone number updated successfully.")
                        break


            elif field_to_edit.lower() == 'e':
                email_valid = True
                taken_emails = cursor.execute("SELECT u_email FROM Users").fetchall()
                while True:
                    new_email = input('\nPlease enter the new email.\n>>>>')
                    if new_email == '':
                        print('\n<!A user email is required!>')
                        continue
                    for email in taken_emails:
                        if new_email in email:
                            email_valid = False
                            break
                    if not email_valid:
                        print('\n<!The email must be unique!>')
                        continue
                    else:
                        cursor.execute("UPDATE Users SET u_email=? WHERE user_id=?;", (new_email, user_to_edit))
                        print("\nUser email updated successfully.")


            elif field_to_edit == 'u':
                pass_valid = True
                taken_passwords = cursor.execute("SELECT u_password FROM Users").fetchall()
                while True:
                    new_pass = input('\nPlease enter the new password.\n>>>>')
                    if new_pass == '':
                        print('\n<!A password is required!>')
                        continue
                    u_password = str(u_password)
                    for password in taken_passwords:
                        if u_password == password:
                            pass_valid = False
                            break
                    if not pass_valid:
                        print('\n<!The user password must be unique!>')
                        continue
                    else:
                        cursor.execute("UPDATE Users SET u_password=? WHERE user_id=?;", (u_password, user_to_edit))
                        print("\nPassword updated successfully")
                        break

            
            elif field_to_edit.lower() == 'a':
                options = [1, 0]
                active = input("\nPlease enter the user's active status (1 for active, 0 for inactive).\n>>>>")
                if active == '':
                    print('\n<!The user must have an active status!>')
                    continue
                if not active.isnumeric():
                    print("\n<!The user's active status must be numeric!>")
                    continue
                active = int(active)
                if active not in options:
                    print("\n<!The active status must be 1 or 0!>")
                    continue
                else:
                    cursor.execute("UPDATE Users SET is_active=? WHERE user_id=?;", (active, user_to_edit))
                    print("\nActive status updated successfully.")


            elif field_to_edit.lower() == 'd':
                while True:
                    date_hired = input("\nPlease enter the date the user was hired (yyyy/mm/dd) (enter if n/a).\n>>>>")

                    if date_hired == "":
                        print("\nExited.")
                        break

                    if len(date_hired) < 10:
                        print("\n<!Please enter the date in the format specified above!>")
                        break

                    if date_test(date_hired):
                        cursor.execute("UPDATE Users SET date_hired=? WHERE user_id=?;", (date_hired, user_to_edit))
                        print("\nDate updated successfully.")
                        break
                    
                    else:
                        print("\n<!Please enter the date in the format specified above!>")
                        continue


            elif field_to_edit.lower() == 'm':
                options = [1, 0]

                while True:
                    man_status = input("\nPlease enter the user's manager status (1 for manager, 0 for regular user).\n>>>>")
                    if man_status == '':
                        print('\n<!The user must have a manager status!>')
                        continue

                    if not man_status.isnumeric():
                        print("\n<!The manager status must be numeric!>")
                        continue
                    
                    man_status = int(man_status)
                    if man_status not in options:
                        print("\n<!The manager status must be 1 or 0!>")
                        continue

                    else:
                        cursor.execute("UPDATE Users SET is_manager=? WHERE user_id=?;", (man_status, user_to_edit))
                        print("\nManager status updated successfully.")
                        break

            break
        connection.commit()

        


def edit_competency():
    exited = False
    compids = []
    competencies = cursor.execute("SELECT * FROM Competencies;").fetchall()

    print(f'{"Comp ID":^7} | {"Comp Name":^29} | {"Date Created":<12}')
    print(f'-----------------------------------------------------------')

    for comp in competencies:
        comp_id, comp_name, date_created = comp
        comp_id = comp_id if comp_id != None else ''
        comp_name = comp_name if comp_name != None else ''
        date_created = date_created if date_created != None else ''

        compids.append(int(comp_id))

        print(f'{comp_id:^7} | {comp_name:<29} | {date_created:^12}')

    while True:
        comp_to_edit = input("\nPlease enter the ID of the competency you wish to edit (enter to quit).\n>>>>")
        if comp_to_edit == '':
            exited = True
            break

        if not comp_to_edit.isnumeric():
            print('\n<!The competency ID must be numeric!>')
            continue

        comp_to_edit = int(comp_to_edit)
        if comp_to_edit not in compids:
            print('\n<!The ID must be an existing competency ID!>')
            continue
        else:
            break

    if exited:
        print('\nExited.')
    else:
        valid_options = ['i', 'n']
        print('\nEnter the first letter of the field you wish to edit:\n(I)D\n(N)ame')

        while True:
            choice = input(">>>>")

            if choice == '':
                print('\n<!Please select a choice!>')
                continue

            if choice.lower() not in valid_options:
                print('\n<!Please select from one of the choices above!>')
                continue

            elif choice.lower() == 'i':
                taken_ids = cursor.execute("SELECT comp_id FROM Competencies;").fetchall()

                while True:
                    id_valid = True
                    new_id = input('\nPlease enter the new ID.\n>>>>')
                    if new_id == '':
                        print('\n<!Please enter an ID!>')
                        continue

                    if not new_id.isnumeric():
                        print('\n<!The new ID must be numeric!>')
                        continue

                    new_id = int(new_id)
                    for id in taken_ids:
                        if new_id == id[0]:
                            id_valid = False
                            break

                    if not id_valid:
                        print('\n<!The new ID must be unique!>')
                        continue
                    else:
                        cursor.execute("UPDATE Competencies SET comp_id=? WHERE comp_id=?;", (new_id, comp_to_edit))
                        print("\nCompetency ID has been updated.")
                        break

                break
            
            else:
                taken_names = cursor.execute("SELECT comp_name FROM Competencies").fetchall()

                while True:
                    name_valid = True
                    new_name = input("\nPlease enter the new name.\n>>>>")
                    if new_name == '':
                        print('\n<!Please enter a name!>')
                        continue

                    for name in taken_names:
                        if new_name == name[0]:
                            name_valid = False
                            break

                    if not name_valid:
                        print('\n<!The new name must be unique!>')
                        continue
                    else:
                        cursor.execute("UPDATE Competencies SET comp_name=? WHERE comp_id=?;", (new_name, comp_to_edit))
                        print("\nCompetency name has been updated.")
                        break

                break

    connection.commit()
                


def edit_assessment():
    exited = False
    assessment_ids = []
    assessment_names = []
    assessments = cursor.execute("SELECT * FROM Assessments")

    print(f'{"Assessment ID":^12} | {"Assessment Name":^24} | {"Date Created":^12} | {"Competency Tested":^12}')
    print(f'-----------------------------------------------------------------------------')

    for assessment in assessments:
        assessment_id, assessment_name, date_created, competency_tested = assessment
        assessment_id = assessment_id if assessment_id != None else ''
        assessment_name = assessment_name if assessment_name != None else ''
        date_created = date_created if date_created != None else ''
        competency_tested = competency_tested if competency_tested != None else ''

        assessment_ids.append(int(assessment_id))
        assessment_names.append(str(assessment_name))

        print(f'{assessment_id:^13} | {assessment_name:<24} | {date_created:^12} | {competency_tested:^12}')

    while True:
        assessment_to_edit = input("\nPlease enter the ID of the assessment you would like to edit ('enter' to exit).\n>>>>")

        if assessment_to_edit == '':
            exited = True
            break
        
        if not assessment_to_edit.isnumeric():
            print("\n<!The assessment ID must be numeric!>")
            continue
        
        assessment_to_edit = int(assessment_to_edit)
        if assessment_to_edit not in assessment_ids:
            print("\n<!The assessment ID must be an existing assesment ID!>")
            continue
        else:
            break

    if exited == True:
        print("\nExited.")
    else:
        valid_options = ['i', 'n', 'c']
        while True:
            choice = input("\nPlease enter the first letter of the field you wish to update:\n(I)D\n(N)ame\n(C)ompetency Tested\n>>>>")
            if choice == '':
                print("\n<!Please enter a field to edit!>")
                continue

            if choice.lower() not in valid_options:
                print("\n<!Please enter a valid option!>")
                continue

            if choice.lower() == 'i':
                taken_ids = assessment_ids
                print('Taken IDs:')
                for i in taken_ids:
                    print(i)

                while True:
                    new_id = input("\nPlease enter the new assessment ID.\n>>>>")
                    if new_id == '':
                        print("\n<!Please enter a numerical value for the new ID!>")
                        continue

                    if not new_id.isnumeric():
                        print("\n<!The new assessment ID must be numeric!>")
                        continue

                    new_id = int(new_id)
                    if new_id in taken_ids:
                        print("\n<!The new ID must be unique!>")
                        continue
                    else:
                        print("Assessment ID reassigned successfully.")
                        cursor.execute("UPDATE Assessments SET assessment_id=? WHERE assessment_id=?", (new_id, assessment_to_edit))
                        break
                
                break
                
            elif choice.lower() == 'n':
                taken_names = assessment_names

                print('Taken Names:')
                for i in taken_names:
                    print(i)

                while True:
                    name_valid = True
                    new_name = input("\nPlease enter the new assessment name.\n>>>>")

                    if new_name == '':
                        print("\n<!Please enter a new name!>")
                        continue
                    
                    for name in taken_names:
                        if new_name.lower() == name.lower():
                            name_valid = False

                    if name_valid == False:
                        print("\n<!The new assessment name must be unique!>")
                        continue
                    else:
                        cursor.execute("UPDATE Assessments SET assessment_name=? WHERE assessment_id=?", (new_name, assessment_to_edit))
                        print("\nAssessment renamed successfully.")
                        break

                break
            
            elif choice.lower() == 'c':
                comp_ids = []
                competencies = cursor.execute("SELECT * FROM Competencies;").fetchall()

                print(f'{"Comp ID":^7} | {"Comp Name":^29} | {"Date Created":<12}')
                print(f'-----------------------------------------------------------')

                for comp in competencies:
                    comp_id, comp_name, date_created = comp
                    comp_id = comp_id if comp_id != None else ''
                    comp_name = comp_name if comp_name != None else ''
                    date_created = date_created if date_created != None else ''

                    comp_ids.append(int(comp_id))

                    print(f'{comp_id:^7} | {comp_name:<29} | {date_created:^12}')

                while True:
                    new_comp_id = input("\nPlease enter the competency being tested.\n>>>>")

                    if new_comp_id == "":
                        print("\n<!Please enter one of the IDs listed above!>")
                        continue

                    if not new_comp_id.isnumeric():
                        print("\n<!The competency ID must be numeric!>")
                        continue

                    new_comp_id = int(new_comp_id)
                    if new_comp_id not in comp_ids:
                        print("\n<!The competency ID must be an existing ID!>")
                        continue
                    else:
                        cursor.execute("UPDATE Assessments SET comp_tested=? WHERE assessment_id=?", (new_comp_id, assessment_to_edit))
                        print("\nTested competency updated successfully.")
                        break
                
                break


            connection.commit()



'''--------------------------------------------------------------
Deleting Competency Assessment Result
-----------------------------------------------------------------
'''
def delete_assessment_result():
    valid_carids = []
    assessment_results = cursor.execute("SELECT * FROM Competency_Assessment_Results").fetchall()
    print(f"{'CAR ID':>7} | {'USER':<7} | {'ASSESSMENT':>10} | {'SCORE':<5} | {'DATE TAKEN':>10} | {'MANAGER':<7}")
    print(f"-----------------------------------------------------------------------------------------------------------")
    for ar in assessment_results:
        car_id, user, assessment, score, date_taken, manager = ar
        car_id = car_id if car_id != None else ''
        user = user if user != None else ''
        assessment = assessment if assessment != None else ''
        score = score if score != None else ''
        date_taken = date_taken if date_taken != None else ''
        manager = manager if manager != None else 'N/A'

        valid_carids.append(int(car_id))

        print(f"{car_id:>7} | {user:<7} | {assessment:>10} | {score:<5} | {date_taken:>10} | {manager:<7}")

    while True:
        car_to_delete = input('\nPlease enter the CAR ID of the record which you wish to delete.\n>>>>')
        if car_to_delete == '':
            print('\n<!You must enter the CAR ID of the record you wish to delete!>')
            continue

        if not car_to_delete.isnumeric():
            print('\n<!The CAR ID must be numeric!>')
            continue

        car_to_delete = int(car_to_delete)
        if car_to_delete not in valid_carids:
            print("\n<!The CAR ID must exist in the list of records!>")
            continue
        else:
            break


    query = ("DELETE FROM Competency_Assessment_Results WHERE car_id=?")
    values = (car_id,)
    cursor.execute(query, values)
    connection.commit()

    print("\nDeleted CAR Successfully.")



# query = ("INSERT INTO Assessments (assessment_id, assessment_name, date_created, comp_tested) VALUES (?,?,?,?)")
# values = (1, "Another Test Assessment", d_string, 2)
# cursor.execute(query, values)
# connection.commit()

# query = ("INSERT INTO Users (user_id, u_fname, u_lname, u_phone, u_email, u_password, date_created, date_hired, is_manager) VALUES (?,?,?,?,?,?,?,?,?)")
# values = ('2', 'Emma', 'Thomas', '0987654321', 'email@secondtest.com', "hashtags", d_string, "08/24/2022", 0)
# cursor.execute(query, values)
# connection.commit()

# cursor.execute(f"INSERT INTO Competencies (comp_id, comp_name, date_created) VALUES ({16}, 'Databases', '08-23-2022')")
# cursor.execute('DELETE FROM Competencies WHERE comp_id=1')
# connection.commit()

# query = ("INSERT INTO Competency_Assessment_Results (car_id, user, assessment, score, date_taken, manager) VALUES (?,?,?,?,?,?)")
# values = (0, 1, 0, 4, "08/11/2022", 1)
# cursor.execute(query, values)
# connection.commit()



'''-----------
    LOGIN MENU
--------------
'''
def login():
    choices = ["y", "n"]


    def enter_email():
        emails = cursor.execute("SELECT u_email FROM Users").fetchall()
        valid = False
        while True:
            correct = True
            email = input("\nPlease enter your email:\n>>>>")

            while True:
                for i in emails:
                    if email in i:
                        valid = True
                        continue
                
                if valid == False:
                    print("\n<!That email is not valid!>")
                    break

                confirmation = input(f'\n{email}: Is this correct? (y or n)\n>>>>')
                if confirmation not in choices:
                    print("\n<!Please enter one of the choices above!>")
                    continue

                elif confirmation == choices[1]:
                    correct = False
                    break

                elif confirmation == choices[0]:
                    correct = True
                    break
            
            if valid == False:
                continue

            if correct == False:
                continue

            elif correct == True:
                return email


    def enter_password(email):
        corr_password = cursor.execute("SELECT u_password, is_manager FROM Users WHERE u_email=?", (email,)).fetchall()
        is_manager = corr_password[0][1]
        password = corr_password[0][0]


        while True:
            password = input("\nPlease enter your password:\n>>>>")
            print(password)
            if password != corr_password[0][0]:
                print("\n<!Incorrect Password!>")
                return False, is_manager, password

            else:
                print("\nLogged in.")
                return True, is_manager, password


    while True:
        print("---------LOGIN---------\n")
        entered_email = enter_email()
        while True:
            redo = True
            entered_password = enter_password(entered_email)
            if entered_password[0] == False:
                while True:
                    choice = input("\nWould you like to re-enter your password? (y or n)\nIf (n), program will be exited.\n>>>>")
                    if choice not in choices:
                        print("\n<!Please enter one of the choices listed above!>")
                        continue
                    
                    elif choice == choices[0]:
                        redo = True
                        break

                    elif choice == choices[1]:
                        redo = False
                        break
            
                if redo == True:
                    continue

                elif redo == False:
                    print("\nExited.")
                    return False,

            elif entered_password[0] == True:
                return entered_email, entered_password[1], entered_password[2]



'''---------------------------
MAIN MENUS FOR THE APPLICATION
------------------------------
'''
def main_menu(is_manager, user_email, user_password):
    user_information = cursor.execute("SELECT u_fname, u_lname, u_phone, u_password, user_id, u_email FROM Users WHERE u_email=? AND u_password=?", (user_email, user_password)).fetchall()
    print(user_information)


    def user_menu(u_firstname, user_id, u_email, u_password):
        print(f"\n\nWelcome, {u_firstname}.")

        while True:
            choices = ['v', '', 'a', 'e']
            user_choice = input("\nWhat would you like to do?\n(V)iew your info\n(A)ssessment results\n(E)dit your info\n(enter) to quit\n>>>>")
            if user_choice.lower() not in choices:
                print("\n<!Please enter one of the options above!>")
                continue

            elif user_choice.lower() == choices[1]:
                print("\nExited.")
                break

            elif user_choice.lower() == choices[0]:
                view_all_users(user_email, user_password)
                continue

            elif user_choice.lower() == choices[2]:
                competency_assessment_results(user_id=user_id)
                continue

            elif user_choice.lower() == choices[3]:
                edit_user(u_email, u_password, user_id)
                continue


    def manager_menu(u_firstname, user_id, u_email, u_password):
        def view_menu():
            while True:
                choices = ['a', 's', 'c', 'e']
                choice = input("\nWould you like to view:\n(A)ll Users\n(S)earch for a User\n(C)ompetency Assessment Result\n(E)xit\n>>>>")
                if choice.lower() not in choices:
                    print("\n<!Please enter one of the choices above!>")
                    continue

                elif choice.lower() == choices[3]:
                    print("\nExited.")
                    break

                elif choice.lower() == choices[0]:
                    view_all_users()
                    continue

                elif choice.lower() == choices[1]:
                    f_name = input("\nPlease enter the first name. (enter) if n/a.\n>>>>")
                    l_name = input("\nPlease enter the last name. (enter) if n/a.\n>>>>")
                    search_user(f_name, l_name)
                    continue

                # GET THIS WIRED UP!!!!!!!!!!!!!!!
                elif choice.lower() == choices[2]:
                    while True:
                        choices = ['u', 'c', 'e']
                        choice = input("\nWould you like to search by:\n(U)ser\n(C)ompetency\n(E)xit\n>>>>")
                        if choice.lower() not in choices:
                            print(choice.lower())
                            print(choices)
                            print("urmom")
                            print("\n<!Please enter one of the choices above!>")
                            continue

                        elif choice.lower() == choices[2]:
                            print("\nExited.")
                            break
                         
                        elif choice.lower() == choices[0]:
                            f_name = input("\nPlease enter the first name. (enter) if n/a.\n>>>>")
                            l_name = input("\nPlease enter the last name. (enter) if n/a.\n>>>>")
                            search_user(f_name, l_name)
                            u_id = input("\nPlease enter the User ID of the user you would like to view:\n>>>>")
                            competency_assessment_results(int(u_id))
                            continue

                        elif choice.lower() == choices[1]:
                            ids = []
                            while True:
                                competencies = cursor.execute("SELECT comp_id, comp_name FROM Competencies").fetchall()
                                print("\nComp ID  | Comp Name")
                                print("--------------------")
                                for competency in competencies:
                                    comp_id, comp_name = competency
                                    comp_id = comp_id if comp_id != None else ''
                                    comp_name = comp_name if comp_name != None else ''
                                    ids.append(comp_id)
                                
                                    print(f"{comp_id:<2} | {comp_name}")

                                search_comp = input("\nPlease enter the id of the competency you would like to search for.\n>>>>")
                                if not search_comp.isnumeric():
                                    print("\n<!The ID must be numeric!>")
                                    continue

                                elif int(search_comp) not in ids:
                                    print("\n<!Please enter an ID from the list above!>")
                                    continue

                                else:
                                    redo = False
                                    while True:
                                        search_comp = int(search_comp)
                                        assessments = cursor.execute("SELECT * FROM Assessments WHERE comp_tested=?", (search_comp,)).fetchall()
                                        if not assessments:
                                            choices = ['y', 'n']
                                            while True:  
                                                choice = input("\nThere are no assessments testing that competency. Would you like to re-search?\n(y) or (n):\n>>>>")
                                                if choice.lower() not in choices:
                                                    print("\n<!Please enter one of the choices above!>")
                                                    continue

                                                elif choice.lower() == choices[0]:
                                                    redo = True
                                                    break

                                                elif choice.lower() == choices[1]:
                                                    break
                                            
                                            break
                                        
                                        break

                                if redo == True:
                                    continue

                                else:
                                    # cars = 
                                    break


                                    #GET THE ASSESSMENT ID FROM USER SO THAT IT CAN DISPLAY
                                    #THE CARs FOR THE COMPETENCY THE USER WANTS

        

        def edit_menu():
            choices = ['u', 'c', 'a', 'e']
            while True:
                choice = input("\nWould you like to edit:\n(U)ser Info\n(C)ompetency Info\n(A)ssessment Info\n(E)xit\n>>>>")
                if choice.lower() not in choices:
                    print("\n<!Please enter one of the choices above!>")
                    continue

                elif choice.lower() == choices[3]:
                    print("\nExited.")
                    break

                elif choice.lower() == choices[0]:
                    man_edit_user()
                    continue

                elif choice.lower() == choices[1]:
                    edit_competency()
                    continue

                elif choice.lower() == choices[2]:
                    edit_assessment()
                    continue



        def add_menu():
            choices = ['u', 'c', 'a', 'car', 'e']
            while True:
                choice = input("\nWould you like to add a(n):\n(U)ser\n(C)ompetency\n(A)sessment\n(CAR)Competency Assessment Result\n(E)xit")
                if choice.lower() not in choices:
                    print("\n<!Please enter one of the choices above!>")
                    continue

                elif choice.lower() == choices[4]:
                    print("\nExited.")
                    break

                elif choice.lower() == choices[0]:
                    add_user()
                    continue

                elif choice.lower() == choices[1]:
                    add_competency()
                    continue

                elif choice.lower() == choices[2]:
                    add_assessment()
                    continue

                elif choice.lower() == choices[3]:
                    add_assessment_result()
                    continue


        def delete_menu():
            delete_assessment_result()
        


        print(f"\n\nWelcome to the manager screen, {u_firstname}.")
        while True:
            choices = ['v', 'e', 'a', 'd', 'q']
            choice = input("\nWould you like to:\n(V)iew/Search for User\n(E)dit User Info\n(D)elete a Competency Assessment Result\n(Q)uit\n>>>>")
            if choice.lower() not in choices:
                print("\n<!Please enter one of the choices above!>")
                continue

            elif choice.lower() == choices[4]:
                print("\nExited.")
                break

            elif choice.lower() == choices[0]:
                view_menu()
                continue

            elif choice.lower() == choices[1]:
                edit_menu()
                continue

            elif choice.lower() == choices[2]:
                add_menu()
                continue

            elif choice.lower() == choices[3]:
                delete_menu()
                continue




    print("\n\n------------ COMPETENCY TRACKER ------------")

    if is_manager == 0:
        user_menu(user_information[0][0], user_information[0][4], user_information[0][5], user_information[0][3])
    
    elif is_manager == 1:
        manager_menu(user_information[0][0], user_information[0][4], user_information[0][5], user_information[0][3])





def main():
    user_info = login()
    print(user_info)

    if user_info[0] != False:
        is_manager = user_info[1]
        user_email = user_info[0]
        user_password = user_info[2]

        main_menu(is_manager, user_email, user_password)

main()
