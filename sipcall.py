#!/usr/bin/python
#coding=utf8

"""
Class обертка над pjsip
"""
import sys
import pjsua as pj
from PyQt4 import QtCore
import threading


LOG_LEVEL = 0

class callCallback(pj.CallCallback):
    def __init__(self, sipaccount = None, call = None):
        """
        конструктор на входе у него sipaccount и новый вызов
        """
        pj.CallCallback.__init__(self, call)
        self.call = call
        self.sipaccount = sipaccount
        self.is_play_file = False

    def start_play_file(self, file_name, slot):
        """
        начинает воспроизведение файла
        """

        self.is_play_file = True
        # создаем плеер wav файла
        self.wav_player_id = pj.Lib.instance().create_player(file_name, loop = False)
        # проключаем канал плеера на разговор
        pj.Lib.instance().conf_connect(pj.Lib.instance().player_get_slot(self.wav_player_id), slot)

    def stop_play_file(self, slot):
        """
        останавилвает воспроизведение файла
        """

        if self.is_play_file:
	    # отключаем player от канала
            pj.Lib.instance().conf_disconnect(pj.Lib.instance().player_get_slot(self.wav_player_id), slot)
            # удаляем плеер
            pj.Lib.instance().player_destroy(self.wav_player_id)
        self.is_play_file = False

    def on_media_state(self):
        """
        уведомление об изменении состояния системы коммутации
        """

        if self.call.info().media_state == pj.MediaState.ACTIVE:
            print "Media is now active"
        else:
            print "Media is inactive"

class callCallbackIn(callCallback):
    """
    callback входящего вызова
    """

    def __init__(self, sipaccount = None, call = None):
        """
        конструктор на входе у него sipaccount и новый вызов
        """
        callCallback.__init__(self, sipaccount, call)
        self.incall = call


    def on_state(self):
        """
        уведомление об изменении состояния вызова
        """
        #print "Call with", self.call.info().remote_uri,
        #print "is", self.call.info().state_text,
        #print "last code =", self.call.info().last_code,
        #print "(" + self.call.info().last_reason + ")"

        # в предответном проключаем одну мелодию
#        if self.call.info().state == pj.CallState.EARLY:
#            call_slot = self.call.info().conf_slot
#            self.start_play_file('/ATS/SOUND/music0.wav', call_slot)

#        # в разговорном подаем другую
#        if self.call.info().state == pj.CallState.CONFIRMED:
#            call_slot = self.call.info().conf_slot
#            self.stop_play_file(call_slot)

#            # проключаем разговор
#            pj.Lib.instance().conf_connect(0, call_slot)
#            pj.Lib.instance().conf_connect(call_slot, 0)

        if self.call.info().state == pj.CallState.DISCONNECTED:
            call_slot = self.call.info().conf_slot
            self.stop_play_file(call_slot)
            # удалем вызов
#            self.sipaccount.calls.remove(self.incall)

        self.sipaccount.sip.emit(QtCore.SIGNAL("callin"), self, self.call.info().state)


# Сообщение от исходящего вызова
class callCallbackOut(callCallback):

    def __init__(self,  sipaccount = None, call = None):
        callCallback.__init__(self, sipaccount, call)

    # уведомление об изменении состояния
    def on_state(self):
        # проключаем разговры

#        if self.call.info().state == pj.CallState.CONFIRMED:
#            self.stop_play_file(0)

#            call_slot = self.call.info().conf_slot
#            pj.Lib.instance().conf_connect(0, call_slot)
#            pj.Lib.instance().conf_connect(call_slot, 0)

#        # в подаем КПВ в сторону пользователя
#        if self.call.info().state == pj.CallState.EARLY:
#            self.start_play_file('/ATS/SOUND/music1.wav', 0)

#        if self.call.info().state == pj.CallState.DISCONNECTED:
#            self.stop_play_file(0)
#            # удалем вызов
#            self.sipaccount.calls.remove(self.outcall)

        #self.sipaccount.sip.callBack.onCallChanged(self)
        
        self.sipaccount.sip.emit(QtCore.SIGNAL("callout"), self, self.call.info().state)
            

class SIPAccountCallback(pj.AccountCallback):
    """
    Callback для получения сообщений от sip account
    """

    def __init__(self, sip, account = None):
        pj.AccountCallback.__init__(self, account)
        self.calls = []
        self.sip = sip


    def on_incoming_call(self, call):
        """
        уведомление о входящем вызове
        """

        call_cb = callCallbackIn(self, call)
        call.set_callback(call_cb)

        # отвечаем ringing
#        call.answer(180)
        # отвечаем call progressом
#        call.answer(183)

        # запомнили вызов
        self.calls.append(call)

        print call.info().state
        self.sip.emit(QtCore.SIGNAL("callin"), call_cb, call.info().state)



    def waiter(self):
        """
        обработчик от таймера ожидания регистрации
        """
        self.on_reg_state()


    def wait(self):
        """
        ожидание регистрации
        """
        self.sem = threading.Semaphore(0)

        self.timeout = threading.Timer(5.0, self.waiter)
        self.timeout.start()
        self.sem.acquire()


    def reg_status(self):
        """
        возвращает статус регистрации
        """
        if self.account.info().reg_status == 200:
            return True
        else:
            return False


    def on_reg_state(self):
        """
        обработчик событий о регистрации
        """
        self.timeout.cancel()
        if self.sem:
            self.sem.release()



class SIP(QtCore.QObject):

    # два сигнала от регистрации и от состояния вызова
#    reg_state = QtCore.pyqtSignal(int)
    def __init__(self, callBack):
        """
        конструктор sip системы
        """
        QtCore.QObject.__init__(self)

        # объект которму все будет передаваться
        self.callBack = callBack

        my_media_cfg = pj.MediaConfig()
        my_media_cfg.clock_rate = 8000
#    my_media_cfg.jb_min = 40
#    my_media_cfg.jb_max = 80
        my_media_cfg.snd_clock_rate = 44100
        my_media_cfg.no_vad = True
        my_media_cfg.quality = 10
#    my_media_cfg.audio_frame_ptime = 80
#    my_media_cfg.audio_frame_ptime = 10
        my_media_cfg.ptime = 0
        my_media_cfg.max_media_ports = 4

        self.lib = pj.Lib()
        
        # sip account, можно будет сделать в принципе несколько
        self.account = None
        self.account_callback = None

        try:
            # инициализируем саму библиотеку
            self.lib.init(log_cfg = pj.LogConfig(level = LOG_LEVEL, callback = self.log_cb), media_cfg = my_media_cfg)
            # создаем транспортный уровень
            self.transport = self.lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(5060))

            self.lib.start()

        except pj.Error, e:
            print "Exception: " + str(e)
            self.lib.destroy()

    def create_account(self, account_info):
        """
        создает новый аккаунт
        """
        self.account = self.lib.create_account(pj.AccountConfig(
                account_info["registrator"].encode('ascii','ignore'),
                account_info["username"].encode('ascii','ignore'),
                account_info["password"].encode('ascii','ignore')))
                
        self.account_callback = SIPAccountCallback(self, self.account)
        self.account.set_callback(self.account_callback)
        # ждем окончания регистрации
        self.account_callback.wait()
        if self.account_callback.reg_status():
            return self.account
        self.delete_account()
        return None

    def delete_account(self):
        if self.account:
            self.account.delete()
        self.account = None

    def make_new_call(self, uri):
        try:
            callback = callCallbackOut(self.account_callback)
            call = self.account.make_call(uri.encode('ascii','ignore'), callback)
            #call.set_callback(callback)
            callback.outcall = call
            self.account_callback.calls.append(call)
            return call
        except pj.Error, e:
            print "Exception: " + str(e)
            return None

    def hangup_calls(self):
        if self.account_callback:
            for call in self.account_callback.calls:
            	call.hangup()

    def log_cb(self, level, str, len):
        """
        вывод отладки
        """
        print str,

    def __del__(self):
        """
        деструктор sip системы
        """
        self.clean()
        print "Destructor"

    def clean(self):
        self.hangup_calls()
        self.transport = None
        if self.account:
            self.account.delete()
        self.account = None
        self.lib.destroy()
        self.lib = None

if __name__ == "__main__":
    sip = SIP(None)
    acc = sip.create_account(None)
    # Menu loop
    while True:
        print "ok"
        input = sys.stdin.readline().rstrip("\r\n")
        if input == "c":
            sip.make_new_call("100")
            
        if input == "s":
            print sip.account_callback.calls

        if input == "q":
            break

    
    sip.clean()
