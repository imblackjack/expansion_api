# _*_ coding: utf-8 _*_
# _*_ author_by zn _*_


from ansible.plugins.callback import CallbackBase


class HocResultsCollector(CallbackBase):
    """
    重写CallbackBase
    """
    def __init__(self, *args, **kwargs):
        super(HocResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        self.host_unreachable[host] = result

    def v2_runner_on_ok(self, result):
        host = result._host.get_name()
        self.host_ok[host] = result

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        self.host_failed[host] = result


class PlayResultsCollector(CallbackBase):
    """
    重写CallbackBase
    """
    def __init__(self, *args, **kwargs):
        super(PlayResultsCollector, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        self.host_unreachable[host] = result

    def v2_runner_on_ok(self, result):
        host = result._host.get_name()
        self.host_ok[host] = result

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        self.host_failed[host] = result
