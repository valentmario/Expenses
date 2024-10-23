# ----------------------------------------------------------------------------#
#                   ***  Top_Codes_View.py   ***                              #
#   List_Transact_Codes : TRcode  TRDesc  GRdesc  CAdesc  StrToSearch         #
# ----------------------------------------------------------------------------#

from Top_Expenses.Modules_Manager import Modul_Mngr
from Common.Common_Functions import *
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data_Manager

from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import *
from Widgt.Widgets import TheButton, TheText, TheCombo


# ---------------------------------------------------------------------------------------
class Top_View_Codes(tk.Toplevel):
    # List is [] for Full Codes Database  or  a limited List for Queries
    def __init__(self, List):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data_Manager
        self.Mod_Mngr = Modul_Mngr
        self.Chat.Attach([self, TOP_CODES_VIEW])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(True, True)
        self.title('*****     Transactions Codes     ***** ')
        self.configure(background=BakGnd)

        self.nRows      = 41
        self.Widg_PosY  = 900
        self.Geometry   = Top_View_geometry
        self.Codes_List = List  # can be a reduced list for selection TRcode on Query or full Table

        if self.Codes_List:
            self.Codes_List = self.Data.Create_CodesTable_FromTR(self.Codes_List)
            self.nRows      = 15
            self.Widg_PosY  = 370
            self.Geometry   = Top_View_geom_reduced
        else:
            self.Codes_List = self.Data.Tree_Codes_View_List
        self.geometry(self.Geometry)

        self.List_Len          = len(self.Codes_List)
        self.Codes_List_Ordr   = self.Codes_List.copy()
        self.Codes_List_Ordr   = List_Order(self.Codes_List_Ordr, iView_TRdesc)
        self.Codes_List_Search = self.Codes_List.copy()
        self.Codes_List_Search = List_Order(self.Codes_List_Search, iView_StrToFind)
        self.View_Type         = VIEW_ALPHAB


        # ----------------------------------    B U T T O N S     ---------------------------------
        self.Txt_StrSerch = TheText(self,Txt_Disab,      10, self.Widg_PosY,    20, 4, '')
        self.Txt_FullDesc = TheText(self, Txt_Disab,    190, self.Widg_PosY,    64, 4, '')
        self.View_StrVar  = tk.StringVar()
        self.Combo_View   = TheCombo(self, self.View_StrVar, 720, self.Widg_PosY, 31, 14,
                                     CODES_VIEW_SEL, VIEW_ALPHAB, self.Clk_OnCombo)
        self.Btn_Exit     = TheButton(self, Btn_Def_En, 720, self.Widg_PosY+50, 13, '  E X I T ', self.Call_OnClose)

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
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Value)
        if Request_Code == CODE_TO_CLOSE:              # Close
            self.Call_OnClose()

        elif Request_Code == CODE_CLEAR_FOCUS:         # Clear Focus
            pass
            # self.Frame_Codes.Clear_Focus()

        elif Request_Code == CODE_CLK_ON_TR_CODES:      # Clicked on Codes Tree [TRcode]
            pass
            # self.Set_Focus_On_Tcode(int(Value))
        elif Request_Code == CODES_DB_UPDATED:
            self.Codes_List = self.Data.Tree_Codes_View_List
            self.View_Type  = VIEWxCODE
            self.Combo_View.SetSelText(VIEWxCODE)
            self.Frame_Codes.Load_Row_Values(self.Codes_List)



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
        Title = '   ' + str(self.List_Len) + '   Codici dei movimenti   '
        self.Frame_Codes.configure(text=Title)
        Nrows       = self.nRows
        nColToVis = 5
        Headings  = ['#0', 'Code', 'Transaction', "Group", 'Category', 'String To Search']
        Anchor    = ['c',  'c',    'w',           'w',     'w',        'w']
        Width     = [ 0,    50,     210,           150,     140,        270]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_Codes.Tree_Setup(Form_List)

    # ---------------------------------------------------------------------------------------------
    def Clk_OnTree_Codes(self, Values):
        TRcode    = int(Values[iView_TRcode])
        StrToFind = Values[iView_StrToFind]
        Full_Rec  = self.Data.Get_TR_Codes_Full(TRcode)
        self.Txt_FullDesc.Set_Text(Full_Rec[iTR_Ful_TRful])
        self.Txt_StrSerch.Set_Text(StrToFind)
        self.Chat.Tx_Request([TOP_CODES_VIEW, [TOP_CODES_MNGR, TOP_QUERY], CODE_CLK_ON_TR_CODES, [TRcode] ])

    # ----------------------------------------------------------------------------------------------
    def Clk_OnCombo(self, Value):
        self.View_Type = Value
        if self.View_Type == VIEW_ALPHAB:
            self.Frame_Codes.Load_Row_Values(self.Codes_List_Ordr)
        if self.View_Type == VIEWxCODE:
            self.Frame_Codes.Load_Row_Values(self.Codes_List)
        if self.View_Type == VIEW_SEARCH:
            self.Frame_Codes.Load_Row_Values(self.Codes_List_Search)
            pass

    # ---------------------------------------------------------------------------------------------
    def Clk_View_GRmngr(self):
        self.Mod_Mngr.Top_Launcher(TOP_GR_MNGR, TOP_CODES_VIEW, [])

    # ---------------------------------------------------------------------------------------------
    def Clk_View_Xlsx_File(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW,TOP_CODES_VIEW, [])

# *************************************************************************************************
