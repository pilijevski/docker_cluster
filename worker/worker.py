import pika

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
recv_conn = pika.BlockingConnection(parameters)

recv_channel = recv_conn.channel()
recv_channel.queue_declare(durable=True, queue='request')
recv_channel.exchange_declare(exchange='request', exchange_type='direct')
recv_channel.queue_bind(exchange='request', queue='request')

COUNT = 0
lyrics = ["Hello, it's me,",
"I was wondering if after all these years you'd like to meet",
"To go over everything",
"They say that time's supposed to heal ya",
"But I ain't done much healing",
"Hello, can you hear me?",
"I'm in California dreaming about who we used to be",
"When we were younger and free",
"I've forgotten how it felt before the world fell at our feet",
"There's such a difference between us",
"And a million miles",
"Hello from the other side",
"I must've called a thousand times",
"To tell you I'm sorry",
"For everything that I've done",
"But when I call you never",
"Seem to be home",
"Hello from the outside",
"At least I can say that I've tried",
"To tell you I'm sorry",
"For breaking your heart",
"But it don't matter, it clearly",
"Doesn't tear you apart anymore",
"Hello, how are you?",
"It's so typical of me to talk about myself, I'm sorry",
"I hope that you're well",
"Did you ever make it out of that town",
"Where nothing ever happened?",
"It's no secret",
"That the both of us",
"Are running out of time",
"So hello from the other side (other side)",
"I must've called a thousand times (thousand times)",
"To tell you I'm sorry",
"For everything that I've done",
"But when I call you never",
"Seem to be home",
"Hello from the outside (outside)",
"At least I can say that I've tried (I've tried)",
"To tell you I'm sorry",
"For breaking your heart",
"But it don't matter, it clearly",
"Doesn't tear you apart anymore",
"Oh, anymore",
"Oh, anymore",
"Oh, anymore",
"Anymore",
"Hello from the other side (other side)",
"I must've called a thousand times (thousand times)",
"To tell you I'm sorry",
"For everything that I've done",
"But when I call you never",
"Seem to be home",
"Hello from the outside (outside)",
"At least I can say that I've tried (I've tried)",
"To tell you I'm sorry",
"For breaking your heart",
"But it don't matter, it clearly",
"Doesn't tear you apart anymore"]

def callback(ch, method, _, body):
    print("Worker received a message:")
    print(body)
    ch.basic_ack(delivery_tag=method.delivery_tag)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.exchange_declare('response')
    global COUNT
    message = lyrics[COUNT]
    COUNT += 1
    channel.basic_publish(exchange='response', routing_key='response', body=message)


print(' [*] Waiting for messages. To exit press CTRL+C')
recv_channel.basic_consume('request', callback)
recv_channel.start_consuming()
