#!/usr/bin/python3
# *********************************************************************************************** #
#                            ***   Main_Window.py   ***                                           #
#      Init / Select  Codes Database                                                              #
#      The Toplevels launch is made by Top_Launcher (that makes the initial controls              #
#        before launch i.e. verify Codes, Xlsx, Transactions etc.                                 #
#      The filesnames Text box is updated at starting or from external request through Chat       #
# *********************************************************************************************** #
#                                                                                                 #
#    Modul_Mngr = Modules_Manager()    and                                                        #
#    Data       = Transact_DB()                                                                   #
#    are istanced on Startup and will NEVER destoyed                                              #
# *********************************************************************************************** #

from Top_Expenses.Modules_Manager import Modul_Mngr

from Data_Classes.Transact_DB import Data
from Chat import Ms_Chat

from Common.Common_Functions import *
from Widgt.Widgets import *

from Top_Expenses.Top_Settings import Top_Settings
from Top_Expenses.Top_Codes_Mngr import Top_Mngr
from Top_Expenses.Top_Codes_View import Top_View_Codes
from Top_Expenses.Top_GR_Codes_Mngr import Top_GR_Codes_Mngr
from Top_Expenses.Top_Xlsx_Rows_View import Top_XLSX_Rows_View
from Top_Expenses.Top_Insert import Top_Insert
from Top_Expenses.Top_View_Transactions import Top_View_Transact
from Top_Expenses.Top_Queries import Top_Queries
from Top_Expenses.Top_View_Message import Top_View_Message

# -------------------------------------------------------------------------------------------------
class Main_Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data
        self.Mod_Mngr = Modul_Mngr
        self.Chat.Attach([self, MAIN_WIND])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry('5x5+900+600')
        self.configure(background=BakGnd)
        self.title('')

        self.Top_Level_Id_Create_List()
        self.Txt1 = TheText(self, Txt_Disab, 20, 20, 36, 6, '')

        # --------------------------------------------------------------------------
        self.Mod_Mngr.Cek_Create_Txt_File()    # Check or Create Files_Names.txt
        if not self.Mod_Mngr.Init_Codes(MAIN_WIND):
            pass
        # ---------------------------------------------------------------------------

        self.geometry(Main_Wind_geometry)
        self.title('*****     Family Expenses     *****')

        Widgets_Styles()   # Setup Styles  once called

        self.Dummy      = '  '
        self.Top_Gen    = None
        self.View_Xlsx  = None
        self.Top_Mngr   = None
        self.Top_View   = None

        self.Btn_Chat = TheButton(self, Btn_Def_En,  20, 150, 14, 'Settings',        self.Clk_Settings)
        self.Btn_Mng = TheButton(self,  Btn_Def_En, 170, 150, 14, 'Files manager',   self.Clk_Manage_Codes)

        self.Btn_Ins  = TheButton(self, Btn_Col_En,  20, 200, 14, 'Load transactions', self.Clk_Insert)
        self.Btn_Query= TheButton(self, Btn_Col_En, 170, 200, 14, 'Queries',         self.Clk_Queries)
        self.Exit     = TheButton(self, Btn_Bol_En,  24, 250, 27, '  E X I T   ',    self.Call_OnClose)

        self.Set_Files_Names_Text()     # Set Txt1 for Files names and selections
        self.Top_Level_Start()
        PRINT('Start Main_Wind ms:  ' + str(self.Chat.Get_Elapsed_Time()))
        self.mainloop()

    # ---------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.destroy()
        return

    # ---------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, MAIN_WIND, Request_Code, Values_List)
        if Request_Code == CODE_SHOW_PARTIC_LIST:
            self.Chat.View_Partic()
        if Request_Code == UPDATE_FILES_NAME:
            self.Set_Files_Names_Text()

    # -----------------------------------------------------------------------------------
    def Clk_Settings(self):
        self.Mod_Mngr.Top_Launcher(TOP_SETTINGS, MAIN_WIND, [])

    # -----------------------------------------------------------------------
    # def Tx_Request(self, Tx_Req_List):       # [Txr, [RecList], Request, [Values]]
    def Clk_Manage_Codes(self):
        self.Mod_Mngr.Top_Launcher(TOP_MNGR, MAIN_WIND, [])

    # ---------------------------------------------------------------------------------------------
    def Clk_Insert(self):
        self.Mod_Mngr.Top_Launcher(TOP_INS, MAIN_WIND, [])

    def Clk_Queries(self):
        self.Mod_Mngr.Top_Launcher(TOP_QUERY, MAIN_WIND, [])

    # -----------------------------------------------------------------------------------
    def Set_Files_Names_Text(self):     # Set text for Files Names and selections
        Full_Codes_DB_Filename = self.Data.Get_Txt_Member(Ix_Codes_File)
        if Full_Codes_DB_Filename == UNKNOWN:
            Codes_Filename = UNKNOWN
        else:
            if self.Mod_Mngr.Cek_Codes_Name(Full_Codes_DB_Filename):
                Codes_Filename = Get_File_Name(Full_Codes_DB_Filename)
            else:
                Codes_Filename = 'Codes filename NOT OK'
        # -----------------------------------------------------------
        Full_Xlsx_Filename = self.Data.Get_Txt_Member(Ix_Xlsx_File)
        if Full_Xlsx_Filename == UNKNOWN:
            Xlsx_Filename = UNKNOWN
        else:
            if self.Mod_Mngr.Cek_Xlsx_Name(Full_Xlsx_Filename):
                Xlsx_Filename = Get_File_Name(Full_Xlsx_Filename)
            else:
                Xlsx_Filename = 'Xlsx filename NOT OK'
        # -------------------------------------------------------------
        Full_Transact_Filename = self.Data.Get_Txt_Member(Ix_Transact_File)
        if Full_Transact_Filename == UNKNOWN:
            Transact_Filename = UNKNOWN
        else:
            if self.Mod_Mngr.Cek_Transactions_Name(Full_Transact_Filename):
                Transact_Filename = Get_File_Name(Full_Transact_Filename)
            else:
                Transact_Filename = 'Transactions filename NOT OK'
        # --------------------------------------------------------------
        Filenames      = "Codes:      " + Codes_Filename + \
                       "\nxlsx:           " + Xlsx_Filename + \
                       "\nTransact:   " + Transact_Filename +'\n'

        Query_List  = self.Data.Get_Txt_Member(Ix_Query_List)
        Values         = []
        for ix in range(Ix_Query_Conto, Ix_Query_CAsel+1):       # setup values for queries
            Values.append(Query_List[ix])

        strQuery       = 'Query:  ' + \
                         str(Values[Ix_Query_Conto]) + '  ' + \
                         str(Values[Ix_Query_Month]) + '  ' + \
                         str(Values[Ix_Query_TotMonths])
        strSelect      = '\nSel:  ' + \
                         str(Values[Ix_Query_TRsel]) + '   ' + \
                         str(Values[Ix_Query_GRsel]) + '   ' + \
                         str(Values[Ix_Query_CAsel])

        TextString = Filenames + strQuery +strSelect
        self.Txt1.Set_Text(TextString)

 # ---------------------------------------------------------------------------------------
    def Top_Level_Start(self):
        Top_List = self.Data.Get_Txt_Member(Ix_TOP_ToStart)
        for Item in Top_List:
            self.Mod_Mngr.Top_Launcher(Item, MAIN_WIND, [])
            pass

    def Top_Level_Id_Create_List(self):
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_Settings,       TOP_SETTINGS])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_Mngr,           TOP_MNGR])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_View_Codes,     TOP_CODES_VIEW])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_GR_Codes_Mngr,  TOP_GR_MNGR])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_XLSX_Rows_View, TOP_XLSX_VIEW])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_Insert,         TOP_INS])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_View_Transact,  TOP_VIEW_TRANSACT])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_Queries,        TOP_QUERY])
        self.Mod_Mngr.Add_Toplevels_Id_List([Top_View_Message,   TOP_VIEW_MESS])
        pass

# ================================================================= #
#                                                                   #
if __name__ == "__main__":                                          #
    Main_WIN = Main_Window()                                        #
#                                                                   #
# ================================================================= #
