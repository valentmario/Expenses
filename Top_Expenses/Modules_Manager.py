# ============================================================================= #
#                 -----   Modules_Mnager.py   -----                             #
#                                                                               #
#    ----------------------------------                                         #
#     Modul_Mngr = Modules_Manager()                                            #
#     Data       = Transact_DB <-- Xlsx_Manager <--                             #
#                  <-- Files_Names_Manager                                      #
#     are instanced on Startup and will NEVER destroyed                         #
#                                                                               #
#    Methodes:  ( returns  True or False)                                       #
#         Codes_DB             Xlsx               Transactions                  #
#       Init_Codes          Init_xlsx           Init_transact                   #
#       Cek_Codes_Name      Cek_xlsx_Name       Cek_Transactions_Name           #
#       Sel_Codes           Sel_Xlsx            Sel_Transact                    #
#       Load_Codes          Load_Xlsx           Load_Transact                   #
#                                                                               #
#    The List on Data is                                                        #
#     [self._Xlsx_Conto,self._Xlsx_Year,self._Xlsx_Month,self._Transact_Year]   #
#     is created from  Xlsx_Conto_Year_Month_Setup(False/True)   and            #
#                      Transact_Year_Setup(False/True)                          #
#      on Cek_Create_Txt_File(),  Cek..Name(), Sel..file(),  Load..Data()       #
#      so all TopLevels are launchd with this filled list                       #
#                                                                               #
# ============================================================================= #
"""
    the rule is:
    methods and data inside the data chain are private and underscored (_).
    the private (_) methods and attributes are accessible only inside data chain.
    public methods are not undscored (_) and should not acces to _attributes,
    but they can retrieve _attributes with Get_somthing_method()

    data chain:
    LOW LEVEL       return  OK  or  'Diagnostic'

    Modules_Manager
    MIDDLE LEVEL    return True or display 'Diagnostic' and return False

    Toplevel modules
    HIGH LEVEL      get only True or False
"""
# ============================================================================== #

from Common.Common_Functions import *
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data
from Widgt.Dialogs import Message_Dlg

# -------------------------------------------------------------------------------------------------
class Modules_Manager:
    def __init__(self):
        self.Data = Data
        self.Chat = Ms_Chat
        self.Dummy = None
        # these attributes are not memorized on Txt_File
        self.Files_Loaded = [NOK, NOK, NOK]     # same structure as Files_Stat LOADED / NOK

        self.Toplevels_Id_List = []     # <class>,  NAME  # List of toplevel to launch in Top_Settings

    # ---------------------------------------------------------------------------------------------
    def Get_Files_Loaded_Status(self):
        return self.Files_Loaded

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
        self.Dummy = Origin  # Origin NOT used
        Full_Codes_DB_Filename = self.Data.Get_Txt_Member(Ix_Codes_File)
        if (Full_Codes_DB_Filename == UNKNOWN) or \
        not (self.Cek_Codes_Name(Full_Codes_DB_Filename)):
            Msg = Message_Dlg(MsgBox_Info, 'Please select a CodesDatabe.db file')
            Msg.wait_window()
            if self.Sel_Codes(Origin):    # return True False
                if self.Load_Codes(Origin):
                    return True
            return False
        else:
            if self.Files_Loaded[Ix_Codes_Loaded] == LOADED:
                return True
            else:
                if self.Load_Codes(Origin):
                    return True
                return False

    # -------------------------------------------------------------------------
    def Init_Xlsx(self, Origin):
        Full_Xlsx_Filename = self.Data.Get_Txt_Member(Ix_Xlsx_File)
        if (Full_Xlsx_Filename == UNKNOWN) or \
        not (self.Cek_Xlsx_Name(Full_Xlsx_Filename)):
            Msg = Message_Dlg(MsgBox_Info, 'Please select a file.xlsx')
            Msg.wait_window()
            if self.Sel_Xlsx(Origin):
                if self.Load_Xlsx(Origin):
                    return True
                return False
        else:
            if self.Files_Loaded[Ix_Xls_Loaded] == LOADED:
                return True
            else:
                if self.Load_Xlsx(Origin):
                    return True
                return False
    # -------------------------------------------------------------------------
    def Init_Transactions(self, Origin):
        Full_Transact_Filename = self.Data.Get_Txt_Member(Ix_Transact_File)
        if (Full_Transact_Filename == UNKNOWN) or \
        not (self.Cek_Transactions_Name(Full_Transact_Filename)):
            Msg = Message_Dlg(MsgBox_Info, 'Please select a Transact_YYYY.db file')
            Msg.wait_window()
            if self.Sel_Transact(Origin):    # return True False
                if self.Load_Transact(Origin):
                    return True
            return False
        else:
            if self.Files_Loaded[Ix_Transact_Loaded] == LOADED:
                return True
            else:
                if self.Load_Transact(Origin):
                    return True
                return False

    # =========================================================================================== #
    #           --------------     Sel_ file Methods    --------------                            #
    # =========================================================================================== #
    def Sel_Codes(self, Origin):
        Full_Filename = self.Data.Sel_Codes_OnData()  # return the full filename
        if self.Cek_Codes_Name(Full_Filename):
            self.Data.Update_Txt_File(Full_Filename, Ix_Codes_File)
            self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def Sel_Xlsx(self, Origin):
        Full_Filename = self.Data.Sel_Xlsx_OnData()  # return the full filename
        if self.Cek_Xlsx_Name(Full_Filename):
            self.Data.Update_Txt_File(Full_Filename, Ix_Xlsx_File)
            self.Data.Xlsx_Conto_Year_Month_Setup(True)
            self.Chat.Tx_Request([Origin, [MAIN_WIND], UPDATE_FILES_NAME, []])
            return True
        else:
            return False

    # -------------------------------------------------------------------------
    def Sel_Transact(self, Origin):
        Full_Filename = self.Data.Sel_Transact_OnData()  # return the full filename
        if self.Cek_Transactions_Name(Full_Filename):
            self.Data.Update_Txt_File(Full_Filename, Ix_Transact_File)
            self.Data.Transact_Year_Setup(True)
            self.Chat.Tx_Request([Origin, [ANY], UPDATE_FILES_NAME, []])
            return True
        else:
            return False

    # =========================================================================================== #
    #           --------------    Load  Methods     --------------                                #
    # =========================================================================================== #
    # the codes filename  and codes tables are OK
    def Load_Codes(self, Origin):
        Reply = self.Data.Load_Codes_Table()       # reply OK or Diagnostic
        if Reply == OK:
            self.Files_Loaded[Ix_Codes_Loaded] = LOADED
            self.Chat.Tx_Request([Origin, [ANY], CODES_DB_UPDATED, []])
            return True
        else:
            Msg = Message_Dlg(MsgBox_Err, Reply)
            Msg.wait_window()
            return False

    # -------------------------------------------------------------------------
    #  the codes filename  and codes tables are OK
    def Load_Xlsx(self, Origin):
        self.Data.Xlsx_Conto_Year_Month_Setup(True)  # neede for lists creating
        Reply = self.Data.Load_Xlsx_Lists()
        if Reply == OK:
            self.Files_Loaded[Ix_Xls_Loaded] = LOADED
            self.Chat.Tx_Request([Origin, [ANY], CODES_DB_UPDATED, []])
            return True
        else:
            Msg = Message_Dlg(MsgBox_Err, Reply)
            Msg.wait_window()
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
            self.Files_Loaded[Ix_Transact_Loaded] = LOADED   # in this caase the database is cleared
            Msg = Message_Dlg(MsgBox_Err, Reply)             # return 'ERROR... '
            Msg.wait_window()

        self.Files_Loaded[Ix_Transact_Loaded] = LOADED
        self.Chat.Tx_Request([Origin, [ANY], CODES_DB_UPDATED, []])
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
    # ----------------------     launch Top_level  after Init_ checkout     --------------------- #
    # =========================================================================================== #
    def Top_Launcher(self, Name, Origin):
        if self.Chat.Check_Name_Is_On_Participants_List(Name):
            self.Chat.Tx_Request([Origin, [Name], CODE_TO_CLOSE, []])
            return
        else:
            Result = self.Make_Checkout(Name, Origin)
            if Result == OK:
                TopLevel = self.Get_TopLev(Name)
                TopLevel()
    # ---------------------------------------------------------------------------------------------
    def Make_Checkout(self, Name, Origin):
        for Item in LAUNCH_CHECKOUT:
            CheckName    = Item[0]
            if CheckName == Name:
                Checklist = Item[1]
                if not Checklist:
                    return OK
                
                for Check in Checklist:
                    if Check == CEK_CODES:                          # CEK_CODES
                        if not self.Init_Codes(Origin):
                            return NOK

                    if Check == CEK_XLSX:                           # CEK_XLSX
                        if not self.Init_Xlsx(Origin):
                            return NOK

                    if Check == CEK_XLSX_MNGR:                      # CEK_XLSX for Top_Mngr
                        # if not self.Init_Xlsx(Origin):
                        self.Init_Xlsx(Origin)
                        return OK

                    if Check == CEK_TRANSACT:                       # CEK_TRANSACT
                        if not self.Init_Transactions(Origin):
                            return NOK

                    if Check == CEK_SUMMARIES:
                        pass
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
