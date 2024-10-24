# ---------------------------------------------------------------------------------- #
#                  *****     Top_Codes_Mngr.py     *****                             #
#                    VIEW  DELETE  ADD  UPDATE   Codes                               #
#      List_Rows_WithoutCode : nRow    Date      FullDesc                            #
#      List View Codes       : TRcode  TR_Desc   GR_Desc  CA_Desc  StrToSearch       #
# ---------------------------------------------------------------------------------- #

from Top_Expenses.Modules_Manager import Modul_Mngr
from Top_Expenses.Super_Top_Codes_Mngr import Super_Top_Mngr

from Widgt.Dialogs import *
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheText
from Widgt.Widgets import TheCombo

# -------------------------------------------------------------------------------------------------
class Top_Codes_Mngr(Super_Top_Mngr):
    def __init__(self, List):
        super().__init__()
        self.Mod_Mngr = Modul_Mngr
        self.List     = List
        self.Dummy    = 0

        # ----------------------   Frames   -------------------------------------------------------
        self.Frame_NoCodes = TheFrame(self, 10, 20, self.Clk_OnTree_NoCodes)
        self.Frame_NoCodes_Setup()
        self.Frame_NoCodes.Frame_View()
        self.View_Without_Code = True
        self.View_Type         = VIEW_ALPHAB

        self.Frame_WithCodes = TheFrame(self, 10, 20, self.Clk_OnTree_WithCodes)
        self.Frame_WithCodes_Setup()

        # --------------------------- Group Select Combo  -----------------------------------------
        self.ComboList = []
        self.GR_Combo  = TheCombo(self, self.StrVar, 60, 776, 32, 23,
                                  [], 'Select  Group', self.Clk_Combo)
        # --------------------------------------  TEXT Boxes  -------------------------------------
        self.Txt_StrFullDesc = TheText(self, Txt_DisBlak,280, 680, 44, 4, '')
        self.Txt_StrToFind   = TheText(self, Txt_Enab,    10, 680, 31, 2, '')
        self.Txt_TR_Desc     = TheText(self, Txt_Enab,    60, 734, 25, 1, '')
        self.Txt_TR_Code     = TheText(self, Txt_DisBlak, 10, 734,  4, 1, 0)

        self.Txt_GR_Code     = TheText(self, Txt_DisBlak, 10, 776,  4, 1, 0)
        self.Txt_CA_Code     = TheText(self, Txt_DisBlak, 10, 816,  4, 1, 0)
        self.Txt_CAdesc      = TheText(self, Txt_DisBlak, 62, 816, 25, 1, 'Category')

        # ----------------------------------    B U T T O N S     ---------------------------------
        self.BtnSelCod = TheButton(self, Btn_Def_En,  60, 860, 22, 'Select Codes DB ',  self.Clk_Sel_Codes)
        self.BtnView   = TheButton(self, Btn_Def_Dis,  60, 900, 22, 'Show Transact Codes', self.Clk_View_Codes)
        self.BtnGRmngr = TheButton(self, Btn_Def_Dis,  60, 940, 22, 'Groups Codes',      self.Clk_GR_Mngr)

        self.BtnDel    = TheButton(self, Btn_Def_Dis,286, 772, 18, 'Delete Last Record',self.Clk_Delete_Record)
        self.BtnAddNew = TheButton(self, Btn_Def_En ,286, 815, 18, 'Add New Record',    self.Clk_Add_New_Record)
        self.BtnSelXls = TheButton(self, Btn_Def_En, 286, 860, 18, 'Select Xlsx file',  self.Clk_Sel_xlsx)
        self.BtnViXlsx = TheButton(self, Btn_Def_Dis,286, 900, 18, 'Show Xlsx Rows',    self.Clk_View_Xlsx)
        self.BtnCekDb  = TheButton(self, Btn_Def_Dis, 286, 940, 18, 'Check codes DB',   self.Clk_Ceck_Codes_DB)

        self.BtnUpdate = TheButton(self, Btn_Def_En,  474, 772, 17, 'Update Code',         self.Clk_Update_Record)
        self.BtnWith_out= TheButton(self, Btn_Def_Dis,474, 815, 17, 'Show with/hout codes',self.Clk_With_out)
        self.BtnInsert = TheButton(self, Btn_Def_En,  474, 860, 17, 'Load Transactions',   self.Clk_Load_Transact)
        self.BtnWiewTransact=TheButton(self, Btn_Def_Dis,474, 900, 17, 'Show Transactions',self.Clk_ViewTransact)
        self.BtnExit   = TheButton(self, Btn_Def_En,  474, 940, 18, 'E X I T ',            self.Call_OnClose)

        self.geometry(Top_Mngr_geometry)
        self.Set_Status()
        if self.Data.Get_Files_Loaded_Stat(Ix_Codes_Loaded):  # In case of Codes not yet Loaded
            self.Load_Trees()

    # ------------------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_CODES_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:
            self.Call_OnClose()
        elif Request_Code == CODE_CLK_ON_TR_CODES:  # Clicked on Codes Tree [TRcode]
            TRcode = Values_List[0]
            self.Reqst_Clkd_On_TRcode(TRcode)
        elif Request_Code == CODES_DB_UPDATED or \
                Request_Code == XLSX_UPDATED:
                self.Mod_Mngr.Init_Xlsx_Lists(TOP_CODES_MNGR)          # Load_Xlsx()
                self.Load_Trees()

    # --------------------------  T R E E     Without  Codes   ------------------------------------
    def Frame_NoCodes_Setup(self):
        Nrows     = 30
        nColToVis = 4
        Headings  = ['#0', 'nRow', 'Date', 'Adeb  ', ' Full Description']
        Anchor    = ['c',   'c',    'c',   'e',      'w']
        Width     = [0,      60,     80,    90,       385]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_NoCodes.Tree_Setup(Form_List)

    def Clk_OnTree_NoCodes(self, Values):
        #  nRow    Date   Accred  Full Descrip
        self.Frame_WithCodes.Clear_Focus()
        self.Chat.Tx_Request([TOP_CODES_MNGR, [ANY], CODE_CLEAR_FOCUS, []])
        self.Clear_Texts()
        self.Set_Row_Without_Code(Values)
        self.Chat.Tx_Request([ TOP_CODES_MNGR, [TOP_XLSX_VIEW], CODE_CLIK_ON_XLSX, [] ])

    # --------------------------  T R E E     With  Codes   ---------------------------------------
    def Frame_WithCodes_Setup(self):
        self.Frame_WithCodes.Frame_Title('  ')
        Nrows     = 30
        nColToVis = 7
        Headings = ['#0',  'Row ',  'Contab ', 'Valuta ', 'Description',  'Accred ', 'Addeb ', 'Code ']
        Anchor   = ['c',   'w',     'c',       'c',       'w',            'e',       'e',      'c'    ]
        Width    = [ 0,     50,      80,        90,        205,            70,        70,       50    ]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_WithCodes.Tree_Setup(Form_List)

    def Clk_OnTree_WithCodes(self, Values):
        #  nRow    Date   Descrip   Accred   Addeb   TRcode
        nRow      = int(Values[iWithCode_nRow])
        TRcode    = int(Values[iWithCode_TRcode])
        Descrip = Values[iWithCode_TR_Desc]
        if int(nRow) < 1 or not Descrip:
            return
        self.Frame_NoCodes.Clear_Focus()
        self.Chat.Tx_Request([TOP_CODES_MNGR, [ANY,], CODE_CLEAR_FOCUS, []])
        self.View_Descr_Text(TRcode, self.GR_Combo)
        # self.Set_State_Butt_New_Updt('disabled', 'normal')  # New Update
        self.Chat.Tx_Request([TOP_CODES_MNGR, [TOP_XLSX_VIEW], CODE_CLIK_ON_XLSX, [] ])
        self.Chat.Tx_Request([TOP_CODES_MNGR, [TOP_XLSX_VIEW, TOP_GR_MNGR], CODE_CLK_ON_TR_CODES, [TRcode] ])

    # ---------------------------------------------------------------------------------------------
    def Load_Trees(self):
        if not self.Data.Get_Files_Loaded_Stat(Ix_Xlsx_Lists_Loaded):
            self.Frame_NoCodes.Frame_Title('  ***   Files  NOT loaded  NO  rows to insert   ***  ')
            self.Frame_WithCodes.Frame_Title('  ***   Files  NOT loaded  NO  rows to insert   ***  ')
            self.View_Frames(0)
        else:
            With_Code_List   = self.Data.Get_WithCodeList()
            XlsxFilename     = Get_File_Name(self.Data.Get_Selections_Member(Ix_Xlsx_File))
            Total            = self.Data.Get_Total_Rows()
            Total_WthoutCode = Total[Ix_Tot_Without_Code]
            Total_WithCode   = Total[Ix_Tot_WithCode]
            TitleNoCode = "  " + XlsxFilename + " :      " + str(Total_WthoutCode) + "  Transactions without code  ...  "
            TitleNoCode += str(Total[Ix_Tot_WithCode])  + "  with code   "
            TitleWith = "   " + XlsxFilename + " :      " + str(Total_WithCode) + "  Transactions with code  ...    "
            TitleWith += str(Total[Ix_Tot_Without_Code]) + "  whithout code   "
            self.Frame_NoCodes.Frame_Title(TitleNoCode)
            self.Frame_WithCodes.Frame_Title(TitleWith)

            self.Frame_NoCodes.Load_Row_Values(self.Data.Get_WithoutCodeList())
            self.Frame_WithCodes.Load_Row_Values(With_Code_List)
            self.View_Frames(Total_WthoutCode)

    # ---------------------------------------------------------------------------------------------
    # invoked on  Delete  Add  and Update  Record
    def Frames_Refresh(self):
        self.Mod_Mngr.Load_Xlsx_Lists_Mngr(TOP_CODES_MNGR, ON_SELECTIONS)
        self.Load_Trees()
        self.View_Frames(-1)
        return True

    # ---------------------------------------------------------------------------------------------
    def View_Frames(self, Total_WthoutCode):
        if Total_WthoutCode == 0:               # 0 No Rows Without codes
            self.View_Without_Code = False
            self.Frame_WithCodes.Frame_View()
            self.Frame_NoCodes.Frame_Hide()
        elif Total_WthoutCode > 0:              # some Rows Without codes
            self.View_Without_Code = True
            self.Frame_WithCodes.Frame_Hide()
            self.Frame_NoCodes.Frame_View()
        elif Total_WthoutCode < 0:              # -1 view frames as selected
            if self.View_Without_Code:
                self.Frame_WithCodes.Frame_Hide()
                self.Frame_NoCodes.Frame_View()
            else:
                self.Frame_WithCodes.Frame_View()
                self.Frame_NoCodes.Frame_Hide()

    # ---------------------------------------------------------------------------------------------
    def Clk_View_Codes(self):
        self.Mod_Mngr.Top_Launcher(TOP_CODES_VIEW, TOP_CODES_MNGR, [])

    # ---------------------------------------------------------------------------------------------
    def Clk_GR_Mngr(self):
        self.Mod_Mngr.Top_Launcher(TOP_GR_MNGR, TOP_CODES_MNGR, [])

    # ---------------------------------------------------------------------------------------------
    def Clk_With_out(self):
        if self.View_Without_Code:
            self.View_Without_Code = False
        else:
            self.View_Without_Code = True
        self.View_Frames(-1)

    # ----------------------------------------------------------------------------------------------
    def Set_Status(self):
        Codes_Loaded = False
        if self.Data.Get_Files_Loaded_Stat(Ix_Codes_Loaded):
            Codes_Loaded = True
        self.BtnView.Btn_Set_Status(Codes_Loaded)
        self.BtnGRmngr.Btn_Set_Status(Codes_Loaded)
        self.BtnCekDb.Btn_Set_Status(Codes_Loaded)
        self.BtnDel.Btn_Set_Status(Codes_Loaded)

        Status      = False
        Xlsx_Loaded = False
        if self.Data.Get_Files_Loaded_Stat(Ix_Xlsx_Lists_Loaded):
            Xlsx_Loaded = True
        if Codes_Loaded and Xlsx_Loaded:
            Status = True
        self.BtnViXlsx.Btn_Set_Status(Xlsx_Loaded)
        self.BtnWith_out.Btn_Set_Status(Status)

        Status = False
        Multiple = self.Data.Get_Multiple_List()
        Total    = self.Data.Get_Total_Rows()
        if Xlsx_Loaded and not Multiple and Total[Ix_Tot_OK]:
            Status = True
        self.BtnInsert.Btn_Set_Status(Status)        # Codes_Loaded   NO_Multiple   Xlsx_Loaded  Rws_OK!0

        self.ComboList = []
        if Codes_Loaded:
            for Rec in self.Data.GR_Codes_Ordered:
                self.ComboList.append(Rec[iGR_GRdesc])
        self.GR_Combo  = TheCombo(self, self.StrVar, 60, 776, 32, 23,
                                  self.ComboList, 'Select  Group', self.Clk_Combo)

    # ---------------------------------------------------------------------------------------------
    def Clk_Sel_Codes(self):
        if self.Mod_Mngr.Sel_Codes_Mngr(TOP_CODES_MNGR):
            self.Set_Status()
            pass

    # ---------------------------------------------------------------------------------------------
    def Clk_Sel_xlsx(self):
        if self.Mod_Mngr.Sel_Xlsx_Mngr(TOP_CODES_MNGR):
            self.Set_Status()
            self.Load_Trees()

    # ---------------------------------------------------------------------------------------------
    def Clk_View_Xlsx(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_CODES_MNGR, [])
        pass

    # --------------------------------------------------------------------------------------------
    def Clk_Load_Transact(self):
        self.Mod_Mngr.Top_Launcher(TOP_INS, TOP_CODES_MNGR, [])

    def Clk_ViewTransact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT, TOP_CODES_MNGR, [])

    # ---------------------------------------------------------------------------------------------
    def Reqst_Clkd_On_TRcode(self, TRcode):
        self.Frame_WithCodes.Clear_Focus()
        self.Clear_Texts()
        Index = -1
        TrCodInt = int(TRcode)
        self.Load_Trees()
        WithList = self.Data.Get_WithCodeList()
        for Rec in WithList:
            Index += 1
            if Rec[iWithCode_TRcode] == TrCodInt:
                self.Frame_WithCodes.Set_List_For_Focus(Index)
                break
        self.View_Descr_Text(TRcode, self.GR_Combo)
        # self.Set_State_Butt_New_Updt('disabled', 'normal')  # New Update

    # -------------------------------------------------------------------------------------------------
    def Clear_Texts(self):
        self.Clear_Only_Text_Widg()
        self.Txt_CAdesc.Set_Text("Category")
        self.GR_Combo.SetSelText('Select Group')

    # -------------------------------------------------------------------------------------------------
    def Set_Row_Without_Code(self, Values):  # nRow, Data_Valuta Full_Description
        self.Frame_NoCodes.Clear_Focus()
        self.Frame_WithCodes.Clear_Focus()
        nRow = int(Values[iNoCode_nRow])  # Row number + Date is Unic
        Date = str(Values[iNoCode_Date])
        Descr = Values[iNoCode_FullDesc]
        Index = - 1
        Without_Recs = self.Data.Get_WithoutCodeList()
        for Rec in Without_Recs:     # Wihtout_Code_Tree_List:
            Index += 1
            if Rec[0] == nRow and Rec[1] == Date:
                self.Frame_NoCodes.Set_Focus(Index)
                self.Clear_Texts()
                #                     nRow              Date           Full Description
                Full_Desc = 'nRow=' + str(nRow) + '  ' + Date + '-' + Descr
                self.Txt_StrFullDesc.Set_Text(Full_Desc)
                NewCode = self.Data.Get_New_Code()
                self.Txt_TR_Code.Set_Text(str(NewCode[0]))
                # self.Set_State_Butt_New_Updt('normal', 'disabled')  # New Update
                break

    # ------------------------     ***   Delete  the last TR Record      --------------------------
    def Clk_Delete_Record(self):
        Result = self.Delete_Code_Record()
        if Result == OK:
            Msg = Message_Dlg(MsgBox_Info, 'Code has correctly deleted')
            Msg.wait_window()
            if self.Frames_Refresh():
                self.Set_Status()
                self.Chat.Tx_Request([TOP_CODES_MNGR, [ANY], CODES_DB_UPDATED, []])
        elif Result == NONE:
            pass
        else:
            Msg = Message_Dlg(MsgBox_Err, Result)
            Msg.wait_window()

    # ------------------------     ***   Add new code Record  the last TR Record      -------------
    def Clk_Add_New_Record(self):
        Result = self.Add_Record_Code()
        if Result == OK:
            Res_List =  self.Data.Check_Codesdatabase(ON_SELECTIONS)
            if not Res_List:
                Msg = Message_Dlg(MsgBox_Info, 'Codice inserito correttamente')
                Msg.wait_window()
                if self.Frames_Refresh():
                    self.Set_Status()
                    self.Chat.Tx_Request([TOP_CODES_MNGR, [ANY], CODES_DB_UPDATED, []])
            else:
                self.Mod_Mngr.Check_Codes_View(CHECK_DBCODES_LOADED, VIEW_OKand_ERROR)

        elif Result == NONE:    # In case of "NO" to add record request
            pass
        else:
            View_Message([Result])
            pass

    # ------------------------     ***   Update TR code Record      -------------------------------
    def Clk_Update_Record(self):
        TrCode = int(self.Txt_TR_Code.Get_Text(NOT_INT))
        if not self.Test_Transaction_Data(TrCode):
            return
        else:
            # self.Set_State_Butt_New_Updt('disabled', 'disabled')  # New Update
            Result = self.Update_Record_Code()
            if Result == OK:
                Res_List = self.Data.Check_Codesdatabase(ON_SELECTIONS)
                if not Res_List:
                    Msg = Message_Dlg(MsgBox_Info, 'Codice aggiornato correttamente')
                    Msg.wait_window()
                    if self.Frames_Refresh():
                        self.Set_Status()
                        self.Chat.Tx_Request([TOP_CODES_MNGR, [ANY], CODES_DB_UPDATED, []])
                else:
                    Msg = Message_Dlg(MsgBox_Info, Res_List[0])
                    Msg.wait_window()

            elif Result == NONE:
                pass
            else:
                Msg = Message_Dlg(MsgBox_Err, Result)
                Msg.wait_window()

    # ---------------------------------------------------------------------------------------------
    def Test_Transaction_Data(self, Code):
        TRcode      = self.Txt_TR_Code.Get_Text(INTEGER)
        TRdesc      = self.Txt_TR_Desc.Get_Text(STRING)
        GRcode      = self.Txt_GR_Code.Get_Text(INTEGER)
        Txt_StrToFind  = self.Txt_StrToFind.Get_Text(STRING)
        StrFullDesc = self.Txt_StrFullDesc.Get_Text(STRING)
        if TRcode != 0 and TRdesc != '' and GRcode != 0:
            # check if Txt_StrToFind  exists  on StrFullDesc
            if StrToFind_in_Fulldescr(Txt_StrToFind, StrFullDesc):
                # check if  Txt_StrToFind  not matches with Full Descriptions on Codes Table
                Result = self.Data.Check_StrToFind_Exist_OnCodTable(Txt_StrToFind, Code)
                if Result[0] == OK:
                    return True
                else:
                    View_Message([Result[1]])
                    pass
                    return False
            else:
                Msg_Dlg = Message_Dlg(MsgBox_Err, 'String to find\nNot matched with Full description')
                Msg_Dlg.wait_window()
                return False

        else:
            Msg_Dlg = Message_Dlg(MsgBox_Err, 'Please complete Transaction data')
            Msg_Dlg.wait_window()
            return False

    # ---------------------------------------------------------------------------------------------
    def Clk_Ceck_Codes_DB(self):
        self.Mod_Mngr.Check_Codes_View(ON_SELECTIONS, VIEW_OKand_ERROR)

# ==============================================================================================================
