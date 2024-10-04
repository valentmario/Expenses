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

import os
import tkinter as tk
from Top_Expenses.Modules_Manager import Modul_Mngr
from Chat import Ms_Chat
from Common.Common_Functions import *
from Data_Classes.Transact_DB import Data

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
        self.Data     = Data
        self.Mod_Mngr = Modul_Mngr
        self.List     = List

        self.Chat.Attach([self, TOP_INS])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)
        self.resizable(False, False)
        self.configure(background=BakGnd)
        self.geometry(Top_Insert_geometry)
        self.title('*****     Insert transactions on database     *****')

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
        self.Sel_Xlsx     = TheButton(self, Btn_Def_En,  20, 900, 19, 'Select xlsx file',    self.Clk_Sel_Xlsx)
        self.ViewXlsx     = TheButton(self, Btn_Def_Dis, 20, 940, 19, 'Show xlsx file',      self.Clk_View_Xlsx)

        self.Cod_Mngr     = TheButton(self, Btn_Def_Dis, 240, 900, 19, 'Codes Manager',      self.Clk_Codes_Mngr)
        self.ViewTransact = TheButton(self, Btn_Def_Dis, 240, 940, 19, 'Show Transactions Db',self.Clk_View_Transact)

        self.Ins_Btn      = TheButton(self, Btn_Def_Dis, 460, 900, 17, 'Insert Transactions', self.Clk_Insert)
        self.Exit         = TheButton(self, Btn_Def_En,  460, 940, 17, '  E X I T  ',         self.Call_OnClose)

        self.Total                        = []
        self.Tot_WithoutCode              = 0
        self.Xlsx_Filename                = ''
        self.Xlsx_Year                    = 0
        self.WithList                     = []
        self.TransactRecords_ToBeInserted = []
        self.TotTransact_ToBeInserted     = 0
        self.Transact_Filename            = ''
        self.Transact_Year                = 0

        if not self.Initialize():
            self.Disable_Buttons()
            self.Init_Status_Texto = ('      ---------------------------------------\n' +
                                      '      Xlsx file or transactions file\n          N O T   O K' +
                                      '\n      ---------------------------------------')
            self.Txt_Init_Status   = TheText(self, Txt_Disab, 140, 450, 28, 4, self.Init_Status_Texto)
        else:
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
        self.Cod_Mngr.Btn_Disable()
        self.ViewTransact.Btn_Disable()
        self.Ins_Btn.Btn_Disable()

        # -------------------------------------------------------------------------------------------------
    def Set_Buttons(self):
        self.ViewXlsx.Btn_Enable()
        self.Cod_Mngr.Btn_Enable()
        self.ViewTransact.Btn_Enable()
        if self.Total[Ix_Tot_Without_Code] == 0:
            self.Ins_Btn.Btn_Enable()
        pass

    # -------------------------------------------------------------------------------------------------
    def Create_New_Transact_Db(self, Year):
        Full_Name = self.Data.Create_TRansact_Filename(Year)
        # Full_Name ="/home/mario/myDatabase.db"
        if self.Data.Create_Transact_DB_File(Full_Name):
            self.Init_Status_Texto = ('New:  ' + str(Year) + '   Transactions Db created')
            Result = self.Data.Load_Transact_Table(Full_Name)
            if Result == OK:
                self.Data.Update_Selections(Full_Name, Ix_Transact_File)
                self.Chat.Tx_Request([TOP_INS, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
            else:
                self.Init_Status_Texto = Result
                return False
        else:
            self.Init_Status_Texto = 'ERROR on creating Transactions Table\nafter creation'
            return False

    # -------------------------------------------------------------------------------------------------
    def Check_For_Xlsx_Transact_Year(self):
        # -----------------   years   NOT  EQUAL    ---------------------------
        TRansact_Years_List = self.Data.Get_Transact_Year_ListInData()[1]
        if self.Xlsx_Year in TRansact_Years_List:
            newTransact_Filename = Transact_ + str(self.Xlsx_Year) + '.db'
            Dir_Name = Get_Dir_Name(self.Data.Get_Selections_Member(Ix_Transact_File))
            Full_Filename = Dir_Name + newTransact_Filename
            File_Exists = os.path.isfile(Full_Filename)
            if not File_Exists:
                self.Init_Status_Texto = ('inexplicably transactions Db  ' + Full_Filename +
                                          '\nfor xlsx year: ' + str(self.Xlsx_Year) + 'doesn"t exist')
                return False

            self.Init_Status_Texto = (str(self.Xlsx_Year) + ' Year for Xlsx   ' + newTransact_Filename +
                                      '   Year for Transactions Db  are OK')
            self.Data.Update_Selections(newTransact_Filename, Ix_Transact_File)
            return True

        else:  # ------------------  any transactions file found ----------
            if not self.Create_New_Transact_Db(self.Xlsx_Year):
                Msg_Dlg = Message_Dlg(MsgBox_Err, self.Data.Init_Status_Texto)
                Msg_Dlg.wait_window()
                return False
            else:
                Msg_Dlg = Message_Dlg(MsgBox_Info, self.Data.Init_Status_Texto)
                Msg_Dlg.wait_window()
                return True

    # --------------------------------------------------------------------------------------------------
    def Initialize(self):          # called on startup and on click Sel file Xlsx
        self.Disable_Buttons()
        self.Init_Status_Texto = ''
        # -------------------  an xlsx file must be loaded  -----------------
        if not self.Data.Get_Files_Loaded_Stat(Ix_Xlsx_File):
            self.Init_Status_Texto = 'An Xlsx file must be selected'
            return False
        self.Xlsx_Filename   = self.Data.Get_Selections_Member(Ix_Xlsx_File)
        self.Xlsx_Year       = Get_Xlsx_Year(self.Xlsx_Filename)
        self.Total           = self.Data.Get_Total_Rows()
        self.Tot_WithoutCode = self.Total[Ix_Tot_Without_Code]
        # -------------------  some Xlsx rows without code  -----------------
        if self.Tot_WithoutCode != 0:
            self.Init_Status_Texto = (str(self.Tot_WithoutCode) + '  Xlsx rows without code\n'
                                            'Update codes\then try again')
            return False

        # -----------------  Transactions file name is unknown    -------------
        else:
            self.Transact_Filename    = self.Data.Get_Selections_Member(Ix_Transact_File)
            if self.Transact_Filename == UNKNOWN:
                if not self.Create_New_Transact_Db(self.Xlsx_Year):
                    return False
                else:
                    self.Initialize_Tansactions()
                    return True

        # -------- Check for transactions year same as xlsx year   -------------
        self.Transact_Year = Get_Transactions_Year(self.Transact_Filename)
        if self.Xlsx_Year == self.Transact_Year:
            return self.Initialize_Tansactions()
        else:
            return self.Check_For_Xlsx_Transact_Year()

    # ------------------------------------------------------------------------------------------------
    def Initialize_Tansactions(self):
        Result = self.Data.Load_Transact_Table(self.Transact_Filename)
        if Result == OK:
            return True
        else:
            self.Init_Status_Texto = Result
            return False

    # -------------------------------------------------------------------------------------------------
    def Clk_Sel_Xlsx(self):
        if not self.Mod_Mngr.Sel_Xlsx(TOP_INS):
            return

        self.Disable_Buttons()
        if not self.Mod_Mngr.Init_Xlsx_Lists(TOP_INS):
            return
        if self.Initialize():
            if self.Init_Status_Texto != '':
                Msg_Dlg = Message_Dlg(MsgBox_Info, self.Init_Status_Texto)
                Msg_Dlg.wait_window()
            self.Set_Texts()
            self.Create_RecordsList_ToBeInserted()
            self.Load_Tree()
            self.Set_Buttons()
        else:
            Msg_Dlg = Message_Dlg(MsgBox_Info, self.Init_Status_Texto)
            Msg_Dlg.wait_window()

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
            self.ViewErr_OnTransact_Db('Fatal error\non open transactions Db')
            return
        for Rec in self.TransactRecords_ToBeInserted:
            if not self.Data.Insert_Transact_Record(Rec):
                self.ViewErr_OnTransact_Db('Fatal error on\ninsert record in transactions Db')
                return
        self.Data.OpenClose_Transactions_Database(False, self.Full_Filename_For_Insert)
        # Check for insertion on Db --------------------
        if not Modul_Mngr.Init_Transactions(TOP_INS):
            return
        self.Create_RecordsList_ToBeInserted()
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
        Xlsx_Filename      = Get_File_Name(Full_Xlsx_Filename)
        self.Txt_Xlsx_Name.Set_Text(Xlsx_Filename)

        Conto = 'Conto: ' + self.Conto
        self.Txt_Conto.Set_Text(Conto)
        Year = 'Year: ' + str(self.intYear)
        self.Txt_Xlsx_Year.Set_Text(Year)

        self.Full_Month    = Get_Xlsx_FullMonth(Full_Xlsx_Filename)
        Month = 'Month: ' + str(self.Full_Month)
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
        FrameTitle = '    ' + strToInsert + '    Transactions to be inserted    '
        self.Frame_Transact.Frame_Title(FrameTitle)

    # -------------------------------------------------------------------------------------------------
    def Frame_Transact_Setup(self):
        Nrows     = 38
        nColToVis = 8
        Headings  = ['#0', 'row','Conto ','Contab  ','Valuta  ','Description','Credits  ','Debits ','code  ']
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




