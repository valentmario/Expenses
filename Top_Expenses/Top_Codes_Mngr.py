# ---------------------------------------------------------------------------------- #
#                  *****     Top_Codes_Mngr.py     *****                             #
#                    VIEW  DELETE  ADD  UPDATE   Code                                #
#      List_Rows_WithoutCode : nRow    Date      FullDesc                            #
#      List View Codes       : TRcode  TR_Desc   GR_Desc  CA_Desc  StrToSearch       #
# ---------------------------------------------------------------------------------- #

from Common.Common_Functions import *
from Top_Expenses.Modules_Manager import Modul_Mngr
from Top_Expenses.Super_Top_Codes_Mngr import Super_Top_Mngr

from Widgt.Dialogs import Print_Received_Message
from Widgt.Dialogs import Message_Dlg
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheText
from Widgt.Widgets import TheCombo

# -------------------------------------------------------------------------------------------------
class Top_Mngr(Super_Top_Mngr):
    def __init__(self):
        super().__init__()
        self.Mod_Mngr = Modul_Mngr

        self.Scroll_Txt = None
        # ----------------------   Frames   -------------------------------------------------------
        self.Frame_NoCodes = TheFrame(self, 10, 20, self.Clk_OnTree_NoCodes)
        self.Frame_NoCodes_Setup()
        self.Frame_NoCodes.Frame_View()
        self.View_Without_Code = True

        self.Frame_WithCodes = TheFrame(self, 10, 20, self.Clk_OnTree_WithCodes)
        self.Frame_WithCodes_Setup()

        # --------------------------- Group Select Combo  -----------------------------------------
        self.ComboList = []
        for Rec in self.Data.GR_Codes_Ordered:
            self.ComboList.append(Rec[iGR_GRdesc])
        self.GR_Combo  = TheCombo(self, self.StrVar, 60, 776, 32, 21,
                                  self.ComboList, 'Select  Group', self.Clk_Combo)

        # --------------------------------------  TEXT Boxes  -------------------------------------
        self.Txt_StrFullDesc = TheText(self, Txt_DisBlak,280, 680, 44, 4, '')
        self.Txt_StrToSerc   = TheText(self, Txt_Enab,    10, 680, 31, 2, '')
        self.Txt_TR_Desc     = TheText(self, Txt_Enab,    60, 734, 25, 1, '')
        self.Txt_TR_Code     = TheText(self, Txt_DisBlak, 10, 734,  4, 1, 0)

        self.Txt_GR_Code     = TheText(self, Txt_DisBlak, 10, 776,  4, 1, 0)
        self.Txt_CA_Code     = TheText(self, Txt_DisBlak, 10, 816,  4, 1, 0)
        self.Txt_CAdesc      = TheText(self, Txt_DisBlak, 62, 816, 25, 1, 'Category')

        # ----------------------------------    B U T T O N S     ---------------------------------
        self.BtnDel    = TheButton(self, Btn_Def_En,  286, 772, 18, 'Delete Last Record', self.Clk_Delete_Record)
        self.BtnAddNew = TheButton(self, Btn_Def_En, 286, 815, 18, 'Add New Record',     self.Clk_Add_New_Record)

        self.BtnUpdate = TheButton(self, Btn_Def_Dis, 474, 772, 17, 'Update Code', self.Clk_Update_Record)

        self.BtnSelCodes= TheButton(self, Btn_Def_En, 60, 860, 22, 'Select Codes DB ', self.Clk_Sel_Codes)
        self.BtnView = TheButton(self, Btn_Def_En,    60, 900, 22, 'View Transact Codes', self.Clk_View_Codes)
        self.BtnSelDB  = TheButton(self, Btn_Def_En,  60, 940, 22, 'Groups Codes',     self.Clk_GR_Mngr)
        self.BtnSelDB  = TheButton(self, Btn_Def_En, 286, 940, 18, 'Check codes DB',   self.Clk_Ceck_Codes_DB)

        self.BtnSelXls = TheButton(self, Btn_Def_En, 286, 860, 18, 'Select Xlsx file', self.Clk_Sel_xlsx)
        self.BtnView   = TheButton(self, Btn_Def_En, 286, 900, 18, 'View Xlsx Rows',   self.Clk_View_Xlsx)
        self.BtnVWithC = TheButton(self, Btn_Def_En, 474, 860, 18, 'View with-hout codes', self.Clk_View_Rows)
        self.BtnExit   = TheButton(self, Btn_Def_En,   474, 940, 18, 'E X I T ', self.Call_OnClose)

        self.Load_Trees()
        self.geometry(Top_Mngr_geometry)

    # ------------------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:
            self.Call_OnClose()
        elif Request_Code == CODE_CLK_ON_TR_CODES:  # Clicked on Codes Tree [TRcode]
            TRcode = Values_List[0]
            self.Reqst_Clkd_On_TRcode(TRcode)
        elif Request_Code == CODES_DB_UPDATED or \
                Request_Code == XLSX_UPDATED:   # Codes dat
            # self.Data.Load_Xlsx_Lists()
            self.Mod_Mngr.Load_Xlsx()
            self.Load_Trees()

    # --------------------------  T R E E     Without  Codes   ------------------------------------
    def Frame_NoCodes_Setup(self):
        Nrows     = 30
        nColToVis = 3
        Headings  = ['#0', 'nRow', 'Date', 'Full Description']
        Anchor    = ['c', 'c', 'c', 'w']
        Width     = [0, 60, 80, 470]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_NoCodes.Tree_Setup(Form_List)

    def Clk_OnTree_NoCodes(self, Values):
        self.Frame_WithCodes.Clear_Focus()
        self.Chat.Tx_Request([TOP_MNGR, [ANY], CODE_CLEAR_FOCUS, []])
        self.Clicked_Mod_Code = 1
        self.Clear_Texts()
        self.Set_Row_Without_Code(Values)
        myList = [Values[1], Values[2]]
        self.Chat.Tx_Request([ TOP_MNGR, [TOP_XLSX_VIEW], CODE_CLIK_ON_XLSX, myList ])

    # --------------------------  T R E E     With  Codes   ---------------------------------------
    def Frame_WithCodes_Setup(self):
        self.Frame_WithCodes.Frame_Title('  ')
        Nrows     = 30
        nColToVis = 7
        Headings = ['#0',  'Row ',  'Contab ', 'Valuta ', 'Description',  'Accred ', 'Addeb ', 'Code ']
        Anchor   = ['c',   'w',     'c',       'c',       'w',            'e',       'e',      'c'    ]
        Width    = [ 0,     50,      80,        90,        190,            70,        70,       50    ]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_WithCodes.Tree_Setup(Form_List)

    def Clk_OnTree_WithCodes(self, Values):
        #  nRow    Date   Descrip   Accred   Addeb   TRcode
        self.Frame_NoCodes.Clear_Focus()
        self.Chat.Tx_Request([TOP_MNGR, [ANY,], CODE_CLEAR_FOCUS, []])
        nRow      = int(Values[iWithCode_nRow])
        Date      = ' '  # Values[iWithCode_Date]
        TRcode    = int(Values[iWithCode_TRcode])
        self.View_Descr_Text(TRcode, self.GR_Combo)
        self.Clicked_Mod_Code = 2
        self.Set_State_Butt_New_Updt('disabled', 'normal')
        self.Chat.Tx_Request([TOP_MNGR, [TOP_XLSX_VIEW], CODE_CLIK_ON_XLSX, [nRow, Date] ])
        self.Chat.Tx_Request([TOP_MNGR, [TOP_XLSX_VIEW, TOP_GR_MNGR], CODE_CLK_ON_TR_CODES, [TRcode] ])

    # ---------------------------------------------------------------------------------------------
    def Load_Trees(self):
        Total = self.Data.Get_Total_Rows()
        XlsxFilename = Get_File_Name(self.Data.Get_Txt_Member(Ix_Xlsx_File))

        Title = "  " + XlsxFilename + " :      " + str(Total[Ix_Tot_Without_Code]) + "  Transactions without code  ...  "
        Title += str(Total[Ix_Tot_WithCode])  + "  with code   "
        self.Frame_NoCodes.Frame_Title(Title)

        Title = "   " + XlsxFilename + " :      " + str(Total[Ix_Tot_WithCode]) + "  Transactions with code  ...    "
        Title += str(Total[Ix_Tot_Without_Code]) + "  whithout code   "
        self.Frame_WithCodes.Frame_Title(Title)

        if Total[Ix_Tot_Without_Code] == 0:
            self.View_Without_Code = False
            self.Frame_WithCodes.Frame_View()
            self.Frame_NoCodes.Frame_Hide()
        else:
            self.View_Without_Code = True
            self.Frame_WithCodes.Frame_Hide()
            self.Frame_NoCodes.Frame_View()

        #    nRow Date  Descr
        self.Frame_NoCodes.Load_Row_Values(self.Data.Get_WithoutCodeList())
        #    nRow Contab Valuta  TRdesc  Accred Addeb TRcode
        self.Frame_WithCodes.Load_Row_Values(self.Data.Get_WithCodeList())

    # ---------------------------------------------------------------------------------------------
    def Frames_Refresh(self):
        self.Mod_Mngr.Load_Xlsx(TOP_MNGR)
        self.Load_Trees()
        if self.View_Without_Code:
            self.Frame_NoCodes.Frame_View()
            self.Frame_WithCodes.Frame_Hide()
        else:
            self.Frame_NoCodes.Frame_Hide()
            self.Frame_WithCodes.Frame_View()


    # ---------------------------------------------------------------------------------------------
    def Clk_View_Codes(self):
        self.Mod_Mngr.Top_Launcher(TOP_CODES_VIEW, TOP_MNGR)

    # ---------------------------------------------------------------------------------------------
    def Clk_GR_Mngr(self):
        self.Mod_Mngr.Top_Launcher(TOP_GR_MNGR, TOP_MNGR)

    # ---------------------------------------------------------------------------------------------
    def Clk_View_Rows(self):
        if not self.View_Without_Code:
            self.Frame_NoCodes.Frame_View()
            self.Frame_WithCodes.Frame_Hide()
            self.View_Without_Code = True
        else:
            self.Frame_NoCodes.Frame_Hide()
            self.Frame_WithCodes.Frame_View()
            self.View_Without_Code = False

    # ---------------------------------------------------------------------------------------------
    def Clk_Sel_Codes(self):
        self.Mod_Mngr.Sel_Codes(TOP_MNGR)

    # ---------------------------------------------------------------------------------------------
    def Clk_Sel_xlsx(self):
        if self.Mod_Mngr.Sel_Xlsx(TOP_MNGR):
            self.Mod_Mngr.Load_Xlsx(TOP_MNGR)

    # ---------------------------------------------------------------------------------------------
    def Clk_View_Xlsx(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_MNGR)

    # ---------------------------------------------------------------------------------------------
    def Reqst_Clkd_On_TRcode(self, TRcode):
        if self.Mod_Mngr.Files_Loaded != LOADED:
            self.View_Descr_Text(TRcode, self.GR_Combo)
            self.Clicked_Mod_Code = 2
            self.BtnUpdate.Set_Btn_State(Btn_Enab)
            return
        self.Frame_WithCodes.Clear_Focus()
        self.Clear_Texts()
        Index = -1
        TrCodInt = int(TRcode)
        self.Load_Trees()
        WithList = self.Data.Get_With_Code_Tree_List
        for Rec in WithList:
            Index += 1
            if Rec[iWithCode_TRcode] == TrCodInt:
                self.Frame_WithCodes.Set_List_For_Focus(Index)
                break
        self.View_Descr_Text(TRcode, self.GR_Combo)
        self.Clicked_Mod_Code = 2
        self.Set_State_Butt_New_Updt('disabled', 'normal')

    # -------------------------------------------------------------------------------------------------
    def Clear_Texts(self):
        self.Clear_Only_Text_Widg()
        self.Txt_CAdesc.Set_Text("Category")
        self.GR_Combo.SetSelText('Select Group')

    # -------------------------------------------------------------------------------------------------
    def Set_Row_Without_Code(self, Values):  # nRow, Data_Valuta Full_Description
        self.Frame_NoCodes.Clear_Focus()
        self.Frame_WithCodes.Clear_Focus()
        nRow = int(Values[0])  # Row number + Date is Unic
        Date = str(Values[1])
        Descr = Values[2]
        Index = - 1
        Without_Recs = self.Data.Get_WithoutCodeList()
        for Rec in Without_Recs:     # Wihtout_Code_Tree_List:
            Index += 1
            if Rec[0] == nRow and Rec[1] == Date:
                self.Frame_NoCodes.Set_Focus(Index)
                self.Clicked_Mod_Code = 1
                self.Clear_Texts()
                #                     nRow              Date           Full Description
                Full_Desc = 'nRow=' + str(nRow) + '  ' + Date + '-' + Descr
                self.Txt_StrFullDesc.Set_Text(Full_Desc)
                NewCode = self.Data.Get_New_Code()
                self.Txt_TR_Code.Set_Text(str(NewCode[0]))
                self.Set_State_Butt_New_Updt('normal', 'disabled')
                break

    # -----------------    Enable Disable Buttons  New / Update Code   ------------------
    def Set_State_Butt_New_Updt(self, StateNew, StateUpdt):
        self.BtnAddNew.configure(state=StateNew)
        self.BtnUpdate.configure(state=StateUpdt)

    # ------------------------     ***   Delete  the last TR Record      --------------------------
    def Clk_Delete_Record(self):
        Result = self.Delete_Code_Record()
        if Result == OK:
            Msg = Message_Dlg(MsgBox_Info, 'Code has correctly deleted')
            Msg.wait_window()
            self.Frames_Refresh()
            self.Chat.Tx_Request([TOP_MNGR, [ANY], CODES_DB_UPDATED, []])
        elif Result == NONE:
            pass
        else:
            Msg = Message_Dlg(MsgBox_Err, Result)
            Msg.wait_window()


    # ------------------------     ***   Add new code Record  the last TR Record      -------------
    def Clk_Add_New_Record(self):
        if self.Clicked_Mod_Code != 1:
            Msg_Dlg = Message_Dlg(MsgBox_Info, 'please setup:\n Transaction\nand Group data')
            Msg_Dlg.wait_window()
            return
        else:
            Result = self.Add_Record_Code()
            if Result == OK:
                Msg = Message_Dlg(MsgBox_Info, 'Code has correctly added')
                Msg.wait_window()
                self.Frames_Refresh()
                self.Chat.Tx_Request([TOP_MNGR, [ANY], CODES_DB_UPDATED, []])
            elif Result == NONE:
                pass
            else:
                Msg = Message_Dlg(MsgBox_Err, Result)
                Msg.wait_window()

    # ------------------------     ***   Update TR code Record      -------------------------------
    def Clk_Update_Record(self):
        if self.Clicked_Mod_Code != 2:
            Msg_Dlg = Message_Dlg(MsgBox_Info, 'Insert data')
            Msg_Dlg.wait_window()
            return
        else:
            self.Set_State_Butt_New_Updt('disabled', 'disabled')
            Result = self.Update_Record_Code()
            if Result == OK:
                Msg = Message_Dlg(MsgBox_Info, 'Code  correctly updated')
                Msg.wait_window()
                self.Frames_Refresh()
                self.Chat.Tx_Request([TOP_MNGR, [ANY], CODES_DB_UPDATED, []])
            elif Result == NONE:
                pass
            else:
                Msg = Message_Dlg(MsgBox_Err, Result)
                Msg.wait_window()

    # ---------------------------------------------------------------------------------------------
    def Clk_Ceck_Codes_DB(self):
        Multiple = self.Data.Check_Codesdatabase()
        if not Multiple:
            Len = self.Data.Get_TR_Codes_Table_Len()
            Info = str(Len)  + '   code records correctly checked out'
            Message = Message_Dlg(MsgBox_Info, Info)
        else:
            Info = 'ERROR on checking out codes database\n\n'
            for TRrecord in Multiple:
                StrToserch = TRrecord[iTR_TRserc]
                FullDescr  = TRrecord[iTR_TRfullDes]
                Info += StrToserch + '\n' + FullDescr +'\n\n'
            Message = Message_Dlg(MsgBox_Err, Info)
        Message.wait_window()
        pass

# ==============================================================================================================
