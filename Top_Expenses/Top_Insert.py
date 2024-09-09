# ---------------------------------------------------------------------------------- #
#                      *****     Top_Insert.py     *****                             #
#                  Insert Transactions on Transactions database                      #
#                                                                                    #
# ---------------------------------------------------------------------------------- #

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

        self.Files_Ident = self.Data.Get_Xlsx_Transact_Ident()
        self.Conto       = self.Files_Ident[Ix_Xlsx_Conto]
        self.intYear     = self.Files_Ident[Ix_Xlsx_Year]
        self.intMonth    = self.Files_Ident[Ix_Xlsx_Month]
        self.Years_Match = False
        self.Continue    = True

        self.Tree_Transact_Title      = ''
        self.Transact_InDatabase_List = []
        self.Full_Filename_For_Insert = self.Data.Get_Txt_Member(Ix_Transact_File)

        self.Trs_Txt   = TheText(self, Txt_Disab,  20,  20, 18, 1, '')
        self.Xlsx_Txt  = TheText(self, Txt_Disab, 200,  20, 19, 1, '')
        self.Year_Txt  = TheText(self, Txt_Disab, 370,  20, 10, 1, '')
        self.Conto_Txt = TheText(self, Txt_Disab, 465,  20, 13, 1, '')

        self.Tot_Text = TheText(self, Txt_Disab, 20, 860, 22, 1, '')

        #  ------------------------------------  B U T T O N s  ---------------------------------------
        self.Ins_Btn = TheButton(self, Btn_Def_En, 220, 860, 19, 'Insert Transactions', self.Clk_Insert)
        TheButton(self, Btn_Def_En, 420, 860, 16, 'Codes Manager',      self.Clk_Codes_Mngr)
        TheButton(self, Btn_Def_En,  20, 900, 19, 'Select  xlsx  file', self.Clk_Sel_xlsx)
        TheButton(self, Btn_Def_En,  20, 940, 19, 'View xlsx file',     self.Clk_View_Xlsx)

        TheButton(self, Btn_Def_En, 220, 900, 19, 'Select  Transactions  file', self.Clk_Sel_Transact)
        TheButton(self, Btn_Def_En, 220, 940, 19, 'View Transactions file',     self.Clk_View_Transact)

        TheButton(self, Btn_Def_En, 420, 940, 16, '  E X I T  ', self.Call_OnClose)

        # --------------------------  T R E E     Transactions to insert   ----------------------------
        self.Frame_Transact = TheFrame(self, 20, 60, self.Clk_Ontree_View)
        self.Frame_Transact_Setup()
        self.Frame_Transact.Frame_View()

        self.WithList                     = []
        self.TransactRecords_ToBeInserted = []
        self.TotTransact_ToBeInserted     = 0

        self.Set_Full_Transact_Name()
        # Full_Transact_Name = self.Data.Get_Txt_Member(Ix_Transact_File)
        # Transact_Name = Get_File_Name(Full_Transact_Name)
        # self.Trs_Txt.Set_Text(Transact_Name)

        Full_Xlsx_Filename = self.Data.Get_Txt_Member(Ix_Xlsx_File)
        Xlsx_Filename      = Get_File_Name(Full_Xlsx_Filename)
        self.Xlsx_Txt.Set_Text(Xlsx_Filename)

        Year = 'Year: ' + str(self.intYear)
        self.Year_Txt.Set_Text(Year)
        Conto = 'Conto: ' + self.Conto
        self.Conto_Txt.Set_Text(Conto)

        # ---------------------------------------------------------------------

        if not self.Check_For_Insert():
            self.Call_OnClose()
            return
        self.Tree_Update()

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
            self.Tree_Update()

    def Frame_Transact_Setup(self):
        Nrows     = 37
        nColToVis = 7
        Headings  = ['#0', 'row', 'Contab  ' ,'Valuta  ', 'Description', 'Credits  ', 'Debits ', 'code  ']
        Anchor    = ['c',  'c',   'c',      'c',          'w',           'e',         'e',       'c'  ]
        Width     = [0,     40,    80,       80,           150,           75,          75,        50,       70  ]
        Form_List_Rows = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_Transact.Tree_Setup(Form_List_Rows)

    # -------------------------------------------------------------------------------------------------
    def Check_For_Insert(self):
        self.Years_Match = False
        self.Ins_Btn.Btn_Disable()
        Total = self.Data.Get_Total_Rows()
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
                for Year in TRansact_Years_List:
                    if XlsxYear == Year:
                        if not self.Load_Transact_Found(Year):
                            self.Call_OnClose()
                            return False  # Insert not enabled
                else:
                    if not self.Create_New_Transact_Db(XlsxYear):
                        return False

        self.Ins_Btn.Btn_Enable()
        self.Years_Match = True
        return True

    # -------------------------------------------------------------------------------------------------
    def Set_Full_Transact_Name(self):
        Full_Transact_Name = self.Data.Get_Txt_Member(Ix_Transact_File)
        Transact_Name = Get_File_Name(Full_Transact_Name)
        self.Trs_Txt.Set_Text(Transact_Name)

    # -------------------------------------------------------------------------------------------------
    def Load_Transact_Found(self, Year):
        Transact_Filename = Transact_ + str(Year) + '.db'
        Msg = 'Found transactions  Db:\n' + Transact_Filename + '\nLoad it'
        Msg_Dlg = Message_Dlg(MsgBox_Ask, Msg)
        Msg_Dlg.wait_window()
        Reply = Msg_Dlg.data
        if Reply != YES:
            return False
        Curr_Full_Filename = self.Data.Get_Txt_Member(Ix_Transact_File)
        Dir_Name           = Get_Dir_Name(Curr_Full_Filename)
        Full_Filename      = Dir_Name + Transact_Filename
        File_Exists        = os.path.isfile(Full_Filename)
        if not File_Exists:
            Messg = 'inexplicably transaction Db:\n' + \
                     Full_Filename + 'doesn"t exist'
            MsgDlg = Message_Dlg(MsgBox_Err, Messg)
            MsgDlg.wait_window()
            return False
        self.Data.Update_Txt_File(Full_Filename, Ix_Transact_File)
        self.Data.Transact_Year_Setup(True)
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
                self.Set_Full_Transact_Name()
                self.Chat.Tx_Request([TOP_INS, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
            Msg = Message_Dlg(MsgBox_Err, 'ERROR on creating\nnew database')
            Msg.wait_window()
            return False
    # -------------------------------------------------------------------------------------------------
    def Create_RecToInsert_From_RowWithCode(self, RecWithCode):
        Files_Ident = self.Data.Get_Xlsx_Transact_Ident()
        Conto = Files_Ident[Ix_Xlsx_Conto]
        RecToInsert = [RecWithCode[iWithCode_nRow],
                       Conto,
                       RecWithCode[iWithCode_Contab],
                       RecWithCode[iWithCode_Valuta],
                       RecWithCode[iWithCode_TR_Desc],
                       RecWithCode[iWithCode_Accr],
                       RecWithCode[iWithCode_Addeb],
                       RecWithCode[iWithCode_TRcode],
                       RecWithCode[iWithCode_TRcode]]
        return RecToInsert

    # -------------------------------------------------------------------------------------------------
    # The case of two identical recodes (Dates, value, Code)
    # for example ATM withdrawals at the same day for the same value
    # must be adjustad manually; i.e. for two 100€ must modified manually
    # in 99.99 and 100.1
    # -------------------------------------------------------------------------------------------------
    def Check_For_Multiple_Record_OnWitCodeList(self, RecToCheck):
        nFound = 0
        Rec    = None
        for Rec in self.WithList:
            if Rec == RecToCheck:
                nFound += 1
        if nFound == 1:
            return False
        else:
            Message = 'Row: ' + str(Rec[iWithCode_nRow]) + \
                      '\nfound in more records WitCode List\nAdjust records\nExit '
            Dlg_Msg = Message_Dlg(MsgBox_Err, Message)
            Dlg_Msg.wait_window()
            return True

    # -------------------------------------------------------------------------------------------------
    def Create_RecordsList_ToBeInserted(self):
        self.WithList = self.Data.Get_WithCodeList()
        self.TransactRecords_ToBeInserted = []
        self.TotTransact_ToBeInserted     = 0
        for Rec in self.WithList:
            if self.Check_For_Multiple_Record_OnWitCodeList(Rec):
                self.Call_OnClose()
                return
            # On transactions database will be inserted record with
            # Year of Valuta  or Year of Contab == self.intYear
            YYYYmmDDvaluta = Get_DMY_From_Date(Rec[iWithCode_Valuta])
            YYYYmmDDcontab = Get_DMY_From_Date(Rec[iWithCode_Contab])
            if YYYYmmDDvaluta[2] == self.intYear or YYYYmmDDcontab[2] == self.intYear:
                if not self.Test_If_Rec_In_Database(Rec):
                    self.TotTransact_ToBeInserted += 1
                    self.TransactRecords_ToBeInserted.append(Rec)
            else:
                pass

    # -------------------------------------------------------------------------------------------------
    def Tree_Update(self):
        if not self.Years_Match:
            self.Frame_Transact.Load_Row_Values([])
            self.Frame_Transact.Frame_Title('   ')
            return
        else:
            self.Create_RecordsList_ToBeInserted()
            strTotal = str(self.TotTransact_ToBeInserted)
            TotTexto = 'Total on ' + str(self.intYear) + ' = ' + strTotal
            self.Tot_Text.Set_Text(str(TotTexto))
            self.Frame_Transact.Load_Row_Values(self.TransactRecords_ToBeInserted)
            FrameTitle = '    ' + strTotal + '    Transactions to be inserted    '
            self.Frame_Transact.Frame_Title(FrameTitle)

    # --------------------------------------------------------------------------------------------------
    #                      0        1         2         3         4        5        6      7
    # List_Transact_DB :  nRow    Conto    Contab    Valuta    TR_Desc   Accred   Addeb  TRcode
    # ---------------------------------------------------------------------------------------------------
    def Clk_Insert(self):
        self.Data.OpenClose_Transactions_Database(True, self.Full_Filename_For_Insert)
        for Rec in self.TransactRecords_ToBeInserted:
            RecToInsert = self.Create_RecToInsert_From_RowWithCode(Rec)
            self.Data.Insert_Transact_Record(RecToInsert)
        self.Data.OpenClose_Transactions_Database(False, self.Full_Filename_For_Insert)
        strTotal = str(self.TotTransact_ToBeInserted)
        Texto    = strTotal + '\ntransactions inserted'
        Messg = Message_Dlg(MsgBox_Info, Texto )
        Messg.wait_window()
        self.Tree_Update()

    # -------------------------------------------------------------------------------------------------
    def Clk_Codes_Mngr(self):
        self.Mod_Mngr.Top_Launcher(TOP_MNGR, TOP_INS)

    # -------------------------------------------------------------------------------------------------
    def Clk_Ontree_View(self, Values):
        pass

    # ---------------------------------------------------------------------------------------------
    def Clk_Sel_xlsx(self):
        self.Ins_Btn.Btn_Disable()
        if self.Mod_Mngr.Sel_Xlsx(TOP_INS):
            if self.Mod_Mngr.Load_Xlsx(TOP_INS):
                self.Tree_Update()

    # -------------------------------------------------------------------------------------------------
    def Clk_View_Xlsx(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_INS)

    # ---------------------------------------------------------------------------------------------
    def Clk_Sel_Transact(self):
        self.Ins_Btn.Btn_Disable()
        self.Frame_Transact.Load_Row_Values([])
        self.Frame_Transact.Frame_Title('   Transactions to be inserted   ')
        self.Frame_Transact.Frame_Title(self.Tree_Transact_Title)
        if self.Mod_Mngr.Sel_Transact(TOP_INS):
            if self.Mod_Mngr.Load_Transact(TOP_INS):
                self.Tree_Update()
                self.Check_For_Insert()
                self.Tree_Update()

    # ---------------------------------------------------------------------------------------------
    def Clk_View_Transact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT, TOP_INS)

    # ---------------------------------------------------------------------------------------------
    def Test_If_Rec_In_Database(self, RecToInsert):
        Result = self.Data.Check_IfTransactRecord_InDatabase(RecToInsert)
        if not Result:
            return False
        else:
            if self.Continue:
                RecToIns = Result[0]
                RecInDB  = Result[1]

                TextoIns = 'Rec to insert:\n'
                for Item in RecToIns:
                    TextoIns += ' ' + str(Item)
                pass
                TextoIns += '\n'

                TextoDb = 'Rec in database:\n'
                for Item in RecInDB:
                    TextoDb += ' ' + str(Item)
                pass
                TextoDb += '\n\nContinue ?'

                MsgText = TextoIns + TextoDb
                Dlg = Message_Dlg(MsgBox_Ask, MsgText)
                Dlg.wait_window()
                Reply = Dlg.data
                if Reply == NO:
                    self.Continue = False
            return True

    # -------------------------------------------------------------------------------------------------
    def Test_If_Year_Month_OK(self, selected_Year, selected_nMonth):
        if selected_Year < self.Data.Min_Year:
            return 1
        if selected_nMonth < 1 or selected_nMonth > 12:
            return 2
        return 3            # Year and month are OK
    # =================================================================================================




