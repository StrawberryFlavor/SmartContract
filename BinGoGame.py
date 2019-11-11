Cversion = '1.0.0'

from hashgard.interop.System.Storage import Get, Put, PutArray, GetArray
from hashgard.interop.System.Runtime import GetTxSender, GetTime, GetRand, TimeFormat
from hashgard.vmop.Builtins import concat
from hashgard.libop.String import join, split, int, str
from hashgard.libop.List import elt_in, list_remove_elt
from hashgard.interop.System.Account import IsValid
from hashgard.interop.System.Bank import ContractAccAddressGet, ContractBalanceSend, ContractBalanceInject, BalanceOf

GARD_DENOM = 'agard'
GARD_FACTOR = 1000000000000000000

OWNER = "gard1xvn48vn3ljwk2d3vynv8ugkl373d93tfp9zae3"
ONE_TIME_ROOM = "one_time_room"  # 一倍房间
TWO_TIMES_ROOM = "two_times_room"  # 两倍房间
FIVE_TIMES_ROOM = "five_times_room"  # 五倍房间
TEN_TIMES_ROOM = "ten_times_room"  # 十倍房间

GMAE_START_TIME = 1572969600
KEY_GAME_TIME_FOR_A_ROUND = 300  # 5 分钟叫号一次
KEY_GAME_TIME_FOR_CALL_NUMBER = 5  # 5秒叫号一次

KEY_GAME_PERIOD = "period"  # 期数
KEY_GAME_PID = "game_pid"  # 期数对应的 pid
KEY_CALL_PID = "call_pid"  # 叫号的pid
KEY_GAME_PERIOD_CALL_NUMBER = "period_call_number"  # 期数的叫号号码
KEY_USER_STAKE = "user_stake"  # 用户投注的期数
KEY_USER_WITHDRAW_STATUS = "user_withdraw_status"  # 用户的兑奖状态
KEY_USER_LOTTERY = "lottery"  # 用户购买的卡
KEY_GAME_BINGO_STATUS = "bingo_status"  # 期的bingo状态
KEY_OWNER = OWNER
KEY_STAKE_POOL = "stake_popl"  # 用户购买奖池
KEY_SYSTEM_POOL = "system_pool"  # 系统奖池
KEY_MULTIPLE = "multiple"  # 用户对于该期的倍数
KEY_ISSUE_TIME = "issue_time"  # 每一期的时间戳
KEY_USER_GRADE = "user_garde"  # 用户标记的号码
KEY_USER_WITHDRAWS_AMOUNT = "user_withdraw_amount"  # 用户中奖的金额
KEY_USER_STAKE_AMOUNT = "user_stake_amount"  # 用户购买的卡单的总额
KEY_USER_ISSUE_MULTIPLE = "user_issue_multipe"  # 用户指定期数购买的倍数


def main(operation, args):
    if operation == "owner":
        return owner()
    if operation == "contractAccount":
        return contractAccount()
    if operation == 'contractKeys':
        return contract_keys()
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
    if operation == "draw_rules":
        if len(args) != 2:
            raise Exception("缺少参数")
        return draw_rules(args[0], args[1])
    if operation == "query_user_stake":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_stake(args[0])
    if operation == "issue":
        return issue()
    if operation == "get_table_generation":
        return get_table_generation()
    if operation == "init":
        return init()
    if operation == "stake":
        if len(args) != 1:
            raise Exception("缺少参数")
        return stake(args[0])
    if operation == "query_user_table_generation":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_user_table_generation(args[0], args[1])
    if operation == "query_period_call_number":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_period_call_number(args[0])
    if operation == "query_period_bingo_status":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_period_bingo_status(args[0])
    if operation == "bingo":
        if len(args) != 1:
            raise Exception("缺少参数")
        return bingo(args[0])
    if operation == "query_period_time":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_period_time(args[0])
    if operation == "add_user_grade":
        if len(args) != 1:
            raise Exception("缺少参数")
        return add_user_grade(args[0])
    if operation == "query_user_grade":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_user_grade(args[0], args[1])
    if operation == "withdraw":
        if len(args) != 1:
            raise Exception("缺少参数")
        return withdraw(args[0])
    if operation == "if_update_period":
        return if_update_period()
    if operation == "query_user_withdraw_amount":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_withdraw_amount(args[0])
    if operation == "query_user_stake_amount":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_stake_amount(args[0])
    if operation == "query_user_issue_multiple":
        if len(args) != 2:
            raise Exception("缺少参数")
        return query_user_issue_multiple(args[0], args[1])
    if operation == "query_now_period_pid":
        return query_now_period_pid()
    return False


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


def get_peroid_pid():  # 计算是否过去五分钟，五分钟为一个整数倍
    now_time = GetTime()
    pid = ((now_time - GMAE_START_TIME) - (
            (now_time - GMAE_START_TIME) % KEY_GAME_TIME_FOR_A_ROUND)) / KEY_GAME_TIME_FOR_A_ROUND
    return pid


def get_call_pid():  # 每15秒叫号一次
    now_time = GetTime()
    pid = ((now_time - GMAE_START_TIME) - (
            (now_time - GMAE_START_TIME) % KEY_GAME_TIME_FOR_CALL_NUMBER)) / KEY_GAME_TIME_FOR_CALL_NUMBER
    return pid


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


def get_table_generation():  # 用户购买的单子，25个数字
    options = []
    result = []
    for r in range(5):
        row = []
        base = 15 * r + 1
        for i in range(base, base + 15):
            row.append(str(i))
        options.append(row)
        result.append([])

    road = GetRand(26)

    index = 0
    step = int(road[index])
    for r in range(len(options)):
        while len(result[r]) < 5:
            step = (step + int(road[index + 1])) % len(options[r])
            item = options[r][step]
            if not elt_in(result[r], item):
                result[r].append(item)
                options[r] = list_remove_elt(options[r], item)
            if index < len(road) - 1:
                index = index + 1

    generation = []
    for _r in range(len(result)):
        for _s in range(len(result[_r])):
            generation.append(result[_r][_s])

    generation[12] = "$"
    return generation


def init():
    if Get(KEY_OWNER):
        raise Exception("已经初始化过")
    Put(KEY_OWNER, OWNER)  # put owner

    return True


def issue():  # 查询当前期数
    return Get(KEY_GAME_PERIOD)


def query_user_stake(address):
    if not IsValid(address):
        raise Exception("请填写正确的地址格式")
    key = concat(KEY_USER_STAKE, address)
    return GetArray(key)  # 查询用户的投注期数, 返回一个列表


# def query_user_withdraw_status(address, period):  # 查询用户指定期数的兑奖状态
#     if not IsValid(address):
#         raise Exception("请填写正确的地址格式")
#     key = concat(concat(KEY_USER_WITHDRAW_STATUS, address), period)
#     return Get(key)


def if_update_period():  # 判断是否过去了五分钟
    now_period = Get(KEY_GAME_PERIOD)  # 当前期号
    pid_key = concat(KEY_GAME_PID, now_period)
    now_period_pid = Get(pid_key)  # 当前期号的 pid
    now_pid = get_peroid_pid()  # 当前 pid
    if now_pid > now_period_pid:  # 判断是否过去了五分钟
        return True
    return False


def query_user_table_generation(address, period):  # 查询用户指定期数购买的表单,返回一个列表
    if not IsValid(address):
        raise Exception("请填写正确的地址格式")
    period_lottery_key = concat(concat(KEY_USER_LOTTERY, address), period)
    return GetArray(period_lottery_key)


def query_period_call_number(period):  # 查询期数的叫号号码
    call_number_key = concat(KEY_GAME_PERIOD_CALL_NUMBER, period)
    return GetArray(call_number_key)  # 返回一个列表


def call_number():  # 叫号
    option = []
    for n in range(1, 76):
        option.append(n)
    rd = GetRand(30)
    res = []
    for _rd in range(len(rd)):
        step = int(rd[_rd]) * 9 % len(option)
        res.append(str(option[step]))
        option = list_remove_elt(option, option[step])
    res.append("$")
    return res


def stake(multiple):  # 用户购买卡单
    if multiple != 1 and multiple != 2 and multiple != 5 and multiple != 10:
        raise Exception("只支持一倍，两倍，五倍，十倍")

    sender = GetTxSender()  # 当前用户

    if BalanceOf(sender, [GARD_DENOM])[0] < 200 * GARD_FACTOR:
        raise Exception("当前余额不足购买")

    now_time = GetTime()

    if not issue():  # 如果当期没有期数
        period = get_period_generation()
        Put(KEY_GAME_PERIOD, period)  # Put 初始的期号
        pid_key = concat(KEY_GAME_PID, period)
        Put(pid_key, get_peroid_pid())  # Put 初始期号的 pid
        time_key = concat(KEY_ISSUE_TIME, period)
        Put(time_key, now_time)  # Put 初始的时间戳

    if if_update_period():  # 已经过了五分钟 返回 true
        period = get_period_generation()  # 新的期号
        Put(KEY_GAME_PERIOD, period)  # Put 新的期号
        now_pid = get_peroid_pid()  # 当前 pid
        pid_key = concat(KEY_GAME_PID, period)
        Put(pid_key, now_pid)  # Put 新的期号的pid
        time_key = concat(KEY_ISSUE_TIME, period)
        Put(time_key, now_time)  # Put 新的期号的时间戳

    now_period = Get(KEY_GAME_PERIOD)  # 当前期

    table_generation = get_table_generation()  # 获取表格
    period_lottery_key = concat(concat(KEY_USER_LOTTERY, sender), now_period)
    user_table = query_user_table_generation(sender, now_period)
    if len(user_table) > 0:
        raise Exception("当期已经买过卡单")

    PutArray(period_lottery_key, table_generation)  # 如果没有购买过，则提交当前表单

    stake_key = concat(KEY_USER_STAKE, sender)
    stake_list = GetArray(stake_key)  # 查询用户的投注列表

    ls = []
    if len(stake_list) == 0:
        ls.append(now_period)
    if len(stake_list) == 24:
        for i in range(len(stake_list)):
            if i != len(stake_list) - 1:
                ls.append(stake_list[i + 1])
        ls.append(now_period)
    if 0 < len(stake_list) < 24:
        for i in range(len(stake_list)):
            ls.append(stake_list[i])
        ls.append(now_period)

    PutArray(stake_key, ls)  # 只记录用户的24期

    stake_amount = stakepool()
    if not stake_amount:
        Put(KEY_STAKE_POOL, 200 * GARD_FACTOR)
    else:
        stake_amount = stake_amount + 200 * GARD_FACTOR
        Put(KEY_STAKE_POOL, stake_amount)  # put 投注池子

    multiple_key = concat(concat(KEY_MULTIPLE, sender), now_period)  # 用户该期的倍数

    Put(multiple_key, multiple)

    call_numbers = query_period_call_number(now_period)  # 返回一个列表, 查询本期的叫号列表
    call_number_key = concat(KEY_GAME_PERIOD_CALL_NUMBER, now_period)
    if len(call_numbers) == 0:
        PutArray(call_number_key, call_number())  # Put 本期的叫号号码

    amount = multiple * 200 * GARD_FACTOR
    stake_amount_key = concat(KEY_USER_STAKE_AMOUNT, sender)
    user_stake_amount = query_user_stake_amount(sender)
    if not user_stake_amount:
        Put(stake_amount_key, amount)  # Put 用户总共购买过的金额
    else:
        user_stake_amount = user_stake_amount + amount
        Put(stake_amount_key, user_stake_amount)

    user_multiple_key = concat(concat(KEY_USER_ISSUE_MULTIPLE, sender), now_period)  # 用户当期购买的倍数
    Put(user_multiple_key, multiple)

    ContractBalanceInject(sender, GARD_DENOM, amount)  # 每次投注花费200个gard

    return True


def draw_rules(address, period):  # 中奖匹配规则
    if not IsValid(address):
        raise Exception("请填写正确的地址格式")

    numbers = query_user_grade(address, period)  # 因为用户标记的号码

    stake_table = query_user_table_generation(address, period)  # 用户购买的表单

    options = []
    for _option in range(5):
        options.append([])
    for t in range(len(stake_table)):
        if t <= 4:
            options[0].append(stake_table[t])  # B 横向五个
            continue
        if 4 < t <= 9:
            options[1].append(stake_table[t])  # I
            continue
        if 9 < t <= 14:
            options[2].append(stake_table[t])  # N
            continue
        if 14 < t <= 19:
            options[3].append(stake_table[t])  # G
            continue
        if 19 < t <= 24:
            options[4].append(stake_table[t])  # O
            continue
    op_l = []
    for _op in range(5):
        op_l.append([])

    for l in range(len(options)):
        op_l[0].append(options[l][0])  # 竖向五个
        op_l[1].append(options[l][1])
        op_l[2].append(options[l][2])
        op_l[3].append(options[l][3])
        op_l[4].append(options[l][4])

    op_r = []
    for _op in range(2):
        op_r.append([])

    for r in range(len(options)):  # 两个斜的一列
        op_r[0].append(options[r][r])
        op_r[1].append(options[r][len(options) - 1 - r])

    status = False
    for i in range(len(options)):
        l_n = 0
        for index in range(len(numbers)):
            if elt_in(options[i], numbers[index]):
                l_n = l_n + 1
        if l_n >= 5:
            status = True
            break

    for i in range(len(op_l)):
        l_n = 0
        for index in range(len(numbers)):
            if elt_in(op_l[i], numbers[index]):
                l_n = l_n + 1
        if l_n >= 5:
            status = True
            break

    for i in range(len(op_r)):
        l_n = 0
        for index in range(len(numbers)):
            if elt_in(op_r[i], numbers[index]):
                l_n = l_n + 1
        if l_n >= 5:
            status = True
            break

    call_list = query_period_call_number(period)  # 查询中奖叫号号码
    for i in range(len(numbers)):
        if not elt_in(call_list, numbers[i]):
            status = False

    return status


def query_period_bingo_status(period):  # 查询当期 bingo 状态
    key = concat(KEY_GAME_BINGO_STATUS, period)
    return Get(key)


def bingo(call):  # 用户中奖按兑奖 bingo
    sender = GetTxSender()
    now_period = issue()  # 当期
    user_table = query_user_table_generation(sender, now_period)
    add_user_grade(call)

    if len(user_table) == 0:
        raise Exception("当期没有购买卡单")

    if query_period_bingo_status(now_period):
        raise Exception("当期已经有人中奖了，无法 BINGO， 请等待当期结束，下次手速快点哦！")

    if not draw_rules(sender, now_period):
        raise Exception("当期没有中奖")

    bingo_key = concat(KEY_GAME_BINGO_STATUS, now_period)
    Put(bingo_key, True)  # 将当期改为 bingo 为 true 的状态

    multiple_key = concat(concat(KEY_MULTIPLE, sender), now_period)  # 用户该期的倍数
    multiple = Get(multiple_key)

    amount = multiple * 10000 * GARD_FACTOR
    withdraw_amount_key = concat(KEY_USER_WITHDRAWS_AMOUNT, sender)
    withdraw_user_amount = query_user_withdraw_amount(sender)  # 查询用户兑奖的奖励
    if not withdraw_user_amount:
        Put(withdraw_amount_key, amount)
    else:
        withdraw_user_amount = withdraw_user_amount + amount
        Put(withdraw_amount_key, withdraw_user_amount)  # Put 用户兑奖的奖励

    ContractBalanceSend(sender, GARD_DENOM, amount)     # 给用户转钱

    return True


def owner():
    return Get(KEY_OWNER)


def contractAccount():
    return ContractAccAddressGet()


def contract_keys():
    return ["owner:string", "issue:string", "syspool:integer", "stakepool:integer", "contractAccount:string"]


def query_user_grade(address, period):  # 查询该期用户的标记号码
    key = concat(concat(KEY_USER_GRADE, address), period)
    return GetArray(key)


def add_user_grade(call):  # 添加用户标记的号码
    sender = GetTxSender()
    now_period = issue()  # 当期期号
    numbers = split(call, "-")  # 用户传进来的号码
    numbers.append("$")
    user_ls = query_user_table_generation(sender, now_period)  # 查询用户购买的表单

    for i in range(len(numbers)):
        if not elt_in(user_ls, numbers[i]):
            raise Exception("用户标记的号码，不在自身购买表单中")

    garde_key = concat(concat(KEY_USER_GRADE, sender), now_period)
    PutArray(garde_key, numbers)  # 提交用户标记的号码
    return True


def query_period_time(period):  # 查询指定期数的时间戳
    time_key = concat(KEY_ISSUE_TIME, period)
    return Get(time_key)  # Put 新的期号的时间戳


def withdraw(period):  # 用户bingo以往的，场景：用户提交标记号码，中奖了，可能没有及时bingo
    sender = GetTxSender()
    grade_list = query_user_grade(sender, period)  # 用户标记的号码
    if len(grade_list) == 0:
        raise Exception("用户该期没有标记过号码")

    if query_period_bingo_status(period):
        raise Exception("当期已经有人中奖了，无法 BINGO， 请等待当期结束，下次手速快点哦！")

    user_table = query_user_table_generation(sender, period)
    if len(user_table) == 0:
        raise Exception("当期没有购买卡单")

    if not draw_rules(sender, period):
        raise Exception("当期没有中奖")

    bingo_key = concat(KEY_GAME_BINGO_STATUS, period)
    Put(bingo_key, True)  # 将当期改为 bingo 为 true 的状态

    multiple_key = concat(concat(KEY_MULTIPLE, sender), period)  # 用户该期的倍数
    multiple = Get(multiple_key)

    amount = multiple * 10000 * GARD_FACTOR

    withdraw_amount_key = concat(KEY_USER_WITHDRAWS_AMOUNT, sender)
    withdraw_user_amount = query_user_withdraw_amount(sender)  # 查询用户兑奖的奖励
    if not withdraw_user_amount:
        Put(withdraw_amount_key, amount)
    else:
        withdraw_user_amount = withdraw_user_amount + amount
        Put(withdraw_amount_key, withdraw_user_amount)  # Put 用户兑奖的奖励

    ContractBalanceSend(sender, GARD_DENOM, amount)  # 给用户转账

    return True


def query_user_withdraw_amount(address):  # 查询用户兑奖的数量
    withdraw_amount_key = concat(KEY_USER_WITHDRAWS_AMOUNT, address)
    return Get(withdraw_amount_key)


def query_user_stake_amount(address):  # 查询用户购买卡单的总额
    stake_amount_key = concat(KEY_USER_STAKE_AMOUNT, address)
    return Get(stake_amount_key)


def query_user_issue_multiple(sender, period):  # 查询用户指定期数的购买倍数
    key = concat(concat(KEY_USER_ISSUE_MULTIPLE, sender), period)
    return Get(key)


def query_now_period_pid():
    pid_key = concat(KEY_GAME_PID, issue())
    return Get(pid_key)  # 当前期号的 pid
