Cversion = '1.0.0'

"""
An Example of HRC-10
"""
from hashgard.interop.System.Bank import AssetInit, AssetSub, AssetAdd, AssetGet, AssetPublisher
from hashgard.interop.System.Storage import Get, Put
from hashgard.interop.System.Runtime import GetTxSender
from hashgard.interop.System.Account import IsValid
from hashgard.vmop.Builtins import concat

KEY_DESCRIPTION = "description"
KEY_NAME = "name"
KEY_ISSUE_NUMBER = "issue_number"
NAME = "发行积分合约"
DESCRIPTION = "Hashgard Enterprise 链上发行积分"


def main(operation, args):
    if operation == 'init':
        return init()

    if operation == "issue":
        if len(args) != 3:
            return False
        return issue(args[0], args[1], args[2])

    if operation == "issue_number":
        return issue_number()

    if operation == 'name':
        return name()

    if operation == 'balanceOf':
        if len(args) != 2:
            return False
        return balance_of(args[0], args[1])

    if operation == "symbol_description":
        if len(args) != 1:
            return False
        return symbol_description(args[0])

    if operation == 'description':
        return description()

    if operation == 'contractKeys':
        return contract_keys()

    if operation == 'mint':
        if len(args) != 3:
            return False
        return mint(args[0], args[1], args[2])

    if operation == 'burn':
        if len(args) != 3:
            return False
        return burn(args[0], args[1], args[2])

    if operation == "mint_self":
        if len(args) != 2:
            return False
        return mint_self(args[0], args[1])

    if operation == "burn_self":
        if len(args) != 2:
            return False
        return burn_self(args[0], args[1])

    if operation == "issue_owner":
        if len(args) != 1:
            return False
        return issue_owner(args[0])

    return False


def init():
    if Get(KEY_NAME):
        return False
    Put(KEY_NAME, NAME)
    Put(KEY_DESCRIPTION, DESCRIPTION)


def issue_number():  # 查询利用此合约发行了多少个积分
    return Get(KEY_ISSUE_NUMBER)


def issue_owner(symbol):  # 查询通过该合约发行积分的发行者
    return AssetPublisher(symbol)


def issue(total, symbol, symbol_des):
    sender = GetTxSender()  # 获取操作者地址
    if issue_owner(symbol):
        raise Exception("此积分已发行")

    AssetInit(sender, total, symbol)  # 给操作者发行积分

    issue_num = issue_number()
    if not issue_num:  # 如果通过该合约暂时没有积分
        Put(KEY_ISSUE_NUMBER, 1)
    else:
        Put(KEY_ISSUE_NUMBER, issue_num + 1)

    des_key = concat(KEY_DESCRIPTION, symbol)
    Put(des_key, symbol_des)  # Put 此积分的描述

    return True


# --------------------------------------------- #
# -------------- query functions -------------- #
# --------------------------------------------- #

def balance_of(address, symbol):  # 查询此地址，该积分的余额
    return AssetGet(address, symbol)


def symbol_description(symbol):  # 查询通过该合约发行的此积分的描述
    des_key = concat(KEY_DESCRIPTION, symbol)
    return Get(des_key)


def name():  # 此合约名称
    return Get(KEY_NAME)


def description():  # 此合约描述
    return Get(KEY_DESCRIPTION)


def contract_keys():
    return ["name:string", "description:string", "issue_number:integer"]


# --------------------------------------------- #
# -------------- basic functions -------------- #
# --------------------------------------------- #

def mint_self(amount, symbol):
    owner = issue_owner(symbol)
    sender = GetTxSender()
    if not owner:
        raise Exception("该积分可能没有发行")
    if amount < 0:
        raise Exception("请输入正确的数量")
    if owner != sender:
        raise Exception("请使用该积分的 owner 地址")
    AssetAdd(sender, amount, symbol)
    return True


def burn_self(amount, symbol):
    owner = issue_owner(symbol)
    sender = GetTxSender()
    if not owner:
        raise Exception("该积分可能没有发行")
    if amount < 0:
        raise Exception("请输入正确的数量")
    balance = balance_of(sender, symbol)
    if balance < amount:
        raise Exception("需要销毁的积分大于自身持有积分")
    if owner != sender:
        raise Exception("请使用该积分的 owner 地址")
    AssetSub(sender, amount, symbol)
    return True


def mint(to_address, amount, symbol):
    if not IsValid(to_address):
        raise Exception("地址长度不合规")

    if amount < 0:
        raise Exception("请输入正确的数量")

    sender = GetTxSender()
    owner = issue_owner(symbol)
    if owner != sender:
        raise Exception("请使用该积分的 owner 地址")
    AssetAdd(to_address, amount, symbol)

    return True


def burn(to_address, amount, symbol):
    if not IsValid(to_address):
        raise Exception("地址长度不合规")

    balance = balance_of(to_address, symbol)
    if amount < 0:
        raise Exception("请输入正确的数量")

    if balance < amount:
        raise Exception("需要销毁的积分大于被销毁者持有积分")

    sender = GetTxSender()
    owner = issue_owner(symbol)
    if owner != sender:
        raise Exception("请使用该积分的 owner 地址")

    AssetSub(to_address, amount, symbol)

    return True
