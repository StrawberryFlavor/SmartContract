Cversion = '1.0.0'

from hashgard.interop.System.Storage import Get, Put, PutArray, GetArray
from hashgard.interop.System.Runtime import GetTxSender, GetTime, GetRand, TimeFormat
from hashgard.vmop.Builtins import concat
from hashgard.libop.String import join, split, int, str
from hashgard.interop.System.Account import IsValid
from hashgard.interop.System.Bank import ContractAccAddressGet, ContractBalanceSend, ContractBalanceInject, BalanceOf

GARD_DENOM = 'agard'
GARD_FACTOR = 1000000000000000000
STAKE_AMOUNT = 200 * GARD_FACTOR  # 单注金额

OWNER = "gard1457qyf93ljsh2ep00uc66djd3n95fljk7y492k"
KEY_GAME_PERIOD = "period"  # 期数
KEY_GAME_TIME = "game_time" # 期数对应得时间戳
KEY_USER_ISSUE_MULTIPLE = "user_issue_multipe"  # 用户指定期数购买的倍数

KEY_GAME_LIST = "period_list"  # 期数列表
GMAE_START_TIME = 1572969600
KEY_GAME_TIME_FOR_A_ROUND = 300  # 5 分钟叫号一次
KEY_USER_STAKE = "user_stake"  # 用户对期数的投注
KEY_USER_ISSUE = "user_issue"  # 用户的投注期数
KEY_USER_WITHDRAW = "user_withdraw"  # 用户兑奖信息
KEY_GAME_WITHDRAW_INFO = "game_withdraw_info"   # 期数的兑奖信息
KEY_GAME_PRIZE = "game_prize"   # 中奖号码
KEY_OWNER = OWNER
KEY_SYSTEM_POOL = "system_pool"  # 系统奖池
KEY_STAKE_POOL = "stake_pool"   # 用户奖池


def main(operation, args):
    if operation == "owner":
        return owner()
    if operation == "contractAccount":
        return contractAccount()
    if operation == 'contractKeys':
        return contract_keys()
    if operation == "inject_system_pool":
        if len(args) != 1:
            raise Exception("缺少参数")
        return inject_system_pool(args[0])
    if operation == "withdraw_system_pool":
        if len(args) != 1:
            raise Exception("缺少参数")
        return withdraw_system_pool(args[0])
    if operation == "issue":
        return issue()
    if operation == "init":
        return init()
    if operation == "query_user_stake":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_user_stake(args[0], args[1])
    if operation == "query_user_stake_list":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_stake_list(args[0])
    if operation == "stake":
        if len(args) != 3:
            raise Exception("缺少参数")
        return stake(args[0], args[1], args[2])
    if operation == "if_stake":
        return if_stake()
    if operation == "query_period_prize_number":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_period_prize_number(args[0])
    if operation == "query_user_if_prize":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_user_if_prize(args[0], args[1])
    if operation == "query_user_withdarw":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_withdraw(args[0])
    if operation == "query_user_withdraw_issue":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_user_withdraw_issue(args[0], args[1])
    if operation == "withdraw":
        if len(args) != 1:
            raise Exception("缺少参数")
        return withdraw(args[0])
    if operation == "query_withdraw_info":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_withdraw_info(args[0])
    if operation == "syspool":
        return syspool()
    if operation == "syspool":
        return syspool()
    if operation == "stakepool":
        return stakepool()
    if operation == "get_period_generation":
        return get_period_generation()
    if operation == "query_period_list":
        return query_period_list()
    if operation == "query_user_stake_amount":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_stake_amount(args[0])
    if operation == "query_period_time":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_period_time(args[0])

    return False


def contract_keys():
    return ["owner:string", "issue:string", "syspool:integer", "stakepool:integer", "contractAccount:string"]


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


def query_period_time(period):   # 获取指定期数得时间戳
    key = concat(KEY_GAME_TIME, period)
    return Get(key)


def get_period_generation():  # 期数生成器
    now_time = GetTime()
    now_time = TimeFormat(now_time)  # 格式 2019-09-25 17:15:30
    time = split(now_time, " ")  # 分成两个元素
    time_01 = time[0]  # 年月日
    time_02 = time[1]  # 分时秒
    time_01 = split(time_01, "-")
    time_02 = split(time_02, ":")
    a = join("", time_01)
    b = concat(time_02[0], time_02[1])
    period = concat(a, b)  # 拼接
    return period


def issue():  # 当期期号
    return Get(KEY_GAME_PERIOD)


def init():
    if Get(KEY_OWNER):
        raise Exception("已经初始化过")
    time = GetTime()
    Put(KEY_OWNER, OWNER)  # Put 合约的 owenr
    now_period = get_period_generation()
    Put(KEY_GAME_PERIOD, now_period)  # Put 最开始的期号
    time_key = concat(KEY_GAME_TIME, now_period)
    Put(time_key, time)             # Put 最开始的期号时间戳
    period_ls = [now_period]
    PutArray(KEY_GAME_LIST, period_ls)  # Put 期数列表


def query_period_list():
    return GetArray(KEY_GAME_LIST)


def if_stake():
    now_time = GetTime()
    now_period = issue()  # 当期
    old_time = query_period_time(now_period)
    if now_time - old_time > KEY_GAME_TIME_FOR_A_ROUND:
        return True
    return False


def query_user_stake(address, period):   # 返回用户对于该期的投注详情，[投注方式（散，和），号码，金额]
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(concat(KEY_USER_STAKE, address), period)
    return GetArray(key)  # 返回用户投注信息，列表


def query_user_stake_list(address):         # 返回用户投注的期数列表
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(KEY_USER_ISSUE, address)
    return GetArray(key)


def stake(mode, multipe, number):  # 用户投注
    ls = []
    now_time = GetTime()
    for i in range(len(number)):
        ls.append(int(number[i]))
    if mode == 0:       # 散值
        for i in range(len(ls)):
            if ls[i] > 6:
                raise Exception("每个数字在1到6之间")
    if mode == 1:       # 和值
        if int(number) < 3 or int(number) > 18:
            raise Exception("最大的和值为18")

    if multipe > 99 or multipe < 1:
        raise Exception("不支持的倍数")

    if if_stake():
        num = draw_number()     # 开启下一期前，开放上一期的中奖号码
        draw_num_key = concat(KEY_GAME_PRIZE, issue())
        Put(draw_num_key, num)      # Put 该期的中奖号码
        update_period = get_period_generation()
        Put(KEY_GAME_PERIOD, update_period)  # Put 新的期数
        time_key = concat(KEY_GAME_TIME, update_period)
        Put(time_key, now_time)         # Put新期数的时间戳
        period_list = []
        ls = GetArray(KEY_GAME_LIST)
        for i in range(len(ls)):
            if len(ls) < 24:
                period_list.append(ls[i])
            if len(ls) >= 24 and i < 23:
                period_list.append(ls[i + 1])
        period_list.append(update_period)
        PutArray(KEY_GAME_LIST, period_list)  # Put 24个期数列表

    sender = GetTxSender()
    period = issue()
    amount = multipe * STAKE_AMOUNT

    if BalanceOf(sender, [GARD_DENOM])[0] < amount:
        raise Exception("余额不足")

    if len(query_user_stake(sender, period)) > 0:
        raise Exception("当期已经购买过")
    user_stake_key = concat(concat(KEY_USER_STAKE, sender), period)
    if mode == 0:  # 0 为散号
        PutArray(user_stake_key, [str(mode), str(multipe), number, str(amount)])
    if mode == 1:  # 1 为和值
        PutArray(user_stake_key, [str(mode), str(multipe), number, str(amount)])

    user_stake_list = []
    ls = query_user_stake_list(sender)
    for i in range(len(ls)):
        if len(ls) < 24:
            user_stake_list.append(ls[i])
        if len(ls) >= 24 and i < 23:
            user_stake_list.append(ls[i + 1])
    user_stake_list.append(period)
    user_stake_list_key = concat(KEY_USER_ISSUE, sender)  # Put 24个用户投注的期数列表
    PutArray(user_stake_list_key, user_stake_list)

    stake_all_amount = query_user_stake_amount(sender)
    stake_amount_key = concat(KEY_USER_STAKE, sender)
    if not stake_all_amount:
        Put(stake_amount_key, amount)
    else:
        stake_all_amount = stake_all_amount + amount
        Put(stake_amount_key, stake_all_amount)         # Put 用户的总共投注金额

    inject_stake_pool(amount)
    return True


def draw_number():      # 开奖号码生成
    number = []
    for i in range(1, 7):
        number.append(i)
    result = []
    rd = GetRand(3)
    for i in range(len(rd)):
        index = int(rd[i]) % len(number)
        result.append(str(number[index]))

    res = concat(concat(result[0], result[1]), result[2])
    return res  # 返回一个字符串


def query_period_prize_number(period):      # 查询该期得中奖号码
    key = concat(KEY_GAME_PRIZE, period)
    return Get(key)


def sum_value_match(number):        # 和值匹配规则
    ls = []
    for i in range(len(number)):
        ls.append(int(number[i]))

    sum = 0
    for i in range(len(ls)):
        sum = ls[i] + sum

    amount = 0      # 应该获得的奖励
    if sum == 4:
        amount = 8000 * GARD_FACTOR
    if sum == 5:
        amount = 4000 * GARD_FACTOR
    if sum == 6:
        amount = 2500 * GARD_FACTOR
    if sum == 7:
        amount = 1600 * GARD_FACTOR
    if sum == 8:
        amount = 1200 * GARD_FACTOR
    if sum == 9:
        amount = 1000 * GARD_FACTOR
    if sum == 10:
        amount = 900 * GARD_FACTOR
    if sum == 11:
        amount = 900 * GARD_FACTOR
    if sum == 12:
        amount = 1000 * GARD_FACTOR
    if sum == 13:
        amount = 1200 * GARD_FACTOR
    if sum == 14:
        amount = 1600 * GARD_FACTOR
    if sum == 15:
        amount = 2500 * GARD_FACTOR
    if sum == 16:
        amount = 4000 * GARD_FACTOR
    if sum == 17:
        amount = 8000 * GARD_FACTOR
    if sum == 18 or sum == 3:
        amount = 24000 * GARD_FACTOR

    return amount


def scatter_value_match(number):        # 散值匹配规则
    ls = []
    for i in range(len(number)):
        ls.append(int(number[i]))

    for i in range(len(ls)):
        same_frequency = 0
        different_frequency = 0
        for l in range(len(ls)):
            if ls[i] == ls[l]:
                same_frequency = same_frequency + 1
            if ls[i] != ls[l]:
                different_frequency = different_frequency + 1

        if same_frequency == 3:  # 3个同号
            amount = 24000 * GARD_FACTOR
            return amount

        if same_frequency == 2:     # 2 个同号
            amount = 8000 * GARD_FACTOR
            return amount

        if different_frequency == 2:       # 3个异号
            amount = 4000 * GARD_FACTOR
            return amount


def query_user_if_prize(address, period):       # 查询用户指定的期数是否中奖
    if not IsValid(address):
        raise Exception("地址格式错误")

    prize_number = query_period_prize_number(period)      # 查询中奖号码
    user_info = query_user_stake(address, period)       # 查询用户得投注信息
    user_numbers = user_info[2]                         # 用户的投注号码
    mul = user_info[1]                                  # 用户的倍数
    if user_info[0] == "0" and prize_number == user_numbers:    # 散号
        amount = scatter_value_match(prize_number)
        return amount * int(mul)
    if user_info[0] == "1":  # 和值
        prize_sum = 0
        for i in range(len(prize_number)):
            prize_sum = int(prize_number[i]) + prize_sum
        if prize_sum == int(user_numbers):
            amount = sum_value_match(prize_number)
            return amount * int(mul)
    amount = 0
    return amount


def query_user_withdraw(address):   # 查询用户总共获取的奖励
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(KEY_USER_WITHDRAW, address)
    return Get(key)


def query_user_withdraw_issue(address, period):  # 查询用户指定期数的获得奖励
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(concat(KEY_USER_WITHDRAW, address), period)
    return Get(key)


def withdraw(period):   # 兑奖
    sender = GetTxSender()
    amount = query_user_if_prize(sender, period)
    if amount <= 0:
        raise Exception("用户没有中奖")

    withdraw_amount = query_user_withdraw_issue(sender, period)
    if withdraw_amount > 0:
        raise Exception("用户已经兑过奖")

    withdraw_user_amount = query_user_withdraw(sender)
    user_withdraw_key = concat(KEY_USER_WITHDRAW, sender)

    if not withdraw_user_amount:
        Put(user_withdraw_key, amount)
    else:
        withdraw_user_amount = withdraw_user_amount + amount
        Put(user_withdraw_key, withdraw_user_amount)                # Put 用户总共获得奖励

    user_withdraw_period_key = concat(concat(KEY_USER_WITHDRAW, sender), period)
    Put(user_withdraw_period_key, amount)           # Put 用户该期获得的奖励

    sys_amount = syspool() - amount
    Put(KEY_SYSTEM_POOL, sys_amount)    # 更新系统奖池

    withdraw_info_key = concat(KEY_GAME_WITHDRAW_INFO, period)
    withdraw_list_info = query_withdraw_info(period)
    withdraw_ls = []
    if len(withdraw_list_info) > 0:
        for i in range(len(withdraw_list_info)):
            withdraw_ls.append(withdraw_list_info[i])
    withdraw_ls.append(sender)
    PutArray(withdraw_info_key, withdraw_ls)      # 提交该期的总共兑奖人
    ContractBalanceSend(sender, GARD_DENOM, amount)     # 给用户转钱

    return True


def query_withdraw_info(period):        # 查询该期的兑奖人信息
    withdraw_info_key = concat(KEY_GAME_WITHDRAW_INFO, period)
    return GetArray(withdraw_info_key)


def query_user_stake_amount(address):       # 查询用户总共投注的钱
    if not IsValid(address):
        raise Exception("地址格式错误")

    key = concat(KEY_USER_STAKE, address)
    return Get(key)
