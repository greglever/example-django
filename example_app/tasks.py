from __future__ import absolute_import
import time
import logging

from django.conf import settings
from celery import shared_task
from celery.exceptions import MaxRetriesExceededError

from example_app.celery import app


import celery
import logging


class UnexpectedException(Exception):
    pass


class ExpectedException(Exception):
    pass


class BaseTask(celery.Task):
    """Abstract base class for all CIP API tasks"""

    abstract = True

    SOME_CLASS_VARIABLE = 'some class variable'

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry at retry."""
        super(BaseTask, self).on_retry(exc, task_id, args, kwargs, einfo)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        msg_tmp = """
        Task with task_id: {task_id}, args: {task_args}, kwargs: {task_kwargs} failed with exception of type: {exc_type}
        """
        # logging.info("**************  TASK FAILURE !!!  *****************")
        logging.warning(
            msg=msg_tmp.format(
                task_id=task_id, task_args=args, task_kwargs=kwargs, exc_type=type(exc)
            )
        )

        if isinstance(exc, ExpectedException):
            logging.info("exc: {exc} of type: {exc_type}".format(exc=exc, exc_type=type(exc)))
        elif isinstance(exc, UnexpectedException):
            logging.info("exc: {exc} of type: {exc_type}".format(exc=exc, exc_type=type(exc)))
        super(BaseTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """Log the exceptions to sentry."""
        super(BaseTask, self).after_return(status, retval, task_id, args, kwargs, einfo)


@app.task(
    throws=(ExpectedException, UnexpectedException),
    autoretry_for=(ExpectedException,),
    # retry_backoff=True,
    # retry_jitter=True,
    retry_kwargs={'max_retries': 2, 'countdown': 1},
    base=BaseTask,
    bind=True,
)
def decorated_autoretry(self, first_arg, second_arg, opt_arg=None):
    # logging.info(decorated_autoretry.request.retries == 2)
    # logging.info("=====================================")
    # logging.info(decorated_autoretry.max_retries)
    # logging.info(decorated_autoretry.retry_kwargs)
    # logging.info("=====================================")
    # decorated_autoretry.retry(max_retries=2, countdown=1, exc=ExpectedException)
    # if decorated_autoretry.request.retries == 2:
    #     decorated_autoretry.request.retries = 0
    logging.info("first_arg: {first_arg}, second_arg: {second_arg}".format(first_arg=first_arg, second_arg=second_arg))
    logging.info(
        "Attempt: {attempt} of {attempts}".format(
            attempt=decorated_autoretry.request.retries+1, attempts=decorated_autoretry.max_retries
        )
    )
    logging.info("UnexpectedException about to be raised...")
    logging.info("Optional Argument: {opt_arg}".format(opt_arg=opt_arg))
    logging.info(decorated_autoretry.request.kwargs)
    # This allows us to add arguments to kwargs before a retry is made
    decorated_autoretry.request.kwargs['opt_arg'] = 'SOMETHING'
    # decorated_autoretry.retry(countdown=1)
    # raise UnexpectedException

    logging.info(msg="Acessing self.SOME_CLASS_VARIABLE... {res}".format(
        res=self.SOME_CLASS_VARIABLE
    ))

    raise ExpectedException


@app.task
def explicit_autoretry():
    logging.info(
        "Attempt: {attempt} of {attempts}".format(
            attempt=explicit_autoretry.request.retries+1, attempts=explicit_autoretry.max_retries
        )
    )
    try:
        raise ExpectedException
    except ExpectedException as e:
        logging.info(msg="Received exception of type: {e_type}".format(e_type=type(e)))
        try:
            explicit_autoretry.retry(countdown=1)
        except MaxRetriesExceededError as e:
            logging.info(msg="Received exception of type: {e_type}".format(e_type=type(e)))


@shared_task
def task_to_run_in_background(parameter):
    for value in range(10):
        logging.info(
            msg="{parameter} for time {value}".format(
                parameter=parameter, value=value
            )
        )
        time.sleep(1)
