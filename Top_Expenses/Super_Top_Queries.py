# ---------------------------------------------------------------------------------- #
#               *****     Super_Top_Queries.py     *****                            #
#      the parent of Top_Queries contains attributs and some methods                 #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
import os
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
        # self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)
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

        self.Years_List  = []
        self.Tot_List    = [ONE_MONTH,TWO_MONTHS,FOUR_MONTHS,SIX_MONTHS,TWELVE_MONTHS]
        self.Date_List   = [VAL_DATE, ACC_DATE]
        self.Files_Ident = self.Data.Get_Xlsx_Transact_Ident()

        self.Year_Selected  = self.Files_Ident[Ix_Transact_Year]
        self.Conto_Selected = ''
        self.Month_Selected = ''
        self.Tot_Selected   = ''
        self.Date_Selected  = ''
        self.TRselected     = ''
        self.GRselected     = ''
        self.CAselected     = ''

        self.Total_Rows  = 0    # The rows in the Trees Months
        self.TR_List     = []
        self.GR_List     = []
        self.CA_List     = []
        self.Total_xCode = []       # [totTR. totGR, totCA]

        self.StrVar_Year  = tk.StringVar
        self.OptMenu_Year = TheCombo(self, self.StrVar_Year, self.Widg_PosX, 20, 21, 16, ['2023', '2024'],
                                      '2023', self.Clk_Year)

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

        # ---------------------------------    Buttons   --------------------------------------------------------------
        self.Btn_Transact_view = TheButton(self, Btn_Def_En, self.Widg_PosX, 370, 17, 'transactions view',
                                           self.Clk_ViewTransact)
        self.Btn_xlsx_file = TheButton(self, Btn_Def_En, self.Widg_PosX, 410, 17, 'xlsx file select', self.Clk_SelXlsx)
        self.Btn_xlsx_View = TheButton(self, Btn_Def_En, self.Widg_PosX, 450, 17, 'xlsx view', self.Clk_XlsxView)

        self.Btn_Summaries = TheButton(self, Btn_Def_En, self.Widg_PosX, 660, 17, ' Summaries ', self.Clk_Summaries)
        self.Btn_Exit = TheButton(self, Btn_Bol_En, self.Widg_PosX, 936, 15, '  E X I T  ', self.Call_OnClose)
        self.View_Year_Conto_Month_Tot_Date()

    # -------------------------------------------------------------------------------------------------------------
    def View_Year_Conto_Month_Tot_Date(self):
        self.Get_Transact_Year_List()
        self.OptMenu_Year.SetValues(self.Years_List)
        self.Files_Ident    = self.Data.Get_Xlsx_Transact_Ident()
        self.Year_Selected  = self.Files_Ident[Ix_Transact_Year]
        self.OptMenu_Year.SetSelText(str(self.Year_Selected))

        Queries_Sel = self.Data.Get_Txt_Member(Ix_Query_List)

        self.Conto_Selected = Queries_Sel[Ix_Query_Conto]
        self.Month_Selected = Queries_Sel[Ix_Query_Month]
        strTot_Months       = Queries_Sel[Ix_Query_TotMonths]
        # iTotMonths          = TOT_MONTH_INT[str]
        pass
        self.Date_Selected = Queries_Sel[Ix_Query_Month]

        self.TRselected     = ''
        self.GRselected     = ''
        self.CAselected     = ''
        pass

    # -------------------------------------------------------------------------------------------------
    def Get_Transact_Year_List(self):
        Full_Transact_filename = self.Data.Get_Txt_Member(Ix_Transact_File)
        Directory  = Get_Dir_Name(Full_Transact_filename)
        Files_List = os.listdir(Directory)
        self.Years_List = []
        for Filename in Files_List:
            # Transact_2024.db
            strYear = Filename[9:13]
            if CheckInteger(strYear):
                iYear = int(strYear)
                self.Years_List.append(iYear)
            pass
        pass


    # -------------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_QUERY)
        self.destroy()

    # -------------------------------------------------------------------------------------------------
    def Clk_Year(self, Value):
        pass

    def Clk_Conto(self, Value):
        pass

    def Clk_Month(self, Value):
       pass

    def Clk_Tot(self, Value):
        pass

    def Clk_Date(self, Value):
        pass

    def Clk_TRsel(self, Value):
        pass

    def Clk_GRsel(self, Value):
        pass

    def Clk_CAsel(self, Value):
        pass


    def Clk_ViewTransact(self):
        pass

    def Clk_SelXlsx(self):
        pass

    def Clk_XlsxView(self):
        pass

    def Clk_Summaries(self):
        pass

# =======================================================================================