#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.plugins.callback.json import CallbackModule

from celerytask.celeryapp import app


@app.task()
def ansible_adhoc(host_list, module_name, module_args, pattern, play_name=None, passwords=None, forks=5):

    loader = DataLoader()
    variable_manager = VariableManager()
    inventory = Inventory(loader=loader,
                          variable_manager=variable_manager,
                          host_list=host_list)
    variable_manager.set_inventory(inventory)

    Options = namedtuple(
                        'Options',[
                            'remote_user', 'forks', 'become_method', 'become_user', 'listhosts', 'listtasks', 'listtags',
                            'syntax', 'module_path', 'become', 'check', 'verbosity', 'connection', 'private_key_file',
                            'host_key_checking'
                            ]
                        )
    options = Options(remote_user='root', forks=10, become_method='sudo', become_user='root', listhosts=False,
                      listtasks=False, listtags=False, syntax=False, module_path=None, become=True, check=False,
                      verbosity=True, connection='smart', private_key_file=None, host_key_checking=False)

    # variable_manager.extra_vars={"ansible_ssh_user":"root" , "ansible_ssh_pass":"password"}
    passwords = passwords
    play_source = {"name": play_name,
                   "hosts": pattern,
                   "gather_facts": "no",
                   "tasks": [{"action": {"module": module_name, "args": module_args}}]}
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)
    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
            stdout_callback='json',
        )
        result_code = tqm.run(play)

    except Exception as e:
        raise  Exception(e)

    finally:
        if tqm is not None:
            tqm.cleanup()
    return dict(retcode=result_code, results=tqm._stdout_callback.results)

@app.task()
def ansible_playbook(playbook, host_list, module_path, passwords=None):
    loader = DataLoader()
    variable_manager = VariableManager()
    inventory = Inventory(loader=loader,
                          variable_manager=variable_manager,
                          host_list=host_list)
    variable_manager.set_inventory(inventory)

    Options = namedtuple('Options',
                         ['remote_user', 'forks', 'become_method', 'become_user', 'listhosts', 'listtasks', 'listtags',
                          'syntax', 'module_path', 'become', 'check', 'verbosity', 'connection', 'private_key_file',
                          'host_key_checking'])
    options = Options(remote_user='root', forks=10, become_method='sudo', become_user='root', listhosts=False,
                      listtasks=False, listtags=False, syntax=False, module_path=None, become=True, check=False,
                      verbosity=True, connection='smart', private_key_file=None, host_key_checking=False)

    # variable_manager.extra_vars={"ansible_ssh_user":"root" , "ansible_ssh_pass":"password"}
    passwords = passwords
    try:
        pbex = PlaybookExecutor(playbooks=[playbook],
                                inventory=inventory,
                                variable_manager=variable_manager,
                                loader=loader,
                                passwords=passwords,
                                options=options)
        pbex._tqm._stdout_callback = CallbackModule()
        result_code = pbex.run()
        return dict(retcode=result_code, results=pbex._tqm._stdout_callback.results)
    except Exception as e:
        raise Exception(e)
