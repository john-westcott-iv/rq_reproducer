from django.core.management.base import BaseCommand, CommandError
from redis_test.redis_client import get_configured_redis_client, QUEUE_NAME
from rq import Queue, Worker
from rq.job import Job
from rq.serializers import JSONSerializer
from rq.defaults import (
    DEFAULT_JOB_MONITORING_INTERVAL,
    DEFAULT_RESULT_TTL,
    DEFAULT_WORKER_TTL,
)


class MyWorker(Worker):
    def _set_connection(self, connection):
        try:
            connection_pool = connection.connection_pool
            current_socket_timeout = connection_pool.connection_kwargs.get(
                "socket_timeout"
            )
            if current_socket_timeout is None:
                timeout_config = {"socket_timeout": self.connection_timeout}
                connection_pool.connection_kwargs.update(timeout_config)
        except AttributeError:
            nodes = connection.get_nodes()
            for node in nodes:
                connection_pool = node.redis_connection.connection_pool
                current_socket_timeout = connection_pool.connection_kwargs.get(
                    "socket_timeout"
                )
                if current_socket_timeout is None:
                    timeout_config = {
                        "socket_timeout": self.connection_timeout
                    }
                    connection_pool.connection_kwargs.update(timeout_config)
        return connection


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write("Getting Redis client...")
        client = get_configured_redis_client()

        self.stdout.write("Creating queue...")
        q = Queue(connection=client, name=QUEUE_NAME)

        self.stdout.write("Done")

        self.stdout.write("Starting a worker...")
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
        w.work()

        self.stdout.write("Done")

