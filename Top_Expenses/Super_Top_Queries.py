# ---------------------------------------------------------------------------------- #
#               *****     Super_Top_Queries.py     *****                             #
#      the parent of Top_Queries contains attributs and some methods                 #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
import os

from Chat import Ms_Chat
from Common.Common_Functions import *
from Data_Classes.Transact_DB import Data
from Widgt.Widgets import *
from Widgt.Dialogs import Message_Dlg
from Top_Expenses.Modules_Manager import Modul_Mngr

# =================================================================================================================
class Super_Top_Queries(tk.Toplevel):
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
        self.Widg_PosX      = xyToHide
        self.Months_on_Tree = 0
        self.iStart_Month   = 0
        self.iTot_Months    = 0
        self.iEnd_Month     = 0

        # This list is loaded from Transact_DB_Table on startup or on selecting Year
        self.OneYear_Transact_List = []

        # This list is created on startup or at each Selection
        # based on Conto Year (ValDate/AccDate) TR GR CA for each month
        self.Transact_xMonth_List = [ [], [], [], [], [], [], [], [], [], [], [], [] ]

        # [Credits, Debits]  for   Frame1, Frame2, Frame3
        self.Tot_CredDeb_xTree  = [[0, 0], [0, 0], [0, 0]]

        self.Years_List  = []  # The years transactions contained on TRANSATCION directory
        self.Tot_List    = [ONE_MONTH,TWO_MONTHS,FOUR_MONTHS,SIX_MONTHS,TWELVE_MONTHS]
        self.Date_List   = [VAL_DATE, ACC_DATE]
        self.Files_Ident = []   # self.Data.Get_Xlsx_Transact_Ident()

        self.Year_Selected  = 0    # all the possible selections
        self.Conto_Selected = ''
        self.Month_Selected = ''
        self.Tot_Selected   = ''
        self.Date_Selected  = ''
        self.TRselected     = ''
        self.GRselected     = ''
        self.CAselected     = ''

        self.Total_Rows  = 0    # Total rows of selected Transactions
        self.TR_List     = []   # Codes on Year Transactions Table for OptMenu_TR
        self.GR_List     = []   # same per GR
        self.CA_List     = []   # same per CA

        # ----------------------------------    C O M B O s -------------------------------------------------------
        self.StrVar_Year  = tk.StringVar
        self.OptMenu_Year = TheCombo(self, self.StrVar_Year, self.Widg_PosX, 20, 21, 16, ['', ''],
                                      '', self.Clk_Year)

        self.StrVar_Conto  = tk.StringVar
        self.OptMenu_Conto = TheCombo(self, self.StrVar_Conto, self.Widg_PosX, 55, 21, 16, Conto_List,
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

        self.StrVar_TR  = tk.StringVar
        self.OptMenu_TR = TheCombo(self, self.StrVar_TR,      self.Widg_PosX, 240, 41, 16, self.TR_List,
                                    'Transaction code', self.Clk_TRsel)
        self.StrVar_GR  = tk.StringVar
        self.OptMenu_GR = TheCombo(self, self.StrVar_GR,     self.Widg_PosX, 275, 41, 16,  self.GR_List,
                                   'Group code', self.Clk_GRsel)
        self.StrVar_CA  = tk.StringVar
        self.OptMenu_CA = TheCombo(self,  self.StrVar_CA,    self.Widg_PosX, 310, 21, 16,  self.CA_List,
                                   'Category code', self.Clk_CAsel)

        # ---------------------------------    Buttons   ----------------------------------------------------------
        self.Btn_DB_View = TheButton(self, Btn_Def_En, self.Widg_PosX, 370, 17, 'transactions view', self.Clk_ViewTransact)
        self.Btn_xlsx_file = TheButton(self, Btn_Def_En, self.Widg_PosX, 410, 17, 'xlsx file select', self.Clk_SelXlsx)
        self.Btn_xlsx_View = TheButton(self, Btn_Def_En, self.Widg_PosX, 450, 17, 'xlsx view', self.Clk_XlsxView)

        self.Btn_Summaries = TheButton(self, Btn_Def_En, self.Widg_PosX, 660, 17, ' Summaries ', self.Clk_Summaries)
        self.Btn_Exit = TheButton(self, Btn_Bol_En, self.Widg_PosX, 936, 15, '  E X I T  ', self.Call_OnClose)
        self.OneYear_Transact_List = self.Data.Get_Transact_Table()
        self.Setup_Year_Conto_Month_Tot_Date()
        self.Set_TR_GR_CA_Sel_List()
        self.Setup_TR_GR_CA_OptManu()
        pass

    # -------------------------------------------------------------------------------------------------------------
    def Clear_Code_Sel(self):
        self.TRselected = ''
        self.GRselected = ''
        self.CAselected = ''

    # -------------------------------------------------------------------------------------------------------------
    def Create_Year_Transact_List(self):
        self.OneYear_Transact_List = self.Data.Get_Transact_Table()
        self.Transact_xMonth_List  = [ [], [], [], [], [], [], [], [], [], [], [], [] ]
        Year  = self.Year_Selected
        Conto = self.Conto_Selected
        TRsel = self.TRselected
        GRsel = self.GRselected
        CAsel = self.CAselected

    # -------------------------------------------------------------------------------------------------------------
    def Setup_Year_Conto_Month_Tot_Date(self):
        self.Years_List = self.Get_Transact_Year_List()
        self.OptMenu_Year.SetValues(self.Years_List)               # List of existing Year Transactions

        self.Files_Ident    = self.Data.Get_Xlsx_Transact_Ident()   # list created on ModulesManager
        self.Year_Selected  = self.Files_Ident[Ix_Transact_Year]
        self.OptMenu_Year.SetSelText(str(self.Year_Selected))

        Queries_Sel = self.Data.Get_Txt_Member(Ix_Query_List)
        self.Conto_Selected = Queries_Sel[Ix_Query_Conto]
        self.Month_Selected = Queries_Sel[Ix_Query_Month]
        self.Tot_Selected   = Queries_Sel[Ix_Query_TotMonths]
        self.Date_Selected  = ACC_DATE
        self.TRselected     = Queries_Sel[Ix_Query_TRsel]
        self.GRselected     = Queries_Sel[Ix_Query_GRsel]
        self.CAselected     = Queries_Sel[Ix_Query_CAsel]
        self.View_Selections()

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
        pass

    # -------------------------------------------------------------------------------------------------------------
    def Setup_TR_GR_CA_OptManu(self):
        self.OptMenu_TR.SetValues([ALLTR, SELTR])
        self.OptMenu_GR.SetValues(self.GR_List)
        self.OptMenu_CA.SetValues(self.CA_List)

        self.OptMenu_TR.SetSelText(self.TRselected)
        self.OptMenu_GR.SetSelText(self.GRselected)
        self.OptMenu_CA.SetSelText(self.CAselected)

    # -------------------------------------------------------------------------------------------------------------
    def View_Selections(self):
        self.OptMenu_Year.SetSelText(self.Year_Selected)
        self.OptMenu_Conto.SetSelText(self.Conto_Selected)
        self.OptMenu_Start.SetSelText(self.Month_Selected)
        self.OptMenu_Tot.SetSelText(self.Tot_Selected)
        self.OptMenu_TR.SetSelText(self.TRselected)
        self.OptMenu_GR.SetSelText(self.GRselected)
        self.OptMenu_CA.SetSelText(self.CAselected)
        self.Chat.Tx_Request([TOP_QUERY, [MAIN_WIND], UPDATE_FILES_NAME, []])

    # -------------------------------------------------------------------------------------------------------------
    def Update_Sel_onTxt(self):
        QueryList = [self.Conto_Selected, self.Month_Selected, self.Tot_Selected,
                     self.TRselected,     self.GRselected,     self.CAselected ]
        self.Data.Update_Txt_File(QueryList, Ix_Query_List)

    # -------------------------------------------------------------------------------------------------------------
    def Get_Transact_Year_List(self):
        Full_Transact_filename = self.Data.Get_Txt_Member(Ix_Transact_File)
        Directory  = Get_Dir_Name(Full_Transact_filename)
        Files_List = os.listdir(Directory)
        Years_List = []
        for Filename in Files_List:
            # Transact_2024.db
            strYear = Filename[9:13]
            if CheckInteger(strYear):
                iYear = int(strYear)
                Years_List.append(iYear)
        return Years_List
    # -------------------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_QUERY)
        self.destroy()

    # -------------------------------------------------------------------------------------------------------------
    def Set_OnTxt_TR_GR_Sel(self):
        QueriesSel = self.Data.Get_Txt_Member(Ix_Query_List)
        QueriesSel[Ix_Query_TRsel] = self.TRselected
        QueriesSel[Ix_Query_GRsel] = self.GRselected
        QueriesSel[Ix_Query_CAsel] = self.CAselected
        self.Data.Update_Txt_File(QueriesSel, Ix_Query_List)

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
    #  this methods are defined here but are redifined on Top_Queries
    #  this is almost the overloading on python

    def Crate_List_Transact_perMonth(self):
        pass

    def Trees_Load(self):
        pass

    def Set_Frames_Title(self):
        pass

    def Set_Geometry_Frames(self):
        pass

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Year(self, Value):
        Curr_Full_Filename = self.Data.Get_Txt_Member(Ix_Transact_File)
        Dir_Name           = Get_Dir_Name(Curr_Full_Filename)
        Full_Filename      = Dir_Name + Transact_ + str(Value) + '.db'
        File_Exists = os.path.isfile(Full_Filename)
        if not File_Exists:
            Msg = Message_Dlg(MsgBox_Err, 'The requested Transactions Db\n dosesn"t exist')
            Msg.wait_window()
            return

        self.Data.Update_Txt_File(Full_Filename, Ix_Transact_File)
        self.Year_Selected  = Value
        self.Month_Selected = JAN
        self.Tot_Selected   = ONE_MONTH
        self.Update_Sel_onTxt()
        self.View_Selections()
        self.Crate_List_Transact_perMonth()
        self.Trees_Load()
        self.Chat.Tx_Request([TOP_QUERY, [MAIN_WIND], UPDATE_FILES_NAME, []])


    # -------------------------------------------------------------------------------------------------------------
    def Clk_Conto(self, Value):
        self.Conto_Selected = Value
        self.Month_Selected = Month_Names[0]
        self.Tot_Selected   = ONE_MONTH
        self.Update_Sel_onTxt()
        self.View_Selections()
        self.Crate_List_Transact_perMonth()
        self.Trees_Load()

    def Clk_Month(self, Value):
        self.Month_Selected = Value
        self.Tot_Selected   = ONE_MONTH
        self.Tot_List       = Queries_Tot_Dict[self.Month_Selected]
        self.OptMenu_Tot.SetValues(self.Tot_List)
        self.OptMenu_Tot.SetSelText(self.Tot_Selected[0])
        self.Update_Sel_onTxt()
        self.View_Selections()
        self.Set_Geometry_Frames()
        self.Set_Frames_Title()
        # self.Crate_List_Transact_perMonth()
        self.Trees_Load()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Tot(self, Value):
        self.Tot_Selected = Value
        self.Tot_List = Queries_Tot_Dict[self.Month_Selected]
        self.Update_Sel_onTxt()
        self.View_Selections()
        self.Set_Geometry_Frames()
        self.Set_Frames_Title()
        # self.Crate_List_Transact_perMonth()
        self.Trees_Load()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_Date(self, Value):
        self.Date_Selected = Value
        self.Update_Sel_onTxt()
        self.View_Selections()
        self.Crate_List_Transact_perMonth()
        self.Trees_Load()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_TRsel(self, Value):
        if Value == ALLTR:
            self.Set_All_Select()
            self.Chat.Tx_Request([TOP_QUERY, [TOP_CODES_VIEW], CODE_TO_CLOSE, []])
        else:
            self.TRselected = ''
            self.GRselected = ''
            self.CAselected = ''
            self.Mod_Mngr.Top_Launcher(TOP_CODES_VIEW, TOP_QUERY)
        self.Update_Sel_onTxt()
        self.View_Selections()

    # ------------  see above  ------------------------
    # called from TOP_CODES_VIEW on click on tree
    def TRcode_Selected_OnTopView(self, TRcode):
        self.TRselected = self.Data.Get_TrDesc_FromCode(TRcode)
        self.GRselected = ''
        self.CAselected = ''
        self.Update_Sel_onTxt()
        self.View_Selections()
        self.Crate_List_Transact_perMonth()
        self.Trees_Load()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_GRsel(self, Value):
        if Value == ALLGR:
            self.Set_All_Select()
        else:
            self.GRselected = Value
            self.TRselected = ''
            self.CAselected = ''
        self.Update_Sel_onTxt()
        self.View_Selections()
        self.Crate_List_Transact_perMonth()
        self.Trees_Load()

    def Clk_CAsel(self, Value):
        if Value == ALLCA:
            self.Set_All_Select()
        else:
            self.CAselected = Value
            self.TRselected = ''
            self.GRselected = ''
        self.Update_Sel_onTxt()
        self.View_Selections()
        self.Crate_List_Transact_perMonth()
        self.Trees_Load()

    # -------------------------------------------------------------------------------------------------------------
    def Clk_ViewTransact(self):
        self.Mod_Mngr.Top_Launcher(TOP_VIEW_TRANSACT, TOP_QUERY)

    # -------------------------------------------------------------------------------------------------------------
    def Clk_XlsxView(self):
        self.Mod_Mngr.Top_Launcher(TOP_XLSX_VIEW, TOP_QUERY)

    # -------------------------------------------------------------------------------------------------------------
    def Clk_SelXlsx(self):
        self.Mod_Mngr.Sel_Xlsx()

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

# =================================================================================================================