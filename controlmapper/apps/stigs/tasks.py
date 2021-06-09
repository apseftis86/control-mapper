from celery import shared_task
from celery.utils.log import get_task_logger
from django.db import transaction
from . import models as benchmark_models
from lxml import etree
import os
logger = get_task_logger(__name__)


# I am not sure I chose the best way to do this.  When looking at some projects I saw that they were
# using transaction.atomic() I am not sure if I should be using this on the saving of other things either
# or if it is even needing to be used here.
@shared_task
def update_benchmark(benchmark_id, data):
    benchmark_data = etree.parse(data).getroot()
    tag = etree.QName(benchmark_data).localname
    if tag == 'Benchmark':
        with transaction.atomic():
            benchmark = benchmark_models.Benchmark.objects.select_for_update().get(id=benchmark_id)
            logger.info('updating benchmark')
            benchmark.update_item(benchmark_data)
    else:
        for component in benchmark_data.getchildren():
            for child in component.getchildren():
                tag = etree.QName(child).localname
                if tag == 'Benchmark':
                    with transaction.atomic():
                        benchmark = benchmark_models.Benchmark.objects.select_for_update().get(id=benchmark_id)
                        logger.info('updating benchmark')
                        benchmark.update_item(child)
                        benchmark.save()
    os.unlink(data)

@shared_task
def save_benchmark(benchmark_id,  data):
    def save_info(benchmark_id, benchmark_data):
        with transaction.atomic():
            benchmark = benchmark_models.Benchmark.objects.select_for_update().get(id=benchmark_id)
            logger.info('Saving benchmark')
            benchmark.save_item(benchmark_data)
            benchmark.upload_completed = True
            benchmark.save()
        return
    benchmark_data = etree.parse(data).getroot()
    tag = etree.QName(benchmark_data).localname
    if tag == 'Benchmark':
        save_info(benchmark_id, benchmark_data)
    else:
        for component in benchmark_data.getchildren():
            for child in component.getchildren():
                tag = etree.QName(child).localname
                if tag == 'Benchmark':
                    save_info(benchmark_id, benchmark_data)
    os.unlink(data)
    return

