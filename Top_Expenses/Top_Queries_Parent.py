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
class Top_Queries_Parent(tk.Toplevel):
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

