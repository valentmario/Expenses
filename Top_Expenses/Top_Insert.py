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
    def __init__(self, Result, Param_List):
        super().__init__()
        self.Chat       = Ms_Chat
        self.Data       = Data
        self.Mod_Mngr   = Modul_Mngr
        self.Result     = Result
        self.Param_List = Param_List

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

        self.Tree_Transact_Title      = ''
        self.Transact_InDatabase_List = []
        self.Full_Filename_For_Insert = self.Data.Get_Selections_Member(Ix_Transact_File)

        self.Txt_TransactYear = TheText(self, Txt_Disab,  20,  20, 18, 1, '')
        self.Txt_Xlsx_Year    = TheText(self, Txt_Disab, 200,  20, 19, 1, '')
        self.Txt_Xlsx_Name    = TheText(self, Txt_Disab, 370,  20, 10, 1, '')
        self.Txt_Conto        = TheText(self, Txt_Disab, 465,  20, 13, 1, '')

        self.Init_Status       = OK
        self.Init_Status_Texto = 'Inititialization status = OK'
        self.Txt_Init_Status   =  TheText(self, Txt_Disab, 20,  860, 70, 1, self.Init_Status_Texto)

        #  ------------------------------------  B U T T O N s  ---------------------------------------
        TheButton(self, Btn_Def_En,  20, 900, 19, 'Select xlsx file',   self.Clk_Sel_Xlsx)
        TheButton(self, Btn_Def_Dis, 20, 940, 19, 'Show xlsx file',     self.Clk_View_Xlsx)

        TheButton(self, Btn_Def_Dis, 220, 900, 19, 'Codes Manager',       self.Clk_Codes_Mngr)
        TheButton(self, Btn_Def_Dis, 220, 940, 19, 'Show Transactions Db',self.Clk_View_Transact)

        self.Ins_Btn = TheButton(self, Btn_Def_En, 420, 900, 17, 'Insert Transactions', self.Clk_Insert)
        TheButton(self, Btn_Def_En, 420, 940, 17, '  E X I T  ', self.Call_OnClose)

        self.WithList                       = []
        self.TransactRecords_ToBeInserted   = []
        self.TotTransact_ToBeInserted       = 0
        self.DoDlg = False
        self.Initialize()

        if not self.Initialize():
            pass
        else:
            # --------------------------  T R E E     Transactions to insert   ----------------------------
            self.Frame_Transact = TheFrame(self, 20, 60, self.Clk_Ontree_View)
            self.Frame_Transact_Setup()
            self.Frame_Transact.Frame_View()

        # self.WithList                       = []
        # self.TransactRecords_ToBeInserted   = []
        # self.TotTransact_ToBeInserted       = 0
        # self.Initialize()

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
            pass
            # self.Load_Tree()

    # --------------------------------------------------------------------------------------------------
    def Initialize(self):
        self.Disable_Buttons()
        self.Init_Status_Texto = -1   # -1=OK  1=NoCodes   2=Not created
        if not self.Check_For_Xlsx_Transact_Files():    # Check Transactions Filename
            return
        if not Modul_Mngr.Init_Transactions(TOP_INS):   # Init Transactions
            return
        # self.Set_Texts()
        # if not self.Create_RecordsList_ToBeInserted():
        #     return
        # self.Load_Tree()
        # self.Set_Buttons()

    # -------------------------------------------------------------------------------------------------
    def Disable_Buttons(self):
        pass

    # -------------------------------------------------------------------------------------------------
    def Set_Buttons(self):
        pass

    # -------------------------------------------------------------------------------------------------
    def Create_New_Transact_Db(self, Year):
        Full_Name = self.Data.Create_TRansact_Filename(Year)
        if self.Data.Create_Transact_DB_File(Full_Name):
            self.Init_Status_Texto = ('New:  ' + str(Year) + '   Transactions Db created')

            if not self.Data.Load_Transact_Table(Full_Name):
                self.Init_Status_Texto = 'ERROR on loading Transactions Table\nafter creation'
                self.Init_Status       = 2
                return False
            self.Data.Update_Selections(Full_Name, Ix_Transact_File)
            self.Chat.Tx_Request([TOP_INS, [MAIN_WIND], UPDATE_FILES_NAME, []])
            return True
        else:
            self.Init_Status_Texto = 'ERROR on creating\nnew database'
            self.Init_Status = 2
            return False
    # -------------------------------------------------------------------------------------------------
    def Check_For_Xlsx_Transact_Files(self):
        Total           = Data.Get_Total_Rows()
        Tot_WithoutCode = Total[Ix_Tot_Without_Code]
        XlsxYear = 0
        if Tot_WithoutCode != 0:  # ---------  some Xlsx rows without code  -----------------
            self.Init_Status = 1
            self.Init_Status_Texto = (str(Tot_WithoutCode) + '  Xlsx rows without code\n'
                                            'Update codes\then try to insert again')
            return False
        else:  # -----------   Check Transactions filename UNKNOWN   ----------------------
            Transact_Filename = Data.Get_Selections_Member(Ix_Transact_File)
            if Transact_Filename == UNKNOWN:
                if not self.Create_New_Transact_Db(XlsxYear):
                    return False   # Init_Status = 2
                else:
                    return True
            else:  # ---  Compare  Year of Xlsx file  with Year of Transactions file  ----
                TransactYear = Get_Transactions_Year(Transact_Filename)
                Files_Ident  = Data.Get_Xlsx_Transact_Ident()
                XlsxYear     = Files_Ident[Ix_Xlsx_Year]
                if XlsxYear == TransactYear:
                    return True
                else:
                    # -----------------   years   NOT  EQUAL    ---------------------------
                    TRansact_Years_List = Data.Get_Transact_Year_ListInData()
                    if XlsxYear in TRansact_Years_List:
                        Result = self.Find_Transact_ForXlsxYear(XlsxYear)
                        if Result == NOK:
                            return False
                        else:
                            Data.Update_Selections(Result, Ix_Transact_File)
                            return True
                    else:  # ------------------  any transactions file found ----------
                        if not self.Create_New_Transact_Db(XlsxYear):
                            return False
                        else:
                            return True

    # -------------------------------------------------------------------------------------------------
    def Find_Transact_ForXlsxYear(self, XlsxYear):
        newTransact_Filename   = Transact_ + str(XlsxYear) + '.db'
        self.Init_Status_Texto = (str(XlsxYear) + ' Year for Xlsx   ' + newTransact_Filename +
                                   '   Year for Transactions Db  is loade')

        Dir_Name           = Get_Dir_Name(Data.Get_Selections_Member(Ix_Transact_File))
        Full_Filename      = Dir_Name + newTransact_Filename
        File_Exists        = os.path.isfile(Full_Filename)
        if not File_Exists:
            Texto = 'inexplicably transactions Db  ' + Full_Filename
            Texto += '\nfor xlsx year: ' + XlsxYear + 'doesn"t exist'
            self.Init_Status = 3
            return False
        return Full_Filename

    # -------------------------------------------------------------------------------------------------
    def Clk_Sel_Xlsx(self):
        self.Ins_Btn.Btn_Disable()
        if not self.Mod_Mngr.Sel_Xlsx(TOP_INS):
            return
        if not self.Mod_Mngr.Init_Xlsx_Lists(TOP_INS):
            return
        self.Initialize()

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
        if not self.Create_RecordsList_ToBeInserted():
            return
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
        self.Txt_TransactYear.Set_Text(Transact_Name)

        Full_Xlsx_Filename = self.Data.Get_Selections_Member(Ix_Xlsx_File)
        Xlsx_Filename      = Get_File_Name(Full_Xlsx_Filename)
        self.Txt_Xlsx_Year.Set_Text(Xlsx_Filename)

        Year = 'Year: ' + str(self.intYear)
        self.Txt_Xlsx_Name.Set_Text(Year)

        Conto = 'Conto: ' + self.Conto
        self.Txt_Conto.Set_Text(Conto)



    # -------------------------------------------------------------------------------------------------
    # def Find_Transact_ForXlsxYear(self, XlsxYear, TransactYear):
    #     newTransact_Filename   = Transact_ + str(XlsxYear) + '.db'
    #     Messg  = str(XlsxYear) + ' Year for Xlsx\n'
    #     Messg += str(TransactYear) + ' Year for Transactions Db\n'
    #     Messg += 'Not equal\n' + newTransact_Filename + '  will be loaded'
    #     Msg_Dlg = Message_Dlg(MsgBox_Info, Messg)
    #     Msg_Dlg.wait_window()
    #     Dir_Name           = Get_Dir_Name(self.Data.Get_Xlsx_Transact_Ident())
    #     Full_Filename      = Dir_Name + newTransact_Filename
    #     File_Exists        = os.path.isfile(Full_Filename)
    #     if not File_Exists:
    #         Messg = 'inexplicably transactions Db:\n' + Full_Filename
    #         Messg += '\nfor xlsx year: ' + XlsxYear + 'doesn"t exist'
    #         MsgDlg = Message_Dlg(MsgBox_Err, Messg)
    #         MsgDlg.wait_window()
    #         return NOK
    #     return Full_Filename

    # -------------------------------------------------------------------------------------------------
    def Create_RecToInsert_From_RowWithCode(self, RecWithCode):
        # Files_Ident = self.Data.Get_Xlsx_Transact_Ident()
        # Conto       = Files_Ident[Ix_Xlsx_Conto]
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
        List_Empty                        = True
        for RecToCheck in self.WithList:
            YearMonthV = Get_YearMonthDay(RecToCheck[iWithCode_Valuta])
            YearV      = YearMonthV[0]
            MonthV     = YearMonthV[1] - 1
            YearMonthC = Get_YearMonthDay(RecToCheck[iWithCode_Contab])
            YearC      = YearMonthC[0]
            MonthC     = YearMonthC[1] - 1
            Check      = True
            Insert     = True
            if YearV == self.intYear  or  YearC == self.intYear:
                if Month_List_Empty[MonthV] and Month_List_Empty[MonthC] :
                    Check = False
                RecToInsert = self.Create_RecToInsert_From_RowWithCode(RecToCheck)
                if Check:
                    if not self.Data.Check_IfTransactRecord_InDatabase(RecToInsert):
                        Insert = True
                else:
                    Insert = True
                if Insert:
                    self.TotTransact_ToBeInserted += 1
                    self.TransactRecords_ToBeInserted.append(RecToInsert)
                    List_Empty = False
        return List_Empty


    # -------------------------------------------------------------------------------------------------
    def Load_Tree(self):
        if  self.Init_Status != -1:
            self.Frame_Transact.Load_Row_Values([])
            self.Frame_Transact.Frame_Title('   ')
            return
        else:
            TotToInsert = self.TotTransact_ToBeInserted
            strToInsert = ' NO '
            if TotToInsert != 0:
                strToInsert = str(TotToInsert)
            self.Frame_Transact.Load_Row_Values(self.TransactRecords_ToBeInserted)
            FrameTitle = '    ' + strToInsert + '    Transactions to be inserted    '
            self.Frame_Transact.Frame_Title(FrameTitle)

    # -------------------------------------------------------------------------------------------------
    def Frame_Transact_Setup(self):
        Nrows = 37
        nColToVis = 7
        Headings = ['#0', 'row', 'Contab  ', 'Valuta  ', 'Description', 'Credits  ', 'Debits ', 'code  ']
        Anchor = ['c', 'c', 'c', 'c', 'w', 'e', 'e', 'c']
        Width = [0, 40, 80, 80, 150, 75, 75, 50, 70]
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




