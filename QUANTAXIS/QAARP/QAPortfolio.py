from .QAAccount import QA_Account
from .QARisk import QA_Risk


class QA_Portfolio():
    
    """
    在portfolio中,我们希望通过cookie来控制account_unit
    对于account的指标,要进行风险控制,组合成最优的投资组合的量

    """
    portfolio_code=['']
    portfolio_account=[]
    for i in range(0,len(portfolio_code)-1,1):
        portfolio_account[i]=QA_Account()
    
    def get_portfolio(self):
        pass

    def get_account_info(self):
        pass

    def cookie_mangement(self):
        
        pass