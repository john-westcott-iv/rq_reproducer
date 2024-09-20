import yaml
from ansible_base.lib.redis.client import get_redis_client

QUEUE_NAME = 'Johns Queue'

cert_location = '/home/ansible/aap/redis'
ca_cert = '/home/ansible/aap/tls/ca.cert'
#redis_user = "eda"
#redis_pass = "2b374566f3838467169a2623ea10c251fc5616daf219440d4a13f1579163fbc9"
extra_settings_file = '/home/ansible/aap/eda/etc/settings.yaml'

def get_configured_redis_client():
    try:
        with open(extra_settings_file, 'r') as stream:
            extra_data = yaml.safe_load(stream)
    except Exception as e:
        print(f"Failed to load {extra_settings_file}: {e}")
        raise e

    return get_redis_client(
        #f'rediss://{redis_user}:{redis_pass}@localhost:6380',
        f'rediss://localhost:6380',
        ssl_certfile=f'{cert_location}/server.crt',
        ssl_keyfile=f'{cert_location}/server.key',
        ssl_ca_certs=ca_cert,
        mode='cluster',
        redis_hosts=extra_data['MQ_REDIS_HA_CLUSTER_HOSTS'],
        ssl=True,
        ssl_check_hostname=False,
        socket_keepalive=True,
        socket_timeout=150,
        socket_connect_timeout=10,
        cluster_error_retry_attempts=3,
    )
