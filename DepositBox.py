Cversion = '1.0.0'

from hashgard.interop.System.Storage import Get, Put
from hashgard.interop.System.Runtime import GetTxSender, GetTime
from hashgard.vmop.Builtins import concat
from hashgard.interop.System.Account import IsValid
from hashgard.interop.System.Bank import ContractAccAddressGet, ContractBalanceSend, ContractBalanceInject, BalanceOf

GARD_DENOM = 'agard'
GARD_FACTOR = 1000000000000000000
OWNER = 'gard1lptjywa93atglpkwzexn7s59l6wngf705jz0ad'

BOX_NAME = "box_name"  # 存款盒子名称
BOX_BOTTOM_LINE = 0 * GARD_FACTOR  # 最低总存款条件
BOX_CEILING = 10000 * GARD_FACTOR  # 存款盒子的最多存款量
BOX_PRICE = 10 * GARD_FACTOR  # 存款盒子的每份最少所存量，存款总量，用户所存数必须是此值的倍数
BOX_INTEREST = 88 * GARD_FACTOR  # 存款盒子的利息的种类和数量
BOX_START_TIME = 1571652000  # 用户可以存入存款盒子的时间。利息必须在接受存款时间之前，注入到存款盒子中
BOX_LOCK_TIME = 1571652300  # 存款盒子的开始计息的时间
BOX_END_TIME = 1571652600  # 存款盒子到期交割本金和利息时间
BOX_TRANSFER_ON = False  # 用户存款后的存款凭证是否可以进行交易, 默认是关闭，一旦打开不能关闭

KEY_BOX_STATUS = "box_status"  # 存款盒子状态，分别为发行期 issue , 存款吸纳期 deposit， 锁定期 locking
ISSUE_STATUS = "issue"  # 发行期
DEPOSIT_STATUS = "deposit"  # 存款吸纳期
LOCK_STATUS = "locking"  # 锁定期
BOX_FAILED = "failed"
BOX_END = "end"

KEY_OWNER = OWNER
KEY_BOX_TRANSFER_ON = BOX_TRANSFER_ON
KEY_BOX_INTEREST = "interest_balance"  # 利息数量
KEY_BOX_DEPOSIT_AMOUNT = "deposit_amount"  # 存款数量

KEY_USER_INJECT_INTEREST = "user_interest"  # 用户注入的利息
KEY_USER_DEPOSIT_AMOUNT = "user_deposit_amount"  # 用户的存款数量

KEY_USER_RECEIVE = "user_receive"  # 用户取出的利益

KEY_ORG = "org"
KEY_WEBSITE = "website"
KEY_LOGO = "logo"
KEY_INTRO = "intro"


def main(operation, args):
    if operation == "contractAccount":
        return contractAccount()
    if operation == "creat_box":
        return creat_box()
    if operation == "owner":
        return owner()
    if operation == "name":
        return name()
    if operation == "bottom_line":
        return bottom_line()
    if operation == "ceiling":
        return ceiling()
    if operation == "price":
        return price()
    if operation == "transfer_on":
        return transfer_on()
    if operation == "interest":
        return interest()
    if operation == "start_time":
        return start_time()
    if operation == "lock_time":
        return lock_time()
    if operation == "end_time":
        return end_time()
    if operation == 'contractKeys':
        return contract_keys()
    if operation == "description":
        if len(args) != 4:
            raise Exception("缺少参数")
        return description(args[0], args[1], args[2], args[3])
    if operation == "org":
        return org()
    if operation == "website":
        return website()
    if operation == "logo":
        return logo()
    if operation == 'intro':
        return intro()
    if operation == "query_interest_balance":
        return query_interest_balance()
    if operation == "query_user_inject_interest":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_inject_interest(args[0])
    if operation == "query_deposit_amount":
        return query_deposit_amount()
    if operation == "query_user_deposit_amount":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_deposit_amount(args[0])
    if operation == "query_box_status":
        return query_box_status()
    if operation == "interest_injection":
        if len(args) != 1:
            raise Exception("缺少参数")
        return interest_injection(args[0])
    if operation == "interest_withdraw":
        if len(args) != 1:
            raise Exception("缺少参数")
        return interest_withdraw(args[0])
    if operation == "deposit":
        if len(args) != 1:
            raise Exception("缺少参数")
        return deposit(args[0])
    if operation == "redeem":
        if len(args) != 1:
            raise Exception("缺少参数")
        return redeem(args[0])
    if operation == "update_box_transfer_on":
        return update_box_transfer_on()
    if operation == "box_transfer":
        if len(args) != 1:
            raise Exception("缺少参数")
        return box_transfer(args[0])
    if operation == "withdraw":
        return withdraw()
    if operation == "query_user_profit":
        if len(args) != 1:
            raise Exception("缺少参数")
        return query_user_profit(args[0])
    return False


def contractAccount():
    return ContractAccAddressGet()


def creat_box():  # 创建盒子，即 init
    if Get(KEY_OWNER):
        raise Exception("已经创建过")

    Put(KEY_OWNER, OWNER)  # 合约 owner
    Put(KEY_BOX_TRANSFER_ON, BOX_TRANSFER_ON)  # 用户存款后的存款凭证是否可以进行交易
    return True


def owner():  # 查看 owner 地址
    return Get(KEY_OWNER)


def name():  # 盒子名称
    return BOX_NAME


def bottom_line():  # 查看最低总存款条件
    return BOX_BOTTOM_LINE


def ceiling():  # 查看存款盒子的最多存款量
    return BOX_CEILING


def price():  # 查看存款盒子的每份最少所存量
    return BOX_PRICE


def transfer_on():  # 查看用户存款后的存款凭证是否可以进行交易
    return Get(KEY_BOX_TRANSFER_ON)


def interest():  # 查看存款盒子的最大利息数量
    return BOX_INTEREST


def start_time():  # 查询用户可以存入存款盒子的时间。利息必须在接受存款时间之前，注入到存款盒子中
    return BOX_START_TIME


def lock_time():  # 查询存款盒子的开始计息的时间
    return BOX_LOCK_TIME


def end_time():  # 查询存款盒子到期交割本金和利息时间
    return BOX_END_TIME


def contract_keys():
    return ["contractAccount:string", "owner:string", "name:string", "interest:integer", "bottom_line:integer",
            "ceiling:integer",
            "price:integer", "start_time:integer", "lock_time:integer", "end_time:integer", "transfer_on:bool",
            "org:string", "website:string", "logo:string", "intro:string"]


def description(var_org, var_website, var_logo, var_intro):  # 添加描述
    sender = GetTxSender()
    if Get(KEY_OWNER) != sender:
        raise Exception("请使用 owner 账户给盒子更改描述")
    Put(KEY_ORG, var_org)
    Put(KEY_WEBSITE, var_website)
    Put(KEY_LOGO, var_logo)
    Put(KEY_INTRO, var_intro)
    return True


def org():  # 返回描述标题
    return Get(KEY_ORG)


def website():  # 返回描述链接
    return Get(KEY_WEBSITE)


def logo():  # 返回 logo 链接
    return Get(KEY_LOGO)


def intro():  # 返回介绍
    return Get(KEY_INTRO)


def query_interest_balance():  # 查询当期盒子利息总额数量
    return Get(KEY_BOX_INTEREST)


def query_user_inject_interest(address):  # 查询用户注入的利息
    key = concat(KEY_USER_INJECT_INTEREST, address)
    return Get(key)


def query_deposit_amount():  # 查询当期盒子的存款数量
    return Get(KEY_BOX_DEPOSIT_AMOUNT)


def query_user_deposit_amount(address):  # 查询用户的存款数量
    key = concat(KEY_USER_DEPOSIT_AMOUNT, address)
    return Get(key)


def query_box_status():  # 查看盒子当前状态
    now_time = GetTime()
    interest_amount = query_interest_balance()
    deposit_amount = query_deposit_amount()

    if now_time <= BOX_START_TIME:  # 小于开始时间为可存入利息的发行期
        return ISSUE_STATUS
    if interest_amount == BOX_INTEREST and BOX_START_TIME < now_time <= BOX_LOCK_TIME:  # 利息等于该存入的利息，并且当前时间大于开始时间，小于开始计息的时间，为可存入存款的存款吸纳期
        return DEPOSIT_STATUS
    if deposit_amount > BOX_BOTTOM_LINE and BOX_LOCK_TIME < now_time <= BOX_END_TIME:  # 存款数量大于最小存款数，并且当前时间大于存款吸纳期，小于最后的结束时间，为存款的锁定期
        return LOCK_STATUS
    if interest_amount == BOX_INTEREST and deposit_amount > BOX_BOTTOM_LINE and now_time > BOX_END_TIME:  # 存款盒子结束，可以取出总收益
        return BOX_END

    return BOX_FAILED


def interest_injection(amount):  # 利息注入
    sender = GetTxSender()
    interest_balance = query_interest_balance()  # 查询盒子注入利息
    user_interest_amount = query_user_inject_interest(sender)  # 用户对盒子注入的利息
    user_inject_key = concat(KEY_USER_INJECT_INTEREST, sender)

    if BalanceOf(sender, [GARD_DENOM])[0] <= amount:
        raise Exception("余额不足")

    if query_box_status() != ISSUE_STATUS:
        raise Exception("当前不处于发行期")

    if amount > BOX_INTEREST:
        raise Exception("大于最大应存利息数")

    if not interest_balance:
        Put(KEY_BOX_INTEREST, amount)  # 记录利息
    else:
        sub = BOX_INTEREST - interest_balance
        if amount > sub:
            raise Exception("超过可存入的利息总额")
        else:
            Put(KEY_BOX_INTEREST, interest_balance + amount)

    if not user_interest_amount:  # 提交用户注入利息
        Put(user_inject_key, amount)
    else:
        Put(user_inject_key, user_interest_amount + amount)

    ContractBalanceInject(sender, GARD_DENOM, amount)  # 转账利息到合约地址

    return True


def interest_withdraw(amount):  # 利息取回
    sender = GetTxSender()
    user_interest_amount = query_user_inject_interest(sender)  # 用户对盒子注入的利息
    interest_balance = query_interest_balance()  # 盒子总利息
    user_inject_key = concat(KEY_USER_INJECT_INTEREST, sender)

    if not user_interest_amount or user_interest_amount == 0:
        raise Exception("没有存入利息")

    box_stauts = query_box_status()
    if box_stauts != BOX_FAILED and box_stauts != ISSUE_STATUS:
        raise Exception("当前盒子状态无法取回注入利息")

    if amount > user_interest_amount:
        raise Exception("取出金额大于注入的利息")
    Put(user_inject_key, user_interest_amount - amount)  # 更改用户的利息
    Put(KEY_BOX_INTEREST, interest_balance - amount)

    ContractBalanceSend(sender, GARD_DENOM, amount)  # 给其转入取出的利息

    return True


def deposit(amount):  # 存款
    sender = GetTxSender()

    if BalanceOf(sender, [GARD_DENOM])[0] <= amount:
        raise Exception("余额不足")

    if amount % BOX_PRICE != 0:
        raise Exception("存款必须是最少所存量的倍数")

    if query_box_status() != DEPOSIT_STATUS:
        raise Exception("当前不处于存款吸纳期，无法存款")

    if amount > BOX_CEILING:
        raise Exception("大于最大允许的存款量")

    deposit_amount = query_deposit_amount()  # 盒子存款总量
    if not deposit_amount:
        Put(KEY_BOX_DEPOSIT_AMOUNT, amount)
    else:
        sub = BOX_CEILING - deposit_amount
        if amount > sub:
            raise Exception("超过可存入的最大存款数")
        else:
            Put(KEY_BOX_DEPOSIT_AMOUNT, deposit_amount + amount)  # 提交存款盒子总量

    user_deposit_amount = query_user_deposit_amount(sender)
    user_deposit_key = concat(KEY_USER_DEPOSIT_AMOUNT, sender)
    if not user_deposit_amount:
        Put(user_deposit_key, amount)
    else:
        Put(user_deposit_key, user_deposit_amount + amount)  # 提交用户的的存款量

    ContractBalanceInject(sender, GARD_DENOM, amount)  # 给盒子转账

    return True


def redeem(amount):  # 赎回，取出存款
    sender = GetTxSender()
    box_deposit_amount = query_deposit_amount()  # 查询盒子的总存款
    user_deposit_amount = query_user_deposit_amount(sender)  # 查询该用户的存款
    user_deposit_key = concat(KEY_USER_DEPOSIT_AMOUNT, sender)

    box_stauts = query_box_status()
    if box_stauts != BOX_FAILED and box_stauts != DEPOSIT_STATUS:
        raise Exception("当前无法取出存款")

    if not user_deposit_amount or user_deposit_amount == 0:
        raise Exception("没有存款，无法取出")

    if amount > user_deposit_amount:
        raise Exception("剩余存款额度不足取出")

    Put(KEY_BOX_DEPOSIT_AMOUNT, box_deposit_amount - amount)  # 提交新的剩余存款额度
    Put(user_deposit_key, user_deposit_amount - amount)  # 提交新的用户存款额度
    ContractBalanceSend(sender, GARD_DENOM, amount)  # 给其转账

    return True


def update_box_transfer_on():  # 更改存款凭证是否可以交易
    sender = GetTxSender()
    if sender != Get(KEY_OWNER):
        raise Exception("请使用创建盒子的账户")

    transfer_status = transfer_on()
    if transfer_status:
        raise Exception("当前已经打开存款凭证可以交易状态，无法更改")

    Put(KEY_BOX_TRANSFER_ON, True)  # 更改为true

    return True


def box_transfer(to_address):  # 存款盒子凭证交易
    if not IsValid(to_address):
        raise Exception("请填写正确的地址")
    sender = GetTxSender()
    if not transfer_on():
        raise Exception("不允许存款凭证交易")

    box_status = query_box_status()
    if box_status != LOCK_STATUS:
        raise Exception("当前不允许交易存款凭证")

    sender_deposit_amount = query_user_deposit_amount(sender)  # 用户的存款
    if not sender_deposit_amount or sender_deposit_amount == 0:
        raise Exception("当前用户没有存款，无法转让")

    sender_deposit_key = concat(KEY_USER_DEPOSIT_AMOUNT, sender)  # 转让人
    to_address_deposit_key = concat(KEY_USER_DEPOSIT_AMOUNT, to_address)  # 接收人
    Put(sender_deposit_key, 0)  # 提交转让人的额度变成 0
    Put(to_address_deposit_key, sender_deposit_amount)  # 提交接收人的额度

    return True


def withdraw():  # 取出存款和利润
    sender = GetTxSender()
    box_status = query_box_status()

    if box_status != BOX_END:
        raise Exception("当前无法取出本金和利息")
    user_deposit_amount = query_user_deposit_amount(sender)

    if not user_deposit_amount or user_deposit_amount == 0:
        raise Exception("当前用户没有存款")

    if query_user_profit(sender) > 0:
        raise Exception("已经取出")

    box_interest = query_interest_balance()
    user_profit = user_deposit_amount * box_interest / BOX_CEILING  # 用户占利息的几成

    user_receive_key = concat(KEY_USER_RECEIVE, sender)
    Put(user_receive_key, user_profit)  # 更新用户利息获得

    ContractBalanceSend(sender, GARD_DENOM, user_deposit_amount + user_profit)  # 给用户转入存款和获得的利息

    return True


def query_user_profit(address):  # 查询用户已经获得利润
    if not IsValid(address):
        raise Exception("请填写正确的地址")
    user_receive_key = concat(KEY_USER_RECEIVE, address)
    return Get(user_receive_key)
