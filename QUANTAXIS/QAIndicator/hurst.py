
import numpy as np
import math
import os
import sys
import matplotlib.pyplot as plt


class RSanalysis:
    '''Performs RS analysis on data stored in a List()'''

    def __init__(self):
        pass

    def run(self, series, exponent=None):
        '''
        :type series: List
        :type exponent: int
        :rtype: float
        '''
        try:
            return self.calculateHurst(series, exponent)
        except Exception as e:
            print("   Error: %s" % e)

    def bestExponent(self, seriesLenght):
        '''
        :type seriesLenght: int
        :rtype: int
        '''
        i = 0
        cont = True
        while(cont):
            if(int(seriesLenght/int(math.pow(2, i))) <= 1):
                cont = False
            else:
                i += 1
        return int(i-1)

    def mean(self, series, start, limit):
        '''
        :type start: int
        :type limit: int
        :rtype: float
        '''
        return float(np.mean(series[start:limit]))

    def sumDeviation(self, deviation):
        '''
        :type deviation: list()
        :rtype: list()
        '''
        return np.cumsum(deviation)

    def deviation(self, series, start, limit, mean):
        '''
        :type start: int
        :type limit: int
        :type mean: int
        :rtype: list()
        '''
        d = []
        for x in range(start, limit):
            d.append(float(series[x] - mean))
        return d

    def standartDeviation(self, series, start, limit):
        '''
        :type start: int
        :type limit: int
        :rtype: float
        '''
        return float(np.std(series[start:limit]))

    def calculateHurst(self, series, exponent=None):
        '''
        :type series: List
        :type exponent: int
        :rtype: float
        '''
        rescaledRange = list()
        sizeRange = list()
        rescaledRangeMean = list()

        if(exponent is None):
            exponent = self.bestExponent(len(series))

        for i in range(0, exponent):
            partsNumber = int(math.pow(2, i))
            size = int(len(series)/partsNumber)

            sizeRange.append(size)
            rescaledRange.append(0)
            rescaledRangeMean.append(0)

            for x in range(0, partsNumber):
                start = int(size*(x))
                limit = int(size*(x+1))

                deviationAcumulative = self.sumDeviation(self.deviation(
                    series, start, limit, self.mean(series, start, limit)))
                deviationsDifference = float(
                    max(deviationAcumulative) - min(deviationAcumulative))
                standartDeviation = self.standartDeviation(
                    series, start, limit)

                if(deviationsDifference != 0 and standartDeviation != 0):
                    rescaledRange[i] += (deviationsDifference /
                                         standartDeviation)

        y = 0
        for x in rescaledRange:
            rescaledRangeMean[y] = x/int(math.pow(2, y))
            y = y+1

        # log calculation
        rescaledRangeLog = list()
        sizeRangeLog = list()
        for i in range(0, exponent):
            rescaledRangeLog.append(math.log(rescaledRangeMean[i], 10))
            sizeRangeLog.append(math.log(sizeRange[i], 10))

        slope, intercept = np.polyfit(sizeRangeLog, rescaledRangeLog, 1)

        ablineValues = [slope * i + intercept for i in sizeRangeLog]

        plt.plot(sizeRangeLog, rescaledRangeLog, '--')
        plt.plot(sizeRangeLog, ablineValues, 'b')
        plt.title(slope)
        # graphic dimension settings
        limitUp = 0
        if(max(sizeRangeLog) > max(rescaledRangeLog)):
            limitUp = max(sizeRangeLog)
        else:
            limitUp = max(rescaledRangeLog)
        limitDown = 0
        if(min(sizeRangeLog) > min(rescaledRangeLog)):
            limitDown = min(rescaledRangeLog)
        else:
            limitDown = min(sizeRangeLog)
        plt.gca().set_xlim(limitDown, limitUp)
        plt.gca().set_ylim(limitDown, limitUp)
        print("Hurst exponent: " + str(slope))
        plt.show()

        return slope

    def quit(self):
        raise SystemExit()


if __name__ == "__main__":
    RSanalysis().run(sys.argv[1:])
