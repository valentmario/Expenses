# ================================================================================= #
#                  *****     Top_XLSX_Rows_View.py     *****                        #
# XLS_Row_List : nRow  Contab  Valuta  Descr1  Accred  Addeb  Descr2                #
# ================================================================================= #

import tkinter as tk
from Common.Common_Functions import *
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data

from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheTextPoints

from Top_Expenses.Modules_Manager import Modul_Mngr

class Top_XLSX_Rows_View(tk.Toplevel):
    def __init__(self, Result, Param_List):
        super().__init__()
        self.Chat = Ms_Chat
        self.Data = Data
        self.Mod_Mngr = Modul_Mngr

        self.Chat.Attach([self, TOP_XLSX_VIEW])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry(Top_Xlsx_View_geometry)
        self.title('***   View Sheet Rows xlsx file   *** ')
        self.configure(background=BakGnd)

        self.Result     = Result
        self.Param_List = Param_List

        self.Txt1 = TheTextPoints(self, Txt_Disab,  20, 860, 33, 4, '', 11)
        self.Txt2 = TheTextPoints(self, Txt_Disab, 310, 860, 60, 4, '', 11)
        TheButton(self, Btn_Def_En, 640, 950, 16, 'E X I T ', self.Call_OnClose)

        # --------------------------   Create Treeview Frame   ------------------------------------
        self.Frame_Sheet_Rows = TheFrame(self, 20, 20, self.Clk_On_Sheets_Row)
        self.Frame_Sheets_Rows_Setup()
        self.Frame_Sheet_Rows.Frame_View()

    # ---------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_XLSX_VIEW)
        self.destroy()
    # ---------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:
            self.Call_OnClose()
        elif Request_Code == XLSX_UPDATED or Request_Code == UPDATE_FILES_NAME:
            self.Frame_Sheets_Rows_View()


    # ---------------------------------------------------------------------------------------------
    def Clk_On_Sheets_Row(self, Values):
        self.Txt1.Set_Text(Values[iRow_Descr1])
        self.Txt2.Set_Text(Values[iRow_Descr2])

    # ---------------------------------------------------------------------------------------------
    def Frame_Sheets_Rows_Setup(self):
        nRows      = 39
        NcolToDisp = 7
        Headings = ['#0', 'Row', "Contab", "Valuta", "Descrizione 1",
                    "Accrediti", "Addebiti", "Descrizione 2"]
        Anchor = ['c', 'c', 'c', 'c', 'w', 'e', 'e', 'w']
        Width  = [0,    40,  80,  80,  160, 70,  70,  250]
        Form_List = [nRows, NcolToDisp, Headings, Anchor, Width]
        self.Frame_Sheet_Rows.Tree_Setup(Form_List)
        self.Frame_Sheets_Rows_View()

    def Frame_Sheets_Rows_View(self):
        XLS_Name  = Get_File_Name(self.Data.Get_Selections_Member(Ix_Xlsx_File))
        FrameText = ('     ' + XLS_Name + ':   ')
        Total = self.Data.Get_Total_Rows()
        FrameText += str(Total[Ix_Tot_OK]) + '  correct transactions   '
        FrameText += str(Total[Ix_Tot_Without_Code]) + '  without code  '

        self.Frame_Sheet_Rows.Frame_Title(FrameText)
        Rows_List = self.Data.Get_X()
        pass
        self.Frame_Sheet_Rows.Load_Row_Values(Rows_List)

    # ---------------------------------------------------------------------------------------------
    def Set_Focus_On_Row(self, Values):
        nRow = int(Values[0])
        Date = Values[1]
        Index = -1
        for Rec in self.Frame_Sheet_Rows.Loaded_List:
            Index +=1
            if Rec[iRow_nRow] == nRow:
                myDate = Rec[iRow_Valuta]
                if myDate == Date:
                    self.Frame_Sheet_Rows.Set_List_For_Focus(Index)
                    self.Txt1.Set_Text(Rec[iRow_Descr1])
                    self.Txt2.Set_Text(Rec[iRow_Descr2])
                    break

# =================================================================================================
