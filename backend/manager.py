from .consumer import Consumer
from .producer import Producer
import logging
from util.message_utils import Action


class Manager:
    def __init__(self, clock=None):
        self.consumers = []
        self.producers = []
        self.logger = logging.getLogger("src.Manager")

        # The simulated neighbourhood. Calling neighbourhood.now() will get the current time in seconds since
        # simulator start
        self.clock = clock

    # Send out a new weather prediction
    def broadcast_new_prediction(self, prediction):
        for producer in self.producers:
            producer.tell({
                'sender': '',
                'action': Action.broadcast,
                'prediction': prediction
            })

    # Broadcasts new producers so existing consumers can use them
    def broadcast_new_producer(self, producer):
        for consumer in self.consumers:
            consumer.tell({
                'sender': '',
                'action': Action.broadcast,
                'producer': producer
            })

    # Register a new producer. Every consumer should be notified about this producer
    def register_producer(self, producer):
        self.logger.debug("Registering new producer %s", producer)
        self.producers.append(producer)
        self.broadcast_new_producer(producer)

    # Register a new consumer
    def register_consumer(self, consumer):
        self.consumers.append(consumer)
        consumer._actor.request_producer()

    def register_contract(self, contract):
        self.clock.registrer_contract(contract)

    # Input API    
    # A job contains an earliest start time, latest start time and load profile
    # (seconds elapsed and power used)
    # TODO: Load profile should be a data set designed for the optimizer algorithm
    def new_job(self, job):
        consumer_ref = Consumer.start(self.producers, job, self.clock)
        self.register_consumer(consumer_ref)

    # Input API
    # Power rating is the maximum power the PV panels can output given perfect conditions
    # Given in watts
    # Weather predictions will give a float that says how many percent of the maximum the
    # PV panels will produce
    def new_producer(self):
        producer_ref = Producer.start(self)
        self.register_producer(producer_ref)
        self.broadcast_new_producer(producer_ref)

    # Input API
    def new_prediction(self, prediction):
        self.broadcast_new_prediction(prediction)