# TALIB & QA

talib是一个c的指标库, qa在1.2.0+ 版本对此进行了支持, 融入QAIndicator中




| TALIB   函数        | 描述                                                         | 所属类别            | QUANTAXIS支持 | 谷歌翻译名称                                |
| ------------------- | ------------------------------------------------------------ | ------------------- | ------------- | ------------------------------------------- |
| AD                  | Chaikin A/D Line                                             |                     | TRUE          | Chaikin A / D线                             |
| ADOSC               | Chaikin A/D Oscillator                                       |                     | TRUE          | Chaikin A / D振荡器                         |
| ADX                 | Average Directional Movement Index                           | Momentum Indicators | TRUE          | 平均方向运动指数                            |
| ADXR                | Average Directional Movement Index Rating                    | Momentum Indicators |               | 平均方向运动指数评级                        |
| APO                 | Absolute Price Oscillator                                    | Momentum Indicators |               | 绝对价格振荡器                              |
| AROON               | Aroon                                                        | Momentum Indicators |               | 阿隆                                        |
| AROONOSC            | Aroon Oscillator                                             | Momentum Indicators |               | Aroon Oscillator                            |
| ATR                 | Average True Range                                           |                     |               | 平均真实范围                                |
| AVGPRICE            | Average Price                                                |                     |               | 平均价格                                    |
| BBANDS              | Bollinger Bands                                              |                     |               | 布林带                                      |
| BETA                | Beta                                                         |                     |               | Beta版                                      |
| BOP                 | Balance Of Power                                             | Momentum Indicators |               | 力量的均衡                                  |
| CCI                 | Commodity Channel Index                                      | Momentum Indicators |               | 商品通道指数                                |
| CDL2CROWS           | Two Crows                                                    | Pattern Recognition | TRUE          | 两只乌鸦                                    |
| CDL3BLACKCROWS      | Three Black Crows                                            | Pattern Recognition | TRUE          | 三只黑乌鸦                                  |
| CDL3INSIDE          | Three Inside Up/Down                                         | Pattern Recognition | TRUE          | 三个内上/下                                 |
| CDL3LINESTRIKE      | Three-Line Strike                                            | Pattern Recognition | TRUE          | 三线罢工                                    |
| CDL3OUTSIDE         | Three Outside Up/Down                                        | Pattern Recognition | TRUE          | 三个外上/下                                 |
| CDL3STARSINSOUTH    | Three Stars In The South                                     | Pattern Recognition | TRUE          | 在南方的三颗星                              |
| CDL3WHITESOLDIERS   | Three Advancing White Soldiers                               | Pattern Recognition | TRUE          | 三位前进的白人士兵                          |
| CDLABANDONEDBABY    | Abandoned Baby                                               | Pattern Recognition | TRUE          | 被遗弃的婴儿                                |
| CDLADVANCEBLOCK     | Advance Block                                                | Pattern Recognition | TRUE          | 提前阻止                                    |
| CDLBELTHOLD         | Belt-hold                                                    | Pattern Recognition | TRUE          | 带保持                                      |
| CDLBREAKAWAY        | Breakaway                                                    | Pattern Recognition | TRUE          | 摆脱                                        |
| CDLCLOSINGMARUBOZU  | Closing Marubozu                                             | Pattern Recognition | TRUE          | 关闭Marubozu                                |
| CDLCONCEALBABYSWALL | Concealing Baby Swallow                                      | Pattern Recognition | TRUE          | 隐藏婴儿燕子                                |
| CDLCOUNTERATTACK    | Counterattack                                                | Pattern Recognition | TRUE          | 反击                                        |
| CDLDARKCLOUDCOVER   | Dark Cloud Cover                                             | Pattern Recognition | TRUE          | 暗云覆盖                                    |
| CDLDOJI             | Doji                                                         | Pattern Recognition | TRUE          | 十字星                                      |
| CDLDOJISTAR         | Doji Star                                                    | Pattern Recognition | TRUE          | 十字星                                      |
| CDLDRAGONFLYDOJI    | Dragonfly Doji                                               | Pattern Recognition | TRUE          | 蜻蜓十字星                                  |
| CDLENGULFING        | Engulfing Pattern                                            | Pattern Recognition | TRUE          | 吞噬模式                                    |
| CDLEVENINGDOJISTAR  | Evening Doji Star                                            | Pattern Recognition | TRUE          | 晚上十字星                                  |
| CDLEVENINGSTAR      | Evening Star                                                 | Pattern Recognition | TRUE          | 晚星                                        |
| CDLGAPSIDESIDEWHITE | Up/Down-gap side-by-side white lines                         | Pattern Recognition | TRUE          | 上/下间隙并排白线                           |
| CDLGRAVESTONEDOJI   | Gravestone Doji                                              | Pattern Recognition | TRUE          | 墓碑十字星                                  |
| CDLHAMMER           | Hammer                                                       | Pattern Recognition | TRUE          | 锤子                                        |
| CDLHANGINGMAN       | Hanging Man                                                  | Pattern Recognition | TRUE          | 挂人                                        |
| CDLHARAMI           | Harami Pattern                                               | Pattern Recognition | TRUE          | Harami模式                                  |
| CDLHARAMICROSS      | Harami Cross Pattern                                         | Pattern Recognition | TRUE          | Harami十字图案                              |
| CDLHIGHWAVE         | High-Wave Candle                                             | Pattern Recognition | TRUE          | 高波浪蜡烛                                  |
| CDLHIKKAKE          | Hikkake Pattern                                              | Pattern Recognition | TRUE          | Hikkake模式                                 |
| CDLHIKKAKEMOD       | Modified Hikkake Pattern                                     | Pattern Recognition | TRUE          | 修改了Hikkake模式                           |
| CDLHOMINGPIGEON     | Homing Pigeon                                                | Pattern Recognition | TRUE          | 归巢鸽                                      |
| CDLIDENTICAL3CROWS  | Identical Three Crows                                        | Pattern Recognition | TRUE          | 相同的三只乌鸦                              |
| CDLINNECK           | In-Neck Pattern                                              | Pattern Recognition | TRUE          | 颈部图案                                    |
| CDLINVERTEDHAMMER   | Inverted Hammer                                              | Pattern Recognition | TRUE          | 倒锤                                        |
| CDLKICKING          | Kicking                                                      | Pattern Recognition | TRUE          | 踢                                          |
| CDLKICKINGBYLENGTH  | Kicking - bull/bear determined by the longer marubozu        | Pattern Recognition | TRUE          | 踢 - 牛/熊由较长的marubozu决定              |
| CDLLADDERBOTTOM     | Ladder Bottom                                                | Pattern Recognition | TRUE          | 梯底                                        |
| CDLLONGLEGGEDDOJI   | Long Legged Doji                                             | Pattern Recognition | TRUE          | 长腿十字星                                  |
| CDLLONGLINE         | Long Line Candle                                             | Pattern Recognition | TRUE          | 长线蜡烛                                    |
| CDLMARUBOZU         | Marubozu                                                     | Pattern Recognition | TRUE          | Marubozu                                    |
| CDLMATCHINGLOW      | Matching Low                                                 | Pattern Recognition | TRUE          | 匹配低                                      |
| CDLMATHOLD          | Mat Hold                                                     | Pattern Recognition | TRUE          | Mat Hold                                    |
| CDLMORNINGDOJISTAR  | Morning Doji Star                                            | Pattern Recognition | TRUE          | 早上十字星                                  |
| CDLMORNINGSTAR      | Morning Star                                                 | Pattern Recognition | TRUE          | 晨星                                        |
| CDLONNECK           | On-Neck Pattern                                              | Pattern Recognition | TRUE          | 颈部图案                                    |
| CDLPIERCING         | Piercing Pattern                                             | Pattern Recognition | TRUE          | 穿孔模式                                    |
| CDLRICKSHAWMAN      | Rickshaw Man                                                 | Pattern Recognition | TRUE          | 人力车人                                    |
| CDLRISEFALL3METHODS | Rising/Falling Three Methods                                 | Pattern Recognition | TRUE          | 上升/下降三种方法                           |
| CDLSEPARATINGLINES  | Separating Lines                                             | Pattern Recognition | TRUE          | 分隔线                                      |
| CDLSHOOTINGSTAR     | Shooting Star                                                | Pattern Recognition | TRUE          | 射击之星                                    |
| CDLSHORTLINE        | Short Line Candle                                            | Pattern Recognition | TRUE          | 短线蜡烛                                    |
| CDLSPINNINGTOP      | Spinning Top                                                 | Pattern Recognition | TRUE          | 旋转陀螺                                    |
| CDLSTALLEDPATTERN   | Stalled Pattern                                              | Pattern Recognition | TRUE          | 停滞的模式                                  |
| CDLSTICKSANDWICH    | Stick Sandwich                                               | Pattern Recognition | TRUE          | 坚持三明治                                  |
| CDLTAKURI           | Takuri (Dragonfly Doji with very long lower shadow)          | Pattern Recognition | TRUE          | Takuri（具有很长阴影的蜻蜓十字星）          |
| CDLTASUKIGAP        | Tasuki Gap                                                   | Pattern Recognition | TRUE          | Tasuki Gap                                  |
| CDLTHRUSTING        | Thrusting Pattern                                            | Pattern Recognition | TRUE          | 推力模式                                    |
| CDLTRISTAR          | Tristar Pattern                                              | Pattern Recognition | TRUE          | 三星模式                                    |
| CDLUNIQUE3RIVER     | Unique 3 River                                               | Pattern Recognition | TRUE          | 独特的3河                                   |
| CDLUPSIDEGAP2CROWS  | Upside Gap Two Crows                                         | Pattern Recognition | TRUE          | 上行差距两乌鸦                              |
| CDLXSIDEGAP3METHODS | Upside/Downside Gap Three Methods                            | Pattern Recognition | TRUE          | 上行/下行差距三种方法                       |
| CMO                 | Chande Momentum Oscillator                                   |                     |               | Chande Momentum Oscillator                  |
| CORREL              | Pearson's Correlation Coefficient (r)                        |                     |               | 皮尔逊的相关系数（r）                       |
| DEMA                | Double Exponential Moving Average                            |                     |               | 双指数移动平均线                            |
| DX                  | Directional Movement Index                                   |                     |               | 定向运动指数                                |
| EMA                 | Exponential Moving Average                                   |                     |               | 指数移动平均线                              |
| HT_DCPERIOD         | Hilbert Transform - Dominant Cycle Period                    |                     |               | 希尔伯特变换 - 主导循环周期                 |
| HT_DCPHASE          | Hilbert Transform - Dominant Cycle Phase                     |                     |               | 希尔伯特变换 - 主导循环阶段                 |
| HT_PHASOR           | Hilbert Transform - Phasor Components                        |                     |               | 希尔伯特变换 - 相量分量                     |
| HT_SINE             | Hilbert Transform - SineWave                                 |                     |               | 希尔伯特变换 - SineWave                     |
| HT_TRENDLINE        | Hilbert Transform - Instantaneous Trendline                  |                     |               | 希尔伯特变换 - 瞬时趋势线                   |
| HT_TRENDMODE        | Hilbert Transform - Trend vs Cycle Mode                      |                     |               | 希尔伯特变换 - 趋势与循环模式               |
| KAMA                | Kaufman Adaptive Moving Average                              |                     |               | 考夫曼自适应移动平均线                      |
| LINEARREG           | Linear Regression                                            |                     |               | 线性回归                                    |
| LINEARREG_ANGLE     | Linear Regression Angle                                      |                     |               | 线性回归角度                                |
| LINEARREG_INTERCEPT | Linear Regression Intercept                                  |                     |               | 线性回归截距                                |
| LINEARREG_SLOPE     | Linear Regression Slope                                      |                     |               | 线性回归斜率                                |
| MA                  | All Moving Average                                           |                     |               | 所有移动平均线                              |
| MACD                | Moving Average Convergence/Divergence                        |                     |               | 移动平均线收敛/发散                         |
| MACDEXT             | MACD with controllable MA type                               |                     |               | 具有可控MA类型的MACD                        |
| MACDFIX             | Moving Average Convergence/Divergence Fix 12/26              |                     |               | 移动平均线收敛/发散修正12/26                |
| MAMA                | MESA Adaptive Moving Average                                 |                     |               | MESA自适应移动平均线                        |
| MAX                 | Highest value over a specified period                        |                     |               | 在指定时间段内的最高价值                    |
| MAXINDEX            | Index of highest value over a specified period               |                     |               | 指定期间内的最高价值指数                    |
| MEDPRICE            | Median Price                                                 |                     |               | 中位数价格                                  |
| MFI                 | Money Flow Index                                             |                     |               | 资金流量指数                                |
| MIDPOINT            | MidPoint over period                                         |                     |               | MidPoint超过期间                            |
| MIDPRICE            | Midpoint Price over period                                   |                     |               | 中点价格超过期间                            |
| MIN                 | Lowest value over a specified period                         |                     |               | 指定时间段内的最低值                        |
| MININDEX            | Index of lowest value over a specified period                |                     |               | 指定期间内的最低值索引                      |
| MINMAX              | Lowest and highest values over a specified period            |                     |               | 指定时间段内的最低和最高值                  |
| MINMAXINDEX         | Indexes of lowest and highest values over a specified period |                     |               | 指定期间内最低和最高值的索引                |
| MINUS_DI            | Minus Directional Indicator                                  |                     |               | 减去方向指示器                              |
| MINUS_DM            | Minus Directional Movement                                   |                     |               | 减去定向运动                                |
| MOM                 | Momentum                                                     |                     |               | 动量                                        |
| NATR                | Normalized Average True Range                                |                     |               | 归一化平均真实范围                          |
| OBV                 | On Balance Volume                                            |                     |               | 平衡量                                      |
| PLUS_DI             | Plus Directional Indicator                                   |                     |               | 加方向指示器                                |
| PLUS_DM             | Plus Directional Movement                                    |                     |               | 加上定向运动                                |
| PPO                 | Percentage Price Oscillator                                  |                     |               | 百分比价格振荡器                            |
| ROC                 | Rate of change : ((price/prevPrice)-1)*100                   |                     |               | 变化率：（（price / prevPrice）-1）* 100    |
| ROCP                | Rate of change Percentage: (price-prevPrice)/prevPrice       |                     |               | 变化率百分比:( price-prevPrice）/ prevPrice |
| ROCR                | Rate of change ratio: (price/prevPrice)                      |                     |               | 变化率:(价格/ prevPrice）                   |
| ROCR100             | Rate of change ratio 100 scale: (price/prevPrice)*100        |                     |               | 变化率100比例:(价格/ prevPrice）* 100       |
| RSI                 | Relative Strength Index                                      |                     |               | 相对强弱指数                                |
| SAR                 | Parabolic SAR                                                |                     |               | 抛物线SAR                                   |
| SAREXT              | Parabolic SAR - Extended                                     |                     |               | 抛物线SAR - 扩展                            |
| SMA                 | Simple Moving Average                                        |                     |               | 简单移动平均线                              |
| STDDEV              | Standard Deviation                                           |                     |               | 标准偏差                                    |
| STOCH               | Stochastic                                                   |                     |               | 随机                                        |
| STOCHF              | Stochastic Fast                                              |                     |               | 随机快速                                    |
| STOCHRSI            | Stochastic Relative Strength Index                           |                     |               | 随机相对强弱指数                            |
| SUM                 | Summation                                                    |                     |               | 合计                                        |
| T3                  | Triple Exponential Moving Average (T3)                       |                     |               | 三次指数移动平均线（T3）                    |
| TEMA                | Triple Exponential Moving Average                            |                     |               | 三次指数移动平均线                          |
| TRANGE              | True Range                                                   |                     |               | 真实范围                                    |
| TRIMA               | Triangular Moving Average                                    |                     |               | 三角移动平均线                              |
| TRIX                | 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA            |                     |               | 三重平滑EMA的1天变化率（ROC）               |
| TSF                 | Time Series Forecast                                         |                     |               | 时间序列预测                                |
| TYPPRICE            | Typical Price                                                |                     |               | 典型价格                                    |
| ULTOSC              | Ultimate Oscillator                                          |                     |               | 终极振荡器                                  |
| VAR                 | Variance                                                     |                     |               | 方差                                        |
| WCLPRICE            | Weighted Close Price                                         |                     |               | 加权收盘价                                  |
| WILLR               | Williams' %R                                                 |                     |               | 威廉姆斯'％R                                |
| WMA                 | Weighted Moving Average                                      |                     |               | 加权移动平均线                              |

