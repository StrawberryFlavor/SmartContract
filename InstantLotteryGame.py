Cversion = '1.0.0'

from hashgard.interop.System.Storage import Get, Put, PutArray, GetArray
from hashgard.interop.System.Runtime import GetTxSender, GetTime, GetRand, TimeFormat, Assert
from hashgard.builtins import concat, substr, append
from hashgard.libgard import join, split, list_remove_elt, int, str
from hashgard.interop.System.Account import IsValid
from hashgard.interop.System.Bank import ContractAccAddressGet, ContractBalanceSend, ContractBalanceInject, BalanceOf

GARD_DENOM = 'agard'
GARD_FACTOR = 1000000000000000000
OWNER = 'gard1xvn48vn3ljwk2d3vynv8ugkl373d93tfp9zae3'
KEY_OWNER = OWNER
KEY_SYSTEM_POOL = "system_prize_pool"
KEY_USER_POOL = "user_prize_pool"
KEY_EVENT_POOL = "event_prize_pool"
KEY_MY_ALL_STAKE = "my_sake"  # 我的投注记录
KEY_MY_STAKE_COUNT = "my_stake_count"  # 我的投注统计
KEY_BETTING_PERSON = "betting_person"
KEY_BETTING_AMOUNT = "betting_amount"
KEY_BETTING_NUMBER = "betting_number"
KEY_SHARED_REWARD = "shared_reward"  # 推广奖励计数
KEY_INVITED_RECORD = "invited_record"  # 被邀请记录
KEY_INVITATION_RECORD = "invitation_record"  # 邀请记录
KEY_INVITATION_CODE = "invitation_code"  # 邀请码
KEY_AMOUNT_EACH_AWARD = "amount_of_each_award"  # 每期中奖额度信息
KEY_PERIOD_STATUS = "period_status"  # 期数状态
KEY_PRIZE_NUMBER = "prize_number"  # 中奖号码
KEY_LOTTERY_USER = "lottery_user_info"  # 开奖时的信息
KEY_REDEMPTION_USER = "redemption"  # 兑奖时的信息
KEY_NUMBER_DRAWS = "now_number_draws"  # 投注期数

KEY_LAST_NUMBER_DRAWS = "last_number_draws"  # 最后一期的期数
KEY_CALUCLATION_NOTE = "calculation_note"  # 用以计算投注数
KEY_NUMBER_BETS_PEER_ISSUE = "Number_of_bets_per_issue"  # 每一期投注次数
KEY_USER_BETS = "user_bets"  # 允许用户的最大投注次数
KEY_FRIST_PRIZE_POOL = "first_prize_pool"  # 一等奖额度
KEY_SECOND_PRIZE_POOL = "second_prize_pool"  # 二等奖额度
KEY_THRID_PRIZE_POOL = "thrid_prize_pool"  # 三等奖额度

KEY_DRAWS_PID = "pid"
KEY_GAME_START_TIME = 1567267200
KEY_GAME_TIME_FOR_A_ROUND = 3600  # 3600 三天


def main(operation, args):
    if operation == 'init':
        return init()
    if operation == 'system_prize_pool_inject':
        if len(args) != 1:
            return False
        return system_prize_pool_inject(args[0])
    if operation == 'syspool':
        return syspool()
    if operation == 'withdraw_system_pool':
        if len(args) != 1:
            return False
        return withdraw_system_pool(args[0])
    if operation == "query_draws_pid":
        return query_draws_pid()
    if operation == "if_lottery":
        return if_lottery()
    if operation == "get_draw_calculation_note":
        if len(args) != 1:
            return False
        return get_draw_calculation_note(args[0])
    if operation == "get_pid":
        return get_pid()
    if operation == "withdraw_system_pool":
        if len(args) != 1:
            return False
        return withdraw_system_pool(args[0])
    if operation == "stake":
        if len(args) != 3:
            return False
        return stake(args[0], args[1], args[2])
    if operation == "stakepool":
        return stakepool()
    if operation == "query_users_number":
        if len(args) != 2:
            return False
        return query_users_number(args[0], args[1])
    if operation == "query_users_number_amount":
        if len(args) != 3:
            return False
        return query_users_number_amount(args[0], args[1], args[2])
    if operation == "query_draws_lottery_user":
        if len(args) != 1:
            return False
        return query_draws_lottery_user(args[0])
    if operation == "draw":
        return draw()
    if operation == "query_amount_award":
        if len(args) != 1:
            return False
        return query_amount_award(args[0])
    if operation == "withdraw":
        if len(args) != 1:
            return False
        return withdraw(args[0])
    if operation == "set_event_pool":
        if len(args) != 1:
            return False
        return set_event_pool(args[0])
    if operation == "ppool":
        return ppool()
    if operation == "query_prize_number":
        if len(args) != 1:
            return False
        return query_prize_number(args[0])
    if operation == "query_user_invitation_code":
        if len(args) != 1:
            return False
        return query_user_invitation_code(args[0])
    if operation == "query_invitation_code_user":
        if len(args) != 1:
            return False
        return query_invitation_code_user(args[0])
    if operation == "get_redemption_information":
        if len(args) != 2:
            return False
        return get_redemption_information(args[0], args[1])
    if operation == "query_invitee":
        if len(args) != 1:
            return False
        return query_invitee(args[0])
    if operation == "query_my_inviter":
        if len(args) != 1:
            return False
        return query_my_inviter(args[0])
    if operation == "invitation_code_generation":
        return invitation_code_generation()
    if operation == "owner":
        return owner()
    if operation == "change_owner":
        if len(args) != 1:
            return False
        return change_owner(args[0])
    if operation == "issue":
        return issue()
    if operation == "lastissue":
        return lastissue()
    if operation == 'contractKeys':
        return contract_keys()
    if operation == "get_period_generation":
        return get_period_generation()
    if operation == "get_stake_account":
        if len(args) != 1:
            return False
        return get_stake_account(args[0])
    if operation == "get_periods_exceeds":
        if len(args) != 2:
            return False
        return get_periods_exceeds(args[0], args[1])
    if operation == "contractAccount":
        return contractAccount()
    if operation == "query_bets_note":
        if len(args) != 2:
            return False
        return query_bets_note(args[0], args[1])
    if operation == "get_promotion_reward":
        if len(args) != 1:
            return False
        return get_promotion_reward(args[0])
    if operation == "get_stake_issue":
        if len(args) != 1:
            return False
        return get_stake_issue(args[0])
    return False


def init():
    if Get(KEY_OWNER):
        return False

    Put(KEY_OWNER, OWNER)  # 添加owner 地址
    Put(KEY_NUMBER_DRAWS, get_period_generation())  # 当前期数 ,格式：20190925
    note_key = concat(Get(KEY_NUMBER_DRAWS), KEY_CALUCLATION_NOTE)
    Put(note_key, 0)  # 投注数
    key = concat(Get(KEY_NUMBER_DRAWS), KEY_DRAWS_PID)
    Put(key, get_pid())  # 初始期数的pid
    return True


def contractAccount():  # 合约的资金账户地址
    return ContractAccAddressGet()


def owner():  # 获取 owner 地址
    return Get(KEY_OWNER)


def change_owner(address):  # 改变 owner 地址
    if not IsValid(address):
        raise Exception("地址格式错误")
    if GetTxSender() != Get(KEY_OWNER):
        raise Exception("请使用 owner 地址调用")
    Put(KEY_OWNER, address)
    return True


def issue():  # 返回当前期数
    return Get(KEY_NUMBER_DRAWS)


def contract_keys():
    return ["owner:string", "issue:string", "syspool:integer", "stakepool:integer", "ppool:integer",
            "contractAccount:string"]


def query_draws_pid():  # 查询当前期数对应的pid
    number_draws = Get(KEY_NUMBER_DRAWS)  # 当前期数
    key = concat(number_draws, KEY_DRAWS_PID)
    return Get(key)


def lastissue():      # 最后一期期数
    last_draw = GetArray(KEY_LAST_NUMBER_DRAWS)[0]
    return last_draw


def if_lottery():  # 判断是否可以开奖
    rd = Get(KEY_NUMBER_DRAWS)  # 当前期
    note_key = concat(rd, KEY_CALUCLATION_NOTE)         # 这一期的的投注次数
    notes = Get(note_key)
    pid = get_pid()  # 当前的pid
    if notes > 0 and pid > query_draws_pid():  # 判断当前期数的pid 是不是还未动，因为pid是个递增的 并且判断当前是否有人投注
        return True
    return False


def get_draw_calculation_note(number_draws):  # 查询期数的总共投注次数
    note_key = concat(number_draws, KEY_CALUCLATION_NOTE)
    return Get(note_key)


def get_pid():  # 获取当前期数pid，主要用于判断是否已经过了一小时
    time = GetTime()
    pid = ((time - KEY_GAME_START_TIME) - (
                time - KEY_GAME_START_TIME) % KEY_GAME_TIME_FOR_A_ROUND) / KEY_GAME_TIME_FOR_A_ROUND
    return pid
    # 返回是个int


def system_prize_pool_inject(amount):  # 给系统奖池授予额度
    sender = GetTxSender()
    if BalanceOf(sender, [GARD_DENOM])[0] < amount:  # 判断余额是否足够初始化
        raise Exception("余额不足")

    sys_pool = Get(KEY_SYSTEM_POOL)
    if not sys_pool:
        ContractBalanceInject(Get(KEY_OWNER), GARD_DENOM, amount)
        Put(KEY_SYSTEM_POOL, amount)  # 记录系统奖池额度
        return True

    balance_amount = sys_pool + amount
    ContractBalanceInject(sender, GARD_DENOM, balance_amount)
    Put(KEY_SYSTEM_POOL, balance_amount)  # 记录总的奖池额度
    return True


def syspool():  # 查询系统奖池额度
    return Get(KEY_SYSTEM_POOL)


def withdraw_system_pool(amount):  # 取回系统奖池额度
    if GetTxSender() != Get(KEY_OWNER):
        raise Exception("请使用合约 owner 地址调用")

    if amount < 0:
        raise Exception("请输入正确的金额")

    balance_amount = syspool() - amount
    if balance_amount < 0:
        raise Exception("系统奖池余额不足")
    ContractBalanceSend(Get(KEY_OWNER), GARD_DENOM, amount)
    key = concat(KEY_SYSTEM_POOL, ContractAccAddressGet())
    Put(key, balance_amount)
    return True


def stake(number, amount, invitation_code):  # 用户投注
    if len(number) != 3:
        raise Exception("请输入正确的投注号码")
    if amount < 10000 * GARD_FACTOR:
        raise Exception("每次投注不能少于 10000gard")
    if if_lottery():
        raise Exception('当前期已经结束，处于开奖期，前往开奖')

    sender_address = GetTxSender()  # 当前调用地址
    if BalanceOf(sender_address, [GARD_DENOM])[0] < 10000 * GARD_FACTOR:
        raise Exception("账户余额不足投注")

    now_time = GetTime()  # 当前时间
    rd = Get(KEY_NUMBER_DRAWS)  # 当前期数
    user_bets_key = concat(KEY_USER_BETS, sender_address)  # 用户投注次数
    user_bets = Get(user_bets_key)

    if not user_bets:
        Put(user_bets_key, 1)
    else:
        if user_bets >= 3:
            raise Exception("当前用户投注次数超过三次")
        else:
            Put(user_bets_key, user_bets + 1)

    now_user_pool = stakepool()  # 当前用户池额度
    if not now_user_pool:
        Put(KEY_USER_POOL, amount)
    else:
        Put(KEY_USER_POOL, amount + now_user_pool)  # 记录每一期的用户池额度

    note_key = concat(rd, KEY_CALUCLATION_NOTE)
    num_note = Get(note_key)  # 获取投注数
    now_note = num_note + 1  # 每个用户投注一次，次数增加一次
    Put(note_key, now_note)  # 记录每一期的总的投注数
    # 投注数每次都增加，避免出现一个过大的列表

    betting_record_key = concat(concat(KEY_NUMBER_BETS_PEER_ISSUE, rd), str(now_note))  # 每一期的投注记录 key

    user_info = [str(now_time), sender_address, number, str(amount)]  # 保存为一个数组
    Assert(user_info[3] == str(amount), "erro")        # 输出address
    PutArray(betting_record_key, user_info)  # 记录投注记录

    number_key = concat(concat(rd, KEY_BETTING_NUMBER), sender_address)  # 用户的投注号码
    amount_key = concat(concat(concat(rd, KEY_BETTING_AMOUNT), number), sender_address)  # 记录用户投注的金额
    stake_all_key = concat(KEY_MY_ALL_STAKE, sender_address)  # 我所有的投注记录，只记录三天以内的

    stake_list = GetArray(stake_all_key)
    if len(stake_list) == 0:
        ls = []
        ls.append(rd)
        PutArray(stake_all_key, ls)  # 记录我的投注记录期号
    else:
        periods_exceeds_list = get_periods_exceeds(sender_address, rd)  # 返回去掉三天外的数组
        PutArray(stake_all_key, periods_exceeds_list)

    numbers = GetArray(number_key)
    if len(numbers) == 0:
        PutArray(number_key, [number])  # 记录用户的投注号码
        Put(amount_key, amount)  # 记录用户对这个号码的投注金额
    else:
        ls = []
        existed = False
        for i in range(len(numbers)):
            ls.append(numbers[i])
            if numbers[i] == number:
                balance = query_users_number_amount(sender_address, rd, number)
                amount = balance + amount
                Put(amount_key, amount)
                existed = True
        if not existed:
            ls.append(number)
            PutArray(number_key, ls)
            Put(amount_key, amount)  # 记录用户对这个号码的投注金额

    invited_key = concat(KEY_INVITED_RECORD, sender_address)  # 被邀请记录
    invited = Get(invited_key)
    invitation_user = query_invitation_code_user(invitation_code)  # 生成邀请码的地址
    invitation_key = concat(KEY_INVITATION_RECORD, invitation_user)  # 上级邀请记录
    if len(invitation_code) == 4 and not invited and invitation_user and invitation_user != sender_address:
        Put(invited_key, invitation_user)  # 提交被邀请记录
        invitation_list_value = GetArray(invitation_key)
        invitation_list = []
        for i in range(len(invitation_list_value)):
            invitation_list.append(invitation_list_value[i])
        invitation_list.append(sender_address)
        PutArray(invitation_key, invitation_list)  # 提交邀请人的邀请记录，由于可以邀请很多人，所有是个列表

    stake_count_key = concat(KEY_MY_STAKE_COUNT, sender_address)  # 我的投注统计，包括投注的总 token，和获取奖励的总 token
    count_value = GetArray(stake_count_key)
    if len(count_value) == 0:
        PutArray(stake_count_key, [str(amount), str(0)])
    if len(count_value) == 2:
        betting_amount = int(count_value[0])  # 总共投注
        reward_amount = int(count_value[1])  # 获得奖励
        PutArray(stake_count_key, [str(betting_amount + amount), str(reward_amount)])  # 提交自己投注记录

    ContractBalanceInject(sender_address, GARD_DENOM, amount)
    return True


def stakepool():  # 查询用户奖池额度
    return Get(KEY_USER_POOL)


def query_users_number(sender_address, rd):  # 查询该地址对应期数，查询用户的所有投注号码
    if not IsValid(sender_address):
        raise Exception("Incorrect address format.")
    number_key = concat(concat(rd, KEY_BETTING_NUMBER), sender_address)
    return GetArray(number_key)  # 返回一个列表


def query_users_number_amount(sender_address, rd, number):  # 根据该地址对应期数的用户投注号码，查询该号码的投注金额
    if not IsValid(sender_address):
        raise Exception("Incorrect address format.")
    amount_key = concat(concat(concat(rd, KEY_BETTING_AMOUNT), number), sender_address)
    return Get(amount_key)


def query_draws_lottery_user(draws):  # 根据期数，查询开奖人的记录
    draws_lettry_key = concat(KEY_LOTTERY_USER, draws)
    return GetArray(draws_lettry_key)


def draw():  # 开奖
    if not if_lottery():
        raise Exception("当前期数还在进行时")
    draws = Get(KEY_NUMBER_DRAWS)  # 当前期数
    sender = GetTxSender()
    if BalanceOf(sender, [GARD_DENOM])[0] <= 0:
        raise Exception("当前账户没有持有 GARD，无法开奖")

    sys_pool = syspool()  # 当前的系统奖池额度
    now_users_pool = stakepool()  # 当前用户池额度

    now_time = GetTime()                        # 获取当前时间
    prize_number = GetRand(3)                   # 生成中奖号码
    prize_key = concat(KEY_PRIZE_NUMBER, draws)
    Put(prize_key, prize_number)  # 记录每一期的中奖号码

    rand_amount = int(GetRand(4))  # 生成随机开奖奖励 amount
    lettry_amount = rand_amount * GARD_FACTOR

    draws_lettry_key = concat(KEY_LOTTERY_USER, draws)
    PutArray(draws_lettry_key, [sender, str(now_time), str(lettry_amount)])  # 增加开奖人记录

    now_users_pool = now_users_pool - lettry_amount
    Put(KEY_USER_POOL, now_users_pool)  # 先从用户奖池扣除这一部分开奖奖金

    # 算出当前中奖人数有多少个
    note_key = concat(draws, KEY_CALUCLATION_NOTE)
    note_num = Get(note_key)  # 当期有多少个投注数, 返回是个int
    fist_amount = 0  # 第一名的总额度
    second_amount = 0  # 二等奖中奖总token额度
    thrid_amount = 0  # 三等奖中奖总token额度
    for i in range(1, note_num + 1):
        betting_info = query_bets_note(draws, str(i))
        number = betting_info[2]
        if first_prize_match(draws, number):
            fist_amount = int(betting_info[3]) + fist_amount
            continue
        if second_prize_match(draws, number):
            second_amount = int(betting_info[3]) + second_amount
            continue
        if thrid_prize_match(draws, number):
            thrid_amount = int(betting_info[3]) + thrid_amount
            continue

    award_key = concat(draws, KEY_AMOUNT_EACH_AWARD)  # 中奖额度信息
    PutArray(award_key, [str(sys_pool), str(now_users_pool), str(fist_amount), str(second_amount), str(thrid_amount)])  # 记录每一期的中奖额度信息

    PutArray(KEY_LAST_NUMBER_DRAWS, [draws, str(now_time)])  # 最后一期期数和期数结束时间

    draws = get_period_generation()
    Put(KEY_NUMBER_DRAWS, draws)  # 期数变更

    key = concat(draws, KEY_DRAWS_PID)
    now_pid = get_pid()
    Put(key, now_pid)  # 更改这期的pid

    ContractBalanceSend(sender, GARD_DENOM, lettry_amount)  # 给开奖人奖金
    return True


def query_bets_note(draws, notes):              # 返回对应期数和对应注数的信息
    betting_record_key = concat(concat(KEY_NUMBER_BETS_PEER_ISSUE, draws), notes)
    betting_info = GetArray(betting_record_key)
    return betting_info


def query_amount_award(draws):  # 查询每一期的中奖额度信息
    award_key = concat(draws, KEY_AMOUNT_EACH_AWARD)
    return GetArray(award_key)


def withdraw(draws):  # 根据期数兑奖
    sender = GetTxSender()
    now_draws = Get(KEY_NUMBER_DRAWS)  # 当前期数
    time = GetTime()  # 当前时间
    last_number = GetArray(KEY_LAST_NUMBER_DRAWS)
    if len(last_number) == 0:
        raise Exception("当前期还无法兑奖")
    last_draws_time = int(last_number[1])  # 最后一期时间
    if int(draws) >= int(now_draws):
        raise Exception("当前期无法兑奖")

    if len(query_users_number(sender, draws)) == 0:
        raise Exception("当前期数没有投注")

    if time - last_draws_time >= 60 * 60 * 24 * 1:              # 计算是否超过一天
        raise Exception("当前已经超过一天未兑奖，无法兑现")

    amount_award_list = query_amount_award(draws)               # 查询每一期的中奖额度信息
    lottery_sys_pool = int(amount_award_list[0])                     # 开奖时的系统池额度
    lottery_users_pool = int(amount_award_list[1])                   # 开奖时的用户池额度
    fist_pool_amount = int(amount_award_list[2])                     # 开奖时候的一等奖额度
    second_pool_amount = int(amount_award_list[3])                   # 开奖时候的二等奖额度
    thrid_pool_amount = int(amount_award_list[4])                    # 开奖时候的三等奖额度

    numbers = query_users_number(sender, draws)                 # 用户投注的所有号码
    withdraws_all_amount = 0                                    # 应该获取到的所有奖金额度
    user_pool_amount = 0                                        # 应该要减去的用户奖池额度
    sys_pool_amount = 0                                         # 应该要减去的系统奖池额度

    for num in numbers:  # 遍历所有号码
        if first_prize_match(draws, num):
            fist_amount = query_users_number_amount(sender, draws, num)
            withdraws_fist_amount = fist_amount * lottery_users_pool / 10 * 4 / fist_pool_amount + lottery_sys_pool / 1000
            user_pool_amount = user_pool_amount + fist_amount * lottery_users_pool / 10 * 4 / fist_pool_amount
            sys_pool_amount = sys_pool_amount + lottery_sys_pool / 1000
            withdraws_all_amount = withdraws_all_amount + withdraws_fist_amount
            continue
        if second_prize_match(draws, num):
            second_amount = query_users_number_amount(sender, draws, num)
            withdraw_second_amount = second_amount * lottery_users_pool / 10 * 2 / second_pool_amount
            withdraws_all_amount = withdraws_all_amount + withdraw_second_amount
            user_pool_amount = user_pool_amount + withdraw_second_amount
            continue
        if thrid_prize_match(draws, num):
            thrid_amount = query_users_number_amount(sender, draws, num)
            withdraws_thrid_amount = thrid_amount * lottery_users_pool / 10 * 1 / thrid_pool_amount
            withdraws_all_amount = withdraws_all_amount + withdraws_thrid_amount
            user_pool_amount = user_pool_amount + withdraws_thrid_amount
            continue

    if withdraws_all_amount > 0:                    # 如果中奖则给其转账,并判断邀请逻辑
        inviter_address = query_my_inviter(sender)  # 上级地址
        event_pool = ppool()                 # 查询活动奖池额度
        sys_pool = syspool()                     # 查询系统奖池额度
        user_pool = stakepool()              # 查询活动奖池
        if inviter_address and event_pool > 0:          # 如果存在邀请者，并或活动奖池大于0

            rd = int(GetRand(1))  # 随机字符串
            pted_event_amount = event_pool / 1000 + event_pool * rd / 1000  # 分配随机 0.1% 到 1% 不等

            sr_key = concat(KEY_SHARED_REWARD, sender)                      # 被邀请的被推广奖励
            sender_reward_list = GetArray(sr_key)
            if len(sender_reward_list) == 0:
                PutArray(sr_key, [str(0), str(pted_event_amount)])
            else:
                promotion_amount = sender_reward_list[0]  # 推广奖励
                promoted_amount = int(sender_reward_list[1])  # 被推广奖励
                PutArray(sr_key, [promotion_amount, str(promoted_amount + pted_event_amount)])  # 提交自己的被推广奖励

            rd = int(GetRand(1))  # 随机字符串
            pro_event_amount = event_pool / 1000 + event_pool * rd / 1000           # 分配随机 0.1% 到 1% 不等

            sr_key = concat(KEY_SHARED_REWARD, inviter_address)                     # 推广者的推广奖励
            invited_reward_list = GetArray(sr_key)                        # 邀请者
            if len(invited_reward_list) == 0:
                PutArray(sr_key, [str(pro_event_amount), str(0)])
            else:
                promotion_amount = int(invited_reward_list[0])  # 推广奖励
                promoted_amount = invited_reward_list[1]  # 被推广奖励
                PutArray(sr_key, [str(promotion_amount + pro_event_amount), promoted_amount])  # 提交推广者的推广奖励

            ContractBalanceSend(sender, GARD_DENOM, pted_event_amount)                       # 给投注人转入被邀请奖励
            ContractBalanceSend(inviter_address, GARD_DENOM, pro_event_amount)              # 给邀请人转推广奖励

            now_event_pool = event_pool - pted_event_amount - pro_event_amount
            Put(KEY_EVENT_POOL, now_event_pool)                                                 # 更新活动奖池额度

        Put(KEY_USER_POOL, user_pool - user_pool_amount)     # 提交用户奖池
        Put(KEY_SYSTEM_POOL, sys_pool - sys_pool_amount)           # 提交系统奖池额度

        stake_count_key = concat(KEY_MY_STAKE_COUNT, sender)  # 我的投注统计，包括投注的总 token，和获取奖励的总 token
        count_value = GetArray(stake_count_key)
        betting_amount = count_value[0]  # 总共投注
        reward_amount = int(count_value[1])  # 获得奖励
        PutArray(stake_count_key, [betting_amount, str(reward_amount + withdraws_all_amount)])  # 提交自己投注记录

        key = concat(concat(KEY_REDEMPTION_USER, draws), sender)  # 兑奖信息
        PutArray(key, [str(time), str(withdraws_all_amount)])  # 提交用户的兑奖信息

        ContractBalanceSend(sender, GARD_DENOM, withdraws_all_amount)  # 给投注人转入获取的奖励
        return True
    else:
        raise Exception("当前投注没有中奖")


def get_promotion_reward(address):  # 查询推广奖励
    sr_key = concat(KEY_SHARED_REWARD, address)
    return GetArray(sr_key)  # 我的推广奖励，我被推广的奖励


def get_redemption_information(sender_address, draws):  # 查询该地址对应期数的兑奖信息
    if not IsValid(sender_address):
        raise Exception("Incorrect address format.")
    key = concat(concat(KEY_REDEMPTION_USER, draws), sender_address)  # 兑奖信息
    return GetArray(key)


def set_event_pool(amount):  # 设立活动奖池
    sender_address = GetTxSender()
    if BalanceOf(sender_address, [GARD_DENOM])[0] < amount:  # 判断余额是否足够初始化
        raise Exception("余额不足")
    event_pool = Get(KEY_EVENT_POOL)
    if not event_pool:
        ContractBalanceInject(sender_address, GARD_DENOM, amount)
        Put(KEY_EVENT_POOL, amount)
        return True
    balance_amount = event_pool + amount
    Put(KEY_EVENT_POOL, balance_amount)
    ContractBalanceInject(sender_address, GARD_DENOM, balance_amount)
    return True


def ppool():  # 查询活动奖池的额度
    return Get(KEY_EVENT_POOL)


def query_prize_number(draws):  # 根据期数查询中奖号码
    key = concat(KEY_PRIZE_NUMBER, draws)
    return Get(key)


def query_user_invitation_code(sender):  # 查询地址查看生成的邀请码
    if not IsValid(sender):
        raise Exception("Incorrect address format.")
    key = concat(KEY_INVITATION_CODE, sender)
    return Get(key)


def query_invitation_code_user(invitation_code):  # 根据邀请码，查询生成邀请码的地址
    key = concat(KEY_INVITATION_CODE, invitation_code)
    return Get(key)


def query_invitee(sender_address):  # 查询被该地址邀请的人
    if not IsValid(sender_address):
        raise Exception("Incorrect address format.")
    key = concat(KEY_INVITATION_RECORD, sender_address)
    return GetArray(key)


def query_my_inviter(sender_address):  # 查询该地址的上级邀请人
    if not IsValid(sender_address):
        raise Exception("Incorrect address format.")
    key = concat(KEY_INVITED_RECORD, sender_address)
    return Get(key)


def invitation_code_generation():  # 邀请码生成
    sender = GetTxSender()  # 获取当前操作人
    for i in range(5, len(sender)):
        invitation_code = concat(concat(sender[i], sender[i+1]), concat(sender[i+2], sender[i+3]))
        if query_invitation_code_user(invitation_code):  # 判断该邀请码是否已经有归属地址
            continue
        else:
            key = concat(KEY_INVITATION_CODE, sender)
            Put(key, invitation_code)  # 提交用户的邀请码信息
            key = concat(KEY_INVITATION_CODE, invitation_code)
            Put(key, sender)  # 提交邀请码对应的人的信息
            break
    return True
    # if query_user_invitation_code(sender):
    #     raise Exception("当前地址已经生成过邀请码")
    # invitation_code = GetRand(4)  # 获取邀请码
    # while True:
    #     if query_invitation_code_user(invitation_code):  # 判断该邀请码是否已经有归属地址
    #         invitation_code = GetRand(4)
    #         continue
    #     else:
    #         key = concat(KEY_INVITATION_CODE, sender)
    #         Put(key, invitation_code)  # 提交用户的邀请码信息
    #         key = concat(KEY_INVITATION_CODE, invitation_code)
    #         Put(key, sender)  # 提交邀请码对应的人的信息
    #         break
    # return True


def first_prize_match(draws, number):  # 一等奖匹配规则
    prize_number = query_prize_number(draws)  # 期数的中奖号码
    if prize_number == number:
        return True
    return False


def second_prize_match(draws, number):  # 二等奖匹配规则
    prize_len = len(number)  # prize_len == 3
    prize_number = query_prize_number(draws)
    result = False

    for i in range(prize_len):
        if i < prize_len - 1:
            if substr(number, i, 2) == substr(prize_number, i, 2):
                result = True
                break
        else:
            if substr(number, i, 1) == substr(prize_number, i, 1) and substr(number, 0, 1) == substr(prize_number, 0,
                                                                                                     1):
                result = True
                break
    return result


def thrid_prize_match(draws, number):  # 三等奖匹配规则
    prize_len = len(number)  # prize_len == 3
    prize_number = query_prize_number(draws)
    result = False
    for i in range(prize_len):
        if substr(number, i, 1) == substr(prize_number, i, 1):
            result = True
            break
    return result


def get_period_generation():  # 期数生成器
    now_time = GetTime()
    now_time = TimeFormat(now_time)  # 格式 2019-09-25 17:15:30
    time = split(now_time, " ")  # 分成两个元素
    time_01 = time[0]  # 年月日
    time_02 = time[1]  # 分时秒
    time_01 = split(time_01, "-")
    time_02 = split(time_02, ":")
    a = join("", time_01)
    b = time_02[0]
    period = concat(a, b)  # 拼接
    return period


def get_stake_account(address):  # 我的投注统计
    stake_count_key = concat(KEY_MY_STAKE_COUNT, address)
    return GetArray(stake_count_key)


def get_stake_issue(address):           # 我的投注列表
    stake_all_key = concat(KEY_MY_ALL_STAKE, address)
    return GetArray(stake_all_key)  # 期数列表


def get_periods_exceeds(address, rd):  # 返回一个三天内的投注列表
    stake_all_key = concat(KEY_MY_ALL_STAKE, address)  # 我所有的投注期号记录，只记录三天以内的
    stake_all_value = GetArray(stake_all_key)  # 期数列表

    for i in range(len(stake_all_value)):
        if int(rd) - int(stake_all_value[i]) > 100 or rd == stake_all_value[i]:                 # 大于1天或者有重复的
            stake_all_value = list_remove_elt(stake_all_value, stake_all_value[i])             # 每次循环判断是否大于三天，然后去除赋值
    return stake_all_value.append(rd)
