Cversion = '1.0.0'

from hashgard.interop.System.Storage import Get, Put, PutArray, GetArray
from hashgard.interop.System.Runtime import GetTxSender, GetTime, GetRand, TimeFormat
from hashgard.vmop.Builtins import concat
from hashgard.libop.List import elt_in, list_remove_elt
from hashgard.libop.String import join, split, int, str
from hashgard.interop.System.Account import IsValid
from hashgard.interop.System.Bank import ContractAccAddressGet, ContractBalanceSend, ContractBalanceInject, BalanceOf


GARD_DENOM = 'agard'
GARD_FACTOR = 1000000000000000000
OWNER = 'gard1dpzx7pmg4x6gjw6ja8znvas5l6kyfjsut4esyw'

KEY_SYSTEM_POOL = "system_prize_pool"  # 系统奖池
KEY_USER_STAKE_LIST = "user_stake_list"       # 用户投注列表
KEY_USER_STAKE_INFO = "user_stake_info"        # 用户投注详情
KEY_USER_PERIOD_TIME = "user_period_time"       # 用户期号的时间戳
KEY_SAVE_NUMBER = "save_number"     # 用户保存的号码
KEY_SAVE_PERIOD = "save_period"     # 用户保存的期号
KEY_USER_PERIOD_TYPE = "user_period_type"   # 用户期数的类型
GAME_TIME_FOR_A_ROUND = 5  # 5秒出一个块
KEY_OWNER = OWNER
KEY_STAKE_POOL = "stake_pool"   # 投注奖池
KEY_USER_WITHDRAW_AMOUNT = "user_withdraw_amount"  # 用户兑奖总金额
KEY_USER_STAKE_AMOUNT = "user_stake_amount"  # 用户兑奖总金额


def main(operation, args):
    if operation == 'emoji_random':
        return emoji_random()
    if operation == "init":
        return init()
    if operation == 'contractKeys':
        return contract_keys()
    if operation == "owner":
        return owner()
    if operation == "stakepool":
        return stakepool()
    if operation == "syspool":
        return syspool()
    if operation == "inject_system_pool":
        if len(args) != 1:
            raise Exception("缺少参数")
        return inject_system_pool(args[0])
    if operation == "withdraw_system_pool":
        if len(args) != 1:
            raise Exception("缺少参数")
        return withdraw_system_pool(args[0])
    if operation == "inject_stake_pool":
        if len(args) != 1:
            raise Exception("缺少参数")
        return inject_stake_pool(args[0])
    if operation == "withdraw_stake_pool":
        if len(args) != 1:
            raise Exception("缺少参数")
        return withdraw_stake_pool(args[0])
    if operation == "get_period_generation":
        return get_period_generation()
    if operation == "query_user_stake_info":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_user_stake_info(args[0], args[1])
    if operation == "query_user_stake_list":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_stake_list(args[0])
    if operation == "query_user_period_time":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_user_period_time(args[0], args[1])
    if operation == "query_user_time_condition":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_time_condition(args[0])
    if operation == "query_period_type":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_period_type(args[0], args[1])
    if operation == "stake":
        if len(args) != 2:
            raise Exception("缺少参数")
        return stake(args[0], args[1])
    if operation == "query_user_save_number":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_user_save_number(args[0], args[1])
    if operation == "query_user_save_period":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_save_period(args[0])
    if operation == "save":
        if len(args) != 1:
            raise Exception("缺少参数")
        return save(args[0])
    if operation == "withdraw":
        return withdraw()
    if operation == "remaining_time":
        if len(args) != 2:
            raise Exception("缺少参数")
        return remaining_time(args[0], args[1])
    if operation == "query_user_withdraw_amount":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_withdraw_amount(args[0])
    if operation == "query_user_period_withdraw_amount":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_user_period_withdraw_amount(args[0], args[1])
    if operation == "query_user_stake_amount":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_stake_amount(args[0])
    return False


def init():
    if Get(KEY_OWNER):
        raise Exception("已经初始化过")
    Put(KEY_OWNER, OWNER)

    return True


def contract_keys():
    return ["owner:string", "syspool:integer", "stakepool:integer", "contractAccount:string"]


def contractAccount():
    return ContractAccAddressGet()


def owner():
    return Get(KEY_OWNER)


def stakepool():
    return Get(KEY_STAKE_POOL)  # 查询用户奖池


def syspool():
    return Get(KEY_SYSTEM_POOL)  # 查询系统奖池


def inject_system_pool(amount):  # 系统奖池注入
    sender = GetTxSender()
    system_amount = syspool()
    if not system_amount:
        Put(KEY_SYSTEM_POOL, amount)
    else:
        system_amount = system_amount + amount
        Put(KEY_SYSTEM_POOL, system_amount)
    ContractBalanceInject(sender, GARD_DENOM, amount)
    return True


def withdraw_system_pool(amount):  # 取回系统奖池额度
    if GetTxSender() != Get(KEY_OWNER):
        raise Exception("请使用合约 owner 地址调用")

    if amount < 0:
        raise Exception("请输入正确的金额")

    balance_amount = syspool() - amount
    if balance_amount < 0:
        raise Exception("系统奖池余额不足")
    ContractBalanceSend(Get(KEY_OWNER), GARD_DENOM, amount)
    Put(KEY_SYSTEM_POOL, balance_amount)
    return True


def inject_stake_pool(amount):  # 用户奖池注入
    sender = GetTxSender()
    stake_amount = stakepool()
    if not stake_amount:
        Put(KEY_STAKE_POOL, amount)
    else:
        stake_amount = stake_amount + amount
        Put(KEY_STAKE_POOL, stake_amount)
    ContractBalanceInject(sender, GARD_DENOM, amount)
    return True


def withdraw_stake_pool(amount):   # 取回用户奖池额度
    if GetTxSender() != Get(KEY_OWNER):
        raise Exception("请使用合约 owner 地址调用")

    if amount < 0:
        raise Exception("请输入正确的金额")

    balance_amount = stakepool() - amount
    if balance_amount < 0:
        raise Exception("系统奖池余额不足")
    ContractBalanceSend(Get(KEY_OWNER), GARD_DENOM, amount)
    Put(KEY_STAKE_POOL, balance_amount)
    return True


def get_period_generation():  # 期数生成器
    now_time = GetTime()
    now_time = TimeFormat(now_time)  # 格式 2019-09-25 17:15:30
    time = split(now_time, " ")  # 分成两个元素
    time_01 = time[0]  # 年月日
    time_02 = time[1]  # 分时秒
    time_01 = split(time_01, "-")
    time_02 = split(time_02, ":")
    a = join("", time_01)
    b = concat(concat(time_02[0], time_02[1]), time_02[2])
    period = concat(a, b)  # 拼接
    return period


def emoji_random():         # 表情随机取
    rd = GetRand(24)
    ls = []
    for i in range(35):
        ls.append(i)
    result = []
    for i in range(len(rd)):
        index = (int(rd[i]) * 4) % len(ls)
        value = ls[index]
        result.append(str(value))
        ls = list_remove_elt(ls, value)

    repeat_index = (int(rd[int(rd[0])]) * 4) % len(result)    # 取随机下标
    old_value = result[repeat_index]       # 取出一个重复的值
    last_value = result[(int(rd[int(rd[len(rd) - 1])]) * 4) % len(result)]       # 取出要替换位置的值
    result[(int(rd[int(rd[len(rd) - 1])]) * 4) % len(result)] = old_value
    result.append(last_value)

    return result


def query_user_stake_info(address, period):        # 查询用户详情
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(concat(KEY_USER_STAKE_INFO, address), period)
    return GetArray(key)


def query_user_stake_list(address):         # 查询用户的投注列表
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(KEY_USER_STAKE_LIST, address)
    return GetArray(key)


def query_user_period_time(address, period):    # 查询用户期数的时间戳
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(concat(KEY_USER_PERIOD_TIME, address), period)
    return Get(key)


def query_user_time_condition(address):       # 查询是否距离最后一期，是否过去5秒
    if not IsValid(address):
        raise Exception("地址格式错误")

    stake_list = query_user_stake_list(address)
    if len(stake_list) == 0:
        return True

    last_period = stake_list[len(stake_list) - 1]       # 最后一期
    old_time = query_user_period_time(address, last_period)  # 最后一期的时间戳
    now_time = GetTime()
    if now_time - old_time > GAME_TIME_FOR_A_ROUND:
        return True

    return False


def query_period_type(address, period):     # 查询用户期数类型
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(concat(KEY_USER_PERIOD_TYPE, address), period)
    return Get(key)


def stake(game_type, operation_type):    # 用户购买
    sender = GetTxSender()
    user_list = emoji_random()  # 随机表情列表
    period = get_period_generation()  # 当期期号

    if query_user_time_condition(sender):       # 查询是否过去5秒
        stake_info_key = concat(concat(KEY_USER_STAKE_INFO, sender), period)
        PutArray(stake_info_key, user_list)     # Put 用户购买后产生的列表

        # Put 用户的投注列表，最多保持24个记录
        stake_list = query_user_stake_list(sender)
        stake_list_key = concat(KEY_USER_STAKE_LIST, sender)
        if len(stake_list) == 0:
            PutArray(stake_list_key, [period])
        if len(stake_list) == 24:
            new_stake_list = []
            for i in range(len(stake_list)):
                if i != len(stake_list) - 1:
                    new_stake_list.append(stake_list[i + 1])
            new_stake_list.append(period)
            PutArray(stake_list_key, new_stake_list)
        else:
            new_stake_list = []
            for i in range(len(stake_list)):
                new_stake_list.append(stake_list[i])
            new_stake_list.append(period)
            PutArray(stake_list_key, new_stake_list)

        period_type_key = concat(concat(KEY_USER_PERIOD_TYPE, sender), period)
        Put(period_type_key, game_type)         # Put 用户当期期数的类型，即表情包
        amount = 200 * GARD_FACTOR

        if BalanceOf(sender, [GARD_DENOM])[0] < amount:
            raise Exception("余额不足")

        inject_stake_pool(amount)  # 给合约地址转钱
        add_user_stake_amount(sender, amount)       # 加入自己的消费额中
        time = GetTime()
        period_time_key = concat(concat(KEY_USER_PERIOD_TIME, sender), period)
        Put(period_time_key, time)          # Put 用户期数的时间戳

        save_period_key = concat(KEY_SAVE_PERIOD, sender)
        if operation_type == 1:      # 1为 直接stake
            save_period_key = concat(KEY_SAVE_PERIOD, sender)
            PutArray(save_period_key, [])  # 把用户保存的表清空
        if operation_type != 1:       # 0 为继续
            save_period_list = GetArray(save_period_key)       # 查询用户保存的期号列表
            if len(save_period_list) == 0:
                raise Exception("当期不是继续的场景")

        return True
    else:
        raise Exception("请等待时间")


def remaining_time(sender, period):     # 查询用户该期剩余时间
    time = query_user_period_time(sender, period)
    now_time = GetTime()
    end_time = time + 30
    return end_time - now_time


def query_user_save_number(address, period):            # 查询用户保存的期号时的号码
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(concat(KEY_SAVE_NUMBER, address), period)
    return Get(key)


def query_user_save_period(address):    # 查询用户保存的期号
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(KEY_SAVE_PERIOD, address)
    return GetArray(key)


def save(number):       # 用户保存号码
    sender = GetTxSender()
    numbers = split(number, "-")
    stake_list = query_user_stake_list(sender)      # 查询用户的投注列表
    if len(stake_list) == 0:
        raise Exception("当期用户没有投注")

    last_stake = stake_list[len(stake_list) - 1]

    old_time = query_user_period_time(sender, last_stake)  # 最后一期的时间戳
    now_time = GetTime()
    if now_time - old_time > 30:
        raise Exception("当期已经过了时间，无法标记")

    last_stake_info = query_user_stake_info(sender, last_stake)     # 查询用户该期的表单

    if numbers[0] != numbers[1]:
        raise Exception("标记的不是同一个")
    num = 0
    for i in range(len(last_stake_info)):
        if last_stake_info[i] == numbers[0]:
            num = num + 1
    if num < 2:
        raise Exception("标记的号码在表情中未出现两次")

    save_num_key = concat(concat(KEY_SAVE_NUMBER, sender), last_stake)
    Put(save_num_key, number)       # 存取用户保存的号码

    save_period_key = concat(KEY_SAVE_PERIOD, sender)
    save_period = GetArray(save_period_key)

    new_save = []
    if len(save_period) != 0:
        for i in range(len(save_period)):
            new_save.append(save_period[i])
    new_save.append(last_stake)
    PutArray(save_period_key, new_save)     # 存取用户保存的期号

    return True


def withdraw():     # 取出奖励
    sender = GetTxSender()
    save_period = query_user_save_period(sender)        # 查询用户标记的期数
    save_period_length = len(save_period)
    if save_period_length == 0:
        raise Exception("当期没有标记，无法兑奖")
    amount = 0
    for i in range(save_period_length):
        amount = (i + 1) * 100 * GARD_FACTOR + amount
        add_user_period_withdraw_amount(sender, save_period[i], (i + 1) * 100 * GARD_FACTOR)

    add_user_withdraw_amount(sender, amount)
    ContractBalanceSend(sender, GARD_DENOM, amount)
    sys_amount = syspool() - amount
    Put(KEY_SYSTEM_POOL, sys_amount)    # 更新系统奖池

    save_period_key = concat(KEY_SAVE_PERIOD, sender)
    PutArray(save_period_key, [])     # 把用户保存的表清空
    return True


def query_user_withdraw_amount(address):        # 查询用户兑奖的金额
    key = concat(KEY_USER_WITHDRAW_AMOUNT, address)
    return Get(key)


def add_user_withdraw_amount(address, amount):
    key = concat(KEY_USER_WITHDRAW_AMOUNT, address)
    withdraw_amount = Get(key)
    if not withdraw_amount:
        Put(key, amount)
    else:
        withdraw_amount = withdraw_amount + amount
        Put(key, withdraw_amount)


def query_user_period_withdraw_amount(address, period):     # 查询用户指定期兑奖的金额
    key = concat(concat(KEY_USER_WITHDRAW_AMOUNT, address), period)
    return Get(key)


def add_user_period_withdraw_amount(address, period, amount):
    key = concat(concat(KEY_USER_WITHDRAW_AMOUNT, address), period)
    Put(key, amount)


def query_user_stake_amount(sender):        # 查询用户总共抵押的钱
    key = concat(KEY_USER_STAKE_AMOUNT, sender)
    return Get(key)


def add_user_stake_amount(sender, amount):
    key = concat(KEY_USER_STAKE_AMOUNT, sender)
    stake_amount = Get(key)
    if not stake_amount:
        Put(key, amount)
    else:
        stake_amount = stake_amount + amount
        Put(key, stake_amount)
