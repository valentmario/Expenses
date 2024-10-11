# ================================================================================= #
#                  *****     Top_View_Transact.py     *****                         #
# XLS_Row_List : nRow  Contab  Valuta  Descr1  Accred  Addeb  Descr2                #
# ================================================================================= #

from Common.Common_Functions import *
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data_Manager

from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import *
from Top_Expenses.Modules_Manager import Modul_Mngr
from Widgt.Widgets import TheButton


# ===================================================================================
class Top_View_Transact(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.Chat      = Ms_Chat
        self.Data      = Data_Manager
        self.Mod_Mngr  = Modul_Mngr
        self.Data_List = List

        self.Chat.Attach([self, TOP_VIEW_TRANSACT])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry(Top_View_geometry)
        self.title('***   View transactions database  *** ')
        self.configure(background=BakGnd)

        self.Form_List_Tot    = []
        self.Form_List_TRGRCA = []

        # --------------------------   Create Treeview Frame   ------------------------------------
        self.Frame_Sheets_Rows = TheFrame(self, 20, 20, self.Clk_On_Sheets_Rows)
        self.Frame_Sheets_Rows_Setup()
        self.Frame_Sheets_Rows_View()
        self.Frame_Sheets_Rows.Frame_View()

        TheButton(self, Btn_Def_En, 620, 950, 16, '  E X I T  ', self.Call_OnClose)

    # ---------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_VIEW_TRANSACT)
        self.destroy()

    # ---------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:           # Close
            self.Call_OnClose()

        elif Request_Code == CODE_CLEAR_FOCUS or Request_Code == CODE_CLK_ON_TR_CODES or Request_Code\
                          == CODE_CLIK_ON_XLSX or Request_Code == XLSX_UPDATED:
            self.Frame_Sheets_Rows.Clear_Focus()
            self.Frame_Sheets_Rows.Load_Row_Values(self.Data.Load_Transact_Table(ON_SELECTIONS))

    # ---------------------------------------------------------------------------------------------
    def Clk_On_Sheets_Rows(self, Values):
        Descr1 = Values[iRow_Descr1]
        Descr2 = Values[iRow_Descr2]
        Descr = Descr2
        if len(Descr1) > len(Descr2):
            Descr = Descr1
        Val = [ Values[iRow_nRow], Values[iRow_Valuta], Descr ]
        self.Chat.Tx_Request([TOP_XLSX_VIEW, [TOP_CODES_MNGR], CODE_CLEAR_FOCUS, Val ])

    # -----------------------------------------------------------------------------------------------------------
    #                      0        1         2         3         4        5        6      7
    # List_Transact_DB :  nRow    Conto    Contab    Valuta    TR_Desc   Accred   Addeb  TRcode
    def Frame_Sheets_Rows_Setup(self):
        Nrow = 42
        Ncol = 8
        Headings = ['#0', 'row', 'Conto', "Contab", 'Valuta', 'Description', 'Accred  ', 'Addebit  ', 'TRcode']
        Anchor   = ['c',  'c',   'c',     'c',      'c',      'w',           'e',       'e',       'c'     ]
        Width    = [ 0,    60,    80,      90,       90,       200,           80,        80,        80     ]
        Form_List = [Nrow, Ncol, Headings, Anchor, Width]
        self.Frame_Sheets_Rows.Tree_Setup(Form_List)
        # self.Frame_Sheets_Rows_View()

    def Frame_Sheets_Rows_View(self):
        TR_Name   = Get_File_Name(self.Data.Get_Selections_Member(Ix_Transact_File))
        FrameText = ('     ' + TR_Name + '   ' + str(self.Data.Get_Len_Transact_Table()) + '   Transactions')
        self.Frame_Sheets_Rows.Frame_Title(FrameText)
        self.Frame_Sheets_Rows.Load_Row_Values(self.Data.Get_Transact_Table())
        pass

    # ---------------------------------------------------------------------------------------------
    def Set_Focus_On_Row(self, Values):
        nRow = int(Values[0])
        Date = Values[1]
        Index = -1
        for Rec in self.Frame_Sheets_Rows.Loaded_List:
            Index +=1
            if Rec[iRow_nRow] == nRow:
                myDate = Rec[iRow_Valuta]
                if myDate == Date:
                    self.Frame_Sheets_Rows.Set_List_For_Focus(Index)
                    break

# =================================================================================================
