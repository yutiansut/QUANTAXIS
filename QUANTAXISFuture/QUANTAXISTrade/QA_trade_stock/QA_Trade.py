# -*- coding: utf-8 -*-

import msvcrt
import sys
import TradeX



TradeX.OpenTdx()

class QA_trade():
	def __init__(self):
		sHost = "218.5.69.35"
		nPort = 7708
		sVersion = "6.36"
		sBranchID =	1
		sAccountNo = "113002406"
		sTradeAccountNo = "113002406"
		sPassword = "170510"
		sTxPassword = "223143"


	def login(self):
		try:
			self.client = TradeX.Logon(self.sHost, self.nPort, self.sVersion, self.sBranchID, self.sAccountNo,self.sTradeAccountNo, self.sPassword, self.sTxPassword)
		except TradeX.error as e:
			print ("error: " + e.message)
			sys.exit(-1)



	def get_assest(self,client):
		self.nCategory = 0

		errinfo, self.result = client.QueryData(self.nCategory)
		if errinfo != "":
			print (errinfo)
		else:
			print (self.result)

	def get_stock_assest(self):
		self.nCategory = 1

		errinfo, self.result = self.client.QueryData(self.nCategory)
		if errinfo != "":
			print (errinfo)
		else:
			print (self.result)


	def get_stock_available(self):
		self.nCategory = 0
		self.nPriceType = 0
		self.sAccount = ""
		self.sStockCode = "000002"
		self.fPrice = 3.11

		errinfo, self.result =self.client.GetTradableQuantity(self.nCategory,self.nPriceType, self.sAccount, self.sStockCode,self.fPrice)
		if errinfo != "":
			print (errinfo)
		else:
			print (self.result)




	def get_ipo_status(self):
		self.status = self.client.QuickIPO()
		print (self.status)
		return self.status

	def get_new_info(self):
		self.status, self.content = self.client.QuickIPODetail()
		if status < 0:
			print (self.status)
		elif status == 0:
			print (self.status)
		else:
			for elem in self.content:
				errinfo, self.result = elem
				if errinfo != "":
					print (errinfo)
				else:
					print (self.result)


	def post_order(self,code,towards,amount):
		#errinfo, self.result = self.client.SendOrder(0, 4, "p001001001005793", "601988", 0, 100)
		errinfo, self.result = self.client.SendOrder(0, 4, "p001001001005793", code,towards,amount)
		if errinfo != "":
			print (errinfo)
		else:
			print (self.result)



	def post_orders(self):
		res = self.client.SendOrders(((0, 0, "p001001001005793", "601988", 3.11, 100), (0, 0, "p001001001005793", "601988", 3.11, 200)))
		for elem in res:
			errinfo, self.result = elem
			if errinfo != "":
				print (errinfo)
			else:
				print (self.result)
				return self.result




	def quote_five(self,codes):
		res = self.client.GetQuotes(('000001', '600600'))
		for elem in res:
			errinfo, self.result = elem
			if errinfo != "":
				print (errinfo)
			else:
				print (self.result)
				return self.result



	def ci(self):
		Category = (0, 1, 3)

		res = client.QueryDatas(Category)
		for elem in res:
			errinfo, result = elem
			if errinfo != "":
				print (errinfo)
			else:
				print (result)




	def close(self):
		del self.client
		TradeX.CloseTdx()


