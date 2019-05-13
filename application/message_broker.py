import pika


class MessageBroker:

    def __init__(self, host='', port='', user='', password=''):
        """Initialize the connection information
          :param user: username name
          :param password: username password
          :param host: host name
          :param port: host port number
      """

        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.channel = None
        self.queues = list()

    def connect(self):
        """ Connect to Message Broker"""
        pass

    def close(self):
        """ Close the connection to Message Broker"""
        pass

    def send(self, message, exchange, queue=""):
        pass

    def receive(self):
        pass


class RabbitMQ(MessageBroker):
    """ RabbitMQ Helper class for connecting to RabbitMQ server,
        implements MessageBroker class
        :param connect(): Connect to RabbitMQ server
        :param queue_declare(): Declare queues
    """

    def connect(self):
        """ Connect to RabbitMQ server using credentials, then connect to a channel
        """
        if not self.conn or self.conn.is_closed:
            try:
                print('Connecting to RabbitMQ')
                credentials = pika.PlainCredentials(self.user, self.password)
                parameters = pika.ConnectionParameters(self.host, int(self.port), '/', credentials)
                self.conn = pika.BlockingConnection(parameters)
            except Exception as err:
                print(err)
                raise err

    def reconnect(self):
        if self.conn or not self.conn.is_closed:
            self.connect()
            self.create_channel()
            for queue in self.queues:
                self.declare_queue(queue)

    def create_channel(self):
        print('Connected. Creating channel.')
        self.channel = self.conn.channel()
        print('Channel created.')

    def declare_queue(self, queue):
        print('Declaring queue')
        if self.channel is None:
            self.reconnect()
        self.queues.append(queue)
        self.channel.queue_declare(durable=True, queue=queue)
        print('Queue' + queue + ' declared')

    def declare_exchange(self, exchange):
        self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')

    def bind_queue(self, exchange, queue):
        self.channel.queue_bind(exchange=exchange, queue=queue)

    def _publish(self, message, exchange, queue=''):
        self.channel.basic_publish(exchange=exchange, routing_key=queue, body=message,
                                   properties=pika.BasicProperties(delivery_mode=2))

    def send(self, message, exchange, queue=""):
        """ Send a message to the RabbitMQ broker on a specified queue
        :param exchange: Exchange
        :param message: Message to be sent
        :param queue: Queue for the message
        """
        print("Sending message to broker")

        try:
            self._publish(message, exchange, queue=queue)
            print("Message sent")
        except pika.exceptions.ConnectionClosed:
            print(pika.exceptions.ConnectionClosed)
            print('reconnecting to queue')
            self.reconnect()
            self._publish(message, exchange, queue)

    def set_consume(self, callback, queue):
        """ Start consuming messages from the initialized channel using the
            receive callback function
            :type queue: string
            :type callback: function"""
        print('Declaring consumer')
        self.channel.basic_qos(prefetch_count=10)
        self.channel.basic_consume(callback, queue=queue)
        print('Start consuming')

    def start_consuming(self):
        self.channel.start_consuming()

    def close(self):
        if self.conn and self.conn.is_open:
            logging.debug('Closing queue connection')
            self.conn.close()
