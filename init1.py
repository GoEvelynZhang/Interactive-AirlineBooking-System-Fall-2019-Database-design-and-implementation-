#!/usr/local/bin/python3

#Import Flask Library
from flask import Flask, jsonify, render_template, request, session, url_for, redirect, flash
import mysql.connector
# from datetime import datetime
import datetime
from dateutil.relativedelta import relativedelta
import json

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = mysql.connector.connect(host='localhost',
                       port=8889,
                       user='root',
                       password='root',
                       database='BookingAir')


# ***************************************************************
# All functionality regarding the flight search, purchase, booking Usage un the root page

@app.route('/')
def hello():
    try:
        username = session["username"]
        print("the current username is", username)
    
        flash("You are logged in to Purchase")
        return render_template('index.html',username = username)
    except:
        return render_template('index.html')

@app.route('/searchTicket', methods=['POST'])
def searchTicket():
    req = json.loads(request.data)
    dep_city = req["from"]
    dep_air = req["froma"]
    arrive_city = req["to"]
    arrive_air = req["toa"]
    date = req["flightdate"]
    date = datetime.datetime.strptime(date, '%m/%d/%Y').date()
    data = ""
    ##input two airports
    if dep_air != "" and arrive_air != "":
        if dep_city == '' and arrive_city == '':
            cursor = conn.cursor()
            query = "SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, price FROM flight  WHERE departure_airport = \'{}\' and arrival_airport = \'{}\' and CAST(departure_time AS DATE) =\'{}\'"
            cursor.execute(query.format(dep_air,arrive_air, date))
   
            data = cursor.fetchall()
   
            cursor.close()
        elif dep_city != '' and arrive_city == '':
            cursor = conn.cursor()
            query = query = "SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.arrival_airport, flight.departure_time, flight.arrival_time, flight.price FROM flight,airport AS A  WHERE A.airport_name = flight.departure_airport and flight.departure_airport = \'{}\' and A.airport_city = \'{}\' and flight.arrival_airport = \'{}\' and CAST(flight.departure_time AS DATE) =\'{}\'"
            cursor.execute(query.format(dep_air,dep_city,arrive_air, date))
            data = cursor.fetchall()
            cursor.close()
        elif dep_city == '' and arrive_city != '':
            cursor = conn.cursor()
            query = "SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.arrival_airport, flight.departure_time, flight.arrival_time, flight.price FROM flight,airport AS A  WHERE A.airport_name = flight.arrival_airport and flight.departure_airport = \'{}\'  and flight.arrival_airport = \'{}\' and A.airport_city = \'{}\' and CAST(flight.departure_time AS DATE) =\'{}\'"
            cursor.execute(query.format(dep_air,arrive_air, arrive_city,date))
            data = cursor.fetchall()
            cursor.close()
        else:
            cursor = conn.cursor()
            query = "SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.arrival_airport, flight.departure_time, flight.arrival_time, flight.price FROM flight,airport AS A, airport AS B  WHERE A.airport_name = flight.departure_airport and B.airport_name = flight.arrival_airport and flight.departure_airport = \'{}\' and A.airport_city =  \'{}\' and flight.arrival_airport = \'{}\' and B.airport_city = \'{}\' and CAST(flight.departure_time AS DATE) =\'{}\'"
            cursor.execute(query.format(dep_air,dep_city,arrive_air, arrive_city,date))
            data = cursor.fetchall()
            cursor.close()

  
    elif dep_air !='' and arrive_air == '':
        if dep_city != "" and arrive_city != "":
            cursor = conn.cursor()
            query = "SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.arrival_airport, flight.departure_time, flight.arrival_time, flight.price FROM flight,airport AS A, airport AS B   WHERE A.airport_name = flight.departure_airport and B.airport_name = flight.arrival_airport and A.airport_city = \'{}\' and flight.departure_airport = \'{}\' and B.airport_city = \'{}\' and CAST(flight.departure_time AS DATE) =\'{}\'"
            cursor.execute(query.format(dep_city,dep_air,arrive_city, date))
   
            data = cursor.fetchall()
   
            cursor.close()
        elif dep_city == "" and arrive_city != "":
            cursor = conn.cursor()
            query = "SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.arrival_airport, flight.departure_time, flight.arrival_time, flight.price FROM flight,airport AS A  WHERE A.airport_name = flight.arrival_airport  and A.airport_city = \'{}\' and flight.departure_airport = \'{}\' and CAST(flight.departure_time AS DATE) =\'{}\'"
            cursor.execute(query.format(arrive_city,dep_air, date))
  
            data = cursor.fetchall()
   
            cursor.close()

        
    elif dep_air == '' and arrive_air != '':
        if dep_city != "" and arrive_city != "":
            cursor = conn.cursor()
            query = "SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.arrival_airport, flight.departure_time, flight.arrival_time, flight.price FROM flight,airport AS A, airport AS B   WHERE A.airport_name = flight.departure_airport and B.airport_name = flight.arrival_airport and A.airport_city = \'{}\'  and B.airport_city = \'{}\' and flight.arrival_airport = \'{}\' and CAST(flight.departure_time AS DATE) =\'{}\'"
            cursor.execute(query.format(dep_city,arrive_city,arrive_air, date))
   
            data = cursor.fetchall()
   
            cursor.close()
        elif dep_city != "" and arrive_city == "":
            cursor = conn.cursor()
            query = "SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.arrival_airport, flight.departure_time, flight.arrival_time, flight.price FROM flight,airport AS A  WHERE A.airport_name = flight.departure_airport  and A.airport_city = \'{}\' and flight.arrival_airport = \'{}\' and CAST(flight.departure_time AS DATE) =\'{}\'"
            cursor.execute(query.format(dep_city,arrive_air, date))
   
            data = cursor.fetchall()
  
            cursor.close()


    else:
        cursor = conn.cursor()
        query = "SELECT flight.airline_name, flight.flight_num, flight.departure_airport, flight.arrival_airport, flight.departure_time, flight.arrival_time, flight.price FROM flight,airport AS A, airport AS B   WHERE A.airport_name = flight.departure_airport and B.airport_name = flight.arrival_airport and A.airport_city = \'{}\' and B.airport_city = \'{}\' and CAST(flight.departure_time AS DATE) =\'{}\'"
        cursor.execute(query.format(dep_city,arrive_city, date))
   
        data = cursor.fetchall()
   
        cursor.close()

           

    


    

    
    
    transfer = []
    for i in range(len(data)):
        current =[]
        current.append(data[i][0])
        current.append(data[i][1])
        current.append(data[i][2])
        current.append(data[i][3])
        current.append(data[i][4])
        current.append(data[i][5])
        current.append(int(data[i][6]))
        transfer.append(current)
    return jsonify({
            "data": transfer
            })

@app.route("/ConfirmCustomerLog",methods = ["POST"])
def ComfirmCustomerLog():
    req = json.loads(request.data)
    result = ''
    try:
        username = session["username"]
        print(username)
    
   
        # check if log in as a right identity
        cursor = conn.cursor()
        query = "SELECT * FROM customer  WHERE email =  \'{}\'  "
        cursor.execute(query.format(username))
        data = cursor.fetchone()
        cursor.close()
        if (data):
            result = 'correct'
        else:
            result = 'wrong_identity'
    except:
        result = 'not_logIn'
    return jsonify({"data":result})
        
        
@app.route('/ConfirmTicketPurchase', methods=['POST'])
def ConfirmTicketPurchase():
    username = session["username"]
    req = json.loads(request.data)
    airline = req[0]
    flight_num = req[1]
    depart_air = req[2]
    arrive_air = req[3]
    depart_time = req[4]
    arrive_time = req[5]
    price = req[6]
    ##get the availabel seat number
    cursor = conn.cursor()
    query = "SELECT seats FROM airplane NATURAL JOIN flight  WHERE airline_name =  \'{}\' and flight_num = \'{}\' "
    cursor.execute(query.format(airline, flight_num))
    total_seat = int(cursor.fetchone()[0])
    cursor.close()
    ##get how many already taken
    cursor = conn.cursor()
    query = "SELECT count(ticket_id) FROM ticket  WHERE airline_name =  \'{}\' and flight_num = \'{}\' "
    cursor.execute(query.format(airline, flight_num))
    taken_seat = int(cursor.fetchone()[0])
    cursor.close()
    print("total_seat:",total_seat)
    print("taken_seat: ",taken_seat)
    state = None
    if (taken_seat):
        pass
    else:
        taken_seat = 0
    if total_seat > taken_seat:
        #current total tickets
        cursor = conn.cursor()
        query = "SELECT max(ticket_id) FROM ticket"
        cursor.execute(query)
        total_ticket = int(cursor.fetchone()[0])
        cursor.close()
        current_ticket_id = total_ticket+1
        #update the ticket
        cursor = conn.cursor()
        query = "INSERT INTO ticket(ticket_id, airline_name, flight_num) VALUES (\'{}\',\'{}\',\'{}\')"
        cursor.execute(query.format(current_ticket_id,airline, flight_num ))
        conn.commit()
       
        cursor.close()
        #update the purchase table
        cursor = conn.cursor()
        query = "INSERT INTO purchases(ticket_id, customer_email, purchase_date) VALUES (\'{}\',\'{}\',\'{}\')"
        cursor.execute(query.format(current_ticket_id,username,datetime.datetime.now().strftime("%Y-%m-%d") ))
        conn.commit()
        cursor.close()
        state = "Successfully Purchased"
        
    else:
        state = "OOPS, this flight already fully booked"



    print(state)
    print(req)
    return jsonify(state)        

#Define route for login
@app.route('/searchFlightStatus',methods = ["POST"])
def searchFlightStatus():
    req = json.loads(request.data)
    flight_num = int(req['flight_num'])
    depart_date = req['depart_date']
    
    arrive_date = req["arrive_date"]
    
    ##only the flight_num
    data = None
    print(flight_num,depart_date,arrive_date )
    if depart_date == 'mm/dd/yyyy' and arrive_date == 'mm/dd/yyyy':
    
        cursor = conn.cursor()
        query = "SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time, arrival_time, status FROM flight WHERE flight_num = \'{}\'"
        cursor.execute(query.format(flight_num))
        data = cursor.fetchall()
        cursor.close()
    elif depart_date != 'mm/dd/yyyy' and arrive_date == 'mm/dd/yyyy':
    
        depart_date = datetime.datetime.strptime(depart_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        cursor = conn.cursor()
        query = "SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time , arrival_time, status FROM flight WHERE flight_num = \'{}\' and CAST(departure_time AS DATE) =\'{}\' "
        cursor.execute(query.format(flight_num, depart_date))
        data = cursor.fetchall()
        cursor.close()
    elif depart_date == 'mm/dd/yyyy' and arrive_date != 'mm/dd/yyyy':
        arrive_date = datetime.datetime.strptime(arrive_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        cursor = conn.cursor()
        query = "SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time , arrival_time, status FROM flight WHERE flight_num = \'{}\' and CAST(arrival_time AS DATE) =\'{}\' "
        cursor.execute(query.format(flight_num, arrive_date))
        data = cursor.fetchall()
        cursor.close()
    else:
        depart_date = datetime.datetime.strptime(depart_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        arrive_date = datetime.datetime.strptime(arrive_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        cursor = conn.cursor()
        query = "SELECT airline_name, flight_num, departure_airport, arrival_airport, departure_time , arrival_time, status FROM flight WHERE flight_num = \'{}\' and CAST(departure_time AS DATE) =\'{}\' and CAST(arrival_time AS DATE) = \'{}\' "
        cursor.execute(query.format(flight_num, depart_date, arrive_date))
        data = cursor.fetchall()
        cursor.close()

    
    return jsonify(data)
# ***************************************************************
# All functionality regarding the Customer Usage
@app.route('/CustomerLogIn')
def login():
    return render_template('CustomerLogIn.html')

@app.route('/CustomerAuth', methods=['GET', 'POST'])
def loginAuth():
    username = request.form['username']
    password = request.form['password']
    cursor = conn.cursor()
    query = "SELECT * FROM customer WHERE email = \'{}\' and password = MD5(\'{}\')"
    cursor.execute(query.format(username,password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('CustomerHome'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username, please try again or register an account first'
        return render_template('CustomerLogIn.html', error=error)

#Define route for register
@app.route('/CustomerRegister')
def CustomerRegister():
    return render_template('CustomerRegister.html')




#Authenticates the register
@app.route('/CusRegisterAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    email = request.form['email']
    password = request.form['password']
    state = request.form['state']
    name = request.form['name']
    city = request.form['city']
    street = request.form['street']
    building = request.form['building']
    phone_number = request.form['phone_number']
    passport_number = request.form['passport_number']
    passport_expiration = request.form['passport_expiration']
    passport_expiration = datetime.datetime.strptime(passport_expiration, "%m/%d/%Y").strftime("%Y-%m-%d")
    passport_country = request.form['passport_country']
    date_of_birth = request.form['date_of_birth']
    date_of_birth = datetime.datetime.strptime(date_of_birth, "%m/%d/%Y").strftime("%Y-%m-%d")

#    if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = "SELECT * FROM customer WHERE email = \'{}\'"
    cursor.execute(query.format(email))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "You have already registered, please go log in directly"
        return render_template('CustomerRegister.html', error = error)
        ##send the error to the page 
    else:
        ins = "INSERT INTO customer(email,name,password,building_number,street,city,state,phone_number,passport_number,passport_expiration,passport_country,date_of_birth) VALUES(\'{}\', \'{}\',MD5(\'{}\'),\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')"
        cursor.execute(ins.format(email,name,password,building,street,city,state,phone_number,passport_number,passport_expiration,passport_country,date_of_birth))
        conn.commit()
        cursor.close()
        # cursor is for the db conenction and operation
        message = "You are Successfully Registered!"
        return render_template('CustomerRegister.html',message = message)

@app.route('/CustomerHome', methods = ["GET",'POST'])
def CustomerHome():
    # session is for controlling the user participating
    #so that user only see posts belonging to them
    one_year_ago = (datetime.datetime.now() - datetime.timedelta(days=1*365)).strftime("%Y-%m-%d")
    six_month_ago = (datetime.datetime.now() - datetime.timedelta(days=0.5*365)).strftime("%Y-%m-%d")
    today2 = datetime.datetime.now().strftime("%Y-%m-%d")

    username = session['username']
    today1 = datetime.datetime.now()
    # hold in the backend
    cursor = conn.cursor()
    query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM ticket NATURAL JOIN purchases WHERE customer_email = \'{}\' AND purchase_date  > \'{}\' ORDER BY purchase_date  DESC"
    query2 = "SELECT SUM(price) FROM purchases NATURAL JOIN flight WHERE customer_email  = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\'"
    cursor.execute(query.format(username,six_month_ago,today1))
    data1 = cursor.fetchall() 
    cursor.close()
    cursor = conn.cursor()
    cursor.execute(query2.format(username,one_year_ago,today2))
    total_spending = cursor.fetchone() 
    cursor.close()
    cursor = conn.cursor()
    query3 = "SELECT  MONTH(purchase_date),sum(price) FROM purchases NATURAL JOIN flight WHERE customer_email  = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\' GROUP BY MONTH(purchase_date) ORDER BY MONTH(purchase_date) "
    cursor.execute(query3.format(username,six_month_ago,today2))
    data2 = cursor.fetchall() 
    cursor.close()
    

    total_spending = total_spending[0]
    
    if total_spending:
        pass
    else:
        total_spending= 0
    # print("success in rendering total_spending")
    monthly_spending =[[int(i[0]),int(i[1])] for i in data2]
    
    month_with_data = [j[0] for j in monthly_spending]
    # print(today1.month)
    month_six = []
    if today1.month >= 6 :
        month_six = [today1.month-(5-i) for i in range(6)]
    elif today1.month <6 :
        month_six = [(12-(6-today1.month-1-i)) for i in range(6-today1.month)]+[j for j in range(1,today1.month+1)]
    six_output = []
    for k in range(6):
        if month_six[k] not in month_with_data:
            six_output.append([month_six[k],0])
        else:
            six_output.append(monthly_spending[month_with_data.index(month_six[k])])
            
 
    return render_template('CustomerPage.html', username=username, posts=data1, total_spending = total_spending, monthly_spending = six_output)

@app.route("/CustomeHomeLogOut")
def CustomeHomeLogOut():
    session.pop('username')
    print("successfully logged out")
    return redirect("/CustomerLogIn")
@app.route("/CustomerPurchase")        
def Customerpurchase():
    
    username = session['username']
    if (username):
        cursor = conn.cursor()
        query = "SELECT * FROM customer WHERE email = \'{}\'"
        cursor.execute(query.format(username))
        data = cursor.fetchone() 
        cursor.close()
        if data:
            flash("You are logged in to Purchase")
            return render_template("index.html", username = username)
        else:
            error = "You are not a registered Customer!"
            return render_template('index.html',error = error)
    else:
        error = ("Please Log In to Purchase")
        return render_template('index.html',error = error)

@app.route('/searchPurchase', methods=['POST'])
def searchPurchase():
    username = session["username"]
    req = json.loads(request.data)  
    start_date = req["datepicker1"] 
    
    end_date = req["datepicker2"]
    
    start_city =  req["Source_City"]
    start_airport = req["Source_Airport"] 
    arrive_city =  req["Dest_City"] 
    arrive_airport =  req["Dest_Airport"]
    print(req)
    ret =[]
    data = None
    if start_date != 'mm/dd/yyyy' and end_date !='mm/dd/yyyy':
        start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        if start_city == '' and arrive_city == '':
            if start_airport == '' and arrive_airport == '':
                
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE customer_email = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\' ORDER BY purchase_date  DESC"
                cursor.execute(query.format(username, start_date, end_date))
                data = cursor.fetchall() 
                cursor.close()
            else:
               
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE customer_email = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\' AND departure_airport =\'{}\' AND arrival_airport =\'{}\' ORDER BY purchase_date  DESC"
                cursor.execute(query.format(username, start_date, end_date,start_airport,arrive_airport))
                data = cursor.fetchall() 
                cursor.close()
        else:
            if start_airport == '' and arrive_airport == '':
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM (ticket NATURAL JOIN purchases NATURAL JOIN flight AS A), airport as B, airport as C WHERE A.departure_airport = B.airport_name and A.arrival_airport = C.airport_name and customer_email = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\' ORDER BY purchase_date  DESC "
                cursor.execute(query.format(username, start_city, arrive_city, start_date,end_date))
                data = cursor.fetchall() 
                cursor.close()
            else:
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM (ticket NATURAL JOIN purchases NATURAL JOIN flight AS A), airport as B, airport as C WHERE A.departure_airport = B.airport_name and A.arrival_airport = C.airport_name and customer_email = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' AND departure_airport = \'{}\' AND arrival_airport = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\'  ORDER BY purchase_date  DESC "
                cursor.execute(query.format(username, start_city, arrive_city, start_airport,arrive_airport,start_date,end_date))
                data = cursor.fetchall() 
                cursor.close()

    else:
        
        
    # if the input is the start and the destination airport  
        if start_city != '' and arrive_city != '':
            if start_airport == '' and arrive_airport == '':
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM (ticket NATURAL JOIN purchases NATURAL JOIN flight AS A), airport as B, airport as C WHERE A.departure_airport = B.airport_name and A.arrival_airport = C.airport_name and customer_email = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' "
                cursor.execute(query.format(username, start_city, arrive_city))
                data = cursor.fetchall() 
                cursor.close()
            else:
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM (ticket NATURAL JOIN purchases NATURAL JOIN flight AS A), airport as B, airport as C WHERE A.departure_airport = B.airport_name and A.arrival_airport = C.airport_name and customer_email = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' AND departure_airport = \'{}\' AND arrival_airport = \'{}\'"
                cursor.execute(query.format(username, start_city, arrive_city,start_airport,arrive_airport))
                data = cursor.fetchall() 
                cursor.close()
        # if the user input are the two airport
        else:
            cursor = conn.cursor()
            query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE customer_email = \'{}\' AND departure_airport = \'{}\' AND arrival_airport = \'{}\' "
            cursor.execute(query.format(username, start_airport, arrive_airport))
            data = cursor.fetchall() 
            cursor.close()

        # deal with the time format inconsistency
    if data:
        for i in range(len(data)):
            current=[]
            current.append(data[i][0])
            current.append(data[i][1])
            current.append(data[i][2])
            current.append(data[i][3].strftime("%Y-%m-%d"))
            ret.append(current)
    else:
        pass
    return jsonify({
            "data": ret
            })
        
   
    
   

@app.route("/searchSpending", methods=['POST'])
def searchSpending():
    username = session["username"]
    req = json.loads(request.data) 
    print(req) 
    start_date = req["date_start"] 
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    end_date = req["date_end"]
    end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    
    cursor = conn.cursor()
    query = "SELECT SUM(price) FROM ticket NATURAL JOIN flight NATURAL JOIN purchases WHERE customer_email  = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\'"
    cursor.execute(query.format(username,start_date,end_date))
    try:
        total_spending = int(cursor.fetchone()[0])
    
    except:
        total_spending = 0
    
    cursor = conn.cursor()
    query = "SELECT MONTH(purchase_date),SUM(price) FROM ticket NATURAL JOIN flight NATURAL JOIN purchases WHERE customer_email  = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\' GROUP BY MONTH(purchase_date) ORDER BY MONTH(purchase_date)"
    cursor.execute(query.format(username,start_date,end_date))
    monthly_spending = cursor.fetchall()
    cursor = conn.cursor()
    month_spending = [[monthly_spending[i][0],int(monthly_spending[i][1])] for i in range(len(monthly_spending))]
    print(month_spending)
    return jsonify({
            "total_spending": total_spending,
            "monthly_spending": month_spending,
            })
# ***************************************************************
# All functionality regarding the Agent Usage

@app.route('/AgentLogIn')
def AgentLogin():
    return render_template('AgentLogIn.html')
@app.route("/AgentAuth",methods=['GET', 'POST'])
def AgentAuth():
    email = request.form['username']
    agent_id = request.form['Agent_id']
    password = request.form['password']
    cursor = conn.cursor()
    query = "SELECT * FROM booking_agent WHERE email =\'{}\' and booking_agent_id = \'{}\' and password = MD5(\'{}\')"
    cursor.execute(query.format(email,agent_id,password))
    #stores the results in a variable
    data = cursor.fetchone()
    print(data)
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if (data):
        #creates a session for the the user
        #session is a built in
        session['username'] = agent_id
        return redirect(url_for('AgentHome'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username, please try again or register an account first'
        return render_template('AgentLogIn.html', error=error)

@app.route("/AgentHome") 
def AgentHome():
    #view the flight
    username = session['username']
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    cursor = conn.cursor()
    query = "SELECT ticket_id, airline_name,customer_email,purchase_date FROM ticket NATURAL JOIN purchases WHERE booking_agent_id = \'{}\' AND purchase_date > \'{}\' ORDER BY purchase_date DESC"

    cursor.execute(query.format(username,today))
    data = cursor.fetchall() 
    cursor.close()
    #view the commission [total commission, commision per ticket, total number of ticket]
    thirty_day = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    cursor = conn.cursor()
    query1 = "SELECT sum(price)*0.1 FROM purchases NATURAL JOIN flight WHERE booking_agent_id = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\'"

    cursor.execute(query1.format(username,thirty_day,today))
    total_commission = cursor.fetchone()[0]
    
    cursor.close()
    cursor = conn.cursor()
    query1 = "SELECT count(*) FROM purchases WHERE booking_agent_id = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\'"

    cursor.execute(query1.format(username,thirty_day,today))
    total_ticket = cursor.fetchone()[0]

    cursor.close()
    average_price = 0
    try:
        average_price = total_commission/total_ticket
    except:
        pass

    ##top customers(number of ticket, number of commisions)
    six_month_ago = (datetime.datetime.now() - datetime.timedelta(days=0.5*365)).strftime("%Y-%m-%d")
    cursor = conn.cursor()
    query2 = "SELECT customer_email,count(ticket_id) FROM purchases WHERE booking_agent_id = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\' GROUP BY customer_email ORDER BY count(ticket_id) DESC"

    cursor.execute(query2.format(username,six_month_ago,today))
    by_number = cursor.fetchall()
    cursor.close()
    cursor = conn.cursor()
    query3 = "SELECT customer_email,sum(price)*0.1 FROM purchases NATURAL JOIN flight WHERE booking_agent_id = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\' GROUP BY customer_email ORDER BY sum(price) DESC"

    cursor.execute(query3.format(username,six_month_ago,today))
    by_commission = cursor.fetchall()
    commission = [[str(by_commission[i][0]),float(by_commission[i][1])] for i in range(len(by_commission))]
    cursor.close()

    print(by_number,by_commission)
    top_cus = [by_number,commission]


    return render_template('AgentPage.html', username = username,posts=data, commission = [total_commission,average_price,total_ticket],top_cus = top_cus )
@app.route("/AgentHomeLogOut")
def AgentHomeLogOut():
    session.pop('username')
    print("Here")
    
    return redirect('/AgentLogIn')

@app.route("/searchBooking", methods = ["POST"])
def searchBooking():
    username = session['username']
    req = json.loads(request.data)
    start_date = req["datepicker1"]
    # begin_date = datetime.datetime.strptime(begin_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    end_date = req["datepicker2"]
    # end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    start_city = req["Source_City"]
    start_airport = req["Source_Airport"]
    arrive_city = req['Dest_City']
    arrive_airport = req['Dest_Airport']
    print(req)
    ret = []
    if start_date != 'mm/dd/yyyy' and end_date !='mm/dd/yyyy':
        start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        if start_city == '' and arrive_city == '':
            if start_airport == '' and arrive_airport == '':
                
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE booking_agent_id = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\' ORDER BY purchase_date  DESC"
                cursor.execute(query.format(username, start_date, end_date))
                data = cursor.fetchall() 
                cursor.close()
            else:
               
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE booking_agent_id = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\' AND departure_airport =\'{}\' AND arrival_airport =\'{}\' ORDER BY purchase_date  DESC"
                cursor.execute(query.format(username, start_date, end_date,start_airport,arrive_airport))
                data = cursor.fetchall() 
                cursor.close()
        else:
            if start_airport == '' and arrive_airport == '':
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM (ticket NATURAL JOIN purchases NATURAL JOIN flight AS A), airport as B, airport as C WHERE A.departure_airport = B.airport_name and A.arrival_airport = C.airport_name and booking_agent_id = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\' ORDER BY purchase_date  DESC "
                cursor.execute(query.format(username, start_city, arrive_city, start_date,end_date))
                data = cursor.fetchall() 
                cursor.close()
            else:
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM (ticket NATURAL JOIN purchases NATURAL JOIN flight AS A), airport as B, airport as C WHERE A.departure_airport = B.airport_name and A.arrival_airport = C.airport_name and booking_agent_id = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' AND departure_airport = \'{}\' AND arrival_airport = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\'  ORDER BY purchase_date  DESC "
                cursor.execute(query.format(username, start_city, arrive_city, start_airport,arrive_airport,start_date,end_date))
                data = cursor.fetchall() 
                cursor.close()

    else:
        
        
    # if the input is the start and the destination airport  
        if start_city != '' and arrive_city != '':
            if start_airport == '' and arrive_airport == '':
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM (ticket NATURAL JOIN purchases NATURAL JOIN flight AS A), airport as B, airport as C WHERE A.departure_airport = B.airport_name and A.arrival_airport = C.airport_name and booking_agent_id = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' "
                cursor.execute(query.format(username, start_city, arrive_city))
                data = cursor.fetchall() 
                cursor.close()
            else:
                cursor = conn.cursor()
                query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM (ticket NATURAL JOIN purchases NATURAL JOIN flight AS A), airport as B, airport as C WHERE A.departure_airport = B.airport_name and A.arrival_airport = C.airport_name and booking_agent_id = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' AND departure_airport = \'{}\' AND arrival_airport = \'{}\'"
                cursor.execute(query.format(username, start_city, arrive_city,start_airport,arrive_airport))
                data = cursor.fetchall() 
                cursor.close()
        # if the user input are the two airport
        else:
            cursor = conn.cursor()
            query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE booking_agent_id = \'{}\' AND departure_airport = \'{}\' AND arrival_airport = \'{}\' "
            cursor.execute(query.format(username, start_airport, arrive_airport))
            data = cursor.fetchall() 
            cursor.close()
    # if begin_date != '' and end_date != '':
        
    #     cursor = conn.cursor()
    #     query = "SELECT ticket_id, airline_name,customer_email, purchase_date FROM purchases NATURAL JOIN ticket WHERE booking_agent_id = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\'  ORDER BY purchase_date DESC"

    #     cursor.execute(query.format(username,begin_date,end_date))
    #     all_booking = cursor.fetchall()
    #     cursor.close()
    #     ret =[]
    #     for i in range(len(all_booking)):
    #         current=[]
    #         current.append(all_booking[i][0])
    #         current.append(all_booking[i][1])
    #         current.append(all_booking[i][2])
    #         current.append(all_booking[i][3].strftime("%Y-%m-%d"))
    #         ret.append(current)
    # else:
    #     pass

    if data:
        for i in range(len(data)):
            current=[]
            current.append(data[i][0])
            current.append(data[i][1])
            current.append(data[i][2])
            current.append(data[i][3].strftime("%Y-%m-%d"))
            ret.append(current)
    else:
        pass
    return jsonify({
            "data": ret
            })
  
   

@app.route("/AgentPurchase")        
def AgentPurchase():
    username = session['username']
   
    
    flash("You are logged in to Purchase")
    return render_template('index.html', username = username)

@app.route("/ConfirmAgentLog",methods = ["POST"])
def ConfirmAgentLog():
    req = json.loads(request.data)
    result = ''
    try:
        username = session["username"]
        print(username)
    
   
        # check if log in as a right identity
        cursor = conn.cursor()
        query = "SELECT * FROM booking_agent WHERE booking_agent_id =  \'{}\'  "
        cursor.execute(query.format(username))
        data = cursor.fetchone()
        cursor.close()
        if (data):
            result = 'correct'
        else:
            result = 'wrong_identity'
    except:
        result = 'not_logIn'
    return jsonify({"data":result})

@app.route("/BookingConfirmTicketPurchase",methods = ["POST"])
def BookingConfirmTicketPurchase():
    username = session['username']
    req = json.loads(request.data)
    airline = req[0]
    flight_num = req[1]
    depart_air = req[2]
    arrive_air = req[3]
    depart_time = req[4]
    arrive_time = req[5]
    price = req[6]
    customer = req[7]
    ##get the availabel seat number
    cursor = conn.cursor()
    query = "SELECT seats FROM airplane NATURAL JOIN flight  WHERE airline_name =  \'{}\' and flight_num = \'{}\' "
    cursor.execute(query.format(airline, flight_num))
    total_seat = int(cursor.fetchone()[0])
    cursor.close()
    ##get how many already taken
    cursor = conn.cursor()
    query = "SELECT count(ticket_id) FROM ticket  WHERE airline_name =  \'{}\' and flight_num = \'{}\' "
    cursor.execute(query.format(airline, flight_num))
    taken_seat = int(cursor.fetchone()[0])
    cursor.close()
   
    state = None
    if (taken_seat):
        pass
    else:
        taken_seat = 0
    if total_seat > taken_seat:
        #current total tickets
        cursor = conn.cursor()
        query = "SELECT max(ticket_id) FROM ticket"
        cursor.execute(query)
        total_ticket = int(cursor.fetchone()[0])
        cursor.close()
        current_ticket_id = total_ticket+1
        #update the ticket
        cursor = conn.cursor()
        query = "INSERT INTO ticket(ticket_id, airline_name, flight_num) VALUES (\'{}\',\'{}\',\'{}\')"
        cursor.execute(query.format(current_ticket_id,airline, flight_num ))
        conn.commit()
       
        cursor.close()
        #update the purchase table
        cursor = conn.cursor()
        query = "INSERT INTO purchases(ticket_id, customer_email,booking_agent_id, purchase_date) VALUES (\'{}\',\'{}\',\'{}\',\'{}\')"
        cursor.execute(query.format(current_ticket_id,customer,username,datetime.datetime.now().strftime("%Y-%m-%d") ))
       
        cursor.close()
        state = "Successfully Purchased"
        
    else:
        state = "OOPS, this flight already fully booked"
    return jsonify(state)

@app.route("/searchComission",methods = ["POST"])
def searchComission():
    username = session['username']
    req = json.loads(request.data)
    day_start = req["day_start"]
    day_start = datetime.datetime.strptime(day_start, "%m/%d/%Y").strftime("%Y-%m-%d")
    day_end = req["day_end"]
    day_end = datetime.datetime.strptime(day_end, "%m/%d/%Y").strftime("%Y-%m-%d")
    #get the total commison fee
    cursor = conn.cursor()
    query = "SELECT sum(price)*0.1 FROM purchases NATURAL JOIN flight WHERE booking_agent_id = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\'"
    cursor.execute(query.format(username, day_start,day_end ))
    data = cursor.fetchone()[0]
    print(data)
    cursor.close()
    total_commission = 0
    if data:
    
        total_commission = float(data)
 
    
    # get the total number of ticket
    cursor = conn.cursor()
    query = "SELECT count(ticket_id) FROM purchases WHERE booking_agent_id = \'{}\' AND purchase_date  BETWEEN  \'{}\' AND \'{}\'"
    cursor.execute(query.format(username, day_start,day_end ))
    total_ticket = cursor.fetchone()[0]
    average_commission =0
    cursor.close()
  
    try:
        average_commission = total_commission / total_ticket
    except:
        average_commission = 0

    print(total_commission,average_commission)



    return jsonify({"total_commission":total_commission,
                    "total_ticket":total_ticket,
                    "average_commission": average_commission,
    })


@app.route("/AgentRegister")
def AgentRegister():
    return render_template('AgentRegister.html')    
@app.route("/AgentRegisterAuth", methods = ["GET","POST"])
def AgentRegisterAuth():
    username = request.form['username']
    password = request.form['password']

#    if not len(password) >= 4:
#                flash("Password length must be at least 4 characters")
 #               return redirect(request.url)

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = "SELECT * FROM booking_agent WHERE email = \'{}\'"
    

    cursor.execute(query.format(username))
    #stores the results in a variable
    data = cursor.fetchone()
    cursor.close()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "You email have already registered, please go log in directly"
        return render_template('AgentRegister.html', error = error)
        ##send the error to the page 
    else:
        cursor = conn.cursor()
        query_num = "SELECT count(*) FROM booking_agent"
        cursor.execute(query_num.format(username))
        num = int(cursor.fetchone()[0])
        agent_id = num+1
        cursor.close()
        cursor = conn.cursor()
        ins = "INSERT INTO booking_agent(email, password,booking_agent_id ) VALUES(\'{}\', MD5(\'{}\'),\'{}\')"
        cursor.execute(ins.format(username, password, agent_id))
        conn.commit()
        cursor.close()
        message = "Successfully registered, your agent_id is " + str(agent_id) + "   Go to Log In!"
        # cursor is for the db conenction and operation
        
        return render_template('AgentRegister.html', message = message)

# ***************************************************************
# All functionality regarding the Staff Usage

@app.route('/StaffLogIn')
def StaffLogIn():
    return render_template('StaffLogIn.html')
@app.route("/StaffAuth",methods=['GET', 'POST'])
def StaffAuth():
    username = request.form['username']
    password = request.form['password']
    airline = request.form['airline']
    cursor = conn.cursor()
    query = "SELECT * FROM airline_staff WHERE username = \'{}\' and password = MD5(\'{}\') and airline_name = \'{}\'"
    cursor.execute(query.format(username,password, airline))
    #stores the results in a variable
    data = cursor.fetchone()
    print(data)
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        session["airline"] = airline
        return redirect(url_for('StaffHome'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username, please try again or register an account first'
        return render_template('StaffLogIn.html', error=error)



@app.route("/StaffHomeLogOut")
def StaffHomeLogOut():
    session.pop("username")
    session.pop("airline")
    return redirect("/StaffLogIn")

@app.route("/StaffRegister")
def StaffRegister():

    
    return render_template('StaffRegister.html')   

@app.route("/StaffRegisterAuth", methods = ["GET","POST"])
def StaffRegisterAuth():
    username = request.form['username']
    password = request.form['password']
    airline = request.form['airline']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
   

    date_of_birth =  datetime.datetime.strptime(date_of_birth, "%m/%d/%Y").strftime("%Y-%m-%d")
    cursor = conn.cursor()
    #executes query
    query = "SELECT * FROM airline_staff WHERE username = \'{}\' AND airline_name = \'{}\'"
    cursor.execute(query.format(username,airline))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "You have already registered, please go log in directly"
        return render_template('StaffRegister.html', error = error)
        ##send the error to the page 
    else:
        ins = "INSERT INTO airline_staff(username, password, airline_name,first_name,last_name,date_of_birth) VALUES(\'{}\', MD5(\'{}\'),\'{}\',\'{}\', \'{}\',\'{}\')"
        cursor.execute(ins.format(username, password,airline, first_name,last_name,date_of_birth))
        conn.commit()
        cursor.close()
        # cursor is for the db conenction and operation
        message = "You are successfully Registered! Please go to Log In"
        return render_template('StaffRegister.html',message =message)

@app.route('/StaffHome', methods = ["GET",'POST'])
def StaffHome():
	# session for staffs to do basic operations 
	# staffs will be able to view charts and tables
    username = session['username']
    airline = session["airline"]
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    cursor = conn.cursor(buffered=True)

    # view my flights by default
    thirty_future_day = (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    query = "SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status FROM flight WHERE airline_name = \'{}\' AND status = 'upcoming' AND CAST(departure_time AS DATE) BETWEEN  \'{}\' AND \'{}\' ORDER BY departure_time DESC"
    cursor.execute(query.format(airline,today,thirty_future_day))
    dafault_flights = cursor.fetchall() 
    cursor.close()
    print(dafault_flights)
    # view top 5 booking agents by last month ticket sales
    cursor = conn.cursor()
    query1 = "SELECT email, booking_agent_id, count(ticket_id) as total FROM purchases NATURAL JOIN ticket NATURAL JOIN booking_agent  WHERE (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE()) AND airline_name = \'{}\' GROUP BY email  ORDER BY count(ticket_id) DESC LIMIT 5"
    cursor.execute(query1.format(airline))
    agents_month = cursor.fetchall() 
    cursor.close()


    # # view top 5 booking agents by last year ticket sales
    cursor = conn.cursor()
    query2 = "SELECT email, booking_agent_id, count(ticket_id) as total FROM purchases NATURAL JOIN ticket NATURAL JOIN booking_agent WHERE (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) AND airline_name = \'{}\' GROUP BY email  ORDER BY count(ticket_id) DESC LIMIT 5"
    cursor.execute(query2.format(airline))
    agents_year = cursor.fetchall() 
    cursor.close()

    # view top 5 booking agents by last year commission
    cursor = conn.cursor()
    query3 = "SELECT email, booking_agent_id, sum(price) * 0.1 as commission FROM ticket NATURAL JOIN flight NATURAL JOIN purchases NATURAL JOIN booking_agent WHERE (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) AND airline_name = \'{}\' GROUP BY email  ORDER BY sum(price) * 0.1 DESC LIMIT 5"
    cursor.execute(query3.format(airline))
    agents_comm = cursor.fetchall() 
    cursor.close()

    # view the most frequent customer and his/her flights
    cursor = conn.cursor(buffered=True)
    query4 = "SELECT email, name, count(ticket_id) as total FROM ticket NATURAL JOIN purchases as T, customer WHERE airline_name = \'{}\' AND T.customer_email = customer.email AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) GROUP BY email  ORDER BY count(ticket_id) DESC"
    cursor.execute(query4.format(airline))
    mf_customer = cursor.fetchone() 
    cursor.close()
    if mf_customer:
         # view the most frequent customer's flights 
        cursor = conn.cursor()
        query5 = "SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE customer_email = \'{}\' AND airline_name = \'{}\'"
        cursor.execute(query5.format(mf_customer[0], airline))
        c_flights = cursor.fetchall()
        cursor.close() 

    else:
        mf_customer = ('N/A','N/A', 0)
        c_flights = ()

    print("our most frequent customers are  ",mf_customer)  

   
    # view reports of last year
    cursor = conn.cursor()
    query6 = "SELECT month(purchase_date) as month, count(ticket_id) as num FROM purchases NATURAL JOIN ticket WHERE purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE() AND airline_name = \'{}\' GROUP BY month ORDER BY month"
    cursor.execute(query6.format(airline))
    year_sales = cursor.fetchall()
    cursor.close()
    year_sales = [[int(j[0]),int(j[1])] for j in year_sales]
    print("Our last year sale is ", year_sales)
    total_sale_ly = sum([int(i[1]) for i in year_sales])

    # view reports of last month
    cursor = conn.cursor()
    query7 = 'SELECT month(purchase_date) as month, count(ticket_id) as num FROM purchases NATURAL JOIN ticket WHERE purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE() AND airline_name = \'{}\' GROUP BY month ORDER BY month'
    cursor.execute(query7.format(airline))
    month_sales = cursor.fetchall()
    if (month_sales):
        month_sales = int(month_sales[0][1])
    else:
        month_sales = "N/A"
    cursor.close()
  

    # view comparison of revenue for last year
    cursor = conn.cursor()
    query8 = "SELECT sum(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE booking_agent_id is null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) AND airline_name = \'{}\'"
    cursor.execute(query8.format(airline))
    testdata = cursor.fetchone()
    direct = None
    if (testdata is not None):
        direct = testdata[0]
    cursor.close()
    dire = 0
    if direct:
        dire = int(direct)
    else:
        dire = 0
    
    cursor = conn.cursor()
    query9 = "SELECT sum(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE booking_agent_id is not null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) AND airline_name = \'{}\'"
    cursor.execute(query9.format(airline))
    testdata = cursor.fetchone()
    indirect = None
    if (testdata is not None):
        indirect = testdata[0]
    cursor.close()
    idr = 0
    if indirect:
        idr = int(indirect)
    else:
        idr = 0
    
    year_pie = [{"name":"Direct","value":dire},{"name":"Indirect","value":idr}]
    # print(year_pie)
    # print(json.dumps(year_pie))

	# view comparison of revenue for last month
    cursor = conn.cursor()
    query10 = "SELECT sum(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE booking_agent_id is null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE()) AND airline_name = \'{}\'"
    cursor.execute(query10.format(airline))
    testdata = cursor.fetchone()
    m_direct = None
    if (testdata is not None):
        m_direct =testdata[0]
    cursor.close()
    m_dire = 0
    if m_direct:
        m_dire = int(m_direct)
    else:
        m_dire = 0
    m_idr = 0
    cursor = conn.cursor()
    query11 = "SELECT sum(price) FROM flight NATURAL JOIN ticket NATURAL JOIN purchases WHERE booking_agent_id is not null AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE()) AND airline_name = \'{}\'"
    cursor.execute(query11.format(airline))
    testdata = cursor.fetchone()
    m_indirect = None
    if (testdata is not None):
        m_indirect = testdata[0]
    cursor.close()
    m_idr = 0
    if m_indirect:
        m_idr = int(m_indirect)
    else:
        m_idr = 0
    month_pie = [{"name":"Direct","value":m_dire},{"name":"Indirect","value":m_idr}]
   
    # view top 3 destinations over the last 3 months
    cursor = conn.cursor()
    query12 = "SELECT airport_city, count(ticket_id) as num FROM purchases NATURAL JOIN ticket NATURAL JOIN flight, airport WHERE airport_name = arrival_airport AND airline_name = \'{}\' AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 3 MONTH) AND CURRENT_DATE()) GROUP BY airport_city ORDER BY count(ticket_id) DESC LIMIT 3"
    cursor.execute(query12.format(airline))
    m_des = cursor.fetchall()
    cursor.close()

    # view top 3 destinations over the last year
    cursor = conn.cursor()
    query13 = "SELECT airport_city, count(ticket_id) as num FROM purchases NATURAL JOIN ticket NATURAL JOIN flight, airport WHERE airport_name = arrival_airport AND airline_name = \'{}\' AND (purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE()) GROUP BY airport_city ORDER BY count(ticket_id) DESC LIMIT 3"
    cursor.execute(query13.format(airline))
    y_des = cursor.fetchall()
    cursor.close()
 

    return render_template("StaffPage.html",username = username, airline = airline, default_flights = dafault_flights,agents_month = agents_month,agents_year=agents_year,agents_comm=agents_comm,mf_customer=mf_customer,c_flights=c_flights,year_sales =year_sales,total_sale_ly=total_sale_ly,month_sales=month_sales,year_pie=year_pie,month_pie=month_pie,m_des = m_des,y_des=y_des )


@app.route('/ViewFlightsByDates',methods = ["POST"])
def ViewFlightsByDates():
    username = session['username']
    airline = session['airline']
    

    req = json.loads(request.data)
    
    
    start_date = req["datepicker1"]
    
    end_date = req["datepicker2"]
    # Source_City"] = document.getElementById("Source_City").value;
    #             data["Source_Airport"] = document.getElementById("Source_Airport").value;
    #             data["Dest_City"] = document.getElementById("Dest_City").value;
    #             data["Dest_Airport"]
    start_city = req["Source_City"]
    arrive_city = req["Dest_City"]
    start_airport= req["Source_Airport"]
    arrive_airport = req["Dest_Airport"]
    

   
    # query = "SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status FROM flight WHERE airline_name = \'{}\' AND CAST(departure_time AS DATE) BETWEEN \'{}\' AND \'{}\'"
    # cursor.execute(query.format(airline, start_date, end_date))
    # data = cursor.fetchall()
    # cursor.close()
    # print(data)
    ret = []
    if start_date != 'mm/dd/yyyy' and end_date !='mm/dd/yyyy':
        start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y-%m-%d")
        if start_city == '' and arrive_city == '':
            if start_airport == '' and arrive_airport == '':
                
                cursor = conn.cursor()
                query = "SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status FROM flight WHERE airline_name = \'{}\' AND CAST(departure_time AS DATE) BETWEEN \'{}\' AND \'{}\'"
                cursor.execute(query.format(airline, start_date, end_date))
                data = cursor.fetchall() 
                cursor.close()
            else:
               
                cursor = conn.cursor()
                query = "SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status FROM flight WHERE airline_name = \'{}\' AND departure_airport = \'{}\' AND arrival_airport = \'{}\' AND CAST(departure_time AS DATE) BETWEEN \'{}\' AND \'{}\'"
                cursor.execute(query.format(airline, start_airport,arrive_airport,start_date, end_date))
                data = cursor.fetchall() 
                cursor.close()
        else:
            if start_airport == '' and arrive_airport == '':
                cursor = conn.cursor()
                query = "SELECT A.airline_name, A.flight_num, A.departure_airport, A.departure_time, A.arrival_airport, A.arrival_time, A.status FROM flight as A, airport as B, airport as C WHERE A.departure_airport = B.airport_name AND A.arrival_airport = C.airport_name AND A.airline_name = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' AND CAST(A.departure_time AS DATE) BETWEEN \'{}\' AND \'{}\'"
                cursor.execute(query.format(airline, start_city, arrive_city, start_date,end_date))
                data = cursor.fetchall() 
                cursor.close()
            else:
                cursor = conn.cursor()
                query = "SELECT airline_name, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, status FROM flight WHERE airline_name = \'{}\' AND departure_airport = \'{}\' AND arrival_airport = \'{}\'"
                cursor.execute(query.format(airline, start_airport,arrive_airport))
                data = cursor.fetchall() 
                cursor.close()

    else:
        
        
    # if the input is the start and the destination airport  
        if start_city != '' and arrive_city != '':
            if start_airport == '' and arrive_airport == '':
                cursor = conn.cursor()
                query = "SELECT A.airline_name, A.flight_num, A.departure_airport, A.departure_time, A.arrival_airport, A.arrival_time, A.status FROM flight as A, airport as B, airport as C WHERE A.departure_airport = B.airport_name AND A.arrival_airport = C.airport_name AND A.airline_name = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' "
        
                cursor.execute(query.format(airline, start_city, arrive_city))
                data = cursor.fetchall() 
                cursor.close()
            else:
                cursor = conn.cursor()
                query = "SELECT A.airline_name, A.flight_num, A.departure_airport, A.departure_time, A.arrival_airport, A.arrival_time, A.status FROM flight as A, airport as B, airport as C WHERE A.departure_airport = B.airport_name AND A.arrival_airport = C.airport_name AND A.airline_name = \'{}\' AND B.airport_city = \'{}\' AND C.airport_city = \'{}\' AND A.departure_airport = \'{}\' AND A.arrival_airport = \'{}\'"
                cursor.execute(query.format(airline, start_city, arrive_city,start_airport,arrive_airport))
                data = cursor.fetchall() 
                cursor.close()
        # if the user input are the two airport
        else:
            cursor = conn.cursor()
            query = "SELECT ticket_id, airline_name,booking_agent_id,purchase_date FROM ticket NATURAL JOIN purchases NATURAL JOIN flight WHERE booking_agent_id = \'{}\' AND departure_airport = \'{}\' AND arrival_airport = \'{}\' "
            cursor.execute(query.format(username, start_airport, arrive_airport))
            data = cursor.fetchall() 
            cursor.close()
   

    return jsonify(data)


@app.route('/CheckCustomerForFlight', methods = ["POST"])
def CheckCustomerForFlight():
    username = session['username']
    airline = session['airline']

    req = json.loads(request.data)
    data = req[1:-1].split(",")
    flight_num = int(data[1].strip())
   
   
    
    cursor = conn.cursor()
    query = "SELECT airline_name, flight_num,customer_email from purchases NATURAL JOIN ticket WHERE airline_name = \'{}\' AND flight_num = \'{}\'"
    cursor.execute(query.format(airline, flight_num))
    data = cursor.fetchall()
    cursor.close()
    print(data)


    return jsonify(data)
@app.route('/CheckCustomerForFlight_interaction',methods = ["POST"])
def CheckCustomerForFlight_interaction():
    username = session['username']
    airline = session['airline']

    req = json.loads(request.data)
   
    flight_num = req[1]
   
   
    
    cursor = conn.cursor()
    query = "SELECT airline_name, flight_num,customer_email from purchases NATURAL JOIN ticket WHERE airline_name = \'{}\' AND flight_num = \'{}\'"
    cursor.execute(query.format(airline, flight_num))
    data = cursor.fetchall()
    cursor.close()
    print(data)


    return jsonify(data)





@app.route('/AuthorizeNewFlight', methods = ["GET",'POST'])
def AuthorizeNewFlight():
    username = session['username']
    airline = session['airline']
    
    req = json.loads(request.data)
    print(req)
    flight_num = req[0]
    departure_airport = req[1]
    departure_time = req[2]
    departure_time  = datetime.datetime.strptime(departure_time,'%m/%d/%y %H:%M:%S')
    arrival_airport = req[3]
    
    arrival_time = req[4]
    
    arrival_time  = datetime.datetime.strptime(arrival_time,'%m/%d/%y %H:%M:%S')
    price = req[5]
    status = req[6]
    airplane_id = req[7]

    cursor = conn.cursor()
    query = "SELECT * FROM flight WHERE airline_name = \'{}\' AND flight_num = \'{}\' "
    cursor.execute(query.format(airline, flight_num))
    data = cursor.fetchall()
    cursor.close()
    state = None
    if (data): 
	    state = "Oops! This flight has already existed."
    else:
        cursor = conn.cursor()
        query = 'INSERT INTO flight(airline_name,flight_num,departure_airport,departure_time,arrival_airport, arrival_time, price, status, airplane_id) values (\'{}\', \'{}\', \'{}\',\'{}\', \'{}\', \'{}\',\'{}\', \'{}\', \'{}\')'
        cursor.execute(query.format(airline, flight_num, departure_airport, departure_time, arrival_airport, arrival_time, price, status, airplane_id))
        conn.commit()
        cursor.close()
        state = "Successfully Inserted!"

    print(state)
    return jsonify(state)

@app.route('/AuthorizeChangeStatus', methods = ["GET",'POST'])
def AuthorizeChangeStatus():
    username = session['username']
    airline = session['airline']

    req = json.loads(request.data)
    flight_num = req[0]
    status = req[1]
    cursor = conn.cursor()
    query = 'SELECT * FROM flight WHERE airline_name = \'{}\' AND flight_num = \'{}\' '
    cursor.execute(query.format(airline, flight_num))
    data = cursor.fetchall()
    cursor.close()
    state = None
    if (data): 
        cursor = conn.cursor()
        query = 'UPDATE flight SET status = \'{}\' WHERE airline_name = \'{}\' AND flight_num = \'{}\''
        cursor.execute(query.format(status, airline, flight_num))
        conn.commit()
        cursor.close()
        state = "Successfully Updated!"		
    else:
        state = "Oops! No such flight is found in our system."

    print(state)
    return jsonify(state)

@app.route('/AuthorizeAddPlane', methods = ["GET",'POST'])
def AuthorizeAddPlane():
    username = session['username']
    airline = session['airline']

    req = json.loads(request.data)
    airplane_id = req[0]
    seats = req[1]
    cursor = conn.cursor()
    query = 'SELECT * FROM airplane WHERE airline_name = \'{}\' AND airplane_id = \'{}\' '
    cursor.execute(query.format(airline, airplane_id))
    data = cursor.fetchall()
    cursor.close()
    state = None
    if (data): 
	    state = "Oops! This airplane has already existed."
    else:
	    cursor = conn.cursor()
	    query = 'INSERT INTO airplane values (\'{}\', \'{}\', \'{}\')'
	    cursor.execute(query.format(airline, airplane_id, seats))
	    conn.commit()
	    cursor.close()
	    state = "Successfully Inserted!"

    print(state)
    return jsonify(state)

@app.route('/AuthorizeAddAirport', methods = ["GET",'POST'])
def AuthorizeAddAirport():
    username = session['username']
    airline = session['airline']

    req = json.loads(request.data)
    airport_name = req[0]
    airport_city = req[1]
    cursor = conn.cursor()
    query = "SELECT * FROM airport WHERE airport_name = \'{}\'"
    cursor.execute(query.format(airport_name))
    data = cursor.fetchall()
    cursor.close()
    state = None
    if (data): 
	    state = "Oops! This airport has already existed."
    else:
	    cursor = conn.cursor()
	    query = "INSERT INTO airport values (\'{}\', \'{}\')"
	    cursor.execute(query.format(airport_name, airport_city))
	    conn.commit()
	    cursor.close()
	    state = "Successfully Inserted!"

    print(state)
    return jsonify(state)



@app.route("/UpdateReportByDate",methods = ['POST'])
def UpdateReportByDate():
    airline = session['airline']
    req = json.loads(request.data)
    start_date = req['date_start']
    start_date = datetime.datetime.strptime(start_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    end_date = req['date_end']
    end_date = datetime.datetime.strptime(end_date, "%m/%d/%Y").strftime("%Y-%m-%d")
    cursor = conn.cursor()
    query = 'SELECT month(purchase_date) as month, count(ticket_id) as num FROM purchases NATURAL JOIN ticket WHERE airline_name = \'{}\' AND purchase_date BETWEEN \'{}\' AND \'{}\' GROUP BY month ORDER BY month'
    cursor.execute(query.format(airline, start_date, end_date))
    data = cursor.fetchall()
    cursor.close()
    total_sale = 0
    monthly = []
    if (data):
        total_sale = sum([int(i[1]) for i in data ])
        monthly = data



    print(req)
    return (jsonify({'total':total_sale,"monthly":monthly}))

@app.route('/UpdateReportLastYear',methods = ['POST'])
def UpdateReportLastYear():
    req = json.loads(request.data)
    airline = session["airline"]
      # view reports of last year
    cursor = conn.cursor()
    query6 = "SELECT month(purchase_date) as month, count(ticket_id) as num FROM purchases NATURAL JOIN ticket WHERE purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 YEAR) AND CURRENT_DATE() AND airline_name = \'{}\' GROUP BY month ORDER BY month"
    cursor.execute(query6.format(airline))
    year_sales = cursor.fetchall()
    cursor.close()
    year_sales = [[int(j[0]),int(j[1])] for j in year_sales]
    print("Our last year sale is ", year_sales)
    total_sale_ly = sum([int(i[1]) for i in year_sales])
    return (jsonify({'total':total_sale_ly,'monthly':year_sales}))

@app.route('/UpdateReportLastMonth',methods = ['POST'])
def UpdateReportLastMonth():
    # view reports of last month
    cursor = conn.cursor()
    airline = session['airline']
    query7 = 'SELECT month(purchase_date) as month, count(ticket_id) as num FROM purchases NATURAL JOIN ticket WHERE purchase_date BETWEEN DATE_SUB(CURRENT_DATE(),INTERVAL 1 MONTH) AND CURRENT_DATE() AND airline_name = \'{}\' GROUP BY month ORDER BY month'
    cursor.execute(query7.format(airline))
    month_sales = cursor.fetchall()
    total_sale = 0
    if (month_sales):
        total_sale = int(month_sales[0][1])
   
    cursor.close()
    return (jsonify({'total':total_sale,'monthly':month_sales}))
# *****************************************************




@app.route("/HomeDirect")
def HomeDirect():
    try: 
        if (session["airline"]):
            return redirect(url_for('StaffHome'))
    except:
        username = session["username"]
        cursor = conn.cursor()
    #executes query
        query = "SELECT * FROM booking_agent WHERE booking_agent_id = \'{}\' "
        cursor.execute(query.format(username))
    #stores the results in a variable
        data = cursor.fetchone()
        cursor.close()
        if (data):
            return redirect(url_for('AgentHome'))
        else:
            return redirect(url_for('CustomerHome'))



@app.route('/logout')
def logout():
    try:
        session.pop('username')
    except:
        pass
    try:
        session.pop("airline")
    except:
        pass
  
    return redirect('/')

        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
