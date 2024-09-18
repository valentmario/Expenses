# ----------------------------------------------------------------------------#
#                   ***  Top_GR_Codes_Mngr.py   ***                           #
#                  Window Class to  View Groups Codes                         #
#           1 Frame_GR_CA  : Groups x Category                                #
#           2 Frame_TRxGR  : Transactions x Group                             #
#           3 Frame_TRxCA  : Transactions per Category                        #
# ----------------------------------------------------------------------------#

import tkinter as tk

from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data
from Common.Common_Functions import *

from Widgt.Dialogs import Print_Received_Message
from Widgt.Tree_Widg import TheFrame
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheText
from Widgt.Widgets import TheCombo

# =============================================================================
class Top_GR_Codes_Mngr(tk.Toplevel):
    def __init__(self, Status, Data_List):
        super().__init__()
        self.Chat  = Ms_Chat
        self.Data  = Data

        self.Chat.Attach([self, TOP_GR_MNGR])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry(Top_GRcodes_geometry)
        self.title('*****     Manage Groups Codes     *****')
        self.configure(background=BakGnd)

        self.Status    = Status
        self.Data_List = Data_List
        self.Dummy     = None
        self.Value     = []

        self.GRdesc       = ''
        self.List_GRxCA   = []
        self.List_GRxCA_Full = []
        self.List_TRxGR   = []
        self.List_TRxCA   = []
        self.GRxCA_Cliked = False

        # --------------------------------  for updating Group vs. Category  --------------------------------
        self.Txt_CAcode = TheText(self, Txt_Disab, 220, 900,  2, 1, 'Cod')
        self.Txt_CAdesc = TheText(self, Txt_Enab,  250, 900, 17, 1, 'Category text')
        self.Txt_GRcode = TheText(self, Txt_Disab, 410, 900,  2, 1, 'Cod')
        self.Txt_GRdesc = TheText(self, Txt_Enab,  440, 900, 17, 1, 'Group Text')

        # ----------------------------------   Category  Combo  ---------------------------------------------
        self.ComboList = []
        for Rec in self.Data.Get_CA_Codes_Table():
            self.ComboList.append(Rec[iCA_CAdesc])
        self.StrVar    = tk.StringVar()
        self.CA_Combo  = TheCombo(self, self.StrVar, 220, 940, 25, 16,
                                  self.ComboList, 'Sel Categ by Group', self.Clk_Combo)

        # ----------------------------------    B U T T O N S     -------------------------------------------
        self.Btn_GR_Updt = TheButton(self, Btn_Def_En, 405, 940, 22, 'Update  Group-Category', self.Clk_GRupdt)
        self.Btn_GR_Updt.Btn_Disable()
        self.Btn_Exit   = TheButton(self, Btn_Bol_En,  680, 940, 11, '  E X I T ',  self.Call_OnClose)

        # ----------------------------    T R E E   of  Groups x Categories      ------------------------------
        self.Frame_GRxCA = TheFrame(self,   232,  10, self.Clk_On_GRxCA_Tree)
        self.Frame_GRxCA_Setup()

        # ----------------------------    T R E E   of  Transactions x Category  ------------------------------
        self.Frame_TRxCA = TheFrame(self,   10,  10, self.Clk_On_TRxCA_Tree)
        self.Frame_TRxCA_Setup()

        # -----------------------------    T R E E   of  Transactions x Group    ------------------------------
        self.Frame_TRxGR = TheFrame(self,  600,  10, self.Clk_On_TRxGR_Tree)
        self.Frame_TRxGR_Setup()

        self.View_Codes_Frame()

    # -------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TOP_GR_MNGR)
        self.destroy()

    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        Print_Received_Message(Transmitter_Name, TOP_MNGR, Request_Code, Values_List)
        if Request_Code == CODE_TO_CLOSE:               # Close
            self.Call_OnClose()
        elif Request_Code == CODE_CLEAR_FOCUS:          # Clear Focus
            self.Frame_TRxGR.Clear_Focus()
            self.Frame_TRxCA.Clear_Focus()
            self.Frame_GRxCA.Clear_Focus()

        elif Request_Code == CODE_CLK_ON_TR_CODES:      # Clicked on Codes Tree [TRcode]
            self.Set_Focus_On_GRxCA(int(Values_List[0]))

        elif Request_Code == CODE_CLIK_ON_XLSX:         # Clicked on Xlsx Tree  [nRow, Date]
            self.Frame_TRxGR.Clear_Focus()
            self.Frame_TRxCA.Clear_Focus()
            self.Frame_GRxCA.Clear_Focus()

        elif Request_Code == CODES_DB_UPDATED:          # Clicked on Code Update
            self.Frame_GRxCA_Setup()
            self.Frame_TRxCA_Setup()
            self.Frame_TRxGR_Setup()

        elif Request_Code == CODE_CLK_ON_TR_CODES:      # Clicked on Codes Tree [TRcode]
            self.Set_Focus_On_GRxCA(Values_List[0])

    # -------------------------------------------------------------------------------------
    def Clk_GRupdt(self):
        GRcode  = self.Txt_GRcode.Get_Text(INTEGER)
        CAcode  = self.Txt_CAcode.Get_Text(INTEGER)
        GRdesc  = self.Txt_GRdesc.Get_Text(STRING).replace('\n', '', 5)
        CAdesc  = self.Txt_CAdesc.Get_Text(STRING).replace('\n', '', 5)
        self.Data.Update_GR_CA_Rec([GRcode, GRdesc, CAcode, CAdesc])

    def Clk_Combo(self, CAdesc):
        if not self.GRxCA_Cliked:
            self.CA_Combo.SetSelText('Sel Categ by Group')
            return
        CAcode = Get_List_Item(self.Data.Get_CA_Codes_Table(), iCA_CAdesc, CAdesc, iCA_CAcode, -1)
        if CAcode == -1:
            return
        self.Txt_CAcode.Set_Text(CAcode)
        self.Txt_CAdesc.Set_Text(CAdesc)

    # -----------------------------------------------------------------------------------------------------------------
    def View_Codes_Frame(self):
        self.Frame_TRxCA.Frame_View()
        self.Frame_GRxCA.Frame_View()
        self.Frame_TRxGR.Frame_View()

        self.Frame_TRxCA.Clear_Focus()
        self.Frame_GRxCA.Clear_Focus()
        self.Frame_TRxGR.Clear_Focus()

    # ----------------------------    T R E E   of  Groups x Categories    --------------------------------------------
    def Frame_GRxCA_Setup(self):
        self.Frame_GRxCA.Frame_Title('  Groups by Category  ')
        Nrows     = 41
        nColToVis = 2
        Headings = ['#0', "Category", "Group"]
        Anchor   = ['c',   'w',        'w']
        Width    = [ 0,   170,         170]
        self.Set_GRxCA_List()
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_GRxCA.Tree_Setup(Form_List)
        self.Frame_GRxCA.Load_Row_Values(self.List_GRxCA)

    # ---------------------------------------------------------------
    def Clk_On_GRxCA_Tree(self, Values):
        self.Chat.Tx_Request([TOP_GR_MNGR, [ANY], CODE_CLEAR_FOCUS, [] ])
        GRdesc = Values[1]
        GRcode = 0
        CAcode = 0
        CAdesc = 'unknown'
        for Rec in self.Data.Get_GR_Codes_Table():
            if Rec[iGR_GRdesc] == GRdesc:
                GRcode = Rec[iGR_Grcode]
                CAcode = Rec[iGR_CAcode]
                for RecCA in self.Data.Get_CA_Codes_Table():
                    if RecCA[iCA_CAcode] == CAcode:
                        CAdesc = RecCA[iCA_CAdesc]
                        break

        for Rec in self.Data.Get_TR_Codes_Full(-1):
            if Rec[iTR_Ful_GRdesc] == GRdesc:
                GRcode = Rec[iTR_Ful_GRcode]
                CAcode = Rec[iTR_Ful_CAcode]
                CAdesc = Rec[iTR_Ful_CAdesc]
                break
        self.Set_List_TRxCA(CAcode)
        self.Frame_TRxCA.Load_Row_Values(self.List_TRxCA)
        self.Set_List_TRxGR(GRcode)
        self.Frame_TRxGR.Load_Row_Values(self.List_TRxGR)

        strLen_TRxCA = str(len(self.List_TRxCA))
        Title = '   ' +strLen_TRxCA + ' Transactions   '
        self.Frame_TRxCA.Frame_Title(Title)
        Head_TRxCA = 'by Cat: ' + CAdesc
        self.Frame_TRxCA.Tree.heading(f'#{1}', text=Head_TRxCA)

        strLen_TRxGR = str(len(self.List_TRxGR))
        Title = '   ' + strLen_TRxGR + ' Transactions   '
        self.Frame_TRxGR.Frame_Title(Title)
        Head_TRxGR = 'by Group ' + GRdesc
        self.Frame_TRxGR.Tree.heading(f'#{1}', text=Head_TRxGR)

        self.Txt_CAcode.Set_Text(str(CAcode))
        self.Txt_CAdesc.Set_Text(CAdesc)
        self.Txt_GRcode.Set_Text(str(GRcode))
        self.Txt_GRdesc.Set_Text(GRdesc)
        self.CA_Combo.SetSelText(CAdesc)
        self.GRxCA_Cliked = True
        self.Btn_GR_Updt.Btn_Enable()

    # ----------------------------    T R E E   of  TRdesc x CAdesc    ------------------------------------------------
    def Frame_TRxCA_Setup(self):
        self.Frame_TRxCA.Frame_Title(' Transactions  ')
        self.Dummy = 0
        Nrows = 41
        nColToVis = 1
        Headings  = ['#0', ' ']
        Anchor    = ['c',   'w']
        Width     = [ 0,   190]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_TRxCA.Tree_Setup(Form_List)

    # ---------------------------------------------------------------
    def Clk_On_TRxCA_Tree(self,Values):
        TRdesc     = Values[0]
        TR_Full    = Get_List_Record(self.Data.Get_TR_Codes_Full(-1), iTR_Ful_TRdesc, TRdesc, [])
        if TR_Full:
            # StrTR = TR_Full[iTR_Ful_TRdesc]
            # self.Frame_TRxGR.Load_Row_Values([[StrTR]])
            GRdesc = TR_Full[iTR_Ful_GRdesc]
            Index = Get_List_Index(self.List_GRxCA, 1, GRdesc, -1)
            if Index != -1:
                self.Frame_GRxCA.Set_Focus(Index)
                self.Txt_CAcode.Set_Text(str(TR_Full[iTR_Ful_CAcode]))
                self.Txt_CAdesc.Set_Text(TR_Full[iTR_Ful_CAdesc])
                self.Txt_GRcode.Set_Text(str(TR_Full[iTR_Ful_GRdesc]))
                self.Txt_GRdesc.Set_Text(TR_Full[iTR_Ful_GRdesc])
                self.CA_Combo.SetSelText(TR_Full[iTR_Ful_CAdesc])
                self.GRxCA_Cliked = True
                self.Btn_GR_Updt.Btn_Enable()
                # TrCode = int(TR_Full[iTR_TRcode])
                # self.Chat.Tx_Request([TOP_GR_MNGR, [TOP_MNGR], CODE_CLK_ON_TR_CODES, [TrCode]])

    # --------------------    T R E E   of  TRcodes x GRcode   --------------------------------------------------------
    def Frame_TRxGR_Setup(self):
        self.Frame_TRxGR.Frame_Title(' Transactions x groups ')
        Nrows = 41
        nColToVis = 1
        Headings = ['#0', '']
        Anchor = ['c', 'w']
        Width = [0, 190]
        Form_List = [Nrows, nColToVis, Headings, Anchor, Width]
        self.Frame_TRxGR.Tree_Setup(Form_List)

    def Clk_On_TRxGR_Tree(self, Values):
        pass
        # TRdesc     = Values[0]
        # TR_Full    = Get_List_Record(self.Data.Get_TR_Codes_Full(-1), iTR_Ful_TRdesc, TRdesc, [])
        # if TR_Full:
        #     StrTR = TR_Full[iTR_Ful_TRdesc]
        #     self.Frame_TRxGR.Load_Row_Values([[StrTR]])
        #     GRdesc = TR_Full[iTR_Ful_GRdesc]
        #     Index = Get_List_Index(self.List_GRxCA, 1, GRdesc, -1)
        #     if Index != -1:
        #         self.Frame_GRxCA.Set_Focus(Index)
        #         TrCode = int(TR_Full[iTR_TRcode])
                # self.Chat.Tx_Request([TOP_GR_MNGR, [TOP_MNGR], CODE_CLK_ON_TR_CODES, [TrCode]])

    # ---------------------------------------------------------------
    def Set_GRxCA_List(self):
        self.List_GRxCA_Full = []
        for RecCA in self.Data.Get_CA_Codes_Ordered():
            CAcode  = RecCA[0]
            CAdescr = RecCA[1]
            Found = False
            for RecGR in self.Data.GR_Codes_Ordered:
                if RecGR[iGR_CAcode] == CAcode:
                    self.List_GRxCA_Full.append([CAdescr, RecGR[iGR_GRdesc]])
                    Found = True
            if not Found:
                self.List_GRxCA_Full.append([CAdescr, ''])
        # --------------------------------------------
        self.List_GRxCA = []
        CUrrent_Descr = ''
        for RecordCA in self.List_GRxCA_Full:
            CAdescr = RecordCA[0]
            if CAdescr != CUrrent_Descr:
                CUrrent_Descr = CAdescr
            else:
                CAdescr = ''
            RecordCA = [CAdescr, RecordCA[1]]
            self.List_GRxCA.append(RecordCA)

    def Set_List_TRxCA(self, Cacode):
        self.List_TRxCA = []
        for Rec in self.Data.Get_TR_Codes_Full(-1):
            if Rec[iTR_Ful_CAcode] == Cacode:
                self.List_TRxCA.append([Rec[iTR_Ful_TRdesc]])
        self.List_TRxCA.sort()

    def Set_List_TRxGR(self, GRcode):
        self.List_TRxGR = []
        for Rec in self.Data.Get_TR_Codes_Full(-1):
            if Rec[iTR_Ful_GRcode] == GRcode:
                self.List_TRxGR.append([Rec[iTR_Ful_TRdesc]])
        self.List_TRxGR.sort()

    def Set_Focus_On_GRxCA(self, TRcode):
        Full_Rec = Get_List_Record(self.Data.Get_TR_Codes_Full, iTR_Ful_TRcode, TRcode, [])
        if not Full_Rec:
            return
        GRdesc = Full_Rec[iTR_Ful_GRdesc]
        TRdesc = Full_Rec[iTR_Ful_TRdesc]
        index = Get_List_Index(self.List_GRxCA, 1, GRdesc, -1)
        if index == -1:
            return
        self.Frame_GRxCA.Set_Focus(index)
        index = Get_List_Index(self.List_TRxCA, 0, TRdesc, -1)
        if index != -1:
            self.Frame_TRxCA.Set_Focus(index)
        index = Get_List_Index(self.List_TRxGR, 0, TRdesc, -1)
        if index != -1:
            self.Frame_TRxGR.Set_Focus(index)
# ***************************************************************************************
