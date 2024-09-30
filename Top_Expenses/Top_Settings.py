# ----------------------------------------------------------------------------------------------- #
#                           ***   Top_Settings.py   ***                                           #
#                        Settings  functions used essentially for developing                      #
# ----------------------------------------------------------------------------------------------- #

from Widgt.Tree_Widg import *
from Widgt.Dialogs import *
from Top_Expenses.Modules_Manager import Modul_Mngr
from Data_Classes.Transact_DB import *

# class Top_Settings(tk.Toplevel): see line 85
# ================================================================================================
class Top_String_Matching(tk.Toplevel):
    def __init__(self):
        super().__init__()

        self.resizable(False, False)
        self.configure(background=BakGnd)
        self.title('***   Find  strings  matchings   ***')
        self.geometry('950x730+10+10')

        # -----------   Matchings frame   ---------------------------------------------------------
        self.Frame_Matchings = TheFrame(self, 10, 10, self.Clk_OnTree_Match)
        self.Frame_Matchings_Setup()
        self.Frame_Matchings.Frame_View()

        self.StringToMatch  = 'BANC'
        self.Matchings_List = []

        self.Txt_StrToMatch = TheText(self, Txt_Enab, 10, 680, 35, 1, 'BANC')
        self.Text1 = TheText(self, Txt_Disab,  10, 580, 35, 2, '')
        self.Text2 = TheText(self, Txt_Disab, 320, 580, 75, 4, '')

        TheButton(self, Btn_Def_En, 320, 680, 18, '  Find matchings ', self.View_Matchings)
        TheButton(self, Btn_Def_En, 810, 680, 12, '  E X I T   ',      self.Call_OnClose)

    # --------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.destroy()

    # --------------------------  T R E E   Matchings       --------------------------------------
    def Frame_Matchings_Setup(self):
        Nrows = 25
        nColToVis = 2
        Headings  = ['#0', 'StringToSearc', 'Transactions full description matchings']
        Anchor    = ['c',  'w',             'w']
        Width = [0, 250, 650]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_Matchings.Tree_Setup(Form_List)
        self.Frame_Matchings.Load_Row_Values([])

    # --------------------------------------------------------------------------------------------
    def Clk_OnTree_Match(self, Values):
        self.Text1.Set_Text(Values[0])
        self.Text2.Set_Text(Values[1])

    # --------------------------------------------------------------------------------------------
    def View_Matchings(self):
        self.Text1.Set_Text('')
        self.Text2.Set_Text('')
        StrToMach = self.Txt_StrToMatch.Get_Text('ASCII').replace('\n', '')
        if not StrToMach:
            self.Frame_Matchings.Load_Row_Values([])
        else:
            self.Matchings_List = []
            StrToMach = self.Txt_StrToMatch.Get_Text('ASCII').replace('\n', '')

            for Rec in Data.Get_Codes_Table():  # Get_Codes_Table():
                StrToSerch =  Rec[iTR_TRserc].replace('\n', '', 5)
                FullDesc   = Rec[iTR_TRfullDes].replace('\n', '', 5)
                if StrForSearc_in_Fulldescr(StrToMach, FullDesc):
                    self.Matchings_List.append([StrToSerch, FullDesc])
                if Rec[iTR_TRcode] == 9999:
                    pass
            if not self.Matchings_List:     # [['StringToSearch', 'StringFullDesc'], ..]
                self.Matchings_List.append(['NONE', 'NONE'])
            self.Frame_Matchings.Load_Row_Values(self.Matchings_List)

# =================================================================================================
class Top_Settings(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data
        self.Mod_Mngr = Modul_Mngr
        self.Chat.Attach([self, TOP_SETTINGS])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry(Settings_geometry)
        self.configure(background=BakGnd)
        self.title('*****     Settings     *****')

        self.Data_List  = List
        self.Dummy      = 0
        self.Files_List = []
        self.Top_List = self.Data.Get_Selections_Member(Ix_TOP_ToStart)

        self.ComboList      = []
        self.StrVar         = tk.StringVar()
        self.ComboList      = [TOP_SETTINGS, TOP_MNGR, TOP_CODES_VIEW, TOP_VIEW_TRANSACT,
                               TOP_GR_MNGR,  TOP_INS,  TOP_QUERY,      TOP_XLSX_VIEW]
        self.Part_Combo = TheCombo(self, self.StrVar, 20, 292, 32, 15,
                                   self.ComboList, '', self.Clk_Combo)
        self.Btn_Sel_Codes_DB  = TheButton(self, Btn_Def_En,  20, 20, 14, 'Select Codes DB file', self.Clk_Sel_Codes_DB)
        self.Btn_View_Codes    = TheButton(self, Btn_Def_En, 170, 20, 14, 'Show Codes DB',        self.Clk_View_Codes_DB)

        self.Btn_Sel_xlsx_File = TheButton(self, Btn_Def_En,  20, 65, 14, 'Select xlsx File',  self.Clk_Sel_xlsx_File)
        self.Btn_View_Xlsx     = TheButton(self, Btn_Def_En, 170, 65, 14, 'Show Xlsx File',   self.Clk_View_xlsx_File)

        self.Btn_Tsel_Transact  = TheButton(self, Btn_Def_En,  20, 110, 14, 'Sel transact file',self.Clk_Sel_Transact)
        self.Btn_ViewTransact   = TheButton(self, Btn_Def_En, 170, 110, 14, 'Show transactions',self.Clk_View_Transact)

        self.Btn_Test_DBcodes  = TheButton(self, Btn_Def_En,  20, 155, 14, 'Check Codes DB',   self.Clk_Check_Codes_DB)
        self.Btn_View_Xlsx_Tot = TheButton(self, Btn_Def_En, 170, 155, 14, 'Show messages',    self.Clk_View_Msg)

        self.Btn_Sel_Codes_DB  = TheButton(self, Btn_Def_En,  20, 200, 14, 'Show selections', self.Clk_View_Selections)
        self.Btn_Sel_xlsx_File = TheButton(self, Btn_Def_En, 170, 200, 14, 'Chat Participants', self.Clk_View_Chat)

        self.Btn_TxtScroll     = TheButton(self, Btn_Def_En,  20, 245, 14, 'for test',         self.Clk_NotUsed)
        # self.Btn_StrMatching   = TheButton(self, Btn_Def_En, 170, 245, 14, 'Strings matching',  self.Clk_Matching)
        self.TestTxt           = TheText(self, Txt_Disab,    170, 248, 16, 1, 'Text')

        self.Btn_Clear_Top     = TheButton(self, Btn_Def_En, 170, 290, 14, 'Clear',  self.Clk_Clear_Top)
        self.Exit              = TheButton(self, Btn_Def_En,  24, 335, 30, 'EXIT',   self.Call_OnClose)

    # ----------------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_SETTINGS)
        self.destroy()

    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, MAIN_WIND, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:
            self.Call_OnClose()
        # elif Request_Code == SOMETHING:
        #   pass

    # -----------------------------------------------------------------------------------
    def Clk_Sel_Codes_DB(self):
        self.Dummy = 0
        self.Mod_Mngr.Sel_Codes(TOP_SETTINGS)
        pass

    def Clk_View_Codes_DB(self):
        self.Mod_Mngr.Top_Launcher(TOP_CODES_VIEW, TOP_SETTINGS, [])

    # -----------------------------------------------------------------------------------
    def Clk_Sel_xlsx_File(self):
        self.Mod_Mngr.Sel_Xlsx(TOP_MNGR)


    def Clk_View_xlsx_File(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_SETTINGS, [])

    # ------------------------------------------------------------------------------------
    def Clk_Sel_Transact(self):
        self.Mod_Mngr.Sel_Transact(TOP_SETTINGS)
        pass

    # ------------------------------------------------------------------------------------
    def Clk_View_Transact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT, TOP_SETTINGS, [])

    # -----------------------------------------------------------------------------------
    @classmethod
    def Clk_View_Msg(cls):
        Top_View_Message(['IL MIO MESSAGGIO\n1\n2\n3\n4'])


    # ------------------------------------------------------------------------------------
    def Clk_View_Chat(self):
        self.Chat.View_Partic()

    # ------------------------------------------------------------------------------------
    @classmethod
    def Val_Check(cls, Value):
        if Value is None:
            return NONE
        else:
            return str(Value)

    def Get_Ident(self):
        # [self._Xlsx_Conto, self._Xlsx_Year, self._Xlsx_Month, self._Transact_Year]
        Files_Ident   = self.Data.Get_Xlsx_Transact_Ident()
        Xlsx_Conto    = self.Val_Check(Files_Ident[Ix_Xlsx_Conto])
        Xlsx_Year     = self.Val_Check(Files_Ident[Ix_Xlsx_Year])
        Xlsx_Month    = self.Val_Check(Files_Ident[Ix_Xlsx_Month])
        Transact_Year = self.Val_Check(Files_Ident[Ix_Transact_Year])
        return [Xlsx_Conto, Xlsx_Year, Xlsx_Month, Transact_Year]

    # ------------------------------------------------------------------------------------
    def Clk_View_Selections(self):
        Total = [0, 0, 0]
        if self.Data.Get_Files_Loaded_Stat(Ix_Xlsx_Lists_Loaded):
            Total = self.Data.Get_Total_Rows()
        Queries_List = self.Data.Get_Selections_Member(Ix_Query_List)
        Files_Status = []
        for Index in range (0, 4):
            Stat = self.Data.Get_Files_Loaded_Stat(Index)
            strStat = LOADED
            if not Stat:
                strStat = 'Not Loaded'
            Files_Status.append(strStat)
        strStat1 = Files_Status[0]
        strStat2 = Files_Status[1]
        strStat3 = Files_Status[2]
        strStat4 = Files_Status[3]

        strText = ''
        strText +=     '-------------  Codes DB  -----------------\n'
        strText += self.Data.Get_Selections_Member(Ix_Codes_File)
        strText += '\n\n------------   Xlsx file  ----------------\n'
        strText += self.Data.Get_Selections_Member(Ix_Xlsx_File)
        strText += '\n\n-----------  Transactions DB  ------------\n'
        strText += self.Data.Get_Selections_Member(Ix_Transact_File)
        strText += '\n\n----------  Files status  ----------------\n'
        strText += strStat1 + '  ' + strStat2 + '  ' + strStat3 + '  ' + strStat4

        # [self._Xlsx_Conto, self._Xlsx_Year, self._Xlsx_Month, self._Transact_Year]
        Str = self.Get_Ident()
        strText += '\n\n--------  Xlsx Transactions  ident -------\n'
        strText += Str[0] + '   ' + Str[1] + '   ' + Str[2] + '   ' + Str[3]

        strText += '\n\n----------  Xlsx total rows   -------------\n'
        strText +=   'Total rows OK ...  ' + str(Total[Ix_Tot_OK])
        strText += '\nTotal with-code .. ' + str(Total[Ix_Tot_WithCode])
        strText += '\nTotal without-code ' + str(Total[Ix_Tot_Without_Code])

        TransactYear = str(self.Data.Get_TransacYear())
        strText += '\n\n---  Queries  selections  -----------------'
        strText +=   '\nQuery Year:       ' + TransactYear
        strText +=   '\nQuery Conto:      ' + Queries_List[Ix_Query_Conto]
        strText +=   '\nQuery month:      ' + Queries_List[Ix_Query_Month]
        strText +=   '\nQuery tot months: ' + Queries_List[Ix_Query_TotMonths]
        strText += '\n\nTR selected:  ' + Queries_List[Ix_Query_TRsel]
        strText +=   '\nGR selected:  ' + Queries_List[Ix_Query_GRsel]
        strText +=   '\nCA selected:  ' + Queries_List[Ix_Query_CAsel]

        strStart = '\n\n------  Toplevel to start  ----------------\n'
        for Top in self.Top_List:
            strStart += Top + '\n'
        strText += strStart
        Msg = Message_Dlg(MsgBox_Info, strText)
        Msg.wait_window()

    def Clk_Clear_Top(self):
        self.Top_List = []
        self.Data.Update_Selections(self.Top_List, Ix_TOP_ToStart)
        self.Part_Combo.SetSelText('')

    def Clk_Combo(self, Val):
        self.Top_List.append(Val)
        self.Data.Update_Selections(self.Top_List, Ix_TOP_ToStart)

    # --------------------------------------------------------------------------------------
    def Clk_Check_Codes_DB(self):
        self.Mod_Mngr.Check_Codes_Db()

    # ----------------------------------------------------------------------------------------
    def Clk_NotUsed(self):
        self.Dummy = 0
        # self.TestTxt.PosXY(190, 245)
        # self.TestTxt.PosX(190)
        File_Dlg    = File_Dialog(FileBox_Codes)
        # File_Dlg.wait_window()
        FileSelected = File_Dlg.FileName
        print(FileSelected)
        pass


    # ----------------------------------------------------------------------------------------
    @staticmethod
    def Clk_Matching():
        Top_String_Matching()

    # ------------------------------------------------------------------------------------------
    def Get_Match_List(self, Match_String):
        Search_Match_list  = []
        FullDesc_Mach_List = []
        for Rec in self.Data.Get_Codes_Table():
            TRsearch = Rec[iTR_TRserc]
            FullDesc = Rec[iTR_TRfullDes]
            if Match_String in TRsearch:
                pass
            if Match_String in FullDesc:
                NoLF_str = FullDesc.replace('\n', '', -1)
                found = NoLF_str + '\n'
                FullDesc_Mach_List.append(found)
        return [Search_Match_list, FullDesc_Mach_List]
        pass
# ==============================================================================================================
