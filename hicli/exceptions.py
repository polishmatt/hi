class HiException(Exception):

    class_message = "Failed"

    def __str__(self):
        return "%s: %s" % (self.class_message, super(HiException, self).__str__())


class InvalidConfigException(HiException):

    class_message = "Invalid config"
