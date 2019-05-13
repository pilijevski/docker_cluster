from database_helper import Database
import pika
import sys
import _thread


db = Database('postgresql+psycopg2', 'postgres', 'password', 'localhost', '5432', 'postgres_db')
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)
recv_conn = pika.BlockingConnection(parameters)

recv_channel = recv_conn.channel()
recv_channel.queue_declare(durable=True, queue='response')
recv_channel.exchange_declare(exchange='response', exchange_type='direct')
recv_channel.queue_bind(exchange='response', queue='response')


def callback(ch, method, _, body):
    print("Adele:",body.decode(),"\nMe: ")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def send_message(_message):
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare('request')
    channel.basic_publish(exchange='request', routing_key='request', body=_message)


def start_app(parameters):
    while True:
        command = input("Enter command [database] [rabbitmq] [exit]\n ")

        if command == "database":
            while True:
                subcommand = input("Enter database command: [back] [insert] [read]\n")

                if subcommand == "insert":
                    name = input('Enter name:\n')
                    mail = input('Enter email:\n')
                    city = input('Enter city\n')
                    phone = input('enter phone\n')
                    db.add_user(name, mail, city, phone)

                if subcommand == "read":
                    sub_subcommand = input("Enter id or 'all'\n")
                    if sub_subcommand == 'all':
                        db.read_users()
                    else:
                        db.read_user(subcommand)

                if subcommand == 'back':
                    break

        if command == "rabbitmq":
            print("Enter message to talk to the other side! [back] to go back\n")
            while True:
                message = input("")
                if message == 'back':
                    break
                else:
                    send_message(message)
        if command == "exit":
            sys.exit(1)


_thread.start_new_thread(start_app, (parameters,))
recv_channel.basic_qos(prefetch_count=3)

print(' [*] Waiting for messages. To exit press CTRL+C\n')
recv_channel.basic_consume(callback, 'response')
recv_channel.start_consuming()
