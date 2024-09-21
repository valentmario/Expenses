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
from tkinter.commondialog import Dialog

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
    def Cek_Create_Selections(self):
        Result = self.Data.Check_Create_Selections()
        if Result == NEW:
            self.Data.Xlsx_Conto_Year_Month_Setup(False, '')
            self.Data.Transact_Year_Setup(False)
            Text = "New Selections file created\nmount the data drive"
            Msg  = Message_Dlg(MsgBox_Info, Text)
            Msg.wait_window()
        else:
            Filename = self.Data.Get_Selections_Member(Ix_Xlsx_File)
            self.Data.Xlsx_Conto_Year_Month_Setup(True, Filename)
            self.Data.Transact_Year_Setup(True)

    # =========================================================================================== #
    #           --------------      Codes  manage     --------------                              #
    #      A correct filename selected,  self.Data.Load_Codes_Table will load the Tables          #
    #      from database. In case of error nothing is changed:  Txt_File  and Db Tables           #
    # =========================================================================================== #
    def Init_Codes(self, Origin):
        Full_Codes_DB_Filename = self.Data.Get_Selections_Member(Ix_Codes_File)
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
                Result = self.Data.Load_Codes_Table(ON_SELECTIONS)
                if Result != OK:
                    Msg_Dlg = Message_Dlg(MsgBox_Err, Result)
                    Msg_Dlg.wait_window()
                    return False
                return False

    # ---------------------------------------------------------------------------------------------
    # call from Sel_codes  Filename=Selection on skopenFile
    # Call from Load       Filename=
    # ---------------------------------------------------------------------------------------------
    def Cek_Codes_Name(self, Filename):
        File_Name = Filename
        if Filename == ON_SELECTIONS:
            File_Name = self.Data.Get_Selections_Member(Ix_Codes_File)

        if File_Name == UNKNOWN or not File_Name:
            return False
        Dirname  = Get_Dir_Name(File_Name)
        filename = Get_File_Name(File_Name)
        errMessage = ''
        if len(filename) < Len_Codes_Filename_Min:
            errMessage = 'Len of Codes filename INCORRECT'
        else:
            iLastBar = int(File_Name.rfind("/") + 1)
            strCodes = File_Name[(iLastBar - 9):(iLastBar + 11)]
            if strCodes != Ident_DB_Filename:
                errMessage = 'DBcodes filename ERROR:\n\n'
                errMessage += filename + '\n' + Dirname  + '\n\nexpected:  ' + Ident_DB_Filename
        if errMessage != '':
            Mess = Message_Dlg(MsgBox_Err, errMessage)
            Mess.wait_window()
            return False
        return True

    # ---------------------------------------------------------------------------------------------
    def Sel_Codes(self, Origin):
        File_Dlg      = File_Dialog(FileBox_Codes)
        Full_Filename = File_Dlg.FileName
        if not Full_Filename:
            return False
        if self.Cek_Codes_Name(Full_Filename):
            Reply =  self.Data.Load_Codes_Table(Full_Filename)
            if Reply == OK:           # The Codes Db is loaded despite some error found
                self.Check_Codes_Db()
                self.Data.Update_Selections(Full_Filename, Ix_Codes_File)
                self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
            else:
                Dlg_Mess = Message_Dlg(MsgBox_Err, Reply)
                Dlg_Mess.wait_window()
                return False

    # ---------------------------------------------------------------------------------------------
    def Check_Codes_Db(self):
        Multiple = self.Data.Check_Codesdatabase()
        pass
        # if not Multiple:
        #     Len = self.Data.Get_TR_Codes_Table_Len()
        #     Info = str(Len) + '   code records correctly checked out'
        #     Message = Message_Dlg(MsgBox_Info, Info)
        # else:
        #     Info = 'ERROR on checking out codes database\n\n'
        #     for TRrecord in Multiple:
        #         StrToserch = TRrecord[iTR_TRserc]
        #         FullDescr = TRrecord[iTR_TRfullDes]
        #         Info += StrToserch + '\n' + FullDescr + '\n\n'
        #     Message = Message_Dlg(MsgBox_Err, Info)
        # Message.wait_window()
        # Top_View_Message([Info])


    # ---------------------------------------------------------------------------------------------
    def Load_Codes(self, Origin):
        if not (self.Cek_Codes_Name(ON_SELECTIONS)):
            Reply = self.Data.Load_Codes_Table(ON_SELECTIONS)  # '': _Codes_Table  or TR_List
            if Reply != OK:                     #  reply:  OK or Diagnostic
                Msg = Message_Dlg(MsgBox_Err, Reply)
                Msg.wait_window()
                return False
            else:
                self.Chat.Tx_Request([Origin, [ANY], CODES_DB_UPDATED, []])
                self.Check_Codes_Db()


    # =============================================================================================== #
    # Create_Xlsx_Lists:  _XLSX_Rows_From_Sheet   (for View Xlsx rows)  calculate Tot_OK  TOT_NOK     #
    #                     _XLSX_Rows_Desc_Compact (for  Lists  with/out code)                         #
    #                           *** the worse case is when any row with data OK are found             #
    #                                                                                                 #
    #                     _With_Code_Tree_List  _Wihtout_Code_Tree_List                               #
    #                     *** if some Without code rows exist: Insert transaction on Db if forbidden  #
    #                     *** the worse case is if a description is matched with more Str_ToSearch    #
    #                                                                                                 #
    # =============================================================================================== #
    def Init_Xlsx_Lists(self, Origin):
        Full_Xlsx_Filename = self.Data.Get_Txt_Member(Ix_Xlsx_File)
        if (Full_Xlsx_Filename == UNKNOWN) or \
        not (self.Cek_Codes_Name(Full_Xlsx_Filename)):
            Msg = Message_Dlg(MsgBox_Info, 'Please select an xlsx file')
            Msg.wait_window()
            if self.Sel_Xlsx(Origin):    # return True False
                return True
            return False
        else:
            if self.Data.Get_Files_Loaded_Stat(Ix_Xlsx_File):
                return True
            else:
                if self.Load_Xlsx_Lists(Origin, ON_SELECTIONS):
                    return True
                return False


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
            self.Data.Xlsx_Conto_Year_Month_Setup(False, '')
            return False
        return True

    # ---------------------------------------------------------------------------------------------
    def Sel_Xlsx(self, Origin):
        File_Dlg      = File_Dialog(FileBox_Xlsx)
        Full_Filename = File_Dlg.FileName
        if not Full_Filename:
            return False
        if self.Cek_Xlsx_Name(Full_Filename):
            Reply =  self.Data.Load_Xlsx_Lists_FromData(Full_Filename)
            if Reply == OK:
                self.Data.Update_Selections(Full_Filename, Ix_Xlsx_File)
                self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
            else:
                Dlg_Mess = Message_Dlg(MsgBox_Err, Reply)
                Dlg_Mess.wait_window()
                return False

    # -------------------------------------------------------------------------------------------------------
    def Load_Xlsx_Lists(self, Origin, Filename):
        File_Name = Filename
        if Filename == ON_SELECTIONS:
            File_Name = self.Data.Get_Selections_Member(Ix_Xlsx_File)
        self.Data.Xlsx_Conto_Year_Month_Setup(True, File_Name)  # neede for lists creating
        Reply = self.Data.Load_Xlsx_Lists_FromData(Filename)
        if Reply == OK:
            self.Data.Update_Selections(Filename, Ix_Xlsx_File)
            self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
            self.Chat.Tx_Request([Origin, [ANY], XLSX_UPDATED, []])
            return True
        else:
            Msg_Dlg = Message_Dlg(MsgBox_Err, Reply)
            Msg_Dlg.wait_window()
            return False

    # =========================================================================================== #
    #     --------------      Transactions  manage     --------------                             #
    #      A correct filename selected,  self.Data.Load_Codes_Table will load the Tables          #
    #      from database. In case of error nothing is changed
    # =========================================================================================== #
    def Init_Transactions(self, Origin):
        Full_Transact_Filename = self.Data.Get_Selections_Member(Ix_Transact_File)
        if Full_Transact_Filename == UNKNOWN:
            Msg = Message_Dlg(MsgBox_Ask, 'filename transactions db file unknown')
            Msg.wait_window()
            return False
        if not self.Cek_Transactions_Name(Full_Transact_Filename):
            return False

        if self.Data.Get_Files_Loaded_Stat(Ix_Transact_Loaded):
            return True
        else:
            if self.Load_Transact(Origin):
                return True
            return False

    # -----------------------------------------------------------------------------------------
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
            iLastBar = int(Full_Transact_Name.rfind("/") + 1)
            Transact_Str = Full_Transact_Name[(iLastBar - 13):(iLastBar + 9)]
            strYear = filename[9:13]

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

    # ----------------------------------------------------------------------------------------------
    def Sel_Transact(self, Origin):
        File_Dlg      = File_Dialog(FileBox_Transact)
        Full_Filename = File_Dlg.FileName
        if not Full_Filename:
            return False
        Reply = ''
        if self.Cek_Transactions_Name(Full_Filename):
            Reply = self.Data.Load_Transact_Table(Full_Filename)
            if Reply == OK:
                self.Data.Update_Selections(Full_Filename, Ix_Transact_File)
                self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
                return True
        else:
            Dlg_Mess = Message_Dlg(MsgBox_Err, Reply)
            Dlg_Mess.wait_window()
            return False

    # -------------------------------------------------------------------------
    def Load_Transact(self, Origin):
        self.Data.Transact_Year_Setup(True)  # needed for lists creating
        self.Chat.Tx_Request([Origin, [ANY], TRANSACT_UPDATED, []])
        Reply = self.Data.Load_Transact_Table()
        if Reply == OK or Reply == EMPTY:
            if Reply == EMPTY:
                Msg = Message_Dlg(MsgBox_Err, 'Transactions Database is EMPTY')
                Msg.wait_window()
            return True
        else:
            Msg = Message_Dlg(MsgBox_Err, Reply)   # display 'ERROR... '
            Msg.wait_window()
            return False


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
            try:
                TopLevel(Result, Param_List)
            except:
                print('Launcher ERROR')
                print(Name_ToLaunch)
                print(Origin)
                Messg = 'Launcher ERROR\n' + 'Toplevel to be launched:  ' + Name_ToLaunch
                Messg += '\nOrigin:   ' + Origin
                Dlg_Ms = Message_Dlg(MsgBox_Err, Messg)
                Dlg_Ms.wait_window()
                pass

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

                    elif Check == CEK_XLSX_LIST:                      # CEK_XLSX LISTS
                        if not self.Init_Xlsx_Lists(Origin):
                            return True

                    elif Check == CEK_TRANSACT:                       # CEK_TRANSACT
                        if not self.Init_Transactions(Origin):
                            return False
                return True

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
