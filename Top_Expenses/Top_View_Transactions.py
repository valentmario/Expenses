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
from Widgt.Widgets import TheButton, TheText


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

        self.resizable(True, True)
        self.geometry(Top_TrView_geometry)
        self.title('***   View transactions database  *** ')
        self.configure(background=BakGnd)

        self.Form_List_Tot    = []
        self.Form_List_TRGRCA = []

        # --------------------------   Create Treeview Frame   ------------------------------------
        self.Frame_Transactions  = TheFrame(self, 80, 20, self.Clk_On_Transaction)
        self.Frame_Transactions_Setup()

        self.Frame_Comp_Transact = TheFrame(self,  5, 20, self.Clk_On_Comp_Transaction)
        self.Frame_Comp_Transact_Setup()
        self.Frame_Comp_Xlsx     = TheFrame(self, 448, 20, self.Clk_On_Comp_Xlsx)
        self.Frame_Comp_Xlsx_Setup()

        self.Compare  = False
        self.Btn_Comp = TheButton(self, Btn_Def_En, 20, 950, 19, 'Compare to Xlsx', self.Clk_Compare)
        self.DescText = TheText(self, Txt_Disab,230, 920, 69, 3, '')
        TheButton(self, Btn_Def_En, 810, 950, 16, '  E X I T  ',     self.Call_OnClose)

        self.Frame_Transactions_Select()

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
            self.Compare = False
            self.Frame_Transactions_Select()
            self.Frame_Transactions.Clear_Focus()

    # ---------------------------------------------------------------------------------------------
    def Clk_Compare(self):
        if self.Compare:
            self.Compare = False
            self.Btn_Comp.Set_Text('Compare with Xlsx')
            self.Frame_Transactions_Select()
        else:
            self.Compare = True
            self.Btn_Comp.Set_Text('View Only Transactions')
            self.Frame_Comp_Transact_Select()


    # ---------------------------------------------------------------------------------------------
    def Frame_Transactions_Select(self):
        self.Frame_Transactions_Title()
        self.Frame_Transactions_Tree_Load()
        self.Frame_Transactions.Frame_View()
        self.Frame_Comp_Transact.Frame_Hide()
        self.Frame_Comp_Xlsx.Frame_Hide()
        pass

    # ---------------------------------------------------------------------------------------------
    def Frame_Comp_Transact_Select(self):
        self.Frame_Comp_Transact_Title()
        self.Frame_Comp_Transact_Tree_Load()
        self.Frame_Comp_Xlsx_Title()
        self.Frame_Comp_Xlsx_Tree_Load()
        self.Frame_Comp_Transact.Frame_View()
        self.Frame_Comp_Xlsx.Frame_View()
        self.Frame_Transactions.Frame_Hide()
        pass

    # ---------------------------------------------------------------------------------------------
    def Comp_Xsx_Load(self):
        pass

    # ---------------------------------------------------------------------------------------------
    def Clk_On_Transaction(self, Values):
        Descr1 = Values[iRow_Descr1]
        Descr2 = Values[iRow_Descr2]
        Descr = Descr2
        if len(Descr1) > len(Descr2):
            Descr = Descr1
        Val = [ Values[iRow_nRow], Values[iRow_Valuta], Descr ]
        self.Chat.Tx_Request([TOP_XLSX_VIEW, [TOP_CODES_MNGR], CODE_CLEAR_FOCUS, Val ])

    # ---------------------------------------------------------------------------------------------
    def Clk_On_Comp_Transaction(self):
        pass

    # ---------------------------------------------------------------------------------------------
    def Clk_On_Comp_Xlsx(self,Value):
        self.DescText.Set_Text(Value)


    # ---------------------------------------------------------------------------------------------
    #                      0        1         2         3         4        5        6      7
    # List_Transact_DB :  nRow    Conto    Contab    Valuta    TR_Desc   Accred   Addeb  TRcode
    def Frame_Transactions_Setup(self):
        Nrow = 42
        Ncol = 8
        Headings = ['#0','row','Conto','Contab','Valuta','Description','Accred  ','Addebit  ','TRcode']
        Anchor   = ['c', 'c',  'c',    'c',     'c',     'w',          'e',       'e',        'c'     ]
        Width    = [ 0,   60,   80,     90,      90,      200,          80,        80,         80     ]
        Form_List = [Nrow, Ncol, Headings, Anchor, Width]
        self.Frame_Transactions.Tree_Setup(Form_List)

    def Frame_Transactions_Title(self):
        TR_Name   = Get_File_Name(self.Data.Get_Selections_Member(Ix_Transact_File))
        FrameText = ('     ' + TR_Name + '   ' + str(self.Data.Get_Len_Transact_Table()) + '   Transactions')
        self.Frame_Transactions.Frame_Title(FrameText)

    def Frame_Transactions_Tree_Load(self):
        self.Frame_Transactions.Load_Row_Values(self.Data.Get_Transact_Table())


    # ---------------------------------------------------------------------------------------------
    #                          0       1       2         3         4
    # Transact_Frame_List :  nRow    Conto    Date    TR_Desc    Amount
    def Frame_Comp_Transact_Setup(self):
        Nrow = 42
        Ncol = 4
        Headings = ['#0', 'row', 'Date', 'Debit  ', 'Description']
        Anchor   = ['c',  'c',   'c',     'c',    'w',           'e']
        Width     = [0,    50,    80,      90,     200,           90]
        Form_List = [Nrow, Ncol, Headings, Anchor, Width]
        self.Frame_Comp_Transact.Tree_Setup(Form_List)

    # ---------------------------------------------------------------------------------------------
    def Frame_Comp_Transact_Title(self):
        TR_Name = Get_File_Name(self.Data.Get_Selections_Member(Ix_Transact_File))
        FrameText = ('     ' + TR_Name + '   ' + str(self.Data.Get_Len_Transact_Table()) + '   Transactions')
        self.Frame_Comp_Transact.Frame_Title(FrameText)

    # ---------------------------------------------------------------------------------------------
    def Frame_Comp_Transact_Tree_Load(self):
        Transactions_Table  = self.Data.Get_Transact_Table()
        Frame_Transact_List = []
        for Rec in Transactions_Table:
            nRow   = Rec[iTransact_nRow]
            Date   = Rec[iTransact_Valuta]
            Amount = Rec[iTransact_Addeb]
            Descr  = Rec[iTransact_TRdesc]
            if Amount == 0.0:
                Amount = Rec[iTransact_Accred]
            Rec_List = [nRow, Date, Amount, Descr]
            Frame_Transact_List.append(Rec_List)
        self.Frame_Comp_Transact.Load_Row_Values(Frame_Transact_List)


    # ---------------------------------------------------------------------------------------------
    #                          0       1       2         3         4
    # Transact_Frame_List :  nRow    Date    Amount   Amount
    def Frame_Comp_Xlsx_Setup(self):
        Nrow = 42
        Ncol = 3
        Headings = ['#0', 'row', 'Date', 'Full Decription']
        Anchor   = ['c',   'c',  'c',     'w']
        Width    = [ 0,     60,   90,      360]
        Form_List = [Nrow, Ncol, Headings, Anchor, Width]
        self.Frame_Comp_Xlsx.Tree_Setup(Form_List)

    # ---------------------------------------------------------------------------------------------
    def Frame_Comp_Xlsx_Title(self):
        Xlsx_Filenamee = Get_File_Name(self.Data.Get_Selections_Member(Ix_Xlsx_File))
        Filename       = Get_File_Name(Xlsx_Filenamee)
        FrameText = ('   ' + 'Xlsx  File:   ' + Filename +  '   ')
        self.Frame_Comp_Xlsx.Frame_Title(FrameText)

    # ---------------------------------------------------------------------------------------------
    def Frame_Comp_Xlsx_Tree_Load(self):
        Xlsx_Rows      = self.Data.Get_Xlsx_Rows_From_Sheet()
        Xlsx_Rows_List = []
        for Row in Xlsx_Rows:
            nRow    = Row[iRow_nRow]
            Date    = Row[iRow_Valuta]
            Descr1 = Row[iRow_Descr1]
            if type(Descr1) is not str:
                Descr1 = ''
            Descr2 = Row[iRow_Descr2]
            if type(Descr2) is not str:
                Descr2 = ''
            FullDes = Descr2
            if len(Descr1) > len(Descr2):
                FullDes = Descr1
            List = [nRow, Date, FullDes]
            Xlsx_Rows_List.append(List)
        self.Frame_Comp_Xlsx.Load_Row_Values(Xlsx_Rows_List)


    # ---------------------------------------------------------------------------------------------
    def Set_Focus_On_Row(self, Values):
        nRow = int(Values[0])
        Date = Values[1]
        Index = -1
        for Rec in self.Frame_Transactions.Loaded_List:
            Index +=1
            if Rec[iRow_nRow] == nRow:
                myDate = Rec[iRow_Valuta]
                if myDate == Date:
                    self.Frame_Transactions.Set_List_For_Focus(Index)
                    break

# =================================================================================================
