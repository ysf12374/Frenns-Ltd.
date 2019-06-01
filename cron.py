import settings, database, datetime, os, sys, inspect

query = "SELECT DISTINCT frenns_id FROM syncinvoice;"
database.cursor.execute(query)

# force  = int(sys.argv[1])
for record in database.cursor:
    frenns_id = record[0]
    query2  = "SELECT max(updated_at) as last_exec FROM syncrevenueprediction WHERE frenns_id = '"+frenns_id+"';"
    cursor2 = database.con.cursor()
    cursor2.execute(query2)

    last_exec = None
    for record2 in cursor2:
        last_exec = record2[0]

    now  = datetime.datetime.now()
    past = now - datetime.timedelta(days=7)
    do_run = True

    if last_exec:
        do_run = last_exec < past

    if do_run: # or force > 0:
        file_path = os.getcwd()
        dirpath = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        os.system("python3 "+dirpath+"/paydays_prediction.py " + frenns_id +" "+ str(now.year) +" "+ "ACCREC")
        os.system("python3 "+dirpath+"/paydays_prediction.py " + frenns_id +" "+ str(now.year) +" "+ "ACCPAY")
        os.system("python3 "+dirpath+"/expense_prediction.py " + frenns_id +" "+ str(now.year) +" "+ str(now.month) +" "+ "ACCREC")
        os.system("python3 "+dirpath+"/expense_prediction.py " + frenns_id +" "+ str(now.year) +" "+ str(now.month) +" "+ "ACCPAY")
