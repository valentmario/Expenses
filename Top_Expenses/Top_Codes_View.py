# ----------------------------------------------------------------------------#
#                   ***  Top_Codes_View.py   ***                              #
#   List_Transact_Codes : TRcode  TRDesc  GRdesc  CAdesc  StrToSearch         #
# ----------------------------------------------------------------------------#
#
import tkinter as tk
from Top_Expenses.Modules_Manager import Modul_Mngr
from Common.Common_Functions import *
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data

from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton


# ---------------------------------------------------------------------------------------
class Top_View_Codes(tk.Toplevel):
    def __init__(self, Result, Codes_List):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data
        self.Mod_Mngr = Modul_Mngr
        self.Chat.Attach([self, TOP_CODES_VIEW])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry(Top_View_geometry)
        self.title('*****     Transactions  Codes     ***** ')
        self.configure(background=BakGnd)

        self.Result = Result
        if Codes_List:
            self.Codes_List = self.Data.Create_CodesTable_FromTR(Codes_List)
        else:
            self.Codes_List = self.Data.Tree_Codes_View_List

        self.List_Len = len(self.Codes_List)
        self.Codes_List_Ordr = self.Codes_List.copy()
        self.Codes_List_Ordr = List_Order(self.Codes_List_Ordr, 1)
        self.Ordered         = True

        self.Keys_Rows_List  = []
        self.Row_Count       = 0

        # ----------------------------------    B U T T O N S     ---------------------------------
        self.Btn_Order  = TheButton(self, Btn_Def_En, 20, 940, 12, 'ordered', self.Clk_Order)
        self.Btn_Exit   = TheButton(self, Btn_Def_En, 705, 940, 10, '  E X I T ', self.Call_OnClose)

        # ---------------------------------    T R E E   of  Codes    -----------------------------
        self.Frame_Codes = TheFrame(self,  10,  10, self.Clk_OnTree_Codes)
        self.Frame_Codes_Setup()
        self.Frame_Codes.Frame_View()
        self.Frame_Codes.Load_Row_Values(self.Codes_List_Ordr)

    # ---------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_CODES_VIEW)
        self.destroy()
        return

    # ---------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Value):
        Print_Received_Message(Transmitter_Name, TOP_MNGR, Request_Code, Value)
        if Request_Code == CODE_TO_CLOSE:               # Close
            self.Call_OnClose()

        elif Request_Code == CODE_CLEAR_FOCUS:          # Clear Focus
            self.Frame_Codes.Clear_Focus()
            # self.Frame_Codes.Load_Row_Values(self.List_View_Codes)

        elif Request_Code == CODE_CLK_ON_TR_CODES:      # Clicked on Codes Tree [TRcode]
            self.Set_Focus_On_Tcode(int(Value))

        elif Request_Code == CODE_CLIK_ON_XLSX:         # Clicked on Xlsx Tree  [nRow, Date]
            self.Frame_Codes.Clear_Focus()

        elif Request_Code == CODES_DB_UPDATED or Request_Code == XLSX_UPDATED:
            self.Ordered = False
            self.Btn_Order.Set_Text('per code')
            self.Frame_Codes.Load_Row_Values(self.Data.Tree_Codes_View_List)
            if Value:
                self.Clk_Order()
                TRcode = Value[0]
                self.Set_Focus_On_Tcode(TRcode)

    # ---------------------------------------------------------------------------------------------
    def Set_Focus_On_Tcode(self, TRcode):
        Index = -1
        for Rec in self.Frame_Codes.Loaded_List:
            Index +=1
            if Rec[iView_TRcode] == TRcode:
                self.Frame_Codes.Set_List_For_Focus(Index)
                break

    # ------------------------   T R E E   of  TRcodes  Setup       -------------------------------
    def Frame_Codes_Setup(self):
        # strTot_Cod = str(self.Data.Get_TR_Codes_Table_Len())
        Title = '   ' + str(self.List_Len) + '   Transactions Codes   '
        self.Frame_Codes.configure(text=Title)
        Nrows     = 43
        nColToVis = 5
        Headings  = ['#0', 'Code', 'Transaction', "Group", 'Category', 'String To Search']
        Anchor    = [' c',  'c',   'w',           'w',     'w',        'w']
        Width     = [0, 50, 190, 140, 140, 270]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_Codes.Tree_Setup(Form_List)

    # ---------------------------------------------------------------------------------------------
    def Clk_OnTree_Codes(self, Values):
        TRcode = int(Values[iView_TRcode])
        self.Chat.Tx_Request([TOP_CODES_VIEW, [TOP_MNGR, TOP_QUERY], CODE_CLK_ON_TR_CODES, [TRcode] ])

    # ----------------------------------------------------------------------------------------------
    def Clk_Order(self):
        if self.Ordered:
            self.Ordered = False
            self.Btn_Order.Set_Text('per code')
            self.Frame_Codes.Load_Row_Values(self.Codes_List)
        else:
            self.Ordered = True
            self.Btn_Order.Set_Text('ordered')
            self.Frame_Codes.Load_Row_Values(self.Codes_List_Ordr)

    # ---------------------------------------------------------------------------------------------
    def Clk_View_GRmngr(self):
        self.Mod_Mngr.Top_Launcher(TOP_GR_MNGR, TOP_CODES_VIEW, [])

    # ---------------------------------------------------------------------------------------------
    def Clk_View_Xlsx_File(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW,TOP_CODES_VIEW, [])

# *************************************************************************************************
