# 时时彩合约操作流程文档

合约地址为：`contractc0630e2b5e723370c1e4058dca7d94bb0b5905f8`



### 查询合约详情：

```shell
hashgardcli query contract data contract9e1d62a209d647131feaa2506f8f830f8eb691e5
```

返回：

```shell
{
  "stakepool": "0",														# 投注奖池
  "ppool": "10000000000000000000000000",								#活动奖池
  "contractAccount": "gard13zw723fud6an4rwrdawfpkw4z2gtfzjcl4l3m5",
  "contractAddress": "contract9e1d62a209d647131feaa2506f8f830f8eb691e5",
  "owner": "gard1lptjywa93atglpkwzexn7s59l6wngf705jz0ad",				#合约 owner
  "issue": "2019093014",												#本期投注的期号
  "syspool": "10000000000000000000000000"								# 系统奖池
}
```



### 邀请

#### 生成邀请码

```shell
hashgardcli tx contract call contract9e1d62a209d647131feaa2506f8f830f8eb691e5 "string:invitation_code_generation" --from $walletname -y
```

`--from` 后为自己操作得钱包账户名称



#### 查看自己生成的邀请码

```shell
hashgardcli query contract method contract9e1d62a209d647131feaa2506f8f830f8eb691e5 "string:query_user_invitation_code,[string:$walletaddress]"
```

`$walletaddress` 填入上述生成邀请码时候使用的钱包地址

返回：

```shell
{
  "address": "contract9e1d62a209d647131feaa2506f8f830f8eb691e5",
  "code": "string:query_user_invitation_code,[string:gard1prylufu5q4q49h8ttzemlptj99czqc980y9vzg]",
  "data": "8343"			#邀请码
}
```



#### 根据邀请码查看生成邀请码的地址

```shell
hashgardcli query contract method contract9e1d62a209d647131feaa2506f8f830f8eb691e5 "string:query_invitation_code_user,[string:8343]"
```



#### 查询地址邀请的人

```shell
hashgardcli query contract method contract9e1d62a209d647131feaa2506f8f830f8eb691e5 "string:query_invitee,[string:gard1prylufu5q4q49h8ttzemlptj99czqc980y9vzg]"   --return array
```



#### 查询该地址的上级

```shell
hashgardcli query contract method contract9e1d62a209d647131feaa2506f8f830f8eb691e5 "string:query_my_inviter,[string:gard1lptjywa93atglpkwzexn7s59l6wngf705jz0ad]"
```



### 投注

```shell
hashgardcli tx contract call contract9e1d62a209d647131feaa2506f8f830f8eb691e5 "string:stake, [string:$number,int:$amount,string:$code]" --from wind --gas 2000000 -y
```

填入参数分别为：投注号码（须为三位号码：如 ”012“），投注金额，邀请码



### 查询投注号码

```shell
hashgardcli query contract method contractc0630e2b5e723370c1e4058dca7d94bb0b5905f8  "string:query_users_number,[string:$walletaddress,string:$issue]"
```

参数依次为：查询的地址，期号



### 查询指定期数投注号码的金额

```shell
hashgardcli query contract method contractc0630e2b5e723370c1e4058dca7d94bb0b5905f8  "string:query_users_number_amount,[string:$walletaddress,string:$issue,string:$number]"  --return integer
```

参数依次为：查询的地址，期号，和投注号码



### 兑奖

```shell
hashgardcli tx contract call contract4ea98b7193fd5337dd09a4799ee1ffabd2483a97 "string:withdraw,[string:$issue]" --from wind --gas 2000000 -y
```

参数为issue，即需要兑奖的期号，注：一天内未兑奖将无法兑奖



### 查询兑奖信息

```shell
hashgardcli query contract method contract262ab8584fe027be0dde74043ad6944f69738240  "string:get_redemption_information,[string:$walletaddress,string:$issue]"
```

参数依次为：查询的地址，期号



### 我的投注统计

包括我的投注，和获奖统计

```shell
hashgardcli query contract method contract262ab8584fe027be0dde74043ad6944f69738240  "string:get_stake_account,[string:$walletaddress]"	 --return array
```



### 我的推广统计

包括我邀请的奖励统计，和被邀请奖励统计

```shell
hashgardcli query contract method contract052fab457101d60e8dd9d58481ce2d77d29d468b  "string:get_promotion_reward,[string:$walletaddress]"  --return array
```



### 查询中奖号码

```shell
hashgardcli query contract method contractc0630e2b5e723370c1e4058dca7d94bb0b5905f8  "string:query_prize_number,[string:$issue]"
```

参数为要查询的期号



