import threading
from threading import Lock
from typing import Dict

from src.aux.logger import Logger


class Singleton(type):
    """
    A metaclass that creates a Singleton base class when called. This is a thread-safe implementation of Singleton.

    This metaclass has been further customized to allow Singletons within Singletons, by implementing a double-lock
    check mechanism (https://stackoverflow.com/a/59476524).

    A metaclass is the class of a class; that is, a class is an instance of its metaclass. You find the metaclass of
    an object in Python with type(obj). Normal new-style classes are of type type. Logger in the code above will be
    of type class 'your_module.Singleton', just as the (only) instance of Logger will be of type class
    'your_module.Logger'. When you call logger with Logger(), Python first asks the metaclass of Logger, Singleton,
    what to do, allowing instance creation to be pre-empted. This process is the same as Python asking a class what
    to do by calling __getattr__ when you reference one of it's attributes by doing myclass.attribute.

    A metaclass essentially decides what the definition of a class means and how to implement that definition. See
    for example http://code.activestate.com/recipes/498149/, which essentially recreates C-style structs in Python
    using metaclasses. The thread What are some (concrete) use-cases for metaclasses? also provides some examples,
    they generally seem to be related to declarative programming, especially as used in ORMs.

    In general, it makes sense to use a metaclass to implement a singleton. A singleton is special because is
    created only once, and a metaclass is the way you customize the creation of a class. Using a metaclass gives you
    more control in case you need to customize the singleton class definitions in other ways.

    Your singletons won't need multiple inheritance (because the metaclass is not a base class), but for subclasses
    ofthe created class that use multiple inheritance, you need to make sure the singleton class is the
    first / leftmost one with a metaclass that redefines __call__ This is very unlikely to be an issue. The instance
    dict is not in the instance's namespace so it won't accidentally overwrite it.

    You will also hear that the singleton pattern violates the "Single Responsibility Principle" -- each class
    should do only one thing. That way you don't have to worry about messing up one thing the code does if you need
    to change another, because they are separate and encapsulated. The metaclass implementation passes this test.
    The metaclass is responsible for enforcing the pattern and the created class and subclasses need not be aware
    that they are singletons.

    https://refactoring.guru/design-patterns/singleton/python/example#example-1
    https://stackoverflow.com/a/6798042
    """

    _logger = Logger("Singleton")

    _instances: Dict = {}
    _instance_locks: Dict = {}
    _singleton_lock: Lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        # double-checked locking pattern
        cls._logger.trace("Inside __call__ of Singleton...")
        cls._logger.trace(f"Called By {cls}...")
        if cls not in cls._instances:
            cls._logger.trace("Trying to get lock...")
            with cls._singleton_lock:
                lock = cls._instance_locks.setdefault(cls, threading.Lock())
            with lock:
                cls._logger.trace("Got lock...")
                if cls not in cls._instances:
                    cls._logger.trace(f"Object of type {cls} being created...")
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
                    with cls._singleton_lock:
                        del cls._instance_locks[cls]
        cls._logger.trace(f"Returning created Instance {cls}")
        return cls._instances[cls]
