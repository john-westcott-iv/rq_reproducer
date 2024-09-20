from django.core.management.base import BaseCommand, CommandError
from redis_test.redis_client import get_configured_redis_client, QUEUE_NAME
from redis_test.redis_action import count_words_at_url
from ansible_base.lib.redis.client import get_redis_client
from rq import Queue
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        client = get_configured_redis_client()
        self.stdout.write("Creating queue...")
        q = Queue(connection=client, name=QUEUE_NAME)
        q.enqueue(count_words_at_url, str(datetime.datetime.now()))
        self.stdout.write("Done")
