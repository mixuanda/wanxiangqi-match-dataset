# 字段允许清单与语义

正式机器契约见`schemas/public-synthetic.schema.json`；Python验证器拒绝任何未知字段。所有层级都禁止任意metadata、原始响应、文本备注和身份字段。对象中保留的字段必须显式存在；未知标量用null，未知棋盘/装备/汇总列表也用null，已观察为空才用空数组。

| 层级 | 允许字段 | 解释 |
|---|---|---|
| 数据集 | schema_version, origin, matches | origin只有synthetic/private_research；公开只接受synthetic |
| 对局 | sample_key, mode, patch, participants | sample_key是文件内局部键；不保存来源对局ID、时间和链接；patch未知不按日期猜测 |
| 参赛观察 | actor_key, selected, final_rank, chess_player, final_board, stages | actor_key只在局内关联，不是跨局玩家身份；final_rank是对局内名次，不是段位 |
| 阶段快照 | stage_index, phase, player_level, energy_left, hero_limit, board, card_summaries, auction | stage_index是已观察记录顺序，不保证连续游戏回合；phase明确战斗/拍卖/unknown |
| 棋子观察 | unit, level, quality, star, equipment, position | 英雄等级、品质、显式星级互相独立；缺星级不能由等级或品质推导 |
| 卡牌汇总 | kind, card, count | 获得/使用/移除摘要；不是购买、刷新、出售或输入顺序 |
| 拍卖源摘要 | card, reported_cost_energy, reported_shared_energy | 仅保留确有的源值；不是完整备选、全部出价或已验证赢家 |

棋手与棋子属于不同实体域，即使中文名称相同也不能合并。`player_level`只表示棋手的报告等级，不能用某个英雄level替代。`hero_limit`与UI容量的对应需单独验证，不代表手牌/背包空间。

`energy_left`可能是阶段结束值，不能默认视为决策前资金。负数必须保留并审查，不静默裁剪为0。跨模式的数值量级不能混用。

本版没有逐动作价格、时间戳、商店选项、手牌、刷新计数、点击回执或策略目标字段；缺失信息不能从卡牌摘要、最终阵容或最终等级贡献中倒推。

合成公开样例的关系键与标签强制使用`toy-`前缀，patch保持null，数值是人工编造。把真实数据的标记改为synthetic并不构成合成来源证明；维护者仍须人工审核。
