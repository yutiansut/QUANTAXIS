# 重新考虑ARP

Account是作为单账户的机制存在的 可以是股票账户,期货账户或者更多

Portfolio作为一个策略的基本单位,包含着本次策略的最大可能集,虽然大部分时候(单账户)Portfolio和Account并无本质区别

当策略需要增资的时候,流程一般如下:

USER对于底下的Portfolio进行增资,然后Portfolio[add money], 对应到相应的account的cash增加



