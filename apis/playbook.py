# _*_ coding: utf-8 _*_
# _*_ author_by zn _*_


from ansible.parsing.dataloader import DataLoader
from ansible.inventory.manager import InventoryManager
from ansible.vars.manager import VariableManager
from collections import namedtuple
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.module_utils.common.collections import ImmutableDict
from ansible.utils.sentinel import Sentinel
from ansible import context
from optparse import Values
from apis import callback


class PlayBookApi(object):
    def __init__(self, playbook_path, hosts):

        # 初始化参数
        self.connection = 'smart'
        self.remote_user = 'root'
        self.verbosity = 0
        self.syntax = None
        self.start_at_task = None

        # InventoryManager类
        self.loader = DataLoader()

        self.hosts = hosts
        # print(",".join(hosts) + ',')
        self.inventory = InventoryManager(loader=self.loader, sources=",".join(hosts) + ',')
        # print(self.inventory)
        print(self.inventory.get_groups_dict())

        self.playbook_path = playbook_path
        # self.inventory = InventoryManager(loader=self.loader, sources=['/tmp/hosts'])
        # self.inventory = InventoryManager(loader=self.loader, sources=",".join(["10.5.17.95", "1.1.1.1"]))



        # VariableManager类)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)

        extra_vars_map = {}
        self.extra_vars = extra_vars_map
        self.variable_manager._extra_vars = self.extra_vars

        # # options
        # self.options = {'verbosity': 0, 'connection': 'smart', 'remote_user': None}
        # self.ops = Values(self.options)

        # callback
        self.results_callback = callback.PlayResultsCollector()

        context.CLIARGS = ImmutableDict(
            connection=self.connection,
            remote_user=self.remote_user,
            verbosity=self.verbosity,
            syntax=self.syntax,
            start_at_task=self.start_at_task
        )

    def playbookrun(self):
        # context._init_global_context(self.ops)

        passwords = dict()

        playbook = PlaybookExecutor(playbooks=self.playbook_path,
                                    inventory=self.inventory,
                                    variable_manager=self.variable_manager,
                                    loader=self.loader, passwords=passwords)

        playbook._tqm._stdout_callback = self.results_callback

        playbook.run()

        results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.results_callback.host_ok.items():
            results_raw['success'][host] = result._result
        for host, result in self.results_callback.host_failed.items():
            results_raw['failed'][host] = result._result
        for host, result in self.results_callback.host_unreachable.items():
            results_raw['unreachable'][host] = result._result

        return results_raw


"""
print(callback.host_unreachable.items())
print(callback.host_ok.items())
for host, result in callback.host_ok.items():
    result_raw['success'][host] = result._result
    result_data.append(result_raw)
for host, result in callback.host_failed.items():
    result_raw['failed'][host] = result._result
    result_data.append(result_raw)
"""

