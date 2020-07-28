import click

from skale.utils.helper import get_abi
from skale.utils.abi_utils import get_contract_address_by_name, get_contract_abi_by_name
from skale.contracts.base_contract import BaseContract, transaction_method


from cli.manager_client import ManagerClient

from cli.config import ENDPOINT, ABI_FILEPATH, ETH_PRIVATE_KEY, LEDGER, TM_URL
from cli.config import ENDPOINT, ABI_FILEPATH, ETH_PRIVATE_KEY, LEDGER, TM_URL, USE_CALLS
from cli.manager_client import init_contract_names

ABI = get_abi(ABI_FILEPATH)


def generate_cmd(contract_name, fn):
    function_name = fn['name']
    params = []

    for input_variable in fn['inputs']:
        if not input_variable.get('components'):

            if input_variable["name"] != "":
                opt_name = f'--{input_variable["name"]}'
                name = input_variable["name"]
            else:
                opt_name = '--option'
                name = 'no name'
            opt = click.Option((opt_name,), prompt=f'Name: {name}, type: {input_variable["type"]}')
            params.append(opt)

    @click.pass_context
    def callback(*args, **kwargs):
        if not ENDPOINT:
            print('Set ENDPOINT option to the environment')
            exit(1)
        mc = ManagerClient(ENDPOINT, ABI)
        is_call = fn['stateMutability'] == 'view' or USE_CALLS


        if not is_call and not (ETH_PRIVATE_KEY or LEDGER or TM_URL):
            print('To execute transactions you should set ETH_PRIVATE_KEY/LEDGER/TM_URL')
            exit(1)

        res = mc.run_func(contract_name, function_name, is_call, kwargs)

        print(f'TRANSACTION_RESULT:{res}')
    return click.Command(function_name, params=params, callback=callback)


def init_groups():
    groups = []
    contract_names = init_contract_names(ABI)
    for contract_name in contract_names:
        group = click.Group(name=f'{contract_name}_cli')
        group_internal = click.Group(name=f'{contract_name}')

        contract_abi = get_contract_abi_by_name(ABI, contract_name)
        for fn in contract_abi:
            if fn.get('name'):
                cmd = generate_cmd(contract_name, fn)
                group_internal.add_command(cmd)
        group.add_command(group_internal)
       
        groups.append(group)
    return groups


if __name__ == "__main__":
    groups = init_groups()
    cmd_collection = click.CommandCollection(sources=groups)
    cmd_collection()
