# ============================================================================= #
#                 -----   Mod_Mngr_Init.py   -----                             #
#                                                                               #
#    ------------------------------------------------------------------         #
#  Modul_Mngr = Modules_Manager()                                               #
#  Data       = Transact_DB <-- Xlsx_Manager <-- Codes_DB <-- Filesnames_Mngr   #
#                                                                               #
#   'Init ' methods are invoked at startup or  before launching a module        #
#           the file to be iniziated will be load only if not loaded            #
#                                                                               #
#    'Sel ' methods select a new file and if correct  it calls Load             #
#                                                                               #
#    'Cek_Name'  check if the filename is correct                               #
#                                                                               #
#    'Load ' methods load files data and if OK  it updates Selections           #
# ============================================================================= #
import os

from Widgt.Dialogs import *
from Widgt.Dialogs import File_Dialog
from Data_Classes.Transact_DB import Data_Manager
from Widgt.Dialogs import View_Message


class Mod_Mngr_Init:
    def __init__(self):
        self.Data = Data_Manager
        self.Chat = Ms_Chat
        self.Dummy = None
        self.Check_Result      = False
        self.Toplevels_Id_List = []   # <class>,  NAME
                                      # List of toplevel to launch in Top_Settings
    # =========================================================================================== #
    #           --------------      Codes  managing     --------------                            #
    #    If Codes filename is correct,   self.Data.Load_Codes_Tables tries to load the Codes      #
    #    Tables (TR, GR, CA) from database. In case of error nothing is changed                   #
    # =========================================================================================== #
    def Init_Codes(self, Origin):
        Codes_DB_Filename = self.Data.Get_Selections_Member(Ix_Codes_File)
        if Codes_DB_Filename == UNKNOWN:
            self.Sel_Codes_Mngr(Origin)

        else:   # if not unknown the filename is OK
            if self.Data.Get_Files_Loaded_Stat(Ix_Codes_Loaded):
                pass
                  # self.Check_Codes_View(CHECK_DBCODES_LOADED, VIEW_ONLY_ERROR)
            else:
                self.Load_Codes_Mngr(Origin, ON_SELECTIONS)

    # ---------------------------------------------------------------------------------------------
    @classmethod
    def Cek_Codes_Name(cls, Full_Filename):         # used only on Sel_Codes_Mngr
        errMessage = ''
        if Full_Filename == UNKNOWN:
            errMessage = 'Codes filename unknown\nPlease select a Codes file'
        else:
            Dirname = Get_Dir_Name(Full_Filename)
            filename = Get_File_Name(Full_Filename)
            if len(filename) < Len_Codes_Filename_Min:
                errMessage = 'Len of Codes filename INCORRECT'
            else:
                iLastBar = int(Full_Filename.rfind("/") + 1)
                strCodes = Full_Filename[(iLastBar - 9):(iLastBar + 11)]
                if strCodes != Ident_DB_Filename:
                    errMessage = 'DBcodes filename ERROR:\n\n'
                    errMessage += filename + '\n' + Dirname + '\n\nexpected:  ' + Ident_DB_Filename
        if errMessage != '':
            Mess = Message_Dlg(MsgBox_Err, errMessage)
            Mess.wait_window()
            return False
        else:
            return True

    # ---------------------------------------------------------------------------------------------
    def Sel_Codes_Mngr(self, Origin):
        File_Dlg = File_Dialog(FileBox_Codes)
        Full_Filename = File_Dlg.FileName  # Cancel
        if not Full_Filename:
            return False
        if self.Cek_Codes_Name(Full_Filename):
            self.Load_Codes_Mngr(Origin, Full_Filename)
            self.Data.Update_Selections(Full_Filename, Ix_Codes_File)
            self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
            return True
        else:
            return False

    # ---------------------------------------------------------------------------------------------
    def Load_Codes_Mngr(self, Origin, Filename):
        File_Name   = Filename
        if Filename == ON_SELECTIONS:
            File_Name = self.Data.Get_Selections_Member(Ix_Codes_File)
        if File_Name == UNKNOWN:
            return False
        Reply = self.Data.Load_Codes_Tables(File_Name)
        self.Check_Codes_View(File_Name, VIEW_ONLY_ERROR)
        if Reply == OK:  # reply:  OK or Diagnostic
            self.Chat.Tx_Request([Origin, [ANY], CODES_DB_UPDATED, []])
            return True
        else:
            Msg_Dlg = Message_Dlg(MsgBox_Err, Reply)
            Msg_Dlg.wait_window()
            View_Message(Reply)
            return False

    # --------------------------------------------------------------------------------------------
    def View_Codes_Check_Error(self, Multiple):
        self.Dummy = 0
        Info = 'ERROR on checking out codes database\n\n'
        Info += '--------------------------------------------\n'
        nLine = -1
        for TRrecord in Multiple:
            nLine += 1
            strCode = 'Code: ' + str(TRrecord[iTR_TRcode])
            strDesc = TRrecord[iTR_TRdesc]
            StrToFind = TRrecord[iTR_TRstrToFind]
            FullDescr = TRrecord[iTR_TRfullDes]
            Info += strCode + '\n' + strDesc + '\n'
            Info += StrToFind + '\n' + FullDescr
            if (nLine % 2) == 0:
                Info += '\n-----------------\n'
            else:
                Info += '\n--------------------------------------------\n'
        View_Message([Info])
        pass

    # --------------------------------------------------------------------------------------------
    def Check_Codes_View(self, DbTo_Check, ViewMsg):
        Multiple = self.Data.Check_Codesdatabase(DbTo_Check)
        if not Multiple:
            if ViewMsg == VIEW_OKand_ERROR:
                Len     = self.Data.Get_TR_Codes_Table_Len()
                Info    = str(Len) + '   codes records correctly checked out'
                Message = Message_Dlg(MsgBox_Info, Info)
                Message.wait_window()
        else:
            self.View_Codes_Check_Error(Multiple)

    # =========================================================================================== #
    #     --------------      Transactions  manage     --------------                             #
    #    If Transactions filename is correct,   TryToLoad_Transactions tries to load              #
    #    the Transactions Tables. In case of error nothing is changed                             #
    # =========================================================================================== #
    def Init_Transactions(self, Origin):
        Transact_Filename = self.Data.Get_Selections_Member(Ix_Transact_File)
        Xlsx_Filename     = self.Data.Get_Selections_Member(Ix_Xlsx_File)

        if Transact_Filename == UNKNOWN and Xlsx_Filename == UNKNOWN:
            Msg_Dlg = Message_Dlg(MsgBox_Info, 'Xlsx and Transations filename unknown\nSelect a Transactions file')
            Msg_Dlg.wait_window()
            return self.Sel_Transact_Mngr(Origin)

        if Transact_Filename != UNKNOWN:
            return self.TryToLoad_Transactions(Origin, Transact_Filename)

        if Xlsx_Filename != UNKNOWN:
            if self.Get_Transact_FromXlsxFilename(Xlsx_Filename):
                if self.Load_Transact_Mngr(Origin, Transact_Filename):
                    return True
            Msg_Dlg = Message_Dlg(MsgBox_Err, 'Impossible to get a transactions Db')
            Msg_Dlg.wait_window()
            return False

    # ------------------------------------------------------------------------------------
    def TryToLoad_Transactions(self, Origin, Transact_Filename):
        if self.Cek_Transactions_Name(Transact_Filename):
            return self.Load_Transact_Mngr(Origin, Transact_Filename)

    # ------------------------------------------------------------------------------------
    def Get_Transact_FromXlsxFilename(self, Xlsx_Filename):
        if not self.Cek_Xlsx_Name(Xlsx_Filename):
            return False
        Transact_Filename = Create_Transactions_Name_FromXlsx(Xlsx_Filename)
        File_Exists       = os.path.isfile(Transact_Filename)
        if not File_Exists:
            Messg = 'inspiegabilmente il file  ' + Transact_Filename + 'non esiste'
            Msg_Dlg = Message_Dlg(MsgBox_Err, Messg)
            Msg_Dlg.wait_window()
            return False
        self.Data.Update_Selections(Transact_Filename, Ix_Transact_File)
        return True

    # -----------------------------------------------------------------------------------------
    # 210987654321 0 12345678901234
    # TRANSACTIONS / Transact_2024.db
    def Cek_Transactions_Name(self, Full_Filename):
        errMessage = ''
        File_Name = Full_Filename
        if File_Name == UNKNOWN:
            errMessage = 'Transactions filename unknown\nPlease select a Transactions file'
        else:
            filename = Get_File_Name(Full_Filename)
            if len(filename) < Len_Transact_Filename:
                errMessage = 'Len of Transactions filename INCORRECT'
            else:
                #  TRANSACTIONS/Transact_   2024.db
                iLastBar = int(File_Name.rfind("/") + 1)
                Transact_Str_Id = File_Name[(iLastBar - 13):(iLastBar + 9)]
                strYear = filename[9:13]
                if Transact_Str_Id != TRANSACT_ID:
                    errMessage = 'Transactions filename ERROR:\n\n'
                    errMessage += filename + '\n' + Transact_Str_Id
                else:
                    if not (Check_strYear(strYear, self.Data.Min_Year, self.Data.Max_Year)):
                        errMessage = 'Transactions Year  not OK:  ' + strYear
        if errMessage != '':
            Msg = Message_Dlg(MsgBox_Err, errMessage)
            Msg.wait_window()
            self.Data.Clear_Transact_Year()  # clear Transact_Year
            return False
        else:
            return True

    # ----------------------------------------------------------------------------------------------
    def Sel_Transact_Mngr(self, Origin):
        File_Dlg      = File_Dialog(FileBox_Transact)
        Full_Filename = File_Dlg.FileName
        if not Full_Filename:
            return False
        if self.Cek_Transactions_Name(Full_Filename):
            if self.Load_Transact_Mngr(Origin, Full_Filename):
                self.Data.Update_Selections(Full_Filename, Ix_Transact_File)
                self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
        return False

    # -------------------------------------------------------------------------
    def Load_Transact_Mngr(self, Origin, Filename):
        File_Name   = Filename
        if Filename == ON_SELECTIONS:
            File_Name = self.Data.Get_Selections_Member(Ix_Transact_File)
        if File_Name == UNKNOWN:
            return False
        Reply = self.Data.Load_Transact_Table(Filename)
        if Reply == OK:
            self.Chat.Tx_Request([Origin, [ANY], TRANSACT_UPDATED, []])
            return True
        else:
            Msg = Message_Dlg(MsgBox_Err, Reply)  # display 'ERROR... '
            Msg.wait_window()
            return False


    # =========================================================================================== #
    #           --------------      Xlsx file  managing     --------------                        #
    # =========================================================================================== #
    def Init_Xlsx_Lists(self, Origin):
        Xlsx_Filename = self.Data.Get_Selections_Member(Ix_Xlsx_File)
        if Xlsx_Filename == UNKNOWN:
            return self.Sel_Xlsx_Mngr(Origin)

        else:  # if not unknown the filename is OK
            if self.Data.Get_Files_Loaded_Stat(Ix_Xlsx_Lists_Loaded):
                return True
            else:
                if self.Load_Xlsx_Lists_Mngr(Origin, ON_SELECTIONS):
                    self.Warning_For_NO_Rows()
                else:
                    return False

    # -------------------------------------------------------------------------
    def Warning_For_NO_Rows(self):
        Total = self.Data.Get_Total_Rows()
        if Total[Ix_Tot_OK] == 0:
            Msg_Dlg = Message_Dlg(MsgBox_Info, 'Any row found')
            Msg_Dlg.wait_window()

    # -------------------------------------------------------------------------
    # /home/mario/bExpenses/bFiles/bXLSX_Files/FIDEU/FIDEU_2023/ FIDEU_2023_01.xlsx
    #                                         765432109876543210 123456789012345678
    def Cek_Xlsx_Name(self, Full_Xlsx_Filename):
        errMessage = ''
        if Full_Xlsx_Filename == UNKNOWN:
            errMessage = 'Xlsx filename unknown\nPlease select an Xlsx file'
        else:
            filename = Get_File_Name(Full_Xlsx_Filename)
            if len(filename) < Len_Xlsx_Filename_Min:
                pass
                errMessage = 'Length of xlsx filename INCORRECT'
            else:
                iLastBar  = int(Full_Xlsx_Filename.rfind("/") + 1)
                ContoDir  = Full_Xlsx_Filename[(iLastBar - 17):(iLastBar - 12)]
                ContoYear = Full_Xlsx_Filename[(iLastBar - 11):iLastBar]
                ContoYearOnfilename = filename[0:11]
                strYear    = filename[6:10]
                strMonth   = filename[11:13]
                pass
                if ContoDir != FIDEU and ContoDir != FLASH and ContoDir != POSTA and ContoDir != AMBRA:
                    errMessage = 'Xlsx Conto not correct'
                elif ContoDir not in ContoYear or ContoDir not in ContoYearOnfilename:
                    errMessage =  'On xlsx filename\n'
                    errMessage += 'Mismatching with\n' + ContoDir + '\n' + ContoYear + '\n' + ContoYearOnfilename
                elif not (Check_strYear(strYear, self.Data.Min_Year, self.Data.Max_Year)):
                    errMessage = 'Year  not OK:  ' + strYear
                elif not (Check_strMonth(strMonth)):
                    errMessage = 'Xlsx Month  not OK:  '  + strMonth
        if errMessage != '':
            Msg = Message_Dlg(MsgBox_Err, errMessage)
            Msg.wait_window()
            self.Data.Clear_Xlsx_Conto_Year_Month()
            return False
        return True

    # ---------------------------------------------------------------------------------------------
    def Sel_Xlsx_Mngr(self, Origin):
        File_Dlg      = File_Dialog(FileBox_Xlsx)
        Full_Filename = File_Dlg.FileName
        if not Full_Filename:
            return False
        if self.Cek_Xlsx_Name(Full_Filename):
            self.Load_Xlsx_Lists_Mngr(Origin, Full_Filename)
            self.Data.Update_Selections(Full_Filename, Ix_Xlsx_File)
            self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
            return True

    # -------------------------------------------------------------------------------------------------------
    def Load_Xlsx_Lists_Mngr(self, Origin, Filename):
        File_Name   = Filename
        if Filename == ON_SELECTIONS:
            File_Name = self.Data.Get_Selections_Member(Ix_Codes_File)
        if File_Name == UNKNOWN:
            return False

        Reply = self.Data.Load_Xlsx_Lists(Filename)
        if Reply == OK:                     #  reply:  OK or Diagnostic
            self.Test_For_MultiChecking()
            self.Chat.Tx_Request([Origin, [ANY], XLSX_UPDATED, []])
            return True
        else:
            View_Message([Reply])
            return False

    # --------------------------------------------------------------------------------------------
    def Test_For_MultiChecking(self):
        Row_MultiCheck_List = self.Data.Xlsx_Rows_MultiMatch_List
        if not Row_MultiCheck_List:
            return True
        Row    = Row_MultiCheck_List[0]
        Nrow   = str(Row[iRow_nRow])
        Date   = str(Row[iRow_Valuta])
        Desc1  = str(Row[iRow_Descr1])
        Desc2  = str(Row[iRow_Descr2])
        Amount = Row[iRow_Addeb]
        if type(Amount) is not float:
            Amount = Row[iRow_Accr]

        Message = ('In Xlsx file for:\n\nRow: ' + Nrow + '\nDate: ' + Date + '\nAmount: ' + str(Amount))
        Message += '\nDesc1: ' + Desc1 + '\nDesc2: ' + Desc2 + '\n\nFound:\n'

        FoundList  = Row_MultiCheck_List[1]
        ListFor_Select = [NONE]
        for TrRec in FoundList:
            strCode   = str(TrRec[iTR_TRcode])
            strDesc   = str(TrRec[iTR_TRdesc])
            ToSelect  = strCode + '/   ' + strDesc
            ListFor_Select.append(ToSelect)
            strToFind = str(TrRec[iTR_TRstrToFind])
            FullDesc  = str(TrRec[iTR_TRfullDes])
            Texto     = '\nCode: ' + strCode + '   Desc: ' + strDesc + '\nString to find:\n' + strToFind
            Texto    += '\nFull Descr:\n' + FullDesc + '\n'
            Message  += Texto
            pass

        Mesg_Sel = View_Message_Select(Message, ListFor_Select)
        Mesg_Sel.wait_window()
        Select = Mesg_Sel.data
        if Select == NONE:
            Code = 0
        else:
            iSlashIndex = Select.rfind('/')
            strCode = Select[:iSlashIndex]
            Code    = int(strCode)
        print(Code)
        if Code == 0:
            return False
        else:
            self.Data.Add_Row_WithCode(Row, Code)
        pass

    # --------------------------------------------------------------------------------------------
    #  invoked  on Main_window
    # ---------------------------------------------------------------------------------------------
    def Add_Toplevels_Id_List(self, Id):
        if Id not in self.Toplevels_Id_List:
            self.Toplevels_Id_List.append(Id)
        pass

    # --------------------------------------------------------------------------------------------
    #  invoked  only internally Main_window
    # ---------------------------------------------------------------------------------------------
    def _Get_TopLev(self, NAME):
        for Id in self.Toplevels_Id_List:
            if Id[Ix_TopName] == NAME:
                return Id[Ix_TopClass]
        return None
# ===========================================================================================================
