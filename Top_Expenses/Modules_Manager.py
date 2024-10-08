# ============================================================================= #
#                 -----   Modules_Manager.py   -----                            #
#                    child of class  Mod_Mngr_Init                              #
#        instanced on start as:    Modul_Mngr = Modules_Manager()               #
#                                                                               #
# ============================================================================= #

import os
import sqlite3

from Top_Expenses.Mod_Mngr_Init import Mod_Mngr_Init
from Widgt.Dialogs import *

class Modules_Manager(Mod_Mngr_Init):
    def __init__(self):
        super().__init__()

        self.Xlsx_Filename      = ''
        self.Xlsx_Year          = None
        self.Total              = []
        self.Tot_WithoutCode    = None

        self.Transact_Filename  = ''
        self.Transact_Year      = None

        # =======================   Selections  settings    ==========================================#
    #                  called at start from Main_Window                                           #
    # =========================================================================================== #
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
            TopLevel = self._Get_TopLev(Name_ToLaunch)
            if self.Make_Checkout(Name_ToLaunch, Origin):
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
            return True
                
        for Check in CheckList:
            if Check == CEK_CODES:                          # CEK_CODES
                if not self.Init_Codes(Origin):
                    return False

            if Check == CEK_XLSX_LIST:                      # CEK_XLSX LISTS
                if not self.Init_Xlsx_Lists(Origin):
                    self.Xlsx_Sel_Request(Origin)
                    pass

            if Check == CEK_TOP_INSERT:                     # CEK_TRANSACT for Top_Insert
                if self.Init_Top_Insert(Origin):
                    pass
                else:
                    return False

            if Check == CEK_TOP_QUERIES:                    # CEK_TRANSACT for Top_Queries
                if not self.Initialize_Tansactions(ON_SELECTIONS):
                    return False
        return True

    # ---------------------------------------------------------------------------------------------
    def Xlsx_Sel_Request(self, Origin):
        Msg_Dlg = Message_Dlg(MsgBox_Err, 'an Xlsx file must be selected')
        Msg_Dlg.wait_window()
        if self.Sel_Xlsx(Origin):
            return True
        else:
            return False

    # -------------------------------------------------------------------------------------------------
    #  controls for launching  Top_Insert
    # -------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------
    def Init_Top_Insert(self, Origin):          # called on startup and on click Sel file Xlsx
        # -------------------  an xlsx file must be loaded  -----------------
        if not self.Init_Xlsx_Lists(Origin):
            return False
        self.Xlsx_Filename   = self.Data.Get_Selections_Member(Ix_Xlsx_File)
        self.Xlsx_Year       = Get_Xlsx_Year(self.Xlsx_Filename)
        self.Total           = self.Data.Get_Total_Rows()
        self.Tot_WithoutCode = self.Total[Ix_Tot_Without_Code]

        if self.Tot_WithoutCode != 0:
            # -------------------  some Xlsx rows without code  -----------------
            Messg = str(self.Tot_WithoutCode) + '  Trovato movimenti senza codice\n'
            Messg += 'Inserisci nuovi codici\te poi riprova'
            Msg_Dlg = Message_Dlg(MsgBox_Info, Messg)
            Msg_Dlg.wait_window()
            return False

        else:
            # -----------------  Transactions file name is unknown    -------------
            self.Transact_Filename    = self.Data.Get_Selections_Member(Ix_Transact_File)
            if self.Transact_Filename == UNKNOWN:
                if self.Create_New_Transact_Db(self.Xlsx_Year):
                    return True
                else:
                    return False
            else:
                # -------- Check for transactions year same as xlsx year   -------------
                self.Transact_Year = Get_Transactions_Year(self.Transact_Filename)
                if self.Xlsx_Year == self.Transact_Year:
                    return self.Initialize_Tansactions(ON_SELECTIONS)
                else:
                    if self.Get_Transact_For_Xlsx_Year():
                        return self.Initialize_Tansactions(ON_SELECTIONS)


    # -------------------------------------------------------------------------------------------------
    def Create_New_Transact_Db(self, Year):
        Full_Name = self.Data.Create_TRansact_Filename(Year)
        ResCreate = self.Data.Create_Transact_DB_File(Full_Name)
        if ResCreate[0] == -1:
            Messg = "Creato un nuovo file movimenti\nper l'anno   " + str(Year)
            Dlg_Msg = Message_Dlg(MsgBox_Info, Messg)
            Dlg_Msg.wait_window()
            return True

        elif ResCreate[0] == 1:
            Messg = "File movimenti per l'anno   " + str(Year) + '\ngià esistente'
            Dlg_Msg = Message_Dlg(MsgBox_Info, Messg)
            Dlg_Msg.wait_window()
            return True
        else:
            Dlg_Msg = Message_Dlg(MsgBox_Err, ResCreate[1])
            Dlg_Msg.wait_window()
            return False

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_For_Xlsx_Year(self):
        # -----------------   years   NOT  EQUAL    ---------------------------
        TRansact_Years_List = self.Data.Get_Transact_Year_ListInData()[1]
        if self.Xlsx_Year in TRansact_Years_List:
            newTransact_Filename = Transact_ + str(self.Xlsx_Year) + '.db'
            Dir_Name             = Get_Dir_Name(self.Data.Get_Selections_Member(Ix_Transact_File))
            Full_Filename        = Dir_Name + newTransact_Filename
            File_Exists          = os.path.isfile(Full_Filename)
            if not File_Exists:
                Messg = ('inspiegabilmente il file  ' + Full_Filename +
                                          '\nper l"anno: ' + str(self.Xlsx_Year) + 'non esiste')
                Msg_Dlg = Message_Dlg(MsgBox_Err, Messg)
                Msg_Dlg.wait_window()
                return False
            self.Data.Update_Selections(Full_Filename, Ix_Transact_File)
            return True

        else:  # ------------------  any transactions file found ----------
            if not self.Create_New_Transact_Db(self.Xlsx_Year):
                return False
            else:
                return True

    # ------------------------------------------------------------------------------------------------
    def Initialize_Tansactions(self, Filename):
        Transact_Filename = Filename
        if Filename == ON_SELECTIONS:
            Transact_Filename = self.Data.Get_Selections_Member(Ix_Transact_File)
        Result = self.Data.Load_Transact_Table(Transact_Filename)
        if Result == OK:
            return True
        else:
            Msg_Dlg = Message_Dlg(MsgBox_Info, Result)
            Msg_Dlg.wait_window()
            return False

# =================================================================================================


# -------------------------------- #
Modul_Mngr = Modules_Manager()     #
# -------------------------------- #
