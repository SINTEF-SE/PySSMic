from backend.consumer import Consumer
from backend.models.job import Job
from tests.mocks import MockManager


def test_create_grid_contract():
    manager = MockManager()
    job = Job(id="job_id", est=0, lst=0, load_profile=None)
    consumer = Consumer(producers=[], job=job, manager=manager)

    expected = dict(id="grid;job_id;0", time=0, time_of_agreement=0, load_profile=None,
                    job_id="job_id", producer_id="grid")
    actual = consumer.create_grid_contract()

    assert actual == expected