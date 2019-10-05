import sys
from PyQt5.QtWidgets import *
from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
import time
import pandas as pd
import sqlite3

TR_REQ_TIME_INTERVAL = 0.2

class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        self._create_kiwoom_instance()
        self._set_signal_slots()

    def _create_kiwoom_instance(self):
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def _set_signal_slots(self):
        self.OnEventConnect.connect(self._event_connect)
        self.OnReceiveTrData.connect(self._receive_tr_data)

    def comm_connect(self):
        self.dynamicCall("CommConnect()")
        self.login_event_loop = QEventLoop()
        self.login_event_loop.exec_()

    def _event_connect(self, err_code):
        if err_code == 0:
            print("connected")
        else:
            print("disconnected")

        self.login_event_loop.exit()

    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def get_master_code_name(self, code):
        code_name = self.dynamicCall("GetMasterCodeName(QString)", code)
        return code_name

    def set_input_value(self, id, value):
        self.dynamicCall("SetInputValue(QString, QString)", id, value)

    def comm_rq_data(self, rqname, trcode, next, screen_no):
        self.dynamicCall("CommRqData(QString, QString, int, QString", rqname, trcode, next, screen_no)
        self.tr_event_loop = QEventLoop()
        self.tr_event_loop.exec_()

    def _comm_get_data(self, code, real_type, field_name, index, item_name):
        ret = self.dynamicCall("CommGetData(QString, QString, QString, int, QString", code,
                               real_type, field_name, index, item_name)
        return ret.strip()

    def _get_repeat_cnt(self, trcode, rqname):
        ret = self.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret

    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False

        if rqname == "opt10081_req":
            self._opt10081(rqname, trcode)

        try:
            self.tr_event_loop.exit()
        except AttributeError:
            pass
        
    def get_code_list_by_market(self, market):
        code_list = self.dynamicCall("GetCodeListByMarket(QString)", market)
        code_list = code_list.split(';')
        return code_list[:-1]

    def _opt10081(self, rqname, trcode):
        data_cnt = self._get_repeat_cnt(trcode, rqname)

        for i in range(data_cnt):
            date = self._comm_get_data(trcode, "", rqname, i, "일자")
            open = self._comm_get_data(trcode, "", rqname, i, "시가")
            high = self._comm_get_data(trcode, "", rqname, i, "고가")
            low = self._comm_get_data(trcode, "", rqname, i, "저가")
            close = self._comm_get_data(trcode, "", rqname, i, "현재가")
            volume = self._comm_get_data(trcode, "", rqname, i, "거래량")

            self.ohlcv['wkdate'].append(date)
            self.ohlcv['jong'].append("233160")
            self.ohlcv['start_price'].append(int(open))
            self.ohlcv['high_price'].append(int(high))
            self.ohlcv['low_price'].append(int(low))
            self.ohlcv['close_price'].append(int(close))
            self.ohlcv['volume'].append(int(volume))
            
    def _opt10001(self, rqname, trcode, jong):
        jong_nm = self._comm_get_data(trcode, "", rqname, 0, "종목명")
        listed_shares = self._comm_get_data(trcode, "", rqname, 0, "상장주식")
        cap = self._comm_get_data(trcode, "", rqname, 0, "시가총액")
        cap_rate = self._comm_get_data(trcode, "", rqname, 0, "시가총액비중")
        foregin_rate = self._comm_get_data(trcode, "", rqname, 0, "외인소진률")
        per = self._comm_get_data(trcode, "", rqname, 0, "PER")
        eps = self._comm_get_data(trcode, "", rqname, 0, "EPS")
        roe = self._comm_get_data(trcode, "", rqname, 0, "ROE")
        pbr = self._comm_get_data(trcode, "", rqname, 0, "PBR")
        ev = self._comm_get_data(trcode, "", rqname, 0, "EV")
        bps = self._comm_get_data(trcode, "", rqname, 0, "BPS")
        sales = self._comm_get_data(trcode, "", rqname, 0, "매출액")
        op_profit = self._comm_get_data(trcode, "", rqname, 0, "영업이익")
        net_income = self._comm_get_data(trcode, "", rqname, 0, "당기순이익")
        traded_shares = self._comm_get_data(trcode, "", rqname, 0, "유통주식")
        traded_shares_rate = self._comm_get_data(trcode, "", rqname, 0, "유통비율")
        
        self.ohlcv['jong'].append(jong)
        self.ohlcv['jong_nm'].append(jong_nm)
        self.ohlcv['listed_shares'].append(listed_shares)
        self.ohlcv['cap'].append(cap)
        self.ohlcv['cap_rate'].append(cap_rate)
        self.ohlcv['foregin_rate'].append(foregin_rate)
        self.ohlcv['per'].append(per)
        self.ohlcv['eps'].append(eps)
        self.ohlcv['roe'].apped(roe)
        self.ohlcv['pbr'].append(pbr)
        self.ohlcv['ev'].append(ev)
        self.ohlcv['bps'].append(bps)
        self.ohlcv['sales'].append(sales)
        self.ohlcv['op_profit'].append(op_profit)
        self.ohlcv['net_income'].append(net_income)
        self.ohlcv['traded_shares'].append(traded_shares)
        self.ohlcv['traded_shares_rate'].append(traded_shares_rate)

if __name__ == "__main__":
#    app = QApplication(sys.argv)
#    kiwoom = Kiwoom()
#    kiwoom.comm_connect()
    
    code_list = kiwoom.get_code_list_by_market('10')
    
    for code in code_list:
        
