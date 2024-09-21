# ================================================================================= #
#                  *****      Top_View_Message.py      *****                        #
# ================================================================================= #

import tkinter as tk

from Common.Common_Functions import *
from Chat import Ms_Chat
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheTextPoints


class Top_View_Message(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.Chat = Ms_Chat
        # self.Data = Data
        # self.Mod_Mngr = Modul_Mngr

        self.Chat.Attach([self, TOP_XLSX_VIEW])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry(Top_View_Mess_geometry)
        self.title('***   Show  message   *** ')
        self.configure(background=BakGnd)
        Messg = List[0]
        if len(List) > 1:
            pass
        self.Txt1 = TheTextPoints(self, Txt_Disab,  20, 20, 50, 20, Messg, 11)
        TheButton(self, Btn_Def_En, 270, 410, 16, 'E X I T ', self.Call_OnClose)

    # ----------------------------------------------------------------------------- #
    def Call_OnClose(self):
        self.Chat.Detach(TOP_XLSX_VIEW)
        self.destroy()

    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        pass
        # Print_Received_Message(Transmitter_Name, MAIN_WIND, Request_Code, Values_List)
        # if Request_Code == CODE_TO_CLOSE:
        #     self.Call_OnClose()
        # elif Request_Code == SOMETHING:
        #   pass