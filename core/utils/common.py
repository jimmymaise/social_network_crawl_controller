class Common:
    @staticmethod
    def warning_when_retry(self, retry_object, sleep, last_result):
        self.logger.warning(
            'Retrying %s: last_result=%s, retrying in %s seconds...',
            retry_object.fn, last_result, sleep)