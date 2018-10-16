from threading import Thread


class CustomThread(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        """ Constructor is always called with keyword args
            Additional boolean attribute isCompleted initially set to False
        """

        super(CustomThread, self).__init__(
            group, target, name, args, kwargs, verbose)
        self.isCompleted = False

    def run(self):
        """ Additional boolean attribute isCompleted set to True if thread executes target successfully """

        super(CustomThread, self).run()
        self.isCompleted = True
