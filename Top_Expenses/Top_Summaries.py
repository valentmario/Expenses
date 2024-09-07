import tkinter as tk

from Chat import Ms_Chat
from Common.Constants import *
from Data_Classes.Transact_DB import Data

from Widgt.Dialogs import Print_Received_Message
from Widgt.Widgets import TheButton

class Top_Summaries(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.Chat   = Ms_Chat
        self.Data   = Data
        self.Dummy = 0
        self.geometry('15x15+900+490')
        self.resizable(False, False)
        self.configure(background=BakGnd)
        self.Chat.Attach([self, TOP_SUMMARIES])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)
        self.title('*****     Balances  per   years     *****')

        self.geometry(Top_Balances_geometry)

        # self.OptMenu_Year = TheCombo(self, self.StrVar_Year, self.Widg_PosX,  20, 21, 16, self.Years_List,
        #                              self.Year_Selected, self.Clk_____)


        self.Btn_Exit      = TheButton(self, Btn_Bol_En,  400, 850, 15, '  E X I T  ',    self.Call_OnClose)

        # --------------------------  Trees-Frames    for  Queries   --------------------------------------------------
        # self.Frame1 = TheFrame(self, xyToHide, 10, self.Click_View)
        # self.Frame2 = TheFrame(self, xyToHide, 10, self.Click_View)
        # self.Frame3 = TheFrame(self, xyToHide, 10, self.Click_View)
        # self.Frames_List = [self.Frame1, self.Frame2, self.Frame3]
        # self.Frames_Setup()

    # -------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_SUMMARIES)
        self.destroy()

    # -------------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:               # Close
            self.Call_OnClose()
        elif Request_Code == CODE_CLEAR_FOCUS:          # Clear Focus
            pass
