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
from enum import CONTINUOUS

from Top_Expenses.Modules_Manager import Modul_Mngr
from Chat import Ms_Chat
from Common.Common_Functions import *
from Data_Classes.Transact_DB import Data_Manager

from Widgt.Dialogs import Print_Received_Message
from Widgt.Dialogs import Message_Dlg
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheText
from Widgt.Widgets import TheCombo

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

        self.Tree_Transact_Title      = ''
        self.Transact_InDatabase_List = []
        self.Full_Filename_For_Insert = self.Data.Get_Selections_Member(Ix_Transact_File)

        self.Txt_TransactName = TheText(self, Txt_Disab,  20,  20, 18,  1, '')
        self.Txt_Xlsx_Name    = TheText(self, Txt_Disab, 200,  20, 19,  1, '')
        self.Txt_Conto        = TheText(self, Txt_Disab, 370,  20, 12,  1, '')
        self.Txt_Xlsx_Year    = TheText(self, Txt_Disab, 484,  20, 11,  1, '')
        self.Txt_Xlsx_Month   = TheText(self, Txt_Disab, 590,  20, 11, 1, '')

        #  ------------------------------------  B U T T O N s  ---------------------------------------
        self.Sel_Xlsx     = TheButton(self, Btn_Def_En,   20, 860, 23, 'Seleziona un file xlsx', self.Clk_Sel_Xlsx)
        self.ViewXlsx     = TheButton(self, Btn_Def_Dis,  20, 900, 23, 'Mostra movimenti xlsx',  self.Clk_View_Xlsx)

        self.StrVar_Conto  = tk.StringVar
        self.OptMenu_Cont  = TheCombo(self, self.StrVar_Conto, 260, 860, 15, 16, Continue_List,
                                      STEP, self.Clk_Continue)
        self.UpToText      = TheText(self, Txt_Enab,          425, 860,   5,  1, '')

        self.ViewTransact = TheButton(self, Btn_Def_Dis,       20, 940,  23, 'Show Transactions on Db',self.Clk_View_Transact)

        self.Ins_Btn      = TheButton(self, Btn_Def_En,        260, 900, 23, 'Inserire Movimenti nel Db', self.Clk_Insert)

        self.ClrDb_Btn    = TheButton(self, Btn_Def_En,        260, 940, 23, '', self.Clk_Delete_DbInsert)

        self.Exit         = TheButton(self, Btn_Def_En,  500, 940, 23, '  F I N E  ',               self.Call_OnClose)

        self.Total           = []
        self.Tot_WithoutCode = 0
        self.Xlsx_Filename   = ''
        self.Xlsx_Year       = 0
        self.WithList        = []
        self.Rows_WithCod_List  = []
        self.Records_ToIns_List = []

        self.TotTransact_ToBeInserted = 0
        self.Transact_Filename        = ''
        self.Transact_Year            = 0
        self.Continue                 = STEP

        # --------------------------  T R E E     Transactions to insert   ----------------------------
        self.Frame_Transact = TheFrame(self, 20, 60, self.Clk_Ontree_View)
        self.Frame_Transact_Setup()
        self.Frame_Transact.Frame_View()

        self.Set_Texts()
        self.Create_RecordsList_ToBeInserted()
        self.Load_Tree(self.Records_ToIns_List)
        self.Set_Buttons()

    # -------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_INS)
        self.destroy()

    # -------------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Values_List)
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
            self.Load_Tree(self.Records_ToIns_List)
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
        self.Transact_Filename = self.Data.Get_Xlsx_Transact_Ident()[Ix_Transact_File]
        self.Transact_Year     = self.Data.Get_TransacYear()

    # -------------------------------------------------------------------------------------------------
    def Clk_Sel_Xlsx(self):
        if not self.Mod_Mngr.Sel_Xlsx_Mngr(TOP_INS):
            return
        self.Disable_Buttons()
        self.Data.Set_Files_Lodad(Ix_Xlsx_Lists_Loaded, False)
        if not self.Mod_Mngr.Init_Top_Insert(TOP_INS):
            return
        self.Set_Data()
        self.Set_Texts()
        self.Create_RecordsList_ToBeInserted()
        self.Load_Tree(self.Records_ToIns_List)
        self.Set_Buttons()

    # --------------------------------------------------------------------------------------------------
    def Purge_FulDesc(self, All, Full_Desc):
        self.Dummy = 0
        ToCheck = Full_Desc
        if All:
           ToCheck = Full_Desc[21:]
        Purged = ''
        for Char in ToCheck:
            if Char == '\n':
                pass
            else:
                Purged += Char
        return Purged

    # ---------------------------------------------------------------------------------------------------
    def Ask_For_RecToInsert(self, Rec_WithCode, RecToIns):
        self.Dummy = 0
        # iWithCode_nRow = 0  iWithCode_Contab= 1  iWithCode_Valuta = 2  iWithCode_TR_Desc = 3
        # iWithCode_Accr = 4  iWithCode_Added = 5  iWithCode_TRcode = 6  iWithCode_FullDesc= 7
        #
        # iTransact_nRow   = 0  iTransact_Conto = 1  iTransact_Contab= 2  iTransact_Valuta = 3
        # iTransact_TRdesc = 4  iTransact_Accred= 5  iTransact_Addeb = 6  iTransact_TRcode = 7
        Message = '---------------------------------------------\nCandidate:\n'
        Message += 'nRow  :   ' + str(Rec_WithCode[iWithCode_nRow]) + '\nDescr :   ' + str(Rec_WithCode[iWithCode_TR_Desc])
        Message += '\nDate  :   ' + str(Rec_WithCode[iWithCode_Valuta])
        Value   = Rec_WithCode[iWithCode_Addeb]
        if not Value:
            Value = Rec_WithCode[iWithCode_Accr]
        Purged  = self.Purge_FulDesc(True, Rec_WithCode[iWithCode_FullDesc])
        Message += '\nAmount:   ' + str(Value) + '\n\nFull Description:\n' + str(Purged)
        Message += '\n\n---------------------------------------------'
        Message += '\nTransaction Code Found:'
        TrCode  = RecToIns[iTransact_TRcode]
        Index   = TrCode
        TRfull  = self.Data. Get_TR_Codes_Full(Index)
        TrDesc  = TRfull[iTR_Ful_TRdesc]
        Group   = TRfull[iTR_Ful_GRdesc]
        Categ   = TRfull[iTR_Ful_CAdesc]
        StrToSrc= TRfull[iTR_Ful_TRfind]
        Full_Des= TRfull[iTR_Ful_TRful]
        Purged = self.Purge_FulDesc(False, Full_Des)
        Message += '\nCode  :   ' + str(TrCode)   + '\nDescr :   ' + str(TrDesc)
        Message += '\nToFind:   ' + str(StrToSrc)
        Message += '\nGroup :   ' + str(Group)    + '\nCateg :   ' + str(Categ)
        Message += '\n\nFullDescription:\n' + str(Purged)
        Message += '\n---------------------------------------------\n\nContinue'

        Msg_Dlg = Message_Dlg(MsgBox_Ask, Message)
        Msg_Dlg.wait_window()
        Reply = Msg_Dlg.data
        if Reply == YES:
            return True
        return False

    # -------------------------------------------------------------------------------------------------
    def Clk_Continue(self, Value):
        self.Continue = Value
        if Value == CONTINUOUS or Value == STEP:
            self.UpToText.Set_Text('')
        elif Value == UPTO:
            UptoNrow = self.UpToText.Get_Text(NOT_INT)
            if UptoNrow == '' or (int(UptoNrow) < 10) :
                self.UpToText.Set_Text('30')

    # -------------------------------------------------------------------------------------------------
    def Check_Ask_Dlg(self, WithCodList):
        if self.Continue == STEP:
            return ASK                          # ask
        elif self.Continue == CONTINUOUS:
            return NOTASK                        # NOT ask
        else:
            nRow_ToEnd = int(self.UpToText.Get_Text(INTEGER))
            nRow       = int(WithCodList[iWithCode_nRow])
            if nRow >= nRow_ToEnd+1:
                return STOP                     # Stop
            else:
                return NOTASK                   # NOT Ask

    # -------------------------------------------------------------------------------------------------
    def Clk_Insert(self):
        self.Ins_Btn.Btn_Disable()
        Result = self.Data.OpenClose_Transactions_Database(True, self.Full_Filename_For_Insert)
        if Result != OK:
            return Result
        ListToInsert = self.Records_ToIns_List
        IndexEnd     = len(self.Records_ToIns_List)
        Remain_List  = self.Records_ToIns_List.copy()
        for Index in range(0, IndexEnd):
            RecToIns    = self.Records_ToIns_List[Index]
            WithCodList = self.Rows_WithCod_List[Index]

            Reply = self.Check_Ask_Dlg(WithCodList)     # STOP  or ASK  or NOT_ASK
            Continue = True                             # NOT_ASK and conitinue
            if Reply == STOP:                           # STOP
                Continue = False
            elif Reply == ASK:                          # ASK
                if not self.Ask_For_RecToInsert(WithCodList, RecToIns):
                    Continue = False                    # Reply = NO

            if Continue:
                Result = self.Data.Insert_Transact_Record(RecToIns)
                if Result != OK:
                    Msg_Dlg = Message_Dlg(MsgBox_Err, Result)
                    Msg_Dlg.wait_window()
                    return
                del Remain_List[0]
                self.Load_Tree(Remain_List)
            else:
                break
        self.Data.OpenClose_Transactions_Database(False, self.Full_Filename_For_Insert)

        # Reload Rows etc for Insert --------------------
        if self.Mod_Mngr.Init_Top_Insert(TOP_INS):
            self.Create_RecordsList_ToBeInserted()
            self.Set_Data()
            self.Set_Texts()
            self.Load_Tree(self.Records_ToIns_List)
            self.Ins_Btn.Btn_Enable()
            self.Chat.Tx_Request([TOP_INS, [ANY], XLSX_UPDATED, []])

    # -------------------------------------------------------------------------------------------------
    def Set_Texts(self):
        self.Files_Ident = self.Data.Get_Xlsx_Transact_Ident()
        self.Conto       = self.Files_Ident[Ix_Xlsx_Conto]
        self.intYear     = self.Files_Ident[Ix_Xlsx_Year]
        self.intMonth    = self.Files_Ident[Ix_Xlsx_Month]
        Texto = 'Delete Transactions db ' + str(self.intYear)
        self.ClrDb_Btn.Set_Text(Texto)

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
        # Xlsx Row candidate for insertion on database:
        # nRow  Contab Valuta Contab Valuta Full_Desc
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
        self.WithList                 = self.Data.Get_WithCodeList()
        self.Rows_WithCod_List        = []
        self.Records_ToIns_List       = []
        self.TotTransact_ToBeInserted = 0

        Month_List_Empty              = self.Data.Create_Transact_Month_List_Empty()
        for Rec_InList in self.WithList:
            YearMonVal = Get_YearMonthDay(Rec_InList[iWithCode_Valuta])
            YearVal      = YearMonVal[0]
            MonthVal     = YearMonVal[1] - 1
            YearMonCont = Get_YearMonthDay(Rec_InList[iWithCode_Contab])
            YearCont      = YearMonCont[0]
            MonthCont     = YearMonCont[1] - 1
            if YearVal == self.intYear  or  YearCont == self.intYear:
                RecToInsert = self.Create_RecToInsert_From_RowWithCode(Rec_InList)
                if Month_List_Empty[MonthVal] and Month_List_Empty[MonthCont]:
                    ToInsert = True
                else:
                    if self.Data.Check_IfTransactRecord_InDatabase(RecToInsert):
                        ToInsert = False
                    else:
                        ToInsert = True
                if ToInsert:
                    self.TotTransact_ToBeInserted += 1
                    # self.Rows_WithCod_List.append(Row_List)
                    self.Rows_WithCod_List.append(Rec_InList)
                    self.Records_ToIns_List.append(RecToInsert)
        pass

    # -------------------------------------------------------------------------------------------------
    def Load_Tree(self, ListToInsert):
        strTotInsert =  '  NO  '
        Len = len(ListToInsert)
        if Len != 0:
            strTotInsert = str(Len)
        FrameTitle = '    ' + strTotInsert + '    Movimenti  da inserire    '
        self.Frame_Transact.Load_Row_Values(ListToInsert)
        self.Frame_Transact.Frame_Title(FrameTitle)

      # -------------------------------------------------------------------------------------------------
    def Frame_Transact_Setup(self):
        Nrows     = 37
        nColToVis = 8
        Headings  = ['#0', 'row','Conto ','Contab  ','Valuta  ','Descrizione ','Entrate  ','Uscite ','codice']
        Anchor    = ['c',  'c',  'c',     'c',       'c',       'w',           'e',       'e',      'c']
        Width     = [ 0,    40,   70,      90,        90,        170,           75,        75,       60]
        Form_List_Rows = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_Transact.Tree_Setup(Form_List_Rows)

    # -------------------------------------------------------------------------------------------------
    def Clk_View_Xlsx(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_INS, [])

    # -------------------------------------------------------------------------------------------------
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
    def Clk_Delete_DbInsert(self):
        Message = 'Cofirm to delete Transactions Db\nYear:  ' + str(self.intYear)
        Msg_dlg = Message_Dlg(MsgBox_Ask, Message)
        Msg_dlg.wait_window()
        Reply = Msg_dlg.data
        if Reply == YES:
            FullTransactFileName = self.Data.Get_Selections_Member(Ix_Transact_File)
            if os.path.exists(FullTransactFileName):
                os.remove(FullTransactFileName)
                self.Data.Update_Selections(UNKNOWN, Ix_Transact_File)
                Message = 'Transactions Db\nYear:  ' + str(self.intYear) + '   deleted\nPlease select an xlsx file'
                Msg_dlg = Message_Dlg(MsgBox_Info, Message)
                Msg_dlg.wait_window()
                self.intYear = 0
                Texto = 'Delete Transactions db '
                self.ClrDb_Btn.Set_Text(Texto)
                self.Clk_Sel_Xlsx()

    # -------------------------------------------------------------------------------------------------
    def Clk_Ontree_View(self, Values):
        pass
    # =================================================================================================




