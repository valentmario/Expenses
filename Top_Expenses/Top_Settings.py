# ----------------------------------------------------------------------------------------------- #
#                           ***   Top_Settings.py   ***                                           #
#                        Settings  functions used essentially for developing                      #
# ----------------------------------------------------------------------------------------------- #

from Chat import Ms_Chat
from Widgt.Widgets import *
from Widgt.Tree_Widg import *
from Top_Expenses.Modules_Manager import Modul_Mngr
from Data_Classes.Transact_DB import *

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
    def __init__(self):
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

        self.Files_List = []
        self.Top_List = self.Data.Get_Txt_Member(Ix_TOP_ToStart)

        self.ComboList = []
        self.StrVar     = tk.StringVar()
        self.ComboList  = [TOP_SETTINGS, TOP_MNGR, TOP_CODES_VIEW, TOP_VIEW_TRANSACT,
                           TOP_GR_MNGR,  TOP_INS,  TOP_QUERY,      TOP_XLSX_VIEW, TOP_SUMMARIES]
        self.Part_Combo = TheCombo(self, self.StrVar, 20, 292, 32, 16,
                                   self.ComboList, '', self.Clk_Combo)
        self.Btn_Sel_Codes_DB  = TheButton(self, Btn_Def_En,  20, 20, 14, 'Select Codes DB file', self.Clk_Sel_Codes_DB)
        self.Btn_View_Codes    = TheButton(self, Btn_Def_En, 170, 20, 14, 'View Codes DB',        self.Clk_View_Codes_DB)

        self.Btn_Sel_xlsx_File = TheButton(self, Btn_Def_En,  20, 65, 14, 'Select xlsx File',     self.Clk_Sel_xlsx_File)
        self.Btn_View_Xlsx     = TheButton(self, Btn_Def_En, 170, 65, 14, 'View Xlsx File',    self.Clk_View_xlsx_File)

        self.Btn_Tsel_Transact  = TheButton(self, Btn_Def_En,  20, 110, 14, 'Sel transact file',self.Clk_Sel_Transact)
        self.Btn_ViewTransact   = TheButton(self, Btn_Def_En, 170, 110, 14, 'View transactions', self.Clk_View_Transact)

        self.Btn_Test_DBcodes  = TheButton(self, Btn_Def_En,  20, 155, 14, 'Check Codes DB',   self.Clk_Check_Codes_DB)
        self.Btn_View_Xlsx_Tot = TheButton(self, Btn_Def_En, 170, 155, 14, 'Summaries',        self.Clk_Summaries)

        self.Btn_Sel_Codes_DB  = TheButton(self, Btn_Def_En,  20, 200, 14, 'View Txt List',     self.Clk_View_TxtList)
        self.Btn_Sel_xlsx_File = TheButton(self, Btn_Def_En, 170, 200, 14, 'Chat Participants', self.Clk_View_Chat)

        self.Btn_TxtScroll     = TheButton(self, Btn_Def_En,  20, 245, 14, 'Files list',         self.Clk_NotUsed)
        # self.Btn_StrMatching   = TheButton(self, Btn_Def_En, 170, 245, 14, 'Strings matching',  self.Clk_Matching)
        self.TestTxt           = TheText(self, Txt_Disab,    170, 245, 14, 1, 'Text')

        self.Btn_Clear_Top     = TheButton(self, Btn_Def_En, 180, 290, 14, 'Clear',  self.Clk_Clear_Top)
        self.Exit              = TheButton(self, Btn_Def_En,  24, 335, 30, 'EXIT',   self.Call_OnClose)

    # ----------------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_SETTINGS)
        self.destroy()

    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, MAIN_WIND, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:
            self.Call_OnClose()

    # -----------------------------------------------------------------------------------
    def Clk_Sel_Codes_DB(self):
        if self.Mod_Mngr.Sel_Codes():
            self.Mod_Mngr.Load_Codes()

    def Clk_View_Codes_DB(self):
        # self.Mod_Mngr.Top_Launcher(TOP_MNGR)
        self.Mod_Mngr.Top_Launcher(TOP_CODES_VIEW)
        # self.Mod_Mngr.Top_Launcher(TOP_GR_MNGR)

    # -----------------------------------------------------------------------------------
    def Clk_Sel_xlsx_File(self):
        self.Mod_Mngr.Sel_Xlsx()

    def Clk_View_xlsx_File(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW)

    # ------------------------------------------------------------------------------------
    def Clk_Sel_Transact(self):
        self.Mod_Mngr.Sel_Transact()

    # ------------------------------------------------------------------------------------
    def Clk_View_Transact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT)

    # -----------------------------------------------------------------------------------
    def Clk_Summaries(self):
        self.Mod_Mngr.Top_Launcher(TOP_SUMMARIES)

    # ------------------------------------------------------------------------------------
    def Clk_View_Chat(self):
        self.Chat.View_Partic()

    def Clk_View_TxtList(self):
        Total = self.Data.Get_Total_Rows()
        Queries_List = self.Data.Get_Txt_Member(Ix_Query_List)
        Files_Status = self.Mod_Mngr.Get_Files_Loaded_Status()
        strText = ''
        strText +=     '-------------  Codes DB  -----------------\n'
        strText += self.Data.Get_Txt_Member(Ix_Codes_File)
        strText += '\n\n------------   Xlsx file  ----------------\n'
        strText += self.Data.Get_Txt_Member(Ix_Xlsx_File)
        strText += '\n\n-----------  Transactions DB  ------------\n'
        strText += self.Data.Get_Txt_Member(Ix_Transact_File)
        strText += '\n\n----------  Files status  ----------------\n'
        strText +=  Files_Status[0] + '   ' + Files_Status[1] + '   ' + Files_Status[2]

        strText += '\n\n----------  Xlsx total rows   -------------\n'
        strText +=   'Total rows OK ...  ' + str(Total[Ix_Tot_OK])
        strText += '\nTotal with-code .. ' + str(Total[Ix_Tot_WithCode])
        strText += '\nTotal without-code ' + str(Total[Ix_Tot_Without_Code])

        strText += '\n\n---  Queries  selections  -----------------'
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
        self.Data.Update_Txt_File(self.Top_List, Ix_TOP_ToStart)
        self.Part_Combo.SetSelText('')

    def Clk_Combo(self, Val):
        self.Top_List.append(Val)
        self.Data.Update_Txt_File(self.Top_List, Ix_TOP_ToStart)

    # --------------------------------------------------------------------------------------
    def Clk_Check_Codes_DB(self):
        Result = self.Data.Check_Codesdatabase()
        if Result[0] == OK:
            Mess = Message_Dlg(MsgBox_Info, Result[1])
        else:
            Mess = Message_Dlg(MsgBox_Err, Result[1])
        Mess.wait_window()

    # ----------------------------------------------------------------------------------------
    # def Clk_NotUsed(self):
    #     # self.TestTxt.PosXY(190, 245)
    #     self.TestTxt.PosX(190)
    #     pass


    def Clk_NotUsed(self):
        Directory = '/media/mario/ACEext4/ACEext4/12_Expenses/bFiles/bXLSX_Files/TRANSACTIONS/'
        self.Files_List = os.listdir(Directory)

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
