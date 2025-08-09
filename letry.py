import mysql.connector as db
import random
from datetime import date, datetime, time

#from dotenv import load_dotenv
#import os
#load_dotenv()
'''user1 = os.getenv("DB_USER")
password1 = os.getenv("DB_PASSWORD")
host1 = os.getenv("DB_HOST")
database1 = os.getenv("DB_NAME")'''
con = db.connect(user='bank',password='bank@123',host='127.0.0.1',database='BMS')
cur = con.cursor()
def safe_int_input(prompt, max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input! Please enter a number.")
            attempts += 1
    print("Maximum attempts exceeded.")
    return False
def chkcnt(cnt):
    if cnt >= 3:
        print('Maximum Tries Exceeded.....!')
        return False
    else:
        print('Wrong Choice......')
        return True
def prtd(data, columns):
    clean_data = [[str(val) if val is not None else '-' for val in row] for row in data]
    all_rows = [columns] + clean_data
    col_widths = [max(len(row[i]) for row in all_rows) + 2 for i in range(len(columns))]
    for col, width in zip(columns, col_widths):
        print(f"{col:<{width}}", end='')
    print()
    for width in col_widths:
        print('-' * width, end='')
    print()
    for row in clean_data:
        for val, width in zip(row, col_widths):
            print(f"{val:<{width}}", end='')
        print()
    return yn(True)
def viewallu():
    cur.execute('SELECT * FROM users;')
    data = cur.fetchall()
    cn = ['Account Name', 'Account Number', 'Account Type', 'Balance', 'Phone Number']
    return prtd(data, cn)
def accdu():
    print('Enter Your details.....')
    accno = safe_int_input('Enter Account Number ->  ')
    if accno is None:
        return False
    cur.execute('SELECT * FROM users WHERE uaccno = %s', (accno,))
    data = cur.fetchall()
    cn = ['Account Name', 'Account Number', 'Account Type', 'Balance', 'Phone Number']
    return prtd(data, cn)
def tranu():
    accno = safe_int_input('Enter Account Number ->  ')
    if accno is None:
        return False
    cur.execute('SELECT * FROM transactions WHERE uaccno = %s', (accno,))
    data = cur.fetchall()
    cn = ['User Name', 'Account Number', 'Account Type', 'credit', 'Debit', 'Date of Transaction', 'Time of Transaction']
    return prtd(data, cn)
def trand():
    dt1 = input('Enter Date of Transaction (YYYY-MM-DD): ')
    cur.execute('SELECT uname, uaccno, uaccty, credit, debit, timeof FROM transactions WHERE dateof = %s;', (dt1,))
    data = cur.fetchall()
    cn = ['User Name', 'Account Number', 'Account Type', 'credit', 'Debit', 'Time of Transaction']
    return prtd(data, cn)
def yn(flag):
    cnt = 0
    while flag:
        wnt = safe_int_input('Do you want to use Bank again?\n1. YES\n2. NO\n>>> ')
        if wnt == 1:
            return True
        elif wnt == 2:
            print('Thank You.....')
            return False
        else:
            cnt += 1
            flag = chkcnt(cnt)
    return flag
def menu(flag):
    cnt = 0
    while flag:
        ch = safe_int_input('''
        1. View all users
        2. Account details of a user
        3. Transaction details of a user
        4. Transactions details of particular day
        5. Exit\n>>> ''')
        if ch == 1:
            flag = viewallu()
        elif ch == 2:
            flag = accdu()
        elif ch == 3:
            flag = tranu()
        elif ch == 4:
            flag = trand()
        elif ch == 5:
            flag = yn(True)
        elif ch == False:
            flag = False
        else:
            cnt += 1
            flag = chkcnt(cnt)
    return flag
def debit(detm, accno):
    cur.execute('SELECT uamt FROM users WHERE uaccno = %s', (accno,))
    data = cur.fetchone()
    if not data or data[0] < detm:
        print("Insufficient funds.")
        return yn(True)
    newm = data[0] - detm
    cur.execute('UPDATE users SET uamt = %s WHERE uaccno = %s', (newm, accno))
    cur.execute('SELECT * FROM users WHERE uaccno = %s', (accno,))
    data = cur.fetchone()
    fd = datetime.now().replace(microsecond=0)
    td = fd.date()
    tt = fd.time().replace(microsecond=0)
    cur.execute('INSERT INTO transactions(uname,uaccno,uaccty,debit,dateof,timeof) VALUES (%s,%s,%s,%s,%s,%s)',
                (data[0], accno, data[2], detm, td, tt))
    con.commit()
    print('Debited Successfully.....!!!!')
    return True
def credit(detm,accno):
    cur.execute('SELECT uamt FROM users WHERE uaccno = %s', (accno,))
    data = cur.fetchone()
    
    newm = data[0] + detm
    cur.execute('UPDATE users SET uamt = %s WHERE uaccno = %s', (newm, accno))
    cur.execute('SELECT * FROM users WHERE uaccno = %s', (accno,))
    data = cur.fetchone()
    fd = datetime.now().replace(microsecond=0)
    td = fd.date()
    tt = fd.time().replace(microsecond=0)
    cur.execute('INSERT INTO transactions(uname,uaccno,uaccty,credit,dateof,timeof) VALUES (%s,%s,%s,%s,%s,%s)',
                (data[0], accno, data[2], detm, td, tt))
    con.commit()
    print('credited Successfully.....!!!!')
    return yn(True)
def pinch(flag,accno):
    cnt =0
    while flag:
        npin  = input('Enter Your New Pin : ')
        if len(npin) == 4:
            npin1 = input('Re-Enter Same Pin : ')
            if npin  == npin1:
                cur.execute('update userd set pin = %s where uaccno = %s',(npin1,accno))
                cur.execute('commit;')
                print('Pin Changed Sucessfully......')
                return yn(True)
            else:
                print('Re- Enter Your Pin ....')
                cnt += 1
                flag = chkcnt(cnt)
        else:
            print('Pin is Invalid.....')
            return yn(True)
    #return yn(True)
def statem(flag,accno):
    dt = input('Enter Starting Date of Transaction : ')
    dt1 = input('Enter Ending Date of Tranaction : ')
    cur.execute('select * from transactions where dateof between %s and %s and uaccno = %s;',(dt,dt1,accno))
    cn = ['User Name','Account Number','Account Type' , 'credit', 'Debit', 'Date of Transaction' , 'Time of Transaction']
    data = cur.fetchall()
    return prtd(data, cn)
def menuu(accno, flag):
    cnt = 0
    while flag:
        ch = safe_int_input('''
        1. Account details
        2. Debit Amount
        3. Credit Amount
        4. Pin change
        5. Statements
        6. Exit\n>>> ''')
        if ch == 1:
            flag = accdu()
        elif ch == 2:
            cur.execute('SELECT uamt FROM users WHERE uaccno = %s', (accno,))
            data1 = cur.fetchall()
            detm = safe_int_input('Enter Amount to Debit : ')
            if detm and detm > 0 and data1 and data1[0][0] > detm:
                flag = debit(detm, accno)
            else:
                print('Insufficient Balance or Invalid Amount.')
                flag = yn(True)
        elif ch == 3:
            cur.execute('SELECT uamt FROM users WHERE uaccno = %s', (accno,))
            data1 = cur.fetchall()
            detm = safe_int_input('Enter Amount to Credit : ')
            if detm < 10000000:
                flag = credit(detm, accno)
            else:
                print('Invalid Amount.')
                flag = yn(True)
        elif ch == 4:
            flag = pinch(flag,accno)
        elif ch == 5:
            flag = statem(flag,accno)
        elif ch == 6:
            flag = yn(True)
        else:
            cnt += 1
            flag = chkcnt(cnt)
    return flag
def login():
    cur.execute('SELECT * FROM userd;')
    data = cur.fetchall()
    print('Enter Your details.....')
    accno = safe_int_input('Enter Account Number -> ')
    pinnum = input('Enter Pin Number -> ')
    for i in data:
        if str(accno) == i[0] and pinnum == i[1]:
            
            menuu(accno, True)
            break
    else:
        print("Invalid login details.")
        return yn(True)
def signup(flag=True):
    print('Enter Your Details.....')
    cnt = 0

    accname = input('Enter your Name -> ')
    while flag:
        if accname and not accname[0].isdigit():
            break
        cnt += 1
        flag = chkcnt(cnt)
        if not flag:
            return False
        accname = input('Re-enter your name : ')

   
    cnt = 0
    accty = input('Enter Account Type (savings or current) -> ')
    while flag:
        if accty.lower() in ['savings', 'current']:
            break
        cnt += 1
        flag = chkcnt(cnt)
        if not flag:
            return False
        accty = input('Re-enter Account Type Again : ')

    
    uamt = safe_int_input('Enter Amount to deposit -> ')
    if uamt is None:
        return False

    
    cnt = 0
    phnum = safe_int_input('Enter your Phone number -> ')
    while flag:
        if phnum is None:
            return False
        nphn = str(phnum)
        if len(nphn) == 10 and nphn.isdigit():
            break
        cnt += 1
        flag = chkcnt(cnt)
        if not flag:
            return False
        phnum = safe_int_input('Re-enter your Phone number : ')

    
    cnt = 0
    pinnum = safe_int_input('Enter New Pin Number (4 digits) -> ')
    while flag:
        if pinnum is None:
            return False
        if len(str(pinnum)) == 4 and str(pinnum).isdigit():
            break
        cnt += 1
        flag = chkcnt(cnt)
        if not flag:
            return False
        pinnum = safe_int_input('Re-enter your Pin Number : ')

    
    new = random.randint(1111, 9999)
    accno = str(new) + str(phnum)

    
    cur.execute('INSERT INTO userd VALUES (%s, %s);', (accno, pinnum))
    cur.execute('INSERT INTO users VALUES (%s, %s, %s, %s, %s);', (accname, accno, accty, uamt, phnum))
    con.commit()
    print('Account Created Successfully....!!!!!')
    return True
print('BANK SYSTEM')
cnt = 0
flag = True
while flag:
    per = safe_int_input('\n1. ADMIN\n2. USER\n3. EXIT\n>>> ')
    if per == 1:
        while flag:
            cur.execute('SELECT * FROM admin;')
            data = cur.fetchall()
            adid = safe_int_input('Enter AdminId : ')
            pas = input('Enter Password : ')
            for i in data:
                if adid == i[0] and pas == i[1]:
                    print('Welcome | Admin.....')
                    flag = menu(flag)
                    break
            else:
                cnt += 1
                flag = chkcnt(cnt)
        break
    elif per == 2:
        while flag:
            log = safe_int_input('1. LOGIN\n2. SIGNUP\n3. Exit\n>>> ')
            if log == 1:
                flag = login()
            elif log == 2:
                flag = signup(flag)
            elif log == 3:
                flag = yn(True)
            else:
                cnt += 1
                flag = chkcnt(cnt)
    elif per == 3:
        print('Thank You.......')
        break
    
    else:
        if per == False:
            break
        cnt += 1
        flag = chkcnt(cnt)
con.commit()
cur.close()
con.close()