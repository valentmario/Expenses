# ------------------------------------------------------------------------------------- #
#                      *****     Top_Insert.py     *****                                #
#                  Insert Transactions on Transactions database                         #
#                                                                                       #
# main methods:                                                                         #
# --------------------------------                                                      #
# Init_Transact_Db:                 (Load_Transact_Table)                               #
# Set_Texts                         (Transact_Name,  Xlsx_Name,  Xlsx_Year,  Conto      #
# Check_Files:                      (Without_Code and Transact_Db exists)
# Create_New_Transact_Db:
# Create_RecordsList_ToBeInserted:  (compare WitCode_List   and   Transact_Db
# Load_Tree:                        (as in  RecordsList_ToBeInserted)
#
# ---------------------------------
# main procedures:
# Startup:              - Init_Transact_Db (Create_New_Transact_Db)
#                       - Check_Files
#                       - Create_RecordsList_ToBeInserted
#                       - Set_Texts
#                       - Load_Tree
#                       - Ins_Btn.En-Disab
#
#
# Clk_Insert            - insert the RecordsList_ToBeInserted
#                       - Init_Transact_Db (Load_anyway)
#                       - Create_RecordsList_ToBeInserted
#                       - Set_Texts
#                       - Load_Tree
#                       - Ins_Btn.En-Disab
#
# Clk_Sel_Xlx           - Sel_Xlsx    then
#                       - as in Startup
#                                                                                       #
# ------------------------------------------------------------------------------------- #

import tkinter as tk
import os
from Top_Expenses.Modules_Manager import Modul_Mngr
from Chat import Ms_Chat
from Common.Common_Functions import *
from Data_Classes.Transact_DB import Data

from Widgt.Dialogs import Print_Received_Message
from Widgt.Dialogs import Message_Dlg
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheText

# -----------------------------------------------------------------------------------------------------
class Top_Insert(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data
        self.Mod_Mngr = Modul_Mngr

        self.Chat.Attach([self, TOP_INS])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)
        self.resizable(False, False)
        self.configure(background=BakGnd)
        self.geometry(Top_Insert_geometry)
        self.title('*****     Insert transactions on database     *****')

        self.Dummy       = 0
        self.Files_Ident = []  # self.Data.Get_Xlsx_Transact_Ident()
        self.Conto       = ''  # self.Files_Ident[Ix_Xlsx_Conto]
        self.intYear     = 0   # self.Files_Ident[Ix_Xlsx_Year]
        self.intMonth    = 1   # self.Files_Ident[Ix_Xlsx_Month]
        self.Years_Match = False
        self.Continue    = True

        self.Tree_Transact_Title      = ''
        self.Transact_InDatabase_List = []
        self.Full_Filename_For_Insert = self.Data.Get_Txt_Member(Ix_Transact_File)

        self.Txt_TransactYear = TheText(self, Txt_Disab,  20,  20, 18, 1, '')
        self.Txt_Xlsx_Year    = TheText(self, Txt_Disab, 200,  20, 19, 1, '')
        self.Txt_Xlsx_Name    = TheText(self, Txt_Disab, 370,  20, 10, 1, '')
        self.Txt_Conto        = TheText(self, Txt_Disab, 465,  20, 13, 1, '')

        #  ------------------------------------  B U T T O N s  ---------------------------------------
        TheButton(self, Btn_Def_En,  20, 900, 19, 'Select xlsx file',   self.Clk_Sel_Xlsx)
        TheButton(self, Btn_Def_En,  20, 940, 19, 'Show xlsx file',     self.Clk_View_Xlsx)

        TheButton(self, Btn_Def_En, 220, 900, 19, 'Codes Manager',       self.Clk_Codes_Mngr)
        TheButton(self, Btn_Def_En, 220, 940, 19, 'Show Transactions Db',self.Clk_View_Transact)

        self.Ins_Btn = TheButton(self, Btn_Def_En, 420, 900, 17, 'Insert Transactions', self.Clk_Insert)
        TheButton(self, Btn_Def_En, 420, 940, 17, '  E X I T  ',
                  self.Call_OnClose)

        # --------------------------  T R E E     Transactions to insert   ----------------------------
        self.Frame_Transact = TheFrame(self, 20, 60, self.Clk_Ontree_View)
        self.Frame_Transact_Setup()
        self.Frame_Transact.Frame_View()

        self.WithList                     = []
        self.TransactRecords_ToBeInserted = []
        self.TotTransact_ToBeInserted     = 0

        self.Startup()

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
            self.Load_Tree()

    # --------------------------------------------------------------------------------------------------
    def Startup(self):
        self.Ins_Btn.Btn_Disable()
        if not self.Check_For_Files():
            return
        if not Modul_Mngr.Init_Transactions(TOP_INS):
            return
        self.Set_Texts()
        if not self.Create_RecordsList_ToBeInserted():
            return
        self.Load_Tree()
        self.Ins_Btn.Btn_Enable()

    # -------------------------------------------------------------------------------------------------
    def Clk_Sel_Xlsx(self):
        self.Ins_Btn.Btn_Disable()
        if not self.Mod_Mngr.Sel_Xlsx(TOP_INS):
            return
        if not self.Mod_Mngr.Init_Xlsx(TOP_INS):
            return
        self.Startup()

    # -------------------------------------------------------------------------------------------------
    def ViewErr_OnTransact_Db(self):
        self.Dummy = 0
        Messg = 'Fatal error on Transact_db database'
        Msg_Dlg = Message_Dlg(MsgBox_Err, Messg)
        Msg_Dlg.wait_window()
        return

    # --------------------------------------------------------------------------------------------------
    #                      0        1         2         3         4        5        6      7
    # List_Transact_DB :  nRow    Conto    Contab    Valuta    TR_Desc   Accred   Addeb  TRcode
    # ---------------------------------------------------------------------------------------------------
    def Clk_Insert(self):
        self.Ins_Btn.Btn_Disable()
        if not self.Data.OpenClose_Transactions_Database(True, self.Full_Filename_For_Insert):
            self.ViewErr_OnTransact_Db()
            return
        for Rec in self.TransactRecords_ToBeInserted:
            if not self.Data.Insert_Transact_Record(Rec):
                self.ViewErr_OnTransact_Db()
                return
        self.Data.OpenClose_Transactions_Database(False, self.Full_Filename_For_Insert)
        # Check for insertion on Db --------------------
        if not Modul_Mngr.Init_Transactions(TOP_INS):
            return
        if not self.Create_RecordsList_ToBeInserted():
            return
        self.Set_Texts()
        self.Load_Tree()

        if not self.Create_RecordsList_ToBeInserted():
            return
        nToInsert = self.TotTransact_ToBeInserted
        if nToInsert != 0:
            Messg = 'Inexplicably there are still\n' + str(nToInsert)
            Msg_Dlg = Message_Dlg(MsgBox_Err, Messg)
            Msg_Dlg.wait_window()
            return
        self.Ins_Btn.Btn_Enable()

    # -------------------------------------------------------------------------------------------------
    def Check_For_Files(self):
        self.Years_Match = False
        self.Ins_Btn.Btn_Disable()
        Total           = self.Data.Get_Total_Rows()
        Tot_WithoutCode = Total[Ix_Tot_Without_Code]
        if Tot_WithoutCode != 0:
            Texto = str(Tot_WithoutCode) + '  Xlsx rows without code\nUpdate codes\then try to insert again'
            Msg_Dlg = Message_Dlg(MsgBox_Err, Texto)
            Msg_Dlg.wait_window()
            return False
        else:
            Files_Ident  = self.Data.Get_Xlsx_Transact_Ident()
            XlsxYear     = Files_Ident[Ix_Xlsx_Year]
            TransactYear = Files_Ident[Ix_Transact_Year]
            if XlsxYear != TransactYear:    # the name may be UNKNOWN
                TRansact_Years_List = self.Data.Get_Transact_Year_ListInData()
                if XlsxYear in TRansact_Years_List:
                    self. Load_Transact_Found(XlsxYear, TransactYear)
                else:
                    if not self.Create_New_Transact_Db(XlsxYear):
                        return False

        self.Ins_Btn.Btn_Enable()
        self.Years_Match = True
        return True

    # -------------------------------------------------------------------------------------------------
    def Set_Texts(self):
        self.Files_Ident = self.Data.Get_Xlsx_Transact_Ident()
        self.Conto       = self.Files_Ident[Ix_Xlsx_Conto]
        self.intYear     = self.Files_Ident[Ix_Xlsx_Year]
        self.intMonth    = self.Files_Ident[Ix_Xlsx_Month]

        Full_Transact_Name = self.Data.Get_Txt_Member(Ix_Transact_File)
        Transact_Name      = Get_File_Name(Full_Transact_Name)
        self.Txt_TransactYear.Set_Text(Transact_Name)

        Full_Xlsx_Filename = self.Data.Get_Txt_Member(Ix_Xlsx_File)
        Xlsx_Filename      = Get_File_Name(Full_Xlsx_Filename)
        self.Txt_Xlsx_Year.Set_Text(Xlsx_Filename)

        Year = 'Year: ' + str(self.intYear)
        self.Txt_Xlsx_Name.Set_Text(Year)

        Conto = 'Conto: ' + self.Conto
        self.Txt_Conto.Set_Text(Conto)

    # -------------------------------------------------------------------------------------------------
    def Load_Transact_Found(self, XlsxYear, TransactYear):
        newTransact_Filename = Transact_ + str(XlsxYear) + '.db'
        Messg  = str(XlsxYear) + ' Year for Xlsx\n'
        Messg += str(TransactYear) + ' Year for Transactions Db\n'
        Messg += 'Not equal\n' + newTransact_Filename + '  will be loaded'
        Msg_Dlg = Message_Dlg(MsgBox_Info, Messg)
        Msg_Dlg.wait_window()

        Curr_Full_Filename = self.Data.Get_Txt_Member(Ix_Transact_File)
        Dir_Name           = Get_Dir_Name(Curr_Full_Filename)
        Full_Filename      = Dir_Name + newTransact_Filename
        File_Exists        = os.path.isfile(Full_Filename)
        if not File_Exists:
            Messg = 'inexplicably transaction Db:\n' + \
                     Full_Filename + 'doesn"t exist'
            MsgDlg = Message_Dlg(MsgBox_Err, Messg)
            MsgDlg.wait_window()
            return False
        self.Data.Update_Txt_File(Full_Filename, Ix_Transact_File)
        self.Data.Transact_Year_Setup(True)
        self.Set_Texts()
        return self.Mod_Mngr.Init_Transactions(TOP_INS)

    # -------------------------------------------------------------------------------------------------
    def Create_New_Transact_Db(self, Year):
        Msg = 'Create new Transactions Db for:\n' + 'Year: ' +str(Year)
        Msg_Dlg = Message_Dlg(MsgBox_Ask, Msg)
        Msg_Dlg.wait_window()
        Reply = Msg_Dlg.data
        if Reply != YES:
            return False
        else:
            Full_Name = self.Data.Create_TRansact_Filename(Year)
            if self.Data.Create_Transact_DB_File(Full_Name):
                Msg = Message_Dlg(MsgBox_Info, ('New:  ' + str(Year) +
                                                '\nTransactions Db created'))
                Msg.wait_window()
                self.Data.Update_Txt_File(Full_Name, Ix_Transact_File)
                self.Data.Transact_Year_Setup(True)
                self.Chat.Tx_Request([TOP_INS, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
            Msg = Message_Dlg(MsgBox_Err, 'ERROR on creating\nnew database')
            Msg.wait_window()
            return False

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
    # The case of two identical records (Dates, value, Code etc.)
    # (for example ATM withdrawals at the same day for the same values)
    # Xlsx must be adjustad manually; i.e. for two 100€ Xlsx must be modified manually:
    # in 99.99 and 100.1
    # nRow    Contab    Valuta    TR_Desc   Accred   Addeb   TRcode
    # -------------------------------------------------------------------------------------------------
    # def Check_For_Multiple_Record_OnWitCodeList(self, RecToCheck):
    #     nFound = 0
    #     Rec    = None
    #     for Rec in self.WithList:
    #         Index = 0
    #         for Item in Rec:
    #
    #
    #         if Rec == RecToCheck:
    #             nFound += 1
    #     if nFound == 1:
    #         return False
    #     else:
    #         Message = 'Row: ' + str(Rec[iWithCode_nRow]) + \
    #                   '\nfound in more records WitCode List\nAdjust records\nExit '
    #         Dlg_Msg = Message_Dlg(MsgBox_Err, Message)
    #         Dlg_Msg.wait_window()
    #         return True

    # -------------------------------------------------------------------------------------------------
    def Create_RecordsList_ToBeInserted(self):
        self.WithList                     = self.Data.Get_WithCodeList()
        self.TransactRecords_ToBeInserted = []
        self.TotTransact_ToBeInserted     = 0
        for RecToCheck in self.WithList:
            Result = Data.Check_For_Multiple_Record_OnWitCodeList(RecToCheck)
            if Result != '':
                self.TotTransact_ToBeInserted = 0
                self.TransactRecords_ToBeInserted = []
                Dlg_Mess = Message_Dlg(MsgBox_Err, Result)
                Dlg_Mess.wait_window()
                return Dlg_Mess

            # On transactions database will be inserted records with
            # Year of Valuta  or Year of Contab == self.intYear
            YYYYmmDDvaluta = Get_DMY_From_Date(RecToCheck[iWithCode_Valuta])
            YYYYmmDDcontab = Get_DMY_From_Date(RecToCheck[iWithCode_Contab])
            if YYYYmmDDvaluta[2] == self.intYear or YYYYmmDDcontab[2] == self.intYear:
                RecToInsert = self.Create_RecToInsert_From_RowWithCode(RecToCheck)
                Result      = self.Data.Check_IfTransactRecord_InDatabase(RecToInsert)
                if not Result:
                    self.TotTransact_ToBeInserted += 1
                    self.TransactRecords_ToBeInserted.append(RecToInsert)
                else:
                    pass
        return True

    # -------------------------------------------------------------------------------------------------
    def Load_Tree(self):
        if not self.Years_Match:
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
        self.Mod_Mngr.Top_Launcher(TOP_MNGR, TOP_INS)

    # -------------------------------------------------------------------------------------------------
    def Clk_View_Xlsx(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_INS)

    # ---------------------------------------------------------------------------------------------
    def Clk_View_Transact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT, TOP_INS)

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




