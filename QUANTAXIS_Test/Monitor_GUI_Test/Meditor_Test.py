from QUANTAXIS_Monitor_GUI.AppMediator import  *

import unittest

class TestMediator(unittest.TestCase):

    def testMeditor(self):

        meditor = Mediator()

        totalCount = 8
        counts_list = meditor.stockListSeperateToListCount(8, totalCount)
        sum = 0
        for i in range(len(counts_list)):
            sum = sum + counts_list[i]
        self.assertEqual(sum , totalCount)

        totalCount = 18
        counts_list = meditor.stockListSeperateToListCount(8, totalCount)
        sum = 0
        for i in range(len(counts_list)):
            sum = sum + counts_list[i]
        self.assertEqual(sum , totalCount)

        totalCount = 19
        counts_list = meditor.stockListSeperateToListCount(9, totalCount)
        sum = 0
        for i in range(len(counts_list)):
            sum = sum + counts_list[i]
        self.assertEqual(sum , totalCount)

        totalCount = 20
        counts_list = meditor.stockListSeperateToListCount(5, totalCount)
        sum = 0
        for i in range(len(counts_list)):
            sum = sum + counts_list[i]
        self.assertEqual(sum , totalCount)

        pass


        totalCount = 42322
        counts_list = meditor.stockListSeperateToListCount(3, totalCount)
        sum = 0
        for i in range(len(counts_list)):
            sum = sum + counts_list[i]
        self.assertEqual(sum, totalCount)

        totalCount = 423122
        counts_list = meditor.stockListSeperateToListCount(3, totalCount)
        sum = 0
        for i in range(len(counts_list)):
            sum = sum + counts_list[i]
        self.assertEqual(sum, totalCount)


        for iTotalCount in range(234,2222):
            counts_list = meditor.stockListSeperateToListCount(3, iTotalCount)
            sum = 0
            for i in range(len(counts_list)):
                sum = sum + counts_list[i]
            self.assertEqual(sum, iTotalCount)

            counts_list = meditor.stockListSeperateToListCount(4, iTotalCount)
            sum = 0
            for i in range(len(counts_list)):
                sum = sum + counts_list[i]
            self.assertEqual(sum, iTotalCount)

            counts_list = meditor.stockListSeperateToListCount(5, iTotalCount)
            sum = 0
            for i in range(len(counts_list)):
                sum = sum + counts_list[i]
            self.assertEqual(sum, iTotalCount)
