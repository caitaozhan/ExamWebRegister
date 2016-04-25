class MainInfoLack(Exception):
    def __init__(self, info):
        Exception.__init__(self)
        self.errorInfo = info

    def __str__(self):
        return "重要信息缺失: %s" % self.errorInfo
