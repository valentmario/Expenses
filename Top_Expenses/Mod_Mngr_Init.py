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

from Widgt.Dialogs import *
from Widgt.Dialogs import File_Dialog
from Data_Classes.Transact_DB import Data_Manager
from Widgt.Dialogs import Top_View_Message


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
    # =========================================================================================== #
    def Init_Codes(self, Origin):
        Codes_DB_Filename = self.Data.Get_Selections_Member(Ix_Codes_File)
        if not self.Cek_Codes_Name(Codes_DB_Filename):
            if self.Sel_Codes(Origin):  # Load Tables and return True False
                return True
            else:
                return False
        else:
            if self.Data.Get_Files_Loaded_Stat(Ix_Codes_Loaded):
                return True
            else:
                if self.Load_Codes(Origin, ON_SELECTIONS):
                    return True
                else:
                    return False

    # ---------------------------------------------------------------------------------------------
    @classmethod
    def Cek_Codes_Name(cls, Full_Filename):
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
    def Sel_Codes(self, Origin):
        File_Dlg = File_Dialog(FileBox_Codes)
        Full_Filename = File_Dlg.FileName
        if not Full_Filename:
            return False
        if self.Cek_Codes_Name(Full_Filename):
            if self.Load_Codes(Origin, Full_Filename):
                self.Data.Update_Selections(Full_Filename, Ix_Codes_File)
                self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
            else:
                return False
        else:
            return False

    # ---------------------------------------------------------------------------------------------
    def Load_Codes(self, Origin, Filename):
        Reply = self.Data.Load_Codes_Tables(Filename)
        if Reply == OK:  # reply:  OK or Diagnostic
            self.Chat.Tx_Request([Origin, [ANY], CODES_DB_UPDATED, []])
            return True
        else:
            Msg = Message_Dlg(MsgBox_Err, Reply)
            Msg.wait_window()
            return False

    # ---------------------------------------------------------------------------------------------
    def Check_Codes_Db(self):
        Multiple = self.Data.Check_Codesdatabase()
        pass
        if not Multiple:
            Len = self.Data.Get_TR_Codes_Table_Len()
            Info = str(Len) + '   code records correctly checked out'
            Message = Message_Dlg(MsgBox_Info, Info)
            Message.wait_window()
        else:
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
            Top_View_Message([Info])

    # =========================================================================================== #
    #     --------------      Transactions  manage     --------------                             #
    #      A correct filename selected,  self.Data.Load_Codes_Tables will load the Tables         #
    #      from database. In case of error nothing is changed                                     #
    # =========================================================================================== #
    def Init_Transactions(self, Origin):
        Transact_Filename = self.Data.Get_Selections_Member(Ix_Transact_File)
        if Transact_Filename == UNKNOWN:
            Msg = Message_Dlg(MsgBox_Err, 'filename of transactions db unknown')
            Msg.wait_window()
            return False
        if not self.Cek_Transactions_Name(Transact_Filename):
            return False

        if self.Data.Get_Files_Loaded_Stat(Ix_Transact_Loaded):
            return True
        else:
            if self.Load_Transact(Origin, ON_SELECTIONS):
                return True
            else:
                return False

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
    def Sel_Transact(self, Origin):
        File_Dlg = File_Dialog(FileBox_Transact)
        Full_Filename = File_Dlg.FileName
        if not Full_Filename:
            return False
        if self.Cek_Transactions_Name(Full_Filename):
            if self.Load_Transact(Origin, Full_Filename):
                self.Data.Update_Selections(Full_Filename, Ix_Transact_File)
                self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
            else:
                return False
        else:
            return False

    # -------------------------------------------------------------------------
    def Load_Transact(self, Origin, Filename):
        Reply = self.Data.Load_Transact_Table(Filename)
        if Reply == OK or Reply == EMPTY:
            if Reply == EMPTY:
                Msg = Message_Dlg(MsgBox_Err, 'Transactions Database is EMPTY')
                Msg.wait_window()
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
        if not self.Cek_Xlsx_Name(Xlsx_Filename):
            if self.Sel_Xlsx(Origin):    # Load Lists and return True False
                return True
            else:
                return False
        else:
            if self.Data.Get_Files_Loaded_Stat(Ix_Xlsx_Lists_Loaded):
                return True
            else:
                if self.Load_Xlsx_Lists(Origin, ON_SELECTIONS):
                    return True
                else:
                    return False

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
    def Sel_Xlsx(self, Origin):
        File_Dlg      = File_Dialog(FileBox_Xlsx)
        Full_Filename = File_Dlg.FileName
        if not Full_Filename:
            return False
        if self.Cek_Xlsx_Name(Full_Filename):
            if self.Load_Xlsx_Lists(Origin, Full_Filename):
               self.Data.Update_Selections(Full_Filename, Ix_Xlsx_File)
               self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
               return True
            else:
                return False
        else:
            return False

    # -------------------------------------------------------------------------------------------------------
    def Load_Xlsx_Lists(self, Origin, Filename):
        Reply = self.Data.Load_Xlsx_Lists_FromData(Filename)
        if Reply == OK:                     #  reply:  OK or Diagnostic
            self.Chat.Tx_Request([Origin, [ANY], XLSX_UPDATED, []])
            return True
        else:
            Top_View_Message([Reply])
            return False


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
