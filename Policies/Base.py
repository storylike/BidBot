import time

class BasePolicy(object):
    '''
        This is policy base class, all practical policies need to be inherited from this base class.
    '''
    def __init__(self):
        self.name = 'BASE'
        self.current_bid_list = []
        pass
    def GetHistoryData(self):
    '''
        This policy model need to get enough history data for analysis.
    '''
        pass
    def UpdateHistoryData(self):
    '''
        When time pass by, this history data need to be updated as new data is generated
    '''
        pass
    def Predict(self):
    '''
        Policy core functionality. In this method, latest history data is analyzed and candidate number list for next
        round is generated.
    '''
        predicted = {}
        return predicted
    def StartBid(self, bidlist=[]):
        pass
    def EndBid(self):
        self.logger("Round {round} end, policy:{name}, bid number(s): {numlist}".format( \
            round = self.round \
            name = self.name \
            numlist = str(self.current_bid_list) \
            ))
    def GotoBidPage(self):
        pass

    def logger(self, logmsg):
        date_today = time.strftime('Y-%m-%d')
        logtime = time.strftime(DATETIMEFMT)
        with open('..\\Log\log_' + date_today + '.txt', 'a+') as log:
            log.write(' '.join(logtime, log_string))
        print ' '.join(logtime, log_string)