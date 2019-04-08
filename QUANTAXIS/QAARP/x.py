    @property
    def average_loss(self):
        return self.loss_pnl.pnl_money.mean()


    def average_pnl(self):
        return abs(self.average_profit / self.average_loss)

    def max_profit(self, pnl):
        return self.profit_pnl(pnl).pnl_money.max()


    def max_loss(self, pnl):
        return self.loss_pnl(pnl).pnl_money.min()


    def max_pnl(self, pnl):
        return abs(self.max_profit(pnl) / self.max_loss(pnl))


    def netprofio_maxloss_ratio(self, pnl):
        return abs(pnl.pnl_money.sum() / self.max_loss(pnl))


    def continue_profit_amount(self, pnl):
        w = []
        w1 = 0
        for _, item in pnl.pnl_money.iteritems():
            if item > 0:
                w1 += 1
            elif item < 0:
                w.append(w1)
                w1 = 0
        if len(w) == 0:
            return 0
        else:
            return max(w)


    def continue_loss_amount(self, pnl):
        l = []
        l1 = 0
        for _, item in pnl.pnl_money.iteritems():
            if item > 0:
                l1 += 1
            elif item < 0:
                l.append(l1)
                l1 = 0
        if len(l) == 0:
            return 0
        else:
            return max(l)


    def average_holdgap(self, pnl):
        return str(pnl.hold_gap.mean())


    def average_profitholdgap(self, pnl):
        return str(self.profit_pnl(pnl).hold_gap.mean())


    def average_losssholdgap(self, pnl):
        return str(self.loss_pnl(pnl).hold_gap.mean())


    def average_evenholdgap(self, pnl):
        return self.even_pnl(pnl).hold_gap.mean()


    def max_cashused(self, pnl):
        return self.target.init_cash - min(self.target.cash)


    def total_taxfee(self, pnl):
        return self.target.history_table_min.commission.sum(
        ) + self.target.history_table_min.tax.sum()
