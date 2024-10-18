# ---------------------------------------------------------------------------------- #
#               *****     Super_Top_Queries.py     *****                             #
#      the parent of Top_Queries contains:                                           #
#                                   all attributs excepted the frames                #
#                                   all click methods                                #
#      the method  Load_All_Data is contained in the child of  Super_Top_Queries     #
#                                                                                    #
# ---------------------------------------------------------------------------------- #

from Chat import Ms_Chat
from Common.Common_Functions import *
from Data_Classes.Transact_DB import Data_Manager
from Widgt.Widgets import *
from Top_Expenses.Modules_Manager import Modul_Mngr
from Top_Expenses.Top_Codes_View import Top_View_Codes

# =================================================================================================================
class Super_Top_Queries(tk.Toplevel):
    def __init__(self, Load_All_Data):
        super().__init__()
        self.Chat     = Ms_Chat
        self.Data     = Data_Manager
        self.Mod_Mngr = Modul_Mngr

        self.Load_All_Data = Load_All_Data
        self.Dummy    = 0
        self.geometry('15x15+900+490')
        self.resizable(False, False)
        self.configure(background=BakGnd)
        self.Chat.Attach([self, TOP_QUERY])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)
        self.title('    ')

        self.Geometry       = ''
        self.nFrames        = 0
        self.Widgtes_PosX   = []
        self.Widg_PosX      = xyToHide
        self.Months_on_Tree = 0
        self.iStart_Month   = 0
        self.iTot_Months    = 0
        self.iEnd_Month     = 0

        # This list is loaded from Transact_DB_Table on startup or on selecting Year
        self.OneYear_Transact_List = []

        # This list is created on startup or at each Selection
        # based on Year, Conto (ValDate/AccDate) TR GR CA for each month
        self.Transact_xMonth_List = [ [], [], [], [], [], [], [], [], [], [], [], [] ]
        self.DateCount_PerMonth   = [ 0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0  ]

        # [Credits, Debits]  for   Frame1, Frame2, Frame3
        self.Tot_CredDeb_xTree  = [[0, 0], [0, 0], [0, 0]]

        self.Transact_Years_List = []  # The years transactions contained on TRANSATCION directory
        self.Tot_List    = [ONE_MONTH,TWO_MONTHS,FOUR_MONTHS,SIX_MONTHS,TWELVE_MONTHS]
        self.Date_List   = [VAL_DATE, ACC_DATE]
        self.Files_Ident = []   # self.Data.Get_Xlsx_Transact_Ident()

        self.Year_Selected  = 0
        self.Conto_Selected = ''
        self.Month_Selected = ''
        self.Tot_Selected   = ''
        self.Date_Selected  = VAL_DATE  # default is Valuta, can be changed through OptMenu_Date
        self.TRselected     = ''
        self.GRselected     = ''
        self.CAselected     = ''

        self.Total_Rows  = 0    # Total rows of selected Transactions
        self.TR_List     = []   # Codes on Year Transactions Table for OptMenu_TR
        self.GR_List     = []   # same per GR
        self.CA_List     = []   # same per CA

        # ------------------    C O M B O s       ---------------------------------------------------
        self.StrVar_Year   = tk.StringVar
        self.OptMenu_Year  = TheCombo(self, self.StrVar_Year, self.Widg_PosX, 20, 15, 16, [''],
                                      'Seleziona un anno', self.Clk_ComboYear)

        self.StrVar_Conto  = tk.StringVar
        self.OptMenu_Conto = TheCombo(self, self.StrVar_Conto, self.Widg_PosX, 55, 15, 16, Conto_List,
                                      FIDEU, self.Clk_Conto)

        self.StrVar_Start  = tk.StringVar
        self.OptMenu_Start = TheCombo(self, self.StrVar_Start, self.Widg_PosX, 90, 21, 16,  Month_Names,
                                      JAN, self.Clk_Month)
        self.StrVar_Tot   = tk.StringVar
        self.OptMenu_Tot  = TheCombo(self,  self.StrVar_Tot,   self.Widg_PosX, 125, 21, 16,  self.Tot_List,
                                     ONE_MONTH, self.Clk_Tot)

        self.StrVar_Date  = tk.StringVar
        self.OptMenu_Date = TheCombo(self,  self.StrVar_Date,  self.Widg_PosX, 160, 21, 16,  self.Date_List,
                                     self.Date_Selected , self.Clk_Date)

        self.StrVar_TR  = tk.StringVar
        self.OptMenu_TR = TheCombo(self, self.StrVar_TR,      self.Widg_PosX, 210, 41, 16, self.TR_List,
                                    'Codice Movimenti', self.Clk_TRsel)
        self.StrVar_GR  = tk.StringVar
        self.OptMenu_GR = TheCombo(self, self.StrVar_GR,     self.Widg_PosX,  245, 41, 16,  self.GR_List,
                                   'Codici Gruppoi', self.Clk_GRsel)
        self.StrVar_CA  = tk.StringVar
        self.OptMenu_CA = TheCombo(self,  self.StrVar_CA,    self.Widg_PosX,  280, 21, 16,  self.CA_List,
                                   'Codici Categorie', self.Clk_CAsel)

        # ---------------------------------    Buttons   ----------------------------------------------------------
        self.Btn_DB_View   = TheButton(self, Btn_Def_En, self.Widg_PosX, 370, 15, 'Mostra i Movimenti', self.Clk_ViewTransact)
        self.Btn_xlsx_file = TheButton(self, Btn_Def_En, self.Widg_PosX, 410, 15, 'Selez. un file Xlsx', self.Clk_SelXlsx)
        self.Btn_xlsx_View = TheButton(self, Btn_Def_En, self.Widg_PosX, 450, 15, 'Mostra file Xlsx',    self.Clk_XlsxView)

        self.Btn_Exit = TheButton(self, Btn_Bol_En, self.Widg_PosX, 936, 13, '  E S C I  ', self.Call_OnClose)
        self.Set_All_Select()
    # -------------------------------------------------------------------------------------------------------------
    def Clear_Code_Sel(self):
        self.TRselected = ''
        self.GRselected = ''
        self.CAselected = ''

    # ------------------  Fill Combos List   and previous selections saved on  Files_Names  -----------------------
    def Set_TR_GR_CA_Sel_List(self):
        TR_List      = []
        GR_List      = []
        CA_List      = []
        self.TR_List = []
        self.GR_List = []
        self.CA_List = []

        for Rec in self.OneYear_Transact_List:
            if Rec[iTransact_TRdesc] not in TR_List:
                TR_List.append(Rec[iTransact_TRdesc])
        TR_List.sort()

        for TRdesc in TR_List:      # List of codes groups categories used in transactions
            GRCAdesc = self.Data.Get_GR_CA_desc_From_TRdesc(TRdesc)
            GRdesc = GRCAdesc[0]
            CAdesc = GRCAdesc[1]
            if GRdesc not in GR_List:
                GR_List.append(GRdesc)
            if CAdesc not in CA_List:
                CA_List.append(CAdesc)
        GR_List.sort()
        CA_List.sort()

        self.TR_List = [ALLTR]          # Put All Transac
        for Item in TR_List:
            self.TR_List.append(Item)

        self.GR_List = [ALLGR]
        for Item in GR_List:
            self.GR_List.append(Item)

        self.CA_List = [ALLCA]
        for Item in CA_List:
            self.CA_List.append(Item)
        self.Setup_Year_Conto_Month_Tot_Date()

    # -------------------------------------------------------------------------------------------------------------
    def Setup_Year_Conto_Month_Tot_Date(self):
        self.Files_Ident    = self.Data.Get_Xlsx_Transact_Ident()   # list created on ModulesManager
        self.Year_Selected  = self.Files_Ident[Ix_Transact_Year]
        # Title = '*****     + str

        List = Data_Manager.Get_Transact_Year_ListInData()
        self.Transact_Years_List = List[1]
        self.Transact_Years_List.sort()
        self.OptMenu_Year.SetValues(self.Transact_Years_List)

        Queries_Sel = self.Data.Get_Selections_Member(Ix_Query_List)
        self.Conto_Selected = Queries_Sel[Ix_Query_Conto]
        self.Month_Selected = Queries_Sel[Ix_Query_Month]
        self.Tot_Selected   = Queries_Sel[Ix_Query_TotMonths]

        self.TRselected     = Queries_Sel[Ix_Query_TRsel]
        self.GRselected     = Queries_Sel[Ix_Query_GRsel]
        self.CAselected     = Queries_Sel[Ix_Query_CAsel]

    # -------------------------------------------------------------------------------------------------------------
    def Setup_TR_GR_CA_OptManu(self):
        self.OptMenu_TR.SetValues([ALLTR, SELTR])
        self.OptMenu_GR.SetValues(self.GR_List)
        self.OptMenu_CA.SetValues(self.CA_List)

        self.OptMenu_TR.SetSelText(self.TRselected)
        self.OptMenu_GR.SetSelText(self.GRselected)
        self.OptMenu_CA.SetSelText(self.CAselected)

    # -------------------------------------------------------------------------------------------------------------
    def Update_Sel_onTxt(self):
        QueryList = [self.Conto_Selected, self.Month_Selected, self.Tot_Selected,
                     self.TRselected,     self.GRselected,     self.CAselected ]
        self.Data.Update_Selections(QueryList, Ix_Query_List)
        self.Chat.Tx_Request([TOP_QUERY, [MAIN_WIND], UPDATE_FILES_NAME, []])

    # -------------------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_QUERY)
        self.destroy()

    # -------------------------------------------------------------------------------------------------------------
    def Set_OnTxt_TR_GR_Sel(self):
        QueriesSel = self.Data.Get_Selections_Member(Ix_Query_List)
        QueriesSel[Ix_Query_TRsel] = self.TRselected
        QueriesSel[Ix_Query_GRsel] = self.GRselected
        QueriesSel[Ix_Query_CAsel] = self.CAselected
        self.Data.Update_Selections(QueriesSel, Ix_Query_List)

    # -------------------------------------------------------------------------------------------------------------
    def Set_All_Select(self):
        self.TRselected = ALLTR
        self.OptMenu_TR.SetSelText(ALLTR)
        self.GRselected = ALLGR
        self.OptMenu_GR.SetSelText(ALLGR)
        self.CAselected = ALLCA
        self.OptMenu_CA.SetSelText(ALLCA)
        self.Set_OnTxt_TR_GR_Sel()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_ComboYear(self, Value):
        self.Dummy = 0
        CurrYear   = self.Year_Selected
        newTransact_Filename = Transact_ + str(Value) + '.db'
        Dir_Name = Get_Dir_Name(self.Data.Get_Selections_Member(Ix_Transact_File))
        Full_Filename = Dir_Name + newTransact_Filename
        # Init Transactions
        if not self.Mod_Mngr.Cek_Transactions_Name(Full_Filename):
            self.OptMenu_Year.SetValues(CurrYear)
            return
        self.Data.Update_Selections(Full_Filename, Ix_Transact_File)
        self.Chat.Tx_Request([TOP_QUERY, [MAIN_WIND], UPDATE_FILES_NAME, []])
        self.Year_Selected = Value

        if self.Mod_Mngr.Load_Transact_Mngr(TOP_QUERY, Full_Filename):
            self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Conto(self, Value):
        self.Conto_Selected = Value
        self.Update_Sel_onTxt()
        self.Load_All_Data()
        self.Set_All_Select()

    def Clk_Month(self, Value):
        self.Month_Selected = Value
        self.Tot_List       = Queries_Tot_Dict[self.Month_Selected]
        self.OptMenu_Tot.SetValues(self.Tot_List)
        self.OptMenu_Tot.SetSelText(self.Tot_Selected[0])
        self.Update_Sel_onTxt()
        self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Tot(self, Value):
        self.Tot_Selected = Value
        self.Tot_List = Queries_Tot_Dict[self.Month_Selected]
        self.Update_Sel_onTxt()
        self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Date(self, Value):
        self.Date_Selected = Value
        self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_TRsel(self, Value):
        if Value == ALLTR:
            self.Set_All_Select()
            self.Chat.Tx_Request([TOP_QUERY, [TOP_CODES_VIEW], CODE_TO_CLOSE, []])
        else:
            self.TRselected = ''
            self.GRselected = ''
            self.CAselected = ''
            Top_View_Codes(self.TR_List)
        self.Update_Sel_onTxt()
        self.Load_All_Data()

    # ------------  see above  ------------------------
    # called from TOP_CODES_VIEW on click on tree
    def TRcode_Selected_OnTopView(self, TRcode):
        self.TRselected = self.Data.Get_TrDesc_FromCode(TRcode)
        self.GRselected = ''
        self.CAselected = ''
        self.Update_Sel_onTxt()
        self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_GRsel(self, Value):
        if Value == ALLGR:
            self.Set_All_Select()
        else:
            self.GRselected = Value
            self.TRselected = ''
            self.CAselected = ''
            self.Update_Sel_onTxt()
        self.Load_All_Data()

    def Clk_CAsel(self, Value):
        if Value == ALLCA:
            self.Set_All_Select()
        else:
            self.CAselected = Value
            self.TRselected = ''
            self.GRselected = ''
            self.Update_Sel_onTxt()
        self.Load_All_Data()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_ViewTransact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT, TOP_QUERY, [])

    # -------------------------------------------------------------------------------------------------------------
    def Clk_XlsxView(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_QUERY, [])

    # -------------------------------------------------------------------------------------------------------------
    def Clk_SelXlsx(self):
        self.Mod_Mngr.Mod_Mngr_Mngr(ON_SELECTIONS)

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Summaries(self):
        pass

    # -------------------------------------------------------------------------------------------------------------
    def Convert_To_Float(self, Value):
        self.Dummy = 0
        flVal      = Value
        Type = type(Value)
        if Type is str or Type is None:
            return 0.00
        if type(Value) is int:
            flVal = float(Value)
        return flVal


    # -------------------------------------------------------------------------------------------------
    def Get_Credit_Debit(self, Rec):
        self.Dummy = 0
        Credit = self.Convert_To_Float(Rec[2])
        Debit  = self.Convert_To_Float(Rec[3])
        return [Credit, Debit]

    # ------------------------------------------------------------------------------------------------------------
    # Rec Query_View_List    : Date    TR_Desc   Accred    Addeb
    # return                  [fl, fl str, str]
    def Credit_Debit_Setup(self, Rec):
        self.Dummy = 0
        Credit     = Rec[iQuery_Accr]         # can be  float or '' or ' '
        Debit      = Rec[iQuery_Addeb]

        floatCredit = Convert_To_Float(Credit)
        floatDebit  = Convert_To_Float(Debit)

        strCredit   = Float_ToString_Setup(floatCredit)
        strDebit    = Float_ToString_Setup(floatDebit)
        CreditDebit_List = [floatCredit, floatDebit, strCredit, strDebit]
        Rec_Queries_List = [Rec[iQuery_Date], Rec[iQuery_Descr], strCredit, strDebit]
        return [Rec_Queries_List, CreditDebit_List]

# =================================================================================================================