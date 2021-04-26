import pika
import psycopg2
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

#channel.queue_declare(queue='rpc_queue')
channel.queue_declare(queue='city_queue')
channel.queue_declare(queue='cit_queue')

def connect(n):
    
    #q = "\""+n1+"\""
    #print(q)
    con = psycopg2.connect(database="restras", user="postgres", password="zoyo", host="127.0.0.1", port="5432")
       
    cur = con.cursor()
    cur.execute(n)
    rows = cur.fetchall()
    con.close()
    return rows

def insert(n):
    
    #q = "\""+n1+"\""
    #print(q)
    con = psycopg2.connect(database="restras", user="postgres", password="zoyo", host="127.0.0.1", port="5432")
       
    cur = con.cursor()
    cur.execute(n)
    con.commit()
    
    con.close()
    return True

def city_request(ch, method, props, body):
    n = str(body)
    #set query
    n1 = n[2:].strip(" '")
    n1 = "select hotel_name,city_name,type from hotel where city_name =\'"+n1+"\'"
    #print(n1)
    response = connect(n1)

    
    print("Query Processed......")    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

def cit_request(ch, method, props, body):
    n = body
    #set query
    n1 = n.decode()
    n1 = n1.split(", ")
    hotel_name = n1[0]
    date = n1[1]
    seat_required = int(n1[2])
    q = "select no_of_seats from booking_history where hotel_name = \'" + hotel_name + "\' and booking_date = \'" + date + "\'"
    response =connect(q)
    seat_limit = "select s_limit from hotel where hotel_name = \'"+hotel_name+"\'"
    response1 =  connect(seat_limit)
    seat_limit = int(response1[0][0])
    if response == []:
    
        if seat_limit >= seat_required:
            #rem_seats = seat_limit-seat_required       
            #q ="insert into availability values(\'"+hotel_name+"\',\'"+date+ "\',"+str(rem_seats) +")"
            #response=insert(q)
            q = "insert into booking_history values(\'"+hotel_name+"\',\'"+date+ "\',"+str(seat_required) +")"#seat_req
            response=insert(q)
            to_send = "success"
            # add entry in booking history
            # add (hotel_name, date, seat_limit-seat_required) in availability
        
        else:
            to_send = str(seat_limit)        
        
    else:
        already_booked = int(response[0][0])
        seats_available = seat_limit - already_booked#booked seats
        if seat_required <= seats_available:
            rem_seats = already_booked + seat_required
            q = "update booking_history set no_of_seats ="+str(rem_seats)+" where hotel_name = \'" + hotel_name + "\' and booking_date = \'" + date + "\'"
            response = insert(q)
            #q = "insert into booking_history values(\'"+hotel_name+"\',\'"+date+ "\',"+str(seat_required) +")"
            #response=insert(q)
            to_send = "success"
        else:
            to_send = str(seats_available)
    
    print("Query Processed......")    
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id = \
                                                         props.correlation_id),
                     body=str(to_send))
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='city_queue', on_message_callback=city_request)
#add sameline

channel.basic_consume(queue='cit_queue', on_message_callback=cit_request)

channel.start_consuming()
