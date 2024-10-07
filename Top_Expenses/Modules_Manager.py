# ============================================================================= #
#                 -----   Modules_Mnager.py   -----                             #
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
import sqlite3
from Widgt.Dialogs import *
from Widgt.Dialogs import File_Dialog
from Data_Classes.Transact_DB import Data_Manager


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
            errMessage = 'Transactions ilename unknown\nPlease select a Transactions file'
        else:
            filename = Get_File_Name(File_Name)
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


# -------------------------------------------------------------------------------
class Modules_Manager(Mod_Mngr_Init):
    def __init__(self):
        super().__init__()
        self.Data = Data_Manager
        self.Chat = Ms_Chat
        self.Dummy = None
        self.Check_Result      = False
        self.Toplevels_Id_List = []   # <class>,  NAME
                                      # List of toplevel to launch in Top_Settings

    # =======================   Selections  settings    =========================
    def Cek_Create_Selections(self):
        Result = self.Data.Check_Create_Selections()
        if Result == NEW:
            self.Data.Clear_Xlsx_Conto_Year_Month()
            self.Data.Clear_Transact_Year()
            Text = "New Selections file created\nmount the data drive if necessary"
            Msg  = Message_Dlg(MsgBox_Info, Text)
            Msg.wait_window()
        else:
            pass


    # =========================================================================================== #
    # Below are coded with the same structure:                                                    #
    # four methodes for              Init..  Check_Name..  Sel..  Load.. methodes                 #
    # for three files manager for    Codes   Xlsx   Transactions                                  #
    # Init..        are invoked by the Module Launcher on launching a Top_Levels class            #
    #               - if the filename on Selections is NOK:                                       #
    #               it calls Sel.. method that calls the Load.. method                            #
    #               if the Load.. method is successfull return True otherwise return False        #
    #               - else: if the file is already loaded  return True                            #
    #                 otherwise it calls  Load.. method and return the result                     #
    #               the Selections are updated after a successfull Load..                         #
    #                                                                                             #
    # Check_Name.. it checks the filename and return True or False                                #
    # Sel..        it calls Dlg_Dialog for selecting a filename.                                  #
    #              on succes it call Load.. method and in case of success Seletions are updated   #
    # Load..       it tries to load file data and return True False                               #
    # Important    In case of an unsuccessfull Load, the status of all previous data remain int   #
    # =========================================================================================== #


    # =========================================================================================== #
    #           --------------      Codes  managing     --------------                            #
    # =========================================================================================== #
    # def Init_Codes(self, Origin):
    #     Codes_DB_Filename = self.Data.Get_Selections_Member(Ix_Codes_File)
    #     if not self.Cek_Codes_Name(Codes_DB_Filename):
    #         if self.Sel_Codes(Origin):    # Load Tables and return True False
    #             return True
    #         else:
    #             return False
    #     else:
    #         if self.Data.Get_Files_Loaded_Stat(Ix_Codes_Loaded):
    #             return True
    #         else:
    #             if self.Load_Codes(Origin, ON_SELECTIONS):
    #                 return True
    #             else:
    #                 return False
    #
    # # ---------------------------------------------------------------------------------------------
    # @classmethod
    # def Cek_Codes_Name(cls, Full_Filename):
    #     errMessage = ''
    #     if Full_Filename == UNKNOWN:
    #         errMessage = 'Codes filename unknown\nPlease select a Codes file'
    #     else:
    #         Dirname  = Get_Dir_Name(Full_Filename)
    #         filename = Get_File_Name(Full_Filename)
    #         if len(filename) < Len_Codes_Filename_Min:
    #             errMessage = 'Len of Codes filename INCORRECT'
    #         else:
    #             iLastBar = int(Full_Filename.rfind("/") + 1)
    #             strCodes = Full_Filename[(iLastBar - 9):(iLastBar + 11)]
    #             if strCodes != Ident_DB_Filename:
    #                 errMessage = 'DBcodes filename ERROR:\n\n'
    #                 errMessage += filename + '\n' + Dirname  + '\n\nexpected:  ' + Ident_DB_Filename
    #     if errMessage != '':
    #         Mess = Message_Dlg(MsgBox_Err, errMessage)
    #         Mess.wait_window()
    #         return False
    #     else:
    #         return True
    #
    # # ---------------------------------------------------------------------------------------------
    # def Sel_Codes(self, Origin):
    #     File_Dlg      = File_Dialog(FileBox_Codes)
    #     Full_Filename = File_Dlg.FileName
    #     if not Full_Filename:
    #         return False
    #     if self.Cek_Codes_Name(Full_Filename):
    #         if self.Load_Codes(Origin, Full_Filename):
    #             self.Data.Update_Selections(Full_Filename, Ix_Codes_File)
    #             self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False
    #
    # # ---------------------------------------------------------------------------------------------
    # def Load_Codes(self, Origin, Filename):
    #     Reply = self.Data.Load_Codes_Tables(Filename)
    #     if Reply == OK:                     #  reply:  OK or Diagnostic
    #         self.Chat.Tx_Request([Origin, [ANY], CODES_DB_UPDATED, []])
    #         return True
    #     else:
    #         Msg = Message_Dlg(MsgBox_Err, Reply)
    #         Msg.wait_window()
    #         return False
    #
    # # ---------------------------------------------------------------------------------------------
    # def Check_Codes_Db(self):
    #     Multiple = self.Data.Check_Codesdatabase()
    #     pass
    #     if not Multiple:
    #         Len = self.Data.Get_TR_Codes_Table_Len()
    #         Info = str(Len) + '   code records correctly checked out'
    #         Message = Message_Dlg(MsgBox_Info, Info)
    #         Message.wait_window()
    #     else:
    #         Info = 'ERROR on checking out codes database\n\n'
    #         Info += '--------------------------------------------\n'
    #         nLine = -1
    #         for TRrecord in Multiple:
    #             nLine += 1
    #             strCode    = 'Code: ' + str(TRrecord[iTR_TRcode])
    #             strDesc    = TRrecord[iTR_TRdesc]
    #             StrToFind = TRrecord[iTR_TRstrToFind]
    #             FullDescr = TRrecord[iTR_TRfullDes]
    #             Info += strCode + '\n' + strDesc + '\n'
    #             Info += StrToFind + '\n' + FullDescr
    #             if (nLine % 2) == 0:
    #                 Info += '\n-----------------\n'
    #             else:
    #                 Info += '\n--------------------------------------------\n'
    #         Top_View_Message([Info])
    #
    # # =========================================================================================== #
    # #     --------------      Transactions  manage     --------------                             #
    # #      A correct filename selected,  self.Data.Load_Codes_Tables will load the Tables         #
    # #      from database. In case of error nothing is changed                                     #
    # # =========================================================================================== #
    # def Init_Transactions(self, Origin):
    #     Transact_Filename = self.Data.Get_Selections_Member(Ix_Transact_File)
    #     if Transact_Filename == UNKNOWN:
    #         Msg = Message_Dlg(MsgBox_Err, 'filename of transactions db unknown')
    #         Msg.wait_window()
    #         return False
    #     if not self.Cek_Transactions_Name(Transact_Filename):
    #         return False
    #
    #     if self.Data.Get_Files_Loaded_Stat(Ix_Transact_Loaded):
    #         return True
    #     else:
    #         if self.Load_Transact(Origin, ON_SELECTIONS):
    #             return True
    #         else:
    #             return False
    #
    # # -----------------------------------------------------------------------------------------
    # # 210987654321 0 12345678901234
    # # TRANSACTIONS / Transact_2024.db
    # def Cek_Transactions_Name(self, Full_Filename):
    #     errMessage = ''
    #     File_Name  = Full_Filename
    #     if File_Name == UNKNOWN:
    #         errMessage = 'Transactions ilename unknown\nPlease select a Transactions file'
    #     else:
    #         filename = Get_File_Name(File_Name)
    #         if len(filename) < Len_Transact_Filename:
    #             errMessage = 'Len of Transactions filename INCORRECT'
    #         else:
    #             #  TRANSACTIONS/Transact_   2024.db
    #             iLastBar = int(File_Name.rfind("/") + 1)
    #             Transact_Str_Id = File_Name[(iLastBar - 13):(iLastBar + 9)]
    #             strYear = filename[9:13]
    #             if Transact_Str_Id != TRANSACT_ID:
    #                 errMessage = 'Transactions filename ERROR:\n\n'
    #                 errMessage += filename + '\n' + Transact_Str_Id
    #             else:
    #                 if not (Check_strYear(strYear, self.Data.Min_Year, self.Data.Max_Year)):
    #                     errMessage = 'Transactions Year  not OK:  ' + strYear
    #     if errMessage != '':
    #         Msg = Message_Dlg(MsgBox_Err, errMessage)
    #         Msg.wait_window()
    #         self.Data.Clear_Transact_Year()   # clear Transact_Year
    #         return False
    #     else:
    #         return True
    #
    # # ----------------------------------------------------------------------------------------------
    # def Sel_Transact(self, Origin):
    #     File_Dlg = File_Dialog(FileBox_Transact)
    #     Full_Filename = File_Dlg.FileName
    #     if not Full_Filename:
    #         return False
    #     if self.Cek_Transactions_Name(Full_Filename):
    #         if self.Load_Transact(Origin, Full_Filename):
    #             self.Data.Update_Selections(Full_Filename, Ix_Transact_File)
    #             self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
    #             return True
    #         else:
    #             return False
    #     else:
    #         return False
    #
    # # -------------------------------------------------------------------------
    # def Load_Transact(self, Origin, Filename):
    #     Reply = self.Data.Load_Transact_Table(Filename)
    #     if Reply == OK or Reply == EMPTY:
    #         if Reply == EMPTY:
    #             Msg = Message_Dlg(MsgBox_Err, 'Transactions Database is EMPTY')
    #             Msg.wait_window()
    #             self.Chat.Tx_Request([Origin, [ANY], TRANSACT_UPDATED, []])
    #         return True
    #     else:
    #         Msg = Message_Dlg(MsgBox_Err, Reply)   # display 'ERROR... '
    #         Msg.wait_window()
    #         return False

    # =============================================================================================== #
    # Create_Xlsx_Lists:  _XLSX_Rows_From_Sheet   (for View Xlsx rows)  calculate Tot_OK  TOT_NOK     #
    #                     _XLSX_Rows_Desc_Compact (for  Lists  with/out code)                         #
    #                           *** the worse case is when any row with data OK are found             #
    #                                                                                                 #
    #                     _With_Code_Tree_List  _Wihtout_Code_Tree_List                               #
    #                     *** if some Without code rows exist: Insert transaction on Db if forbidden  #
    #                                                                                                 #
    # =============================================================================================== #
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
            Msg = Message_Dlg(MsgBox_Err, Reply)
            Msg.wait_window()
            return False

    # =========================================================================================== #
    #            ***    Toplevel    Module   launcher     ***                                     #
    # =========================================================================================== #
    # Name           = Moudule Name to launch
    # Origin         = The requesting Module
    # List_For_Start =  List of Parameters to pass to Recipient
    #                   until 2024 10 03  is used only on TopCodes_View
    # ---------------------------------------------------------------------------------------------
    def Top_Launcher(self, Name_ToLaunch, Origin, List):
        if self.Chat.Check_Name_Is_On_Participants_List(Name_ToLaunch):
            self.Chat.Tx_Request([Origin, [Name_ToLaunch], CODE_TO_CLOSE, []])
            return
        else:
            TopLevel  = self.Get_TopLev(Name_ToLaunch)
            self.Check_Result = self.Make_Checkout(Name_ToLaunch, Origin)
            if self.Check_Result == 3:  # Transactions NOK
                if not self.Sel_Transact(TOP_MNGR):
                    return
            try:
                TopLevel(List)
            except sqlite3.Error as e:
                print(Name_ToLaunch)
                print(Origin)
                print(e)
                return False
            finally:
                pass
                return True

    # ---------------------------------------------------------------------------------------------
    def Make_Checkout(self, Name, Origin):
        self.Check_Result = False
        CheckList = []
        for Item in LAUNCH_CHECKOUT:
            CheckName    = Item[0]
            if CheckName == Name:
                ListForCheck = Item[1]
                for Check in ListForCheck:
                    CheckList.append(Check)
                break
        if not CheckList:
            return -1
                
        for Check in CheckList:
            if Check == CEK_CODES:                          # CEK_CODES
                if not self.Init_Codes(Origin):
                    return 1

            if Check == CEK_XLSX_LIST:                      # CEK_XLSX LISTS
                if not self.Init_Xlsx_Lists(Origin):
                    if not self.Xlsx_Sel_Request(Origin):
                        return 2

            if Check == CEK_TOP_INSERT:                     # CEK_TRANSACT for Top_Insert
                # if not Top_Insert_Init():
                    return 3

            if Check == CEK_TOP_QUERIES:                    # CEK_TRANSACT for Top_Queries
                # if not Top_Insert_Init():
                    return 4
        return -1

    # ---------------------------------------------------------------------------------------------
    def Xlsx_Sel_Request(self, Origin):
        Msg_Dlg = Message_Dlg(MsgBox_Err, 'an Xlsx file must be selected')
        Msg_Dlg.wait_window()
        if self.Sel_Xlsx(Origin):
            return True
        else:
            return False

    # ---------------------------------------------------------------------------------------------
    def Add_Toplevels_Id_List(self, Id):
        if Id not in self.Toplevels_Id_List:
            self.Toplevels_Id_List.append(Id)
        pass

    # ---------------------------------------------------------------------------------------------
    def Get_TopLev(self, NAME):
        for Id in self.Toplevels_Id_List:
            if Id[Ix_TopName] == NAME:
                return Id[Ix_TopClass]
        return None
# -------------------------------------------------------------------------------------------------


# -------------------------------- #
Modul_Mngr = Modules_Manager()     #
# -------------------------------- #
