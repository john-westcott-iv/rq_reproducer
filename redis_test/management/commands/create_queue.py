from django.core.management.base import BaseCommand, CommandError
from redis_test.redis_client import get_configured_redis_client, QUEUE_NAME
from ansible_base.lib.redis.client import get_redis_client
from rq import Queue


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            client = get_configured_redis_client()
        except Exception as e:
            raise CommandError(e)
        
        
        self.stdout.write("Creating queue...")
        try:
            q = Queue(connection=client, name=QUEUE_NAME)
        except Exception as e:
            raise CommandError(e)
        
        self.stdout.write("Done")
