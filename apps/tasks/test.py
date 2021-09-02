# _*_ coding: utf-8 _*_
# _*_ author_by zn _*_

from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from collections import namedtuple
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.utils.sentinel import Sentinel
from ansible import context
from optparse import Values

from ansible.plugins.callback import CallbackBase


# InventoryManager类
loader = DataLoader()
inventory = InventoryManager(loader=loader, sources=['/tmp/hosts'])

# VariableManager类
VariableManager(loader=loader, inventory=inventory)
variable_manager = VariableManager(loader=loader, inventory=inventory)
extra_vars = {'ansible_ssh_port': '30022'}
variable_manager._extra_vars = extra_vars


# options
Options = {'verbosity': 0, 'connection': 'smart', 'remote_user': None}
options = Values(Options)


# play 执行对象和模块
play_source = dict(
    name='Ansible Play ad-hoc test',
    hosts='10.5.17.95',
    gather_facts='yes',
    tasks=[
        dict(action=dict(module='shell', args='touch /tmp/ad-hoc.test1'))
    ]
)

# print(play_source)

context._init_global_context(options)

play = Play.load(play_source, variable_manager=variable_manager, loader=loader)


class HocResultsCollector(CallbackBase):
    """
    重新CallbackBase
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

    def v2_runner_on_skipped(self, result):
        pass

    def v2_playbook_on_stats(self, stats):
        pass


callback = HocResultsCollector()


passwords = dict()
tqm = TaskQueueManager(
    inventory=inventory,
    variable_manager=variable_manager,
    loader=loader,
    passwords=passwords,
    stdout_callback=callback
)

# tqm.run(play)
result = tqm.run(play)

result_raw = {'success': {}, 'failed': {}, 'unreachable': {}}

# print(callback.host_unreachable.items())
# print(callback.host_ok.items())

for host, result in callback.host_unreachable.items():
    result_raw['unreachable'][host] = result._result
    print(result_raw)

# for host, result in callback.host_ok.items():
#     result_raw['success'][host] = result._result
#     result_data.append(result_raw)
# for host, result in callback.host_failed.items():
#     result_raw['failed'][host] = result._result
#     result_data.append(result_raw)
