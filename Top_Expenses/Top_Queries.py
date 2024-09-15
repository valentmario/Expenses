# ---------------------------------------------------------------------------------- #
#                      *****     Top_Queries.py     *****                            #
#                      Queries  on Transactions database                             #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
from Common.Common_Functions import *
from Top_Expenses.Super_Top_Queries import Super_Top_Queries

from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import TheFrame

# ---------------------------------------------------------------------------------------------------------------------
class Top_Queries(Super_Top_Queries):
    def __init__(self):
        super().__init__(self.Trees_Update)

        # --------------------------  Trees-Frames    for  Queries   --------------------------------------------------
        self.Frame1 = TheFrame(self, xyToHide, 10, self.Click_OnFrame)  # frames for transactions
        self.Frame2 = TheFrame(self, xyToHide, 10, self.Click_OnFrame)
        self.Frame3 = TheFrame(self, xyToHide, 10, self.Click_OnFrame)
        self.Frames_List = [self.Frame1, self.Frame2, self.Frame3]      # the lists of transactions frames
        self.Frames_Setup()

        self.Frame1_Tot = TheFrame(self, xyToHide, 10, self.Click_OnTot) # small frames for total on frame
        self.Frame2_Tot = TheFrame(self, xyToHide, 10, self.Click_OnTot)
        self.Frame3_Tot = TheFrame(self, xyToHide, 10, self.Click_OnTot)

        self.Frames_Tot_List = [self.Frame1_Tot, self.Frame2_Tot, self.Frame3_Tot]  # the lists of totals
        self.Tot_Frames_Setup()

        # ----------------------------------------------------------------
        self.Frame_Average = TheFrame(self, xyToHide, 10, self.Click_OnTot)  # the frame for month average of expensess
        self.Frame_Average_Setup()

        self.Frame_TotRows = TheFrame(self, xyToHide, 10, self.Click_OnTot)  # the frame for total number of rows
        self.TotRows_Frame_Setup()

        self.Frame_TotCred = TheFrame(self, xyToHide, 10, self.Click_OnTot)  # the frame for total credits
        self.Credit_Frame_Setup()

        self.Frame_TotDebit = TheFrame(self, xyToHide, 10, self.Click_OnTot)  # the frame for total debits
        self.Debit_Frame_Setup()

        self.Show_Selections()  # show the selections for year, conto, month, total months, TR, GR, CA
        self.Trees_Update()     # setup frames geometry, load values on trees

    # ------------------------------------------------------------------------------------------------
    def Trees_Update(self):
        self.Setup_Year_Conto_Month_Tot_Date()
        self.Show_Selections()
        self.Set_Geometry_Frames()
        self.Set_Widgets_PosX()
        self.Set_Frames_Title()
        self.Set_TR_GR_CA_Sel_List()
        self.Create_Transact_List_perMonth()
        self.Trees_Load()

    # -------------------------------------------------------------------------------------------------
    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:  # Close
            self.Call_OnClose()
        elif Request_Code == TRANSACT_UPDATED:
            self.Call_OnClose()
        elif Request_Code == CODE_CLK_ON_TR_CODES:
            self.TRcode_Selected_OnTopView(Values_List[0])  # The Value is Transact_Code
            pass

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
    def Frame_Average_Setup(self):
        Nrows     = 1
        nColToVis = 1
        Headings  = ['#0', 'month  average  ']
        Anchor    = ['c',  'e']
        Width     = [ 0,    140]
        Form_ListT = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_Average.Tree_Setup(Form_ListT)

    # --------------------------------------------------------------------------------------------------
    def TotRows_Frame_Setup(self):
        Nrows     = 1
        nColToVis = 1
        Headings  = ['#0', 'total   rows  ']
        Anchor    = ['c',  'e']
        Width     = [ 0,    140]
        Form_ListT = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_TotRows.Tree_Setup(Form_ListT)

    # --------------------------------------------------------------------------------------------------
    def Credit_Frame_Setup(self):
        Nrows     = 1
        nColToVis = 1
        HeadingsC = ['#0', 'total  credits  ']
        Anchor    = ['c',  'e']
        Width     = [ 0,    140]
        Form_ListCred     = [Nrows, nColToVis, HeadingsC, Anchor, Width]
        self.Frame_TotCred = TheFrame(self, xyToHide, 10, self.Click_OnTot)
        self.Frame_TotCred.Tree_Setup(Form_ListCred)

    def Debit_Frame_Setup(self):
        Nrows     = 1
        nColToVis = 1
        HeadingsC = ['#0', 'total  debits  ']
        Anchor    = ['c',  'e']
        Width     = [ 0,    140]
        Form_ListDeb = [Nrows, nColToVis, HeadingsC, Anchor, Width]
        self.Frame_TotDebit = TheFrame(self, xyToHide, 10, self.Click_OnTot)
        self.Frame_TotDebit.Tree_Setup(Form_ListDeb)

    # -------------------------------------------------------------------------------------------------
    def Click_OnTot(self, Value):
        self.Dummy = Value
        self.Frame_TotRows.Clear_Focus()
        self.Frame_TotCred.Clear_Focus()
        self.Frame_TotDebit.Clear_Focus()
        self.Frame1_Tot.Clear_Focus()
        self.Frame2_Tot.Clear_Focus()
        self.Frame3_Tot.Clear_Focus()

    # -------------------------------------------------------------------------------------------------
    def Click_OnFrame(self, Value):
        self.Dummy = Value

   # -------------------------------------------------------------------------------------------------
    def Set_Geometry_Frames(self):
        Geometry_Index       = Queries_Geometry_Index[ self.Tot_Selected]
        self.Geometry        = Top_Query_geometry[Geometry_Index]
        self.Widgtes_PosX    = Queries_Frames_PosX[Geometry_Index]
        self.nFrames         = Queries_nFrames[ self.Tot_Selected]
        self.Months_on_Tree  = Queries_nMonts_xTree[ self.Tot_Selected]
        self.iStart_Month    = MONTH_INT[self.Month_Selected]
        self.iTot_Months     = TOT_MONTH_INT[self.Tot_Selected]
        self.iEnd_Month      = self.iStart_Month + self.iTot_Months -1
        self.Tot_List        = Queries_Tot_Dict[self.Month_Selected]
        self.geometry(self.Geometry)

    # -------------------------------------------------------------------------------------------------
    def Set_Widgets_PosX(self):
        # 10,  xyToHide,  xyToHide,  450
        PosXok = self.Widgtes_PosX[3]
        self.Btn_Clk_Year.SetX(PosXok)
        self.OptMenu_Conto.PosX(PosXok)
        self.OptMenu_Start.PosX(PosXok)
        self.OptMenu_Tot.PosX(PosXok)
        self.OptMenu_Tot.SetValues(self.Tot_List)
        self.OptMenu_Date.PosX(PosXok)

        self.OptMenu_TR.PosX(PosXok)
        self.OptMenu_GR.PosX(PosXok)
        self.OptMenu_CA.PosX(PosXok)
        self.Btn_xlsx_View.SetX(PosXok)
        self.Btn_xlsx_file.SetX(PosXok)

        self.Btn_DB_View.SetX(PosXok)
        self.Btn_Exit.SetX(PosXok)

        self.Frame1.Frame_PosXY(self.Widgtes_PosX[0], 10)
        self.Frame2.Frame_PosXY(self.Widgtes_PosX[1], 10)
        self.Frame3.Frame_PosXY(self.Widgtes_PosX[2], 10)
        self.Frame1_Tot.Frame_PosXY(self.Widgtes_PosX[0], 910)
        self.Frame2_Tot.Frame_PosXY(self.Widgtes_PosX[1], 910)
        self.Frame3_Tot.Frame_PosXY(self.Widgtes_PosX[2], 910)

        self.Frame_Average.Frame_PosXY(self.Widgtes_PosX[3], 640)
        self.Frame_TotRows.Frame_PosXY(self.Widgtes_PosX[3], 710)
        self.Frame_TotCred.Frame_PosXY(self.Widgtes_PosX[3], 780)
        self.Frame_TotDebit.Frame_PosXY(self.Widgtes_PosX[3],850)

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
    # Check for insert in Transact_xMonth_List (year[Date] Conto (TR GR CA)  return iMonth or -1
    def CheckForInsert(self, Rec):
        # Check for Year
        Date = Rec[iTransact_Valuta]
        if self.Date_Selected == ACC_DATE:
            Date = Rec[iTransact_Contab]
        if int(Date[0:4]) == self.Year_Selected:
                pass
        else:
            return -1

        # Check for Conto
        if self.Conto_Selected != Rec[iTransact_Conto]:
            return -1

        # Check for TR
        if self.TRselected != ALLTR and self.TRselected != '':
            if self.TRselected == Rec[iTransact_TRdesc]:
                pass
            else:
                return -1

        # Check for GR
        GR_CA_List = self.Data.Get_GR_CA_desc_From_TRdesc(Rec[iTransact_TRdesc])
        if self.GRselected != ALLGR and self.GRselected != '':
            if self.GRselected == GR_CA_List[0]:
                pass
            else:
                return -1

        # Check for CA
        if self.CAselected != ALLCA and self.CAselected != '':
            if self.CAselected == GR_CA_List[1]:
                pass
            else:
                return -1

        iMonth = int(Date[5:7]) - 1
        return iMonth

    # -------------------------------------------------------------------------------------------------
    # Create Transact_xMonth_List on base of Conto, Year, Date, TR, GR, CA
    # On Db      :[nRow    Contab    Valuta    TR_Desc   Accred   Addeb   TRcode]
    # Query view : ['Date', 'Description', 'Credits  ', 'Debits  ']
    # (date based on VALDATE/ACCDATE)  (Conto <- self.ContoSelected)
    # -------------------------------------------------------------------------------------------------
    def Create_Transact_List_perMonth(self):
        DateIndex = iTransact_Valuta
        if self.Date_Selected == ACC_DATE:
            DateIndex = iTransact_Contab
        self.Transact_xMonth_List  = [ [], [], [], [], [], [], [], [], [], [], [], [] ]
        for Rec in self.OneYear_Transact_List:
            iMonth = self.CheckForInsert(Rec)
            if iMonth >= 0:
                # ['Date', 'Description', 'Credits  ', 'Debits  ']
                View_Rec = [Rec[DateIndex], Rec[iTransact_TRdesc], Rec[iTransact_Accred], Rec[iTransact_Addeb]]
                self.Transact_xMonth_List[iMonth].append(View_Rec)
        pass

    # -------------------------------------------------------------------------------------------------
    # from Transact_xMonth_List (created on base of Conto,Year, Date, TR, GR, CA)
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
        #                         Cred Deb
        self.Total_Rows = 0
        for index in range(0, self.nFrames):
            Frame     = self.Frames_List[index]
            Frame_Tot = self.Frames_Tot_List[index]
            Frame_List  = []  #
            Month_Start = Init_End_Months[index][0]
            Month_End   = Init_End_Months[index][1]
            for Ix_Month in range(Month_Start, Month_End):
                for Rec in self.Transact_xMonth_List[Ix_Month]:
                    Rec_CredDeb_List = self.Credit_Debit_Setup(Rec)
                    Frame_List.append(Rec_CredDeb_List[0])
                    self.Tot_CredDeb_xTree[index][0] += Rec_CredDeb_List[1][0]
                    self.Tot_CredDeb_xTree[index][1] += Rec_CredDeb_List[1][1]
                    # Frame_List.append(Rec)
                    # Accr_Debits = self.Get_Credit_Debit(Rec)
                    # Credit      = Accr_Debits[0]
                    # Debit       = Accr_Debits[1]
                    # self.Tot_CredDeb_xTree[index][0] += Credit
                    # self.Tot_CredDeb_xTree[index][1] += Debit
                    Tot_Rec += 1
                pass

            Frame.Load_Row_Values(Frame_List)
            Credit = Float_ToString_Setup(self.Tot_CredDeb_xTree[index][0])
            Debit  = Float_ToString_Setup(self.Tot_CredDeb_xTree[index][1])
            LenList= len(Frame_List)
            self.Total_Rows += LenList
            Tot_Transact = str(LenList) + '   transactions '
            Tot_List = [[Tot_Transact, Credit, Debit]]
            Frame_Tot.Load_Row_Values(Tot_List)
        PRINT('***  Tot of Trees records: '+str(Tot_Rec)+'  ***')

        Total_Credit = self.Tot_CredDeb_xTree[0][0] + self.Tot_CredDeb_xTree[1][0] + self.Tot_CredDeb_xTree[2][0]
        Total_Debit  = self.Tot_CredDeb_xTree[0][1] + self.Tot_CredDeb_xTree[1][1] + self.Tot_CredDeb_xTree[2][1]

        strAverage    = Float_ToString_Setup(Total_Debit/self.iTot_Months)
        strTot_Credit = Float_ToString_Setup(Total_Credit)
        strTot_Debit  = Float_ToString_Setup(Total_Debit)

        self.Frame_Average.Load_Row_Values([[strAverage]])
        self.Frame_TotCred.Load_Row_Values([[strTot_Credit]])
        self.Frame_TotDebit.Load_Row_Values([[strTot_Debit]])
        self.Frame_TotRows.Load_Row_Values([[self.Total_Rows, 2]])

    # selections for conto, month, total months, TR, GR, CA
    def Show_Selections(self):
        self.OptMenu_Conto.SetSelText(self.Conto_Selected)
        self.OptMenu_Start.SetSelText(self.Month_Selected)
        self.OptMenu_Tot.SetSelText(self.Tot_Selected)
        self.OptMenu_TR.SetSelText(self.TRselected)
        self.OptMenu_GR.SetSelText(self.GRselected)
        self.OptMenu_CA.SetSelText(self.CAselected)

# =====================================================================================================
