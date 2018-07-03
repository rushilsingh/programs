"""    
{
    "ThreadName": [func, (args), {kwargs}],
    "AnotherThread": [otherfunc, (otherargs), {other_kw}]
}
"""
from custom_thread import CustomThread
from time import sleep


def func(*args, **kwargs):
    """ Simple function just prints and returns arguments it was called with 
        If it is passed a key word argument 'error' with value True, it raises an exception 
    """

    print "I was called with args = {0} and kwargs = {1}".format(args, kwargs)

    if "error" in kwargs:
        if kwargs["error"] == True:
            raise Exception("I raise exception if boolean error is True")

    return (args, kwargs)


mappings = {
    "Thread A": [func, (1, 2, 3), {"error": False}],
    "Thread B": [func, (0,), {"key": "value"}]
}


mappings_error = {
    "Thread C": [func, (4, 5), {"name": "John"}],
    "Thread E": [func, (6, 7, 8), {"error": True}]
}


class Pool(object):
    """ Pool object manages a group of threads """

    def __init__(self, func_bind, number=10, *args, **kwargs):
        """ Either dictionary or function is passed as func_bind.
            Threads are created and stored in a dictionary with their names as keys
        """
    
        self.threads = {}
        if type(func_bind) is dict:
            for tname, func_ref in func_bind.iteritems():
                func_name, func_args, func_kwargs = func_ref
                t = CustomThread(name=tname, target=func_name,
                                 args=func_args, kwargs=func_kwargs)
                self.threads[tname] = t
        else:
            for i in xrange(number):
                t = CustomThread(target=func_bind, args=args, kwargs=kwargs)
                self.threads[t.getName()] = t

    def start(self):
        """ Start all threads in pool """

        for t in self.threads.values():
            t.start()

    def isCompleted(self):
        """ Return True if all threads have completed. Otherwise, check every 20 seconds.
            If any thread is still incomplete after 2 minutes, return False to indicate timeout
        """

        sleep_count = 0
        all_completed = True

        while sleep_count <= 10:
            for t in self.threads.values():  # Check all threads for completion
                if not t.isCompleted:
                    all_completed = False
                    break

            if all_completed:
                return True
            else:  # Sleep for 20 seconds and increment sleep_count by 1
                sleep(20)
                sleep_count += 1

        return False  # Timeout
