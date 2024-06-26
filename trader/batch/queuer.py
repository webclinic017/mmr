from redis import Redis
from rq import Queue
from rq.job import Job
from trader.common.logging_helper import setup_logging
from typing import Callable, cast, Dict, List, Optional, Union


logging = setup_logging(module_name='queuer')

class Queuer():
    def __init__(self,
                 redis_queue: str = '',
                 redis_server_address: str = '127.0.0.1',
                 redis_server_port: int = 6379):
        self.redis_conn = Redis(host=redis_server_address, port=redis_server_port)
        self.redis_queue = redis_queue
        self.rq = Queue(self.redis_queue, connection=self.redis_conn)
        self.redis_server_address = redis_server_address
        self.redis_server_port = redis_server_port
        self.jobs_cache: Dict[str, bool] = {}

    def args_id(self, args):
        str_hash = ''
        for a in args:  # type: ignore
            str_hash += str(a)
        return str_hash

    def job_id(self, job):
        return self.args_id(job.args)

    def current_queue(self) -> Dict[str, bool]:
        if len(self.jobs_cache) > 0:
            return self.jobs_cache
        else:
            for job in self.rq.jobs:
                self.jobs_cache[self.job_id(job)] = True
            return self.jobs_cache

    def refresh_queue(self) -> Dict[str, bool]:
        self.jobs_cache = {}
        return self.current_queue()

    def get_job(self, job_id: str) -> Optional[Job]:
        for job in self.rq.jobs:
            if job.id == job_id:
                return job
        return None

    def drain_queue(self):
        self.jobs_cache = {}
        self.rq.empty()

    def is_job_queued(self, job_or_id: Union[Job, str], force_refresh=False):
        if force_refresh:
            self.refresh_queue()

        if type(job_or_id) is str:
            return self.args_id(job_or_id) in self.current_queue()
        else:
            return self.job_id(job_or_id) in self.current_queue()

    def enqueue(self, func: Callable, args: List) -> Job:
        job_id = self.args_id(args)
        job = cast(Job, self.rq.enqueue(func, job_id=job_id, *args))
        job.save()
        self.jobs_cache[job_id] = True
        logging.debug('{} {} {} {}'.format(self.redis_queue, self.redis_conn, self.redis_server_address, self.redis_server_port))
        return job
