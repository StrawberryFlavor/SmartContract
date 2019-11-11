# SmartContract
基于 NeoVM 基础上改版的 Python 智能合约



### [InstantLotteryGame.py](./InstantLotteryGame.py)

时时彩合约



### [DepositBox.py](./DepositBox.py)

存款盒子合约



###  [BinGO](./BinGoGame.py)

用区块链的形式去实现的 bingo 小游戏，中奖（标记）号码连成一条线 即 Bingo

#### BinGo 游戏规则

1. 游戏频度：5分钟/期

2.  房间设计：1倍区，2倍区，5倍区，10倍区

3. 投注：购买一张宾果卡，参与游戏，随机产生 75 个号码。75个号码随机分布在5张宾果卡内
4.  产生 75 以内的 30 个随机数

4.  中奖规则：中奖（标记）号码连成一条线，通过系统验证后即中奖