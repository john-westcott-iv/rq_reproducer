1. Create a venv and `pip install -r requirements.txt`.
1. `./manage.py run_worker` - This will start a worker in your current shell connected to a queue in redis.
1. In a seperate window: `./manage.py enqueue_message` - This will push a message into the queue that the worker will pick up. The worker is not fully functional to it will raise an exception but keep going.
1. Run `./manage.py check_workers` - This will show you that redis knows there is a worker connected to the queue.
1. Down the primary Redis node - You will see the worker get an exception and then attempt to reconnect.
1. Run `./manage.py enqueue_message` - You will see the worker pickup the message and raise another exception like the first.
1. Run `./manage.py check_workers` - This will now show no workers attached to the queue.
