import asyncio
from asyncio import Task


class Scheduler:
    """
    Simple Python pattern to schedule non-blocking tasks that run periodically.

    Python 3.7 makes asynchronous programming in Python a bit smoother and more accessible than previous releases. In
    particular, I like using Tasks, which are a subclass of Futures (which are themselves analogous to Promises in
    Javascript). In most cases, you do not need to use Futures but can instead just work with coroutines and Tasks
    through a higher-level API.
    Tasks are coroutine schedulers. Coroutines are subroutines except they allow execution to be suspended and then
    resumed. You can wrap a coroutine in a Task and it will schedule it for execution as soon as possible. We will use
    Tasks and coroutines to run something in the background periodically, inspired by the setInterval method in
    Javascript.

    https://phoolish-philomath.com/asynchronous-task-scheduling-in-python.html
    """

    @staticmethod
    async def _run_periodically(wait_time, func, *args):
        """
        Helper for schedule_task_periodically.

        Wraps a function in a coroutine that will run the given function indefinitely.

        :param wait_time: seconds to wait between iterations of func
        :param func: the function that will be run
        :param args: any args that need to be provided to func
        """
        while True:
            func(*args)
            await asyncio.sleep(wait_time)

    @staticmethod
    def schedule_task_periodically(wait_time, func, *args) -> Task:
        """
        Schedule a function to run periodically as an asyncio.Task

        :param wait_time: interval (in seconds)
        :param func: the function that will be run
        :param args: any args needed to be provided to func

        :return: an asyncio Task that has been scheduled to run
        """
        return asyncio.get_event_loop().create_task(Scheduler._run_periodically(wait_time, func, *args))

    @staticmethod
    async def cancel_scheduled_task(task: Task):
        """
        Gracefully cancels a task.

        :type task: asyncio.Task
        """
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass
