# ---------------------------------------------------------------------------------- #
#                      *****     Top_Queries.py     *****                            #
#                      Queries  on Transactions database                             #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
import tkinter as tk

from Chat import Ms_Chat
from Common.Common_Functions import *
from Data_Classes.Transact_DB import Data

from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheText
from Widgt.Widgets import TheCombo

from Top_Expenses.Modules_Manager import Modul_Mngr

# ---------------------------------------------------------------------------------------------------------------------
class Top_Queries(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data
        self.Mod_Mngr = Modul_Mngr
        self.Dummy    = 0
        self.geometry('15x15+900+490')
        self.resizable(False, False)
        self.configure(background=BakGnd)
        self.Chat.Attach([self, TOP_QUERY])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)
        self.title('*****     Queries on transactions database     *****')

        self.Geometry       = ''
        self.nFrames        = 0
        self.Widgtes_PosX   = []
        self.Widg_PosX      = 9999
        self.Months_on_Tree = 0
        self.iStart_Month   = 0
        self.iTot_Months    = 0
        self.iEnd_Month     = 0

        self.OneYear_Transact_List   = []    # Cred Deb
        self.Tot_CredDeb_xTree       = [[0, 0], [0,    0], [0, 0]]
        self.Months_TR_Database_List = [ [], [], [], [], [], [], [], [], [], [], [], [] ]

        self.Tot_List       = [ONE_MONTH,TWO_MONTHS,FOUR_MONTHS,SIX_MONTHS,TWELVE_MONTHS]

        self.Files_Ident    = self.Data.Get_Xlsx_Transact_Ident()
        self.Year_Selected  = self.Files_Ident[Ix_Transact_Year]
        self.Conto_Selected = ''
        self.Month_Selected = JAN
        self.Tot_Selected   = ONE_MONTH
        self.Date_List      = [VAL_DATE, ACC_DATE]
        self.Date           = VAL_DATE
        self.TRselected  = ''
        self.GRselected  = ''
        self.CAselected  = ''

        self.Total_Rows  = 0    # The rows in the Trees Months
        self.TR_List     = []
        self.GR_List     = []
        self.CA_List     = []
        self.Total_xCode = []       # [totTR. totGR, totCA]

        # steps to add a widget:   1-Create widget    2-Set_Widgets_PosX and Y

        # ------------  OPTION  MENUS   Year  Conto Month Total  TR GR CA  with default values  -----------------------

        strYear          = 'Year =  ' + str(self.Year_Selected)
        self.Txt_Year    = TheText(self, Txt_Disab, 450, 20, 17, 1, strYear)
        self.StrVar_Year = tk.StringVar
        self.OptMenu_Conto = TheCombo(self, self.StrVar_Year, self.Widg_PosX,  55, 21, 16, Conto_List,
                                     FIDEU, self.Clk_Conto)
        self.StrVar_Start  = tk.StringVar
        self.OptMenu_Start = TheCombo(self, self.StrVar_Start, self.Widg_PosX, 90, 21, 16,  Month_Names,
                                      JAN, self.Clk_Month)
        self.StrVar_Tot   = tk.StringVar
        self.OptMenu_Tot  = TheCombo(self,  self.StrVar_Tot,   self.Widg_PosX, 125, 21, 16,  self.Tot_List,
                                     ONE_MONTH, self.Clk_Tot)

        self.StrVar_Date  = tk.StringVar
        self.OptMenu_Date = TheCombo(self,  self.StrVar_Date,  self.Widg_PosX, 160, 21, 16,  self.Date_List,
                                     VAL_DATE, self.Clk_Date)

        self.Txt_SelTrGrCa = TheText(self, Txt_Disab, 450, 207, 16, 1,  'TR GR CA  select')

        self.StrVar_TR  = tk.StringVar
        self.OptMenu_TR = TheCombo(self, self.StrVar_TR,      self.Widg_PosX, 240, 41, 16, self.TR_List,
                                    '', self.Clk_TRsel)
        self.StrVar_GR  = tk.StringVar
        self.OptMenu_GR = TheCombo(self, self.StrVar_GR,     self.Widg_PosX, 275, 41, 16,  self.GR_List,
                                   '', self.Clk_GRsel)
        self.StrVar_CA  = tk.StringVar
        self.OptMenu_CA = TheCombo(self,  self.StrVar_CA,    self.Widg_PosX, 310, 21, 16,  self.CA_List,
                                   '', self.Clk_CAsel)
        # self.Create_Year_Transact_List()
        # TheText(self, Txt_Disab, self.Widg_PosX, 450, 19, 1, 'start - end balances')
        # TheText(self, Txt_Disab, 450, 20, 19, 1, 'start - end summaries')

        # ---------------------------------    Buttons   --------------------------------------------------------------
        self.Btn_xlsx_file = TheButton(self, Btn_Def_En,  self.Widg_PosX,   370, 17, 'xlsx file select',self.Clk_SelXlsx)
        self.Btn_xlsx_View = TheButton(self, Btn_Def_En,  self.Widg_PosX,   410, 17, 'xlsx view', self.Clk_XlsxView)

        self.Btn_Transact_Sel = TheButton(self, Btn_Def_En, self.Widg_PosX, 450, 17, 'transact  file select', self.Clk_Sel_Transact)
        self.Btn_Transact_view = TheButton(self, Btn_Def_En, self.Widg_PosX,490, 17, 'transactions view', self.Clk_ViewTransact)

        self.Btn_Summaries = TheButton(self, Btn_Def_En,   self.Widg_PosX,  660, 17, ' Summaries ', self.Clk_Summaries)
        self.Btn_Exit      = TheButton(self, Btn_Bol_En,   self.Widg_PosX,  936, 15, '  E X I T  ',  self.Call_OnClose)

        # --------------------------  Trees-Frames    for  Queries   --------------------------------------------------
        self.Frame1 = TheFrame(self, xyToHide, 10, self.Click_OnFrame)
        self.Frame2 = TheFrame(self, xyToHide, 10, self.Click_OnFrame)
        self.Frame3 = TheFrame(self, xyToHide, 10, self.Click_OnFrame)
        self.Frames_List = [self.Frame1, self.Frame2, self.Frame3]
        self.Frames_Setup()

        self.Frame1_Tot = TheFrame(self, xyToHide, 10, self.Click_OnTot)
        self.Frame2_Tot = TheFrame(self, xyToHide, 10, self.Click_OnTot)
        self.Frame3_Tot = TheFrame(self, xyToHide, 10, self.Click_OnTot)

        self.Frames_Tot_List = [self.Frame1_Tot, self.Frame2_Tot, self.Frame3_Tot]
        self.Tot_Frames_Setup()
        # ----------------------------------------------------------------
        self.Frame_TotRows = TheFrame(self, xyToHide, 10, self.Click_OnTot)
        self.TotRows_Frame_Setup()

        self.Frame_Credit = TheFrame(self, xyToHide, 10, self.Click_OnTot)
        self.Credit_Frame_Setup()

        self.Frame_Debit = TheFrame(self, xyToHide, 10, self.Click_OnTot)
        self.Debit_Frame_Setup()

        self.Set_Geometry_Frames()
        self.Set_Widgets_PosX()
        self.Set_Frames_Title()
        self.Trees_Load()
        self.Set_Combos_List_Sel()

    # -------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_QUERY)
        self.destroy()

    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:  # Close
            self.Call_OnClose()
        elif Request_Code == TRANSACT_UPDATED:
            pass

    # -------------------------------------------------------------------------------------------------
    def Clk_Summaries(self):
        self.Mod_Mngr.Top_Launcher(TOP_SUMMARIES)

    # ------------------  Fill Combos List   and previous selections saved on  Files_Names  ---------------------------
    def Set_Combos_List_Sel(self):
        TR_List      = []
        self.TR_List = []
        self.GR_List = []
        self.CA_List = []

        for Rec in self.OneYear_Transact_List:
            if Rec[iTransact_TRdesc] not in TR_List:
                TR_List.append(Rec[iTransact_TRdesc])
        TR_List.sort()
        for TRdesc in TR_List:
            GRCAdesc = self.Data.Get_GR_CA_desc_From_TRdesc(TRdesc)
            GRdesc = GRCAdesc[0]
            CAdesc = GRCAdesc[1]
            if GRdesc not in self.GR_List:
                self.GR_List.append(GRdesc)
            if CAdesc not in self.CA_List:
                self.CA_List.append(CAdesc)
        self.TR_List = [ALLTR]
        for Item in TR_List:
            self.TR_List.append(Item)
        self.GR_List.sort()
        self.CA_List.sort()
        strToPrint  = 'Len TR_List: '+str(len(self.TR_List))+'   Len GR_List: '+str(len(self.GR_List))
        strToPrint += '   Len CA_List: '+str(len(self.CA_List))
        PRINT(strToPrint)

        self.OptMenu_TR.SetValues(self.TR_List)
        self.OptMenu_GR.SetValues(self.GR_List)
        self.OptMenu_CA.SetValues(self.CA_List)

        self.OptMenu_TR.SetSelText(self.TRselected)
        self.OptMenu_GR.SetSelText(self.GRselected)
        self.OptMenu_CA.SetSelText(self.CAselected)

    # -------------------------------------------------------------------------------------------------
    # Three Frames for transactions view
    def Frames_Setup(self):
        Nrows     = 42
        nColToVis = 4
        Headings  = ['#0', 'Date',  'Description', 'Credits  ', 'Debits  ']
        Anchor    = ['c',   'c',       'w',           'e',       'e']
        Width     = [0,      100,      160,           70,        70]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        for Frame in self.Frames_List:
            Frame.Tree_Setup(Form_List)

    # -------------------------------------------------------------------------------------------------
    # Three Frames for Total Cred Deb view on each Transactions Frame  view
    def Tot_Frames_Setup(self):
        Nrows     = 1
        nColToVis = 3
        Headings  = ['#0', '      Total  ',  'Credits  ', 'Debits  ']
        Anchor    = ['c',   'c',                  'e',       'e']
        Width     = [ 0,     220,                  90,        90]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        for Frame in self.Frames_Tot_List:
            Frame.Tree_Setup(Form_List)

    # --------------------------------------------------------------------------------------------------
    def TotRows_Frame_Setup(self):
        Nrows     = 1
        nColToVis = 2
        Headings  = ['#0', 'total', 'checked']
        Anchor    = ['c',  'c',     'c']
        Width     = [ 0,    70,      70]
        Form_ListT = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_TotRows.Tree_Setup(Form_ListT)

    # --------------------------------------------------------------------------------------------------
    def Credit_Frame_Setup(self):
        Nrows     = 1
        nColToVis = 1
        HeadingsC = ['#0', 'Credits  ']
        Anchor    = ['c',  'e']
        Width     = [ 0,    140]
        Form_ListCred     = [Nrows, nColToVis, HeadingsC, Anchor, Width]
        self.Frame_Credit = TheFrame(self, xyToHide, 10, self.Click_OnTot)
        self.Frame_Credit.Tree_Setup(Form_ListCred)

    def Debit_Frame_Setup(self):
        Nrows     = 1
        nColToVis = 1
        HeadingsC = ['#0', 'Debits  ']
        Anchor    = ['c',  'e']
        Width     = [ 0,    140]
        Form_ListDeb = [Nrows, nColToVis, HeadingsC, Anchor, Width]
        self.Frame_Debit = TheFrame(self, xyToHide, 10, self.Click_OnTot)
        self.Frame_Debit.Tree_Setup(Form_ListDeb)

    # -------------------------------------------------------------------------------------------------
    def Click_OnTot(self, Value):
        self.Dummy = Value
        self.Frame_TotRows.Clear_Focus()
        self.Frame_Credit.Clear_Focus()
        self.Frame_Debit.Clear_Focus()
        self.Frame1_Tot.Clear_Focus()
        self.Frame2_Tot.Clear_Focus()
        self.Frame3_Tot.Clear_Focus()

    # -------------------------------------------------------------------------------------------------
    def Click_OnFrame(self, Value):
        self.Dummy = Value

   # -------------------------------------------------------------------------------------------------
    def Set_Geometry_Frames(self):
        Type_Tot             = self.Tot_Selected
        Geometry_Index       = Queries_Geometry_Index[Type_Tot]
        self.Geometry        = Top_Query_geometry[Geometry_Index]
        self.Widgtes_PosX    = Queries_Frames_PosX[Geometry_Index]
        self.nFrames         = Queries_nFrames[Type_Tot]
        self.Months_on_Tree  = Queries_nMonts_xTree[Type_Tot]
        self.iStart_Month    = MONTH_INT[self.Month_Selected]
        self.iTot_Months     = TOT_MONTH_INT[self.Tot_Selected]
        self.iEnd_Month      = self.iStart_Month + self.iTot_Months -1
        self.Tot_List        = Queries_Tot_Dict[self.Month_Selected]
        self.geometry(self.Geometry)

    # -------------------------------------------------------------------------------------------------
    def Set_Widgets_PosX(self):
        # 10,  xyToHide,  xyToHide,  450
        PosXok = self.Widgtes_PosX[3]
        self.OptMenu_Conto.PosX(PosXok)
        self.OptMenu_Start.PosX(PosXok)
        self.OptMenu_Tot.PosX(PosXok)
        self.OptMenu_Tot.SetValues(self.Tot_List)
        self.OptMenu_Date.PosX(PosXok)

        self.Txt_SelTrGrCa.PosX(PosXok)
        self.Btn_Summaries.SetX(PosXok)

        self.OptMenu_TR.PosX(PosXok)
        self.OptMenu_GR.PosX(PosXok)
        self.OptMenu_CA.PosX(PosXok)
        self.Btn_xlsx_View.SetX(PosXok)
        self.Btn_xlsx_file.SetX(PosXok)
        self.Btn_Transact_Sel.SetX(PosXok)
        self.Btn_Transact_view.SetX(PosXok)
        self.Btn_Exit.SetX(PosXok)

        self.Frame1.Frame_PosXY(self.Widgtes_PosX[0], 10)
        self.Frame2.Frame_PosXY(self.Widgtes_PosX[1], 10)
        self.Frame3.Frame_PosXY(self.Widgtes_PosX[2], 10)
        self.Frame1_Tot.Frame_PosXY(self.Widgtes_PosX[0], 910)
        self.Frame2_Tot.Frame_PosXY(self.Widgtes_PosX[1], 910)
        self.Frame3_Tot.Frame_PosXY(self.Widgtes_PosX[2], 910)

        self.Frame_TotRows.Frame_PosXY(self.Widgtes_PosX[3], 710)
        self.Frame_Credit.Frame_PosXY(self.Widgtes_PosX[3], 780)
        self.Frame_Debit.Frame_PosXY(self.Widgtes_PosX[3], 850)

    # -------------------------------------------------------------------------------------------------
    def Set_Frames_Title(self):
        Tit1 = '   ' + self.Month_Selected + '   '
        self.Frame1.Frame_Title(Tit1)
        nextMonth2 = self.iStart_Month + self.Months_on_Tree
        if nextMonth2 <= 12:
            Tit2 = '   ' + Month_Names[nextMonth2-1] + '   '
            self.Frame2.Frame_Title(Tit2)
            nextMonth3 = self.iStart_Month  + self.Months_on_Tree *2
            if nextMonth3 <= 12:
                Tit3 = '   ' + Month_Names[nextMonth3-1] + '   '
                self.Frame3.Frame_Title(Tit3)

    # -------------------------------------------------------------------------------------------------
    def View_Trees_Values(self):
        self.Set_Geometry_Frames()
        self.Set_Widgets_PosX()
        self.Set_Frames_Title()
        self.Trees_Load()

        if self.GRselected == '':
            return
        Tot = 0
        # for Rec in self.OneYear_Transact_List:
        #     if Rec[iTransact_GRdesc] == self.GRselected:
        #         PRINT(Rec)
        #         Tot += 1
        PRINT('Len of Trees Rows: ' +str(Tot)+'\n----------------------------------')

    def Update_Selections(self):
        # self.Data.Update_Ins_Query_year(self.Conto_Selected, Ix_Query_Conto)
        # self.Data.Update_Ins_Query_year(self.Month_Selected, Ix_Query_Month)
        # self.Data.Update_Ins_Query_year(self.Tot_Selected, Ix_Query_TotMonths)
        # self.Data.Update_Ins_Query_year(self.TRselected, Ix_Query_TRsel)
        # self.Data.Update_Ins_Query_year(self.GRselected, Ix_Query_GRsel)
        # self.Data.Update_Ins_Query_year(self.CAselected, Ix_Query_CAsel)

        self.OptMenu_Conto.SetSelText(self.Conto_Selected)
        self.OptMenu_Start.SetSelText(self.Month_Selected)
        self.OptMenu_Tot.SetSelText(self.Tot_Selected)
        self.OptMenu_TR.SetSelText(self.TRselected)
        self.OptMenu_GR.SetSelText(self.GRselected)
        self.OptMenu_CA.SetSelText(self.CAselected)

        self.Chat.Tx_Request([TOP_QUERY, [MAIN_WIND], XLSX_UPDATED, []])

    # -------------------------------------------------------------------------------------------------
    def Clk_Conto(self, Value):
        self.Conto_Selected = Value
        self.Month_Selected = Month_Names[0]
        self.Tot_Selected   = ONE_MONTH
        self.Update_Selections()
        self.View_Trees_Values()

    def Clk_Month(self, Value):
        self.Month_Selected = Value
        self.Update_Selections()
        self.Tot_List = Queries_Tot_Dict[self.Month_Selected]
        self.View_Trees_Values()

    # -------------------------------------------------------------------------------------------------
    def Clk_Tot(self, Value):
        self.Tot_Selected = Value
        self.Update_Selections()
        self.Tot_List = Queries_Tot_Dict[self.Month_Selected]
        self.View_Trees_Values()

    # -------------------------------------------------------------------------------------------------
    def Clk_Date(self, Value):
        self.Date_List = Value


    # -------------------------------------------------------------------------------------------------
    def Clear_Code_Sel(self):
        self.TRselected = ''
        self.GRselected = ''
        self.CAselected = ''

    # -------------------------------------------------------------------------------------------------
    def Clk_TRsel(self, Val):
        Value = Val
        if Val == NONE:
            Value = ''
        self.Clear_Code_Sel()
        self.TRselected = Value
        self.Update_Selections()
        self.Tot_List = Queries_Tot_Dict[self.Month_Selected]
        self.View_Trees_Values()

    def Clk_GRsel(self, Value):
        self.Clear_Code_Sel()
        self.GRselected = Value
        self.Update_Selections()
        self.Tot_List = Queries_Tot_Dict[self.Month_Selected]
        self.View_Trees_Values()

    def Clk_CAsel(self, Value):
        self.Clear_Code_Sel()
        self.CAselected = Value
        self.Update_Selections()
        self.Tot_List = Queries_Tot_Dict[self.Month_Selected]
        self.View_Trees_Values()


    # -------------------------------------------------------------------------------------------------
    def Trees_Load(self):
        Tot_Rec = 0
        Month_Start  = MONTH_INT[self.Month_Selected] - 1
        Total_Months_xTree = self.Months_on_Tree
        Start1 = Month_Start
        End1   = Month_Start + Total_Months_xTree
        Start2 = End1
        End2   = Month_Start + Total_Months_xTree * 2
        Start3 = End2
        End3   = Month_Start + Total_Months_xTree * 3
        Init_End_Months  = [[Start1, End1], [Start2, End2], [Start3, End3]]
        self.Tot_CredDeb_xTree = [[0,   0], [0, 0], [0, 0]]
        #                          Cred Deb
        self.Total_Rows = 0
        for index in range(0, self.nFrames):
            Frame     = self.Frames_List[index]
            Frame_Tot = self.Frames_Tot_List[index]
            List  = []
            Month_Start = Init_End_Months[index][0]
            Month_End   = Init_End_Months[index][1]
            for Ix_Month in range(Month_Start, Month_End):
                for Rec in self.Months_TR_Database_List[Ix_Month]:
                    Checked_Rec = self.Check_Record_To_Insert(Rec)
                    if Checked_Rec:
                        List.append(Checked_Rec)
                        Accr_Debits = self.Get_Credit_Debit(Checked_Rec)
                        Credit = Accr_Debits[0]
                        Debit  = Accr_Debits[1]

                        self.Tot_CredDeb_xTree[index][0] += Credit
                        self.Tot_CredDeb_xTree[index][1] += Debit
                        Tot_Rec += 1
                pass
            Frame.Load_Row_Values(List)
            Credit = Float_ToString_Setup(self.Tot_CredDeb_xTree[index][0])
            Debit  = Float_ToString_Setup(self.Tot_CredDeb_xTree[index][1])
            LenList= len(List)
            self.Total_Rows += LenList
            Tot_Transact = str(LenList) + '   transactions '
            Tot_List = [[Tot_Transact, Credit, Debit]]
            Frame_Tot.Load_Row_Values(Tot_List)
        PRINT('***  Tot of Trees_Load: '+str(Tot_Rec)+'  ***')

        Total_Credit = self.Tot_CredDeb_xTree[0][0] + self.Tot_CredDeb_xTree[1][0] + self.Tot_CredDeb_xTree[2][0]
        Total_Debit  = self.Tot_CredDeb_xTree[0][1] + self.Tot_CredDeb_xTree[1][1] + self.Tot_CredDeb_xTree[2][1]

        flTot_Credit = Float_ToString_Setup(Total_Credit)
        flTot_Debit = Float_ToString_Setup(Total_Debit)

        # self.Frame_TotCred.Load_Row_Values([[flTot_Credit]])
        # self.Frame_TotDebit.Load_Row_Values([[flTot_Debit]])
        # self.Frame_TotRows.Load_Row_Values([[self.Total_Rows, 2]])

    # ---------------------------------------------------------------------------------------------
    def Check_Record_To_Insert(self, Rec_ToIns):
        Conto_ToCheck = Rec_ToIns[iTransact_Conto]
        TRcode       = Rec_ToIns[iTransact_TRcode]
        TR_GR_CAdesc = self.Data.Get_TR_GR_CA_desc_From_TRcode(TRcode)
        TR_ToCheck   = TR_GR_CAdesc[0]
        GR_ToCheck   = TR_GR_CAdesc[1]
        CA_ToCheck   = TR_GR_CAdesc[2]

        Checked = False
        if self.Conto_Selected == FidFlhPost:
            if Conto_ToCheck == AMBRA:
                pass
            else:
                Checked = True
        elif self.Conto_Selected == Conto_ToCheck:
            Checked = True
        if not Checked:
            return []

        Checked = False
        TRsel = True
        if self.TRselected == ALLTR or self.TRselected == '':
            TRsel = False
        if not TRsel and self.GRselected == '' and self.CAselected == '':
            Checked = True
        elif self.TRselected == TR_ToCheck or self.GRselected == GR_ToCheck or self.CAselected == CA_ToCheck:
            Checked = True
        if not Checked:
            return []
        # Rec_Checked = [It_Date(Rec_ToIns[iTransact_Date]), Rec_ToIns[iTransact_TRdesc],
        #                Rec_ToIns[iTransact_Accred], Rec_ToIns[iTransact_Addeb]]
        # return Rec_Checked
    # -------------------------------------------------------------------------------------------------
    def Get_Credit_Debit(self, Rec):
        self.Dummy = 0
        Credit = self.Convert_To_Float(Rec[2])
        Debit  = self.Convert_To_Float(Rec[3])
        return [Credit, Debit]

    # -------------------------------------------------------------------------------------------------
    def Clk_XlsxView(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW)

    # -------------------------------------------------------------------------------------------------
    def Clk_SelXlsx(self):
        self.Mod_Mngr.Sel_Xlsx()

    # -------------------------------------------------------------------------------------------------
    def Clk_Sel_Transact(self):
        self.Mod_Mngr.Sel_Transact()

    # -------------------------------------------------------------------------------------------------
    def Clk_ViewTransact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT)


    # -----------------------------------------------------------------------------------------------
    def Convert_To_Float(self, Value):
        self.Dummy = 0
        flVal      = Value
        Type = type(Value)
        if Type is str or Type is None:
            return 0.00
        if type(Value) is int:
            flVal = float(Value)
        return flVal

    def View_Data(self):
        pass

# =====================================================================================================
