# ============================================================================= #
#                 -----   Modules_Mnager.py   -----                             #
#                                                                               #
#    ----------------------------------                                         #
#     Modul_Mngr = Modules_Manager()                                            #
#     Data       = Transact_DB <-- Xlsx_Manager <--                             #
#                  <-- Files_Names_Manager                                      #
#     are instanced on Startup and will NEVER destroyed                         #
#                                                                               #
#   filenames Cek:                                                              #
#   at startup     the  names saved on Txt_File                                 #
#   on selection   the names that are selected on File dialog                   #
#                                                                               #
#   'Init ' methods are invoked at startup or  before launching a module        #
#           the file to be iniziated will be load only if not loaded            #
#                                                                               #
#    'Sel ' methods select a new file and if correct                            #
#           the name is saved on Txt_File                                       #
#                                                                               #
#    'Load ' methods load files if not loaded                                   #
#                                                                               #
#   'Sel files ' methods are invoked at start or from a Click().                #
#                if the file selection is not OK, nothing change,               #
#                else the file is loade and marked LOADED  only on OK           #
#                marking LOADED/NO is made on Load methods in the data class    #
# ============================================================================= #

from Common.Common_Functions import *
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data
# from Top_Expenses.Top_View_Message import Top_View_Message
from Widgt.Dialogs import Message_Dlg
from Widgt.Dialogs import File_Dialog

# -------------------------------------------------------------------------------------------------
class Modules_Manager:
    def __init__(self):
        self.Data = Data
        self.Chat = Ms_Chat
        self.Dummy = None
        self.Toplevels_Id_List = []     # <class>,  NAME  # List of toplevel to launch in Top_Settings

    # =======================   Files_Names.txt  settings    ======================================
    def Cek_Create_Txt_File(self):
        Result = self.Data.Check_Create_Txt_File()
        if Result == NEW:
            self.Data.Xlsx_Conto_Year_Month_Setup(False)
            self.Data.Transact_Year_Setup(False)
            Text = "New Txt_File.txt created\nmount the data drive"
            Msg  = Message_Dlg(MsgBox_Info, Text)
            Msg.wait_window()
        else:
            self.Data.Xlsx_Conto_Year_Month_Setup(True)
            self.Data.Transact_Year_Setup(True)

    # =========================================================================================== #
    #           --------------   Init_    Methodss    --------------                              #
    # =========================================================================================== #
    def Init_Codes(self, Origin):
        Full_Codes_DB_Filename = self.Data.Get_Txt_Member(Ix_Codes_File)
        if (Full_Codes_DB_Filename == UNKNOWN) or \
        not (self.Cek_Codes_Name(Full_Codes_DB_Filename)):
            Msg = Message_Dlg(MsgBox_Info, 'Please select a CodesDatabe.db file')
            Msg.wait_window()
            if self.Sel_Codes(Origin):    # return True False
                return True
            return False
        else:
            if self.Data.Get_Files_Loaded_Stat(Ix_Codes_Loaded):
                return True
            else:
                if self.Load_Codes(Origin):
                    return True
                if self.Sel_Codes(Origin):
                    return False
                return True

    # ------------------------------------------------------------------------
    def Init_Xlsx_Rows(self, Origin):
        Full_Xlsx_Filename = self.Data.Get_Txt_Member(Ix_Xlsx_File)
        if (Full_Xlsx_Filename == UNKNOWN) or \
        not (self.Cek_Xlsx_Name(Full_Xlsx_Filename)):
            Msg = Message_Dlg(MsgBox_Info, 'Please select a file.xlsx')
            Msg.wait_window()
            if self.Sel_Xlsx(Origin):
                if self.Load_Xlsx_Rows(Origin):
                    return True
                return False
        else:
            if self.Data.Get_Files_Loaded_Stat(Ix_Xlsx_Rows_Loaded):
                return True
            else:
                if self.Load_Xlsx_Rows(Origin):
                    return True
                return False

    # -------------------------------------------------------------------------
    def Init_Xlsx_Lists(self, Origin):
        if not self.Init_Xlsx_Rows(Origin):
            return False
        else:
            if self.Data.Get_Files_Loaded_Stat(Ix_Transact_Loaded):
                return True
            else:
                if self.Load_Xlsx_Lists(Origin):
                    return True
                return False

    # -------------------------------------------------------------------------
    def Init_Transactions(self, Origin):
        Full_Transact_Filename = self.Data.Get_Txt_Member(Ix_Transact_File)
        if (Full_Transact_Filename == UNKNOWN) or \
        not (self.Cek_Transactions_Name(Full_Transact_Filename)):
            Msg = Message_Dlg(MsgBox_Ask, 'Please select a transactions db file')
            Msg.wait_window()
            if self.Sel_Transact(Origin):
                if self.Load_Transact(Origin):
                    return True
                else:
                    return False
            else:
                Msg = Message_Dlg(MsgBox_Info, 'new database must be created')
                Msg.wait_window()
                return False
        else:
                if self.Load_Transact(Origin):
                    return True
                else:
                    return False

    # =========================================================================================== #
    #           --------------     Sel_ file Methods    --------------                            #
    # =========================================================================================== #
    def Sel_Codes(self, Origin):
        File_Dlg      = File_Dialog(FileBox_Codes)
        Full_Filename = File_Dlg.FileName
        if self.Cek_Codes_Name(Full_Filename):
            Reply =  self.Data.Load_Codes_Table(Full_Filename)
            if Reply == OK:    # it will set LOAD/NO
                self.Data.Update_Txt_File(Full_Filename, Ix_Codes_File)
                self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
            else:
                Dlg_Mess = Message_Dlg(MsgBox_Err, Reply)
                Dlg_Mess.wait_window()
                return False

    # -------------------------------------------------------------------------
    def Sel_Xlsx(self, Origin):
        File_Dlg      = File_Dialog(FileBox_Xlsx)
        Full_Filename = File_Dlg.FileName
        if not Full_Filename:
            return False
        if self.Cek_Xlsx_Name(Full_Filename):
            Reply = self.Cek_Xlsx_Name(Full_Filename)
            if Reply != OK:
                pass
            # if self.Data.Load_Xlsx_Lists_FromData():
            #     self.Data.Update_Txt_File(Full_Filename, Ix_Xlsx_File)
            #     self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
            #     return True
        else:
            return False

    # -------------------------------------------------------------------------
    def Sel_Transact(self, Origin):
        File_Dlg      = File_Dialog(FileBox_Transact)
        Full_Filename = File_Dlg.FileName
        if self.Cek_Transactions_Name(Full_Filename):
            if self.Data.Load_Transact_Table():
                self.Data.Update_Txt_File(Full_Filename, Ix_Transact_File)
                self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
        else:
            return False

    # =========================================================================================== #
    #           --------------    Load  Methods     --------------                                #
    # =========================================================================================== #
    # the codes filename  is OK
    def Load_Codes(self, Origin):
        Reply = self.Data.Load_Codes_Table('')
        Result = True
        if Reply != OK:                     #  reply:  OK or Diagnostic
            Result = False
            Msg = Message_Dlg(MsgBox_Err, Reply)
            Msg.wait_window()
        self.Chat.Tx_Request([Origin, [ANY], CODES_DB_UPDATED, []])
        self.Data.Check_Codesdatabase()
        return Result

    # ----------------------------------------------------------------------------------------------------- #
    # Load_Xlsx_Rows:     _XLSX_Rows_From_Sheet   (for View Xlsx rows)  calculate Tot_OK  TOT_NOK           #
    #                     _XLSX_Rows_Desc_Compact (for  Lists  with/out code)                               #
    #                           *** the worse case is when any row with data OK are found                   #
    # Create_Xlsx_List:  _With_Code_Tree_List  _Wihtout_Code_Tree_List                                      #
    #                     *** if some Without code rows exist: Insert transaction on Db if forbidden        #
    #                     *** the worse case is if a description is matched with more Str_ToSearch          #
    #                                                                                                       #
    # ----------------------------------------------------------------------------------------------------- #
    def Load_Xlsx_Rows(self, Origin):
        Reply = self.Data.Load_Xlsx_Rows_FromSheet()
        if Reply == OK:
            self.Chat.Tx_Request([Origin, [ANY], XLSX_ROWS_LOADED, []])
            return True
        else:
            Dlg_Mess = Message_Dlg(MsgBox_Err, Reply)
            Dlg_Mess.wait_window()
            return False

    # -------------------------------------------------------------------------------------------------------
    def Load_Xlsx_Lists(self, Origin):
        self.Data.Xlsx_Conto_Year_Month_Setup(True)  # neede for lists creating
        Reply = self.Data.Load_Xlsx_Lists_FromData()
        if Reply == OK:
            self.Chat.Tx_Request([Origin, [ANY], XLSX_UPDATED, []])
            return True
        else:
            self.Top_Launcher(TOP_VIEW_MESS, TOP_SETTINGS, [Reply])
            return False

    # -------------------------------------------------------------------------
    def Load_Transact(self, Origin):
        self.Data.Transact_Year_Setup(True)  # needed for lists creating
        Reply = self.Data.Load_Transact_Table()
        if Reply == OK or Reply == EMPTY:
            Result = True
            if Reply == EMPTY:
                Msg = Message_Dlg(MsgBox_Err, 'Transactions Database is EMPTY')
                Msg.wait_window()
        else:
            Result = False
            Msg = Message_Dlg(MsgBox_Err, Reply)   # display 'ERROR... '
            Msg.wait_window()

        self.Data.Set_Files_Lodad(Ix_Transact_Loaded, True)
        self.Chat.Tx_Request([Origin, [ANY], TRANSACT_UPDATED, []])
        return Result


    # =========================================================================================== #
    #           --------------    Cek_ names Methods    --------------                            #
    # =========================================================================================== #
    @classmethod
    def Cek_Codes_Name(cls, Full_Codes_Name):
        if Full_Codes_Name == UNKNOWN or not Full_Codes_Name:
            return False
        Dirname  = Get_Dir_Name(Full_Codes_Name)
        filename = Get_File_Name(Full_Codes_Name)
        errMessage = ''
        if len(filename) < Len_Codes_Filename_Min:
            errMessage = 'Len of Codes filename INCORRECT'
        else:
            iLastBar = int(Full_Codes_Name.rfind("/") + 1)
            strCodes = Full_Codes_Name[(iLastBar - 9):(iLastBar + 11)]
            if strCodes != Ident_DB_Filename:
                errMessage = 'DBcodes filename ERROR:\n\n'
                errMessage += filename + '\n' + Dirname  + '\n\nexpected:  ' + Ident_DB_Filename
        if errMessage != '':
            Mess = Message_Dlg(MsgBox_Err, errMessage)
            Mess.wait_window()
            return False
        return True

    # -------------------------------------------------------------------------
    # /home/mario/bExpenses/bFiles/bXLSX_Files/FIDEU/FIDEU_2023/ FIDEU_2023_01.xlsx
    #                                         765432109876543210 123456789012345678
    def Cek_Xlsx_Name(self, Full_Xlsx_Filename):
        if Full_Xlsx_Filename == UNKNOWN or not Full_Xlsx_Filename:
            return False
        errMessage = ''
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
                errMessage = 'Bank conto not correct'
            elif ContoDir not in ContoYear or ContoDir not in ContoYearOnfilename:
                errMessage = 'Mismatching with\n' + ContoDir + '\n' + ContoYear + '\n' + ContoYearOnfilename
            elif not (Check_strYear(strYear, self.Data.Min_Year, self.Data.Max_Year)):
                errMessage = 'Year  not OK:  ' + strYear
            elif not (Check_strMonth(strMonth)):
                errMessage = 'Month  not OK:  '  + strMonth
        if errMessage != '':
            Msg = Message_Dlg(MsgBox_Err, errMessage)
            Msg.wait_window()
            self.Data.Xlsx_Conto_Year_Month_Setup(False)
            return False
        return True

    # -------------------------------------------------------------------------
    # 210987654321 0 12345678901234
    # TRANSACTIONS / Transact_2024.db
    def Cek_Transactions_Name(self, Full_Transact_Name):
        if Full_Transact_Name == UNKNOWN or not Full_Transact_Name:
            return False
        TransactionsIdent = TRANSACTIONS + '/' + Transact_
        filename = Get_File_Name(Full_Transact_Name)
        errMessage = ''

        if len(filename) < Len_Transact_Filename:
            errMessage = 'Len of Transactions filename INCORRECT'
        else:
            iLastBar      = int(Full_Transact_Name.rfind("/") + 1)
            Transact_Str  = Full_Transact_Name[(iLastBar-13):(iLastBar+9)]
            strYear       = filename[9:13]

            if Transact_Str != TransactionsIdent:
                errMessage = 'Transactions filename ERROR:\n\n'
                errMessage += filename + '\n' + Transact_Str
            else:
                if not (Check_strYear(strYear, self.Data.Min_Year, self.Data.Max_Year)):
                    errMessage = 'Year  not OK:  ' + strYear
        if errMessage != '':
            Msg = Message_Dlg(MsgBox_Err, errMessage)
            Msg.wait_window()
            self.Data.Transact_Year_Setup(False)
            return False
        return True


    # =========================================================================================== #
    #            ***    Toplevel    Module   launcher     ***                                     #
    # =========================================================================================== #
    # Name           = Moudule Name to launch
    # Origin         = The requesting Module
    # List_For_Start =  List of Parameters to pass to Recipient
    # -------------------------------------------------
    def Top_Launcher(self, Name_ToLaunch, Origin, Param_List):
        if self.Chat.Check_Name_Is_On_Participants_List(Name_ToLaunch):
            self.Chat.Tx_Request([Origin, [Name_ToLaunch], CODE_TO_CLOSE, []])
            return
        else:
            TopLevel  = self.Get_TopLev(Name_ToLaunch)
            Result    = self.Make_Checkout(Name_ToLaunch, Origin)
            TopLevel(Result, Param_List)

    # ---------------------------------------------------------------------------------------------
    def Make_Checkout(self, Name, Origin):
        for Item in LAUNCH_CHECKOUT:
            CheckName    = Item[0]
            if CheckName == Name:
                Checklist = Item[1]
                if not Checklist:
                    return True
                
                for Check in Checklist:
                    if Check == CEK_CODES:                          # CEK_CODES
                        if not self.Init_Codes(Origin):
                            return False

                    elif Check == CEK_XLSX_ROWS:                      # CEK_XLSX ROWS
                        if not self.Init_Xlsx_Rows(Origin):
                            return False

                    elif Check == CEK_XLSX_LIST:                      # CEK_XLSX LISTS
                        if not self.Init_Xlsx_Rows(Origin):
                            return NOK
                        if not self.Init_Xlsx_Lists(Origin):
                            return True

                    elif Check == CEK_TRANSACT:                       # CEK_TRANSACT
                        if not self.Init_Transactions(Origin):
                            return NOK
                return OK

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
