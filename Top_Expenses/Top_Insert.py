# ------------------------------------------------------------------------------------- #
#                      *****     Top_Insert.py     *****                                #
#                  Insert Transactions on Transactions database                         #
#                                                                                       #
# main methods:                                                                         #
# --------------------------------                                                      #
# Set_Texts                         (Transact_Name,  Xlsx_Name,  Xlsx_Year,  Conto      #
# Check_Files:                      (Without_Code and Transact_Db exists)               #
# Create_New_Transact_Db:                                                               #
# Create_RecordsList_ToBeInserted:  (compare WitCode_List   and   Transact_Db           #
# Load_Tree:                        (as in  RecordsList_ToBeInserted)                   #
#                                                                                       #
# ------------------------------------------------------------------------------------- #

import tkinter as tk
from Top_Expenses.Modules_Manager import Modul_Mngr
from Chat import Ms_Chat
from Common.Common_Functions import *
from Data_Classes.Transact_DB import Data_Manager

from Widgt.Dialogs import Print_Received_Message
from Widgt.Dialogs import Message_Dlg
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheText

# ==================================================================================================== #
#  --------------------        class Top_Insert(tk.Toplevel)        --------------------------------   #
# ==================================================================================================== #
class Top_Insert(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data_Manager
        self.Mod_Mngr = Modul_Mngr
        self.List     = List

        self.Chat.Attach([self, TOP_INS])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)
        self.resizable(False, False)
        self.configure(background=BakGnd)
        self.geometry(Top_Insert_geometry)
        self.title('*****     Inserimento movimenti nel database     *****')

        self.Dummy       = 0
        self.Files_Ident = self.Data.Get_Xlsx_Transact_Ident()
        self.Conto       = self.Files_Ident[Ix_Xlsx_Conto]
        self.intYear     = self.Files_Ident[Ix_Xlsx_Year]
        self.intMonth    = self.Files_Ident[Ix_Xlsx_Month]
        self.Full_Month  = ''

        self.WithList                       = []
        self.TransactRecords_ToBeInserted   = []
        self.TotTransact_ToBeInserted       = 0
        self.Transact_Filename              = ''

        self.Tree_Transact_Title      = ''
        self.Transact_InDatabase_List = []
        self.Full_Filename_For_Insert = self.Data.Get_Selections_Member(Ix_Transact_File)

        self.Txt_TransactName = TheText(self, Txt_Disab,  20,  20, 18,  1, '')
        self.Txt_Xlsx_Name    = TheText(self, Txt_Disab, 200,  20, 19,  1, '')
        self.Txt_Conto        = TheText(self, Txt_Disab, 370,  20, 12,  1, '')
        self.Txt_Xlsx_Year    = TheText(self, Txt_Disab, 484,  20, 11,  1, '')
        self.Txt_Xlsx_Month   = TheText(self, Txt_Disab, 590,  20, 11, 1, '')

        #  ------------------------------------  B U T T O N s  ---------------------------------------
        self.Sel_Xlsx     = TheButton(self, Btn_Def_En,   20, 900, 23, 'Seleziona un file xlsx', self.Clk_Sel_Xlsx)
        self.ViewXlsx     = TheButton(self, Btn_Def_Dis,  20, 940, 23, 'Mostra movimenti xlsx',  self.Clk_View_Xlsx)

        self.Cod_Mngr     = TheButton(self, Btn_Def_Dis, 260, 900, 23, 'Gestore files',         self.Clk_Codes_Mngr)
        self.ViewTransact = TheButton(self, Btn_Def_Dis, 260, 940, 23, 'Mostra movimenti nel Db',self.Clk_View_Transact)

        self.Ins_Btn      = TheButton(self, Btn_Def_En, 500, 900, 23, 'Inserire Movimenti nel Db', self.Clk_Insert)
        self.Exit         = TheButton(self, Btn_Def_En,  500, 940, 23, '  F I N E  ',               self.Call_OnClose)

        self.Total                        = []
        self.Tot_WithoutCode              = 0
        self.Xlsx_Filename                = ''
        self.Xlsx_Year                    = 0
        self.WithList                     = []
        self.TransactRecords_ToBeInserted = []
        self.TotTra_ToInset               = []
        self.TotTransact_ToBeInserted     = 0
        self.Transact_Filename            = ''
        self.Transact_Year                = 0

        # --------------------------  T R E E     Transactions to insert   ----------------------------
        self.Frame_Transact = TheFrame(self, 20, 60, self.Clk_Ontree_View)
        self.Frame_Transact_Setup()
        self.Frame_Transact.Frame_View()

        self.Set_Texts()
        self.Create_RecordsList_ToBeInserted()
        self.Load_Tree()
        self.Set_Buttons()

    # -------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_INS)
        self.destroy()

    # -------------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:               # Close
            self.Call_OnClose()
        elif Request_Code == CODE_CLEAR_FOCUS:          # Clear Focus
            pass
        elif Request_Code == CODE_CLK_ON_TR_CODES:      # Clicked on Codes Tree [TRcode]
            pass
        elif Request_Code == CODE_CLIK_ON_XLSX:         # Clicked on Xlsx Tree  [nRow, Date]
            pass
        elif Request_Code == XLSX_UPDATED:
            self.Set_Texts()
            self.Create_RecordsList_ToBeInserted()
            self.Load_Tree()
            self.Set_Buttons()

    # -------------------------------------------------------------------------------------------------
    def Disable_Buttons(self):
        self.ViewXlsx.Btn_Disable()
        self.ViewTransact.Btn_Disable()
        self.Ins_Btn.Btn_Disable()

        # -------------------------------------------------------------------------------------------------
    def Set_Buttons(self):
        Xlsx_Filename = self.Data.Get_Selections_Member(Ix_Xlsx_File)
        if Xlsx_Filename != UNKNOWN:
            if self.Mod_Mngr.Cek_Xlsx_Name(Xlsx_Filename):
                self.ViewXlsx.Btn_Enable()
        Transact_Filename = self.Data.Get_Selections_Member(Ix_Transact_File)
        if Transact_Filename != UNKNOWN:
            if self.Mod_Mngr.Cek_Transactions_Name(Transact_Filename):
                self.ViewTransact.Btn_Enable()
        self.Set_Data()
        if self.Total[Ix_Tot_Without_Code] == 0:
            self.Ins_Btn.Btn_Enable()

    # -------------------------------------------------------------------------------------------------
    def Set_Data(self):
        # Ix_Tot_OK, Ix_Tot_WithCode, Ix_Tot_Without_Code
        self.Total             = self.Data.Get_Total_Rows()
        self.Xlsx_Filename     = self.Data.Get_Xlsx_Transact_Ident()[Ix_Xlsx_File]
        self.TotTra_ToInset    = self.TotTransact_ToBeInserted
        self.Transact_Filename = self.Data.Get_Xlsx_Transact_Ident()[Ix_Transact_File]
        self.Transact_Year     = self.Data.Get_TransacYear()

        # -------------------------------------------------------------------------------------------------
    def Clk_Sel_Xlsx(self):
        if not self.Mod_Mngr.Sel_Xlsx(TOP_INS):
            return
        self.Disable_Buttons()
        self.Data.Set_Files_Lodad(Ix_Transact_File, False)
        if not self.Mod_Mngr.Init_Top_Insert(TOP_INS):
            return
        self.Set_Data()
        self.Set_Texts()
        self.Create_RecordsList_ToBeInserted()
        self.Load_Tree()
        self.Set_Buttons()

    # -------------------------------------------------------------------------------------------------
    def ViewErr_OnTransact_Db(self, Texto):
        self.Dummy = 0
        Msg_Dlg    = Message_Dlg(MsgBox_Err, Texto)
        Msg_Dlg.wait_window()
        return

    # --------------------------------------------------------------------------------------------------
    #                      0        1         2         3         4        5        6      7
    # List_Transact_DB :  nRow    Conto    Contab    Valuta    TR_Desc   Accred   Addeb  TRcode
    # ---------------------------------------------------------------------------------------------------
    def Clk_Insert(self):
        self.Ins_Btn.Btn_Disable()
        if not self.Data.OpenClose_Transactions_Database(True, self.Full_Filename_For_Insert):
            self.ViewErr_OnTransact_Db('Errore fatale\n nell"aprire il Movimenti')
            return
        for Rec in self.TransactRecords_ToBeInserted:
            if not self.Data.Insert_Transact_Record(Rec):
                self.ViewErr_OnTransact_Db('Errore fatale\n nell"inserire Movimenti')
                return
        self.Data.OpenClose_Transactions_Database(False, self.Full_Filename_For_Insert)
        # Check for insertion on Db --------------------
        if not Modul_Mngr.Init_Transactions(TOP_INS):
            return
        if self.Mod_Mngr.Init_Top_Insert(TOP_INS):
            self.Create_RecordsList_ToBeInserted()
            self.Set_Data()
            self.Set_Texts()
            self.Load_Tree()
            self.Ins_Btn.Btn_Enable()

    # -------------------------------------------------------------------------------------------------
    def Set_Texts(self):
        self.Files_Ident = self.Data.Get_Xlsx_Transact_Ident()
        self.Conto       = self.Files_Ident[Ix_Xlsx_Conto]
        self.intYear     = self.Files_Ident[Ix_Xlsx_Year]
        self.intMonth    = self.Files_Ident[Ix_Xlsx_Month]

        Full_Transact_Name = self.Data.Get_Selections_Member(Ix_Transact_File)
        Transact_Name      = Get_File_Name(Full_Transact_Name)
        self.Txt_TransactName.Set_Text(Transact_Name)

        Full_Xlsx_Filename = self.Data.Get_Selections_Member(Ix_Xlsx_File)
        self.Xlsx_Filename = Get_File_Name(Full_Xlsx_Filename)
        self.Txt_Xlsx_Name.Set_Text(self.Xlsx_Filename)

        Conto = 'Conto: ' + self.Conto
        self.Txt_Conto.Set_Text(Conto)
        Year = 'Anno: ' + str(self.intYear)
        self.Txt_Xlsx_Year.Set_Text(Year)

        self.Full_Month    = Get_Xlsx_FullMonth(Full_Xlsx_Filename)
        Month = 'Mese: ' + str(self.Full_Month)
        self.Txt_Xlsx_Month.Set_Text(Month)

    # -------------------------------------------------------------------------------------------------
    def Create_RecToInsert_From_RowWithCode(self, RecWithCode):
        RecToInsert = [RecWithCode[iWithCode_nRow],
                       self.Conto,
                       RecWithCode[iWithCode_Contab],
                       RecWithCode[iWithCode_Valuta],
                       RecWithCode[iWithCode_TR_Desc],
                       RecWithCode[iWithCode_Accr],
                       RecWithCode[iWithCode_Addeb],
                       RecWithCode[iWithCode_TRcode]]
        return RecToInsert

    # -------------------------------------------------------------------------------------------------
    def Create_RecordsList_ToBeInserted(self):
        self.WithList                     = self.Data.Get_WithCodeList()
        self.TransactRecords_ToBeInserted = []
        self.TotTransact_ToBeInserted     = 0
        Month_List_Empty                  = self.Data.Create_Transact_Month_List_Empty()
        for Rec_InList in self.WithList:
            YearMonthV = Get_YearMonthDay(Rec_InList[iWithCode_Valuta])
            YearV      = YearMonthV[0]
            MonthV     = YearMonthV[1] - 1
            YearMonthC = Get_YearMonthDay(Rec_InList[iWithCode_Contab])
            YearC      = YearMonthC[0]
            MonthC     = YearMonthC[1] - 1
            if YearV == self.intYear  or  YearC == self.intYear:
                RecToInsert = self.Create_RecToInsert_From_RowWithCode(Rec_InList)
                if Month_List_Empty[MonthV] and Month_List_Empty[MonthC]:
                    ToInsert = True
                else:
                    if self.Data.Check_IfTransactRecord_InDatabase(RecToInsert):
                        ToInsert = False
                    else:
                        ToInsert = True
                if ToInsert:
                    self.TotTransact_ToBeInserted += 1
                    self.TransactRecords_ToBeInserted.append(RecToInsert)
        pass

    # -------------------------------------------------------------------------------------------------
    def Load_Tree(self):
        strToInsert =  '  NO  '
        if self.TotTransact_ToBeInserted != 0:
            strToInsert = str(self.TotTransact_ToBeInserted )
        self.Frame_Transact.Load_Row_Values(self.TransactRecords_ToBeInserted)
        FrameTitle = '    ' + strToInsert + '    Movimenti  da inserire    '
        self.Frame_Transact.Frame_Title(FrameTitle)

    # -------------------------------------------------------------------------------------------------
    def Frame_Transact_Setup(self):
        Nrows     = 38
        nColToVis = 8
        Headings  = ['#0', 'row','Conto ','Contab  ','Valuta  ','Descrizione ','Entrate  ','Uscite ','codice']
        Anchor    = ['c',  'c',  'c',     'c',       'c',       'w',           'e',       'e',      'c']
        Width     = [ 0,    40,   70,      90,        90,        170,           75,        75,       60]
        Form_List_Rows = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_Transact.Tree_Setup(Form_List_Rows)

    # -------------------------------------------------------------------------------------------------
    def Clk_Codes_Mngr(self):
        self.Mod_Mngr.Top_Launcher(TOP_MNGR, TOP_INS, [])

    # -------------------------------------------------------------------------------------------------
    def Clk_View_Xlsx(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_INS, [])

    # ---------------------------------------------------------------------------------------------
    def Clk_View_Transact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT, TOP_INS, [])

    # -------------------------------------------------------------------------------------------------
    def Test_If_Year_Month_OK(self, selected_Year, selected_nMonth):
        if selected_Year < self.Data.Min_Year:
            return 1
        if selected_nMonth < 1 or selected_nMonth > 12:
            return 2
        return 3            # Year and month are OK

    # -------------------------------------------------------------------------------------------------
    def Clk_Ontree_View(self, Values):
        pass
    # =================================================================================================




