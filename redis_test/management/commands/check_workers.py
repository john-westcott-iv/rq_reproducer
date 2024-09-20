from django.core.management.base import BaseCommand, CommandError
from redis_test.management.commands.run_worker import MyWorker
from redis_test.redis_client import QUEUE_NAME
from rq import Queue
from redis_test.redis_client import get_configured_redis_client
from redis_test.redis_client import get_configured_redis_client, QUEUE_NAME
from rq import Queue, Worker
from rq.job import Job
from rq.serializers import JSONSerializer
from rq.defaults import (
     DEFAULT_JOB_MONITORING_INTERVAL,
     DEFAULT_RESULT_TTL,
     DEFAULT_WORKER_TTL,
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        client = get_configured_redis_client()
        q = Queue(name=QUEUE_NAME, connection=client)
        w = MyWorker(
            queues=[q],
            name="Test Worker",
            default_result_ttl=DEFAULT_RESULT_TTL,
            connection=client,
            # exc_handler=exc_handler,
            # exception_handlers=exception_handlers,
            default_worker_ttl=DEFAULT_WORKER_TTL,
            job_class=Job,
            queue_class=Queue,
            log_job_description=True,
            job_monitoring_interval=DEFAULT_JOB_MONITORING_INTERVAL,
            disable_default_exception_handler=False,  # noqa: E501
            prepare_for_work=True,
            serializer=None,
        )
        self.stdout.write(f"Workers for queue: {', '.join(w.all(queue=q))}")

