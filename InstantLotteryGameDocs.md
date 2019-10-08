# 时时彩合约操作流程文档

合约地址为：`contractaf4e12578e579affc09dd434c8faee45c1060778`



### 查询合约详情：

```shell
hashgardcli query contract data contractaf4e12578e579affc09dd434c8faee45c1060778
```

返回：

```shell
{
  "stakepool": "0",														# 投注奖池
  "ppool": "10000000000000000000000000",								#活动奖池
  "contractAccount": "gard13zw723fud6an4rwrdawfpkw4z2gtfzjcl4l3m5",
  "contractAddress": "contractaf4e12578e579affc09dd434c8faee45c1060778",
  "owner": "gard1lptjywa93atglpkwzexn7s59l6wngf705jz0ad",				#合约 owner
  "issue": "2019093014",												#本期投注的期号
  "syspool": "10000000000000000000000000"								# 系统奖池
}
```



### 邀请

#### 生成邀请码

```shell
hashgardcli tx contract call contractaf4e12578e579affc09dd434c8faee45c1060778 "string:invitation_code_generation" --from $walletname -y
```

`--from` 后为自己操作得钱包账户名称



#### 查看自己生成的邀请码

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778 "string:query_user_invitation_code,[string:$walletaddress]"
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
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778 "string:query_invitation_code_user,[string:8343]"
```



#### 查询地址邀请的人

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778 "string:query_invitee,[string:gard1prylufu5q4q49h8ttzemlptj99czqc980y9vzg]"   --return array
```



#### 查询该地址的上级

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778 "string:query_my_inviter,[string:gard1lptjywa93atglpkwzexn7s59l6wngf705jz0ad]"
```



### 投注

```shell
hashgardcli tx contract call contractaf4e12578e579affc09dd434c8faee45c1060778 "string:stake, [string:$number,int:$amount,string:$code]" --from wind --gas 2000000 -y
```

填入参数分别为：投注号码（须为三位号码：如 ”012“），投注金额，邀请码



### 查询投注号码

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778  "string:query_users_number,[string:$walletaddress,string:$issue]"    --return array
```

参数依次为：查询的地址，期号

返回：

```shell
{
  "address": "contractaf4e12578e579affc09dd434c8faee45c1060778",
  "code": "string:query_users_number,[string:gard1xvn48vn3ljwk2d3vynv8ugkl373d93tfp9zae3,string:2019093021]",
  "data": "[888]"
}

```

返回的 data 中的参数为改期此地址投注的号码



### 查询指定期数投注号码的金额

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778  "string:query_users_number_amount,[string:$walletaddress,string:$issue,string:$number]"  --return integer
```

参数依次为：查询的地址，期号，和投注号码



### 开奖

```shell
hashgardcli tx contract call contractaf4e12578e579affc09dd434c8faee45c1060778 "string:draw" --from wind -y
```



### 查询开奖人记录

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778  "string:query_draws_lottery_user,[string:2019093021]"   --return array
```

参数为需要查询的指定期数

返回：

```shell
{
  "address": "contractaf4e12578e579affc09dd434c8faee45c1060778",
  "code": "string:query_draws_lottery_user,[string:2019093021]",
  "data": "[gard1xvn48vn3ljwk2d3vynv8ugkl373d93tfp9zae3,1570521673,1883000000000000000000]"
}
```

返回的 data 中的列表参数依次为：开奖地址，开奖时间，开奖奖励



### 查询指定期数的中奖额度信息

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778  "string:query_amount_award,[string:2019093021]"   --return array
```

参数为需要查询的指定期数

返回：

```shell
{
  "address": "contractaf4e12578e579affc09dd434c8faee45c1060778",
  "code": "string:query_amount_award,[string:2019093021]",
  "data": "[10000000000000000000000000,8117000000000000000000,0,10000000000000000000000,0]"
}
```

返回的 data 中的列表参数依次为：开奖时的系统奖池额度，开奖时的用户奖池额度，一等奖总共中奖投注额度，二等奖总共中奖投注额度，三等奖总共中奖投注额度



### 兑奖

```shell
hashgardcli tx contract call contractaf4e12578e579affc09dd434c8faee45c1060778 "string:withdraw,[string:$issue]" --from wind --gas 2000000 -y
```

参数为issue，即需要兑奖的期号，注：一天内未兑奖将无法兑奖



### 查询兑奖信息

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778  "string:get_redemption_information,[string:$walletaddress,string:$issue]"	 --return array
```

参数依次为：查询的地址，期号

返回：

```shell
{
  "address": "contractaf4e12578e579affc09dd434c8faee45c1060778",
  "code": "string:get_redemption_information,[string:gard1xvn48vn3ljwk2d3vynv8ugkl373d93tfp9zae3,string:2019093021]",
  "data": "[1570523965,1623400000000000000000]"
}
```

返回的 data 中的列表参数依次为：兑奖的时间戳，兑奖获得的奖励



### 我的投注统计

包括我的投注，和获奖统计

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778  "string:get_stake_account,[string:$walletaddress]"	 --return array
```



### 我的推广统计

包括我邀请的奖励统计，和被邀请奖励统计

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778  "string:get_promotion_reward,[string:$walletaddress]"  --return array
```



### 查询中奖号码

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778  "string:query_prize_number,[string:$issue]"
```

参数为要查询的期号



### 我的投注期数

```shell
hashgardcli query contract method contractaf4e12578e579affc09dd434c8faee45c1060778  "string:get_stake_issue,[string:$walletaddress]" --return array
```

参数为需要查询的钱包地址

