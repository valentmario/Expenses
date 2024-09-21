# ---------------------------------------------------------------------------------- #
#            *****     Super_Top_Codes_Mngr.py     *****                             #
#                        VIEW  DELETE  ADD  UPDATE                                   #
#      List_Rows_WithoutCode : nRow    Date      FullDesc                            #
#      List View Codes       : TRcode  TR_Desc   GR_Desc  CA_Desc  StrToSearch       #
# ---------------------------------------------------------------------------------- #

import tkinter as tk
from Common.Common_Functions import *
from Chat import Ms_Chat
from Data_Classes.Transact_DB import Data

from Widgt.Dialogs import Message_Dlg
from Widgt.Widgets import TheText
from Widgt.Widgets import TheCombo

# -------------------------------------------------------------------------------------------------
class Super_Top_Mngr(tk.Toplevel):
    def __init__(self, Result, List):
        super().__init__()
        self.Chat = Ms_Chat
        self.Data = Data
        self.Chat.Attach([self, TOP_MNGR])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry('5x5+900+600')
        self.title('*****     Transactions  Codes  Manager     *****')
        self.configure(background=BakGnd)

        self.Clicked_Mod_Code = 0  # 0=Off  1=Insert-Add  2=Update
        self.Txt_TR_Code = None
        self.GR_Code     = None
        self.CA_Code     = None

        # --------------------------------     C O M B O s           ------------------------------
        self.StrVar_Conto  = tk.StringVar
        # self.OptMenu_Conto = TheCombo(self, self.StrVar_Conto, self.Widg_PosX,  55, 21, 16, Conto_List,
        #                              FIDEU, self.Clk_Conto)
        self.StrVar    = tk.StringVar()
        self.GR_Combo  = TheCombo(self, self.StrVar, xyToHide, xyToHide, 1, 1, [], '', self.Clk_Combo)

        # --------------------------------------  TEXT Boxes  -------------------------------------
        self.Txt_StrFullDesc = TheText(self, ANY, 0, 0, 0, 0, '')
        self.Txt_StrToSerc   = TheText(self, ANY, 0, 0, 0, 0, '')
        self.Txt_TR_Desc     = TheText(self, ANY, 0, 0, 0, 0, '')
        self.Txt_TR_Code     = TheText(self, ANY, 0, 0, 0, 0, '')

        self.Txt_GR_Code     = TheText(self, ANY, 0, 0, 0, 0, '')
        self.Txt_CA_Code     = TheText(self, ANY, 0, 0, 0, 0, '')
        self.Txt_CAdesc      = TheText(self, ANY, 0, 0, 0, 0, '')

    # ---------------------------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Tx_Request([TOP_MNGR, [TOP_XLSX_VIEW, TOP_GR_MNGR, TOP_CODES_VIEW], CODE_TO_CLOSE, []])
        self.Chat.Detach(TOP_MNGR)
        self.destroy()

    # -----------------------------------------------------------------------------------------------
    def Clk_Combo(self, GRdesc):
        if self.Clicked_Mod_Code == 0:
            self.GR_Combo.SetSelText('Select  Group')
        else:

            GRrec = Get_List_Record(self.Data.Get_GR_Codes_Table(), iGR_GRdesc, GRdesc, [])
            if not GRrec:
                return
            CAcode = GRrec[iGR_CAcode]
            CArec = Get_List_Record(self.Data.Get_CA_Codes_Table(), iCA_CAcode, CAcode, -1)
            if not CArec:
                return
            self.Txt_GR_Code.Set_Text(GRrec[iGR_Grcode])
            self.Txt_CA_Code.Set_Text(CArec[iCA_CAcode])
            self.Txt_CAdesc.Set_Text(CArec[iCA_CAdesc])

    # ------------------------     ***   Delete  the last Tr Record      --------------------------
    def Delete_Code_Record(self):
        Last_Rec  = self.Data.Get_Last_TRrec()
        Last_Code = int(Last_Rec[0])
        Descrip   = Last_Rec[iTR_TRdesc]
        Msg = 'DELETE  Code '
        Msg += str(Last_Code) + '\n' + Descrip
        Msg_Dlg = Message_Dlg(MsgBox_Ask, Msg)
        Msg_Dlg.wait_window()
        Reply = Msg_Dlg.data
        if Reply != YES:
            return NONE
        else:
            # -------------  Delete Transact Code ------------------------
            Result = self.Data.Delete_Last_TR_Code(Last_Code)
            if Result != OK:
                return Result

        Result = self.Data.Load_Codes_Table()
        if Result != OK:
            errMessage = 'ERRON on reloading codes dababase\nafter a delete operation\n\n'
            errMessage += Result
            return errMessage

        Result = self.Data.Check_If_Code_Exist(Last_Code)    # check if record has canceled
        if Result:
            Msg = ('Code ' + str(Last_Code) + '  ' + Descrip + '\n NOT  deleted ???')
            return Msg
        else:
            return OK

    # ------------------------     ***   Add new code Record  the last Tr Record      -------------
    def Add_Record_Code(self):
        TR_Code = self.Txt_TR_Code.Get_Text(INTEGER)
        GR_Code = self.Txt_GR_Code.Get_Text(INTEGER)
        CA_Code = self.Txt_CA_Code.Get_Text(INTEGER)
        TR_Desc_Full = self.Txt_TR_Desc.Get_Text('Str')
        TR_Desc = TR_Desc_Full.replace('\n', '', 5)
        StringToSearch = self.Txt_StrToSerc.Get_Text('Str').replace('\n', '', 5)
        String_FullDesc = self.Txt_StrFullDesc.Get_Text('Str').replace('\n', '', 5)
        TR_Record = [TR_Code, GR_Code, CA_Code, TR_Desc, StringToSearch, String_FullDesc]

        Result = self.Data.Check_Codes_Record_Is_OK(TR_Record)  # Check if data of record are OK
        if Result != OK:
            return Result

        if self.Data.Check_If_Code_Exist(TR_Code):
            return 'The code number exists\nand can not be inserted'

        Msg = 'Confirm to add Code  ' + str(TR_Code)
        Msg += '\nDescription  : ' + str(TR_Desc)
        Msg_Dlg = Message_Dlg(MsgBox_Ask, Msg)
        Msg_Dlg.wait_window()
        Reply = Msg_Dlg.data
        if Reply != YES:
            return NONE
        else:
            # -------------  Add Transact Code ------------------------
            Result = self.Data.Add_TR_Record(TR_Record)
            if Result != OK:
                errMessage = 'ERRON on reloading codes dababase\nafter a delete operation\n\n'
                errMessage += Result
                return errMessage
            Result = self.Data.Load_Codes_Table()
            if Result != OK:
                errMessage = 'ERRON on reloading codes dababase\nafter a delete operation\n\n'
                errMessage += Result
                return errMessage

            self.Chat.Tx_Request([TOP_MNGR, [ANY],  CODES_DB_UPDATED, []])

            if not self.Data.Check_If_Code_Exist(TR_Code):  # check if record has canceled
                Msg = ('Code ' + str(TR_Code) + '  ' + TR_Desc + '\n NOT  added ???')
                return Msg
            else:
                return OK

    # ------------------------     ***   Update TR code Record      -------------------------------
    def Update_Record_Code(self):
        TR_Code = self.Txt_TR_Code.Get_Text(INTEGER)
        GR_Code = self.Txt_GR_Code.Get_Text(INTEGER)
        CA_Code = self.Txt_CA_Code.Get_Text(INTEGER)

        TR_Desc = self.Txt_TR_Desc.Get_Text('Str').replace('\n', '', 5)
        StringToSearch     = self.Txt_StrToSerc.Get_Text('Str').replace('\n', '', 5)
        FullDesc           = self.Txt_StrFullDesc.Get_Text('str')
        # --------------------------------------------------------------------------------
        TR_Record_ToUpdate = [TR_Code, GR_Code, CA_Code, TR_Desc, StringToSearch, FullDesc]
        # ---------------------------------------------------------------------------------
        Result = self.Data.Check_Codes_Record_Is_OK(TR_Record_ToUpdate)  # Check if data of record are OK
        if Result != OK:
            return Result
        Msg = 'Confirm update Code:  '
        Msg += str(TR_Code) + '\nDescription: ' + TR_Desc
        Msg_Dlg = Message_Dlg(MsgBox_Ask, Msg)
        Msg_Dlg.wait_window()
        Reply = Msg_Dlg.data
        if Reply != YES:
            return NONE
        else:
            # -------------  Update Transact Code ------------------------
            Result = self.Data.Update_DB_TR_Codes(TR_Record_ToUpdate)
            if Result != OK:
                errMessage = 'ERRON on reloading codes dababase\nafter a delete operation\n\n'
                errMessage += Result
                return errMessage
            Result = self.Data.Load_Codes_Table()
            if Result != OK:
                errMessage = 'ERRON on reloading codes dababase\nafter a delete operation\n\n'
                errMessage += Result
                return errMessage
            else:
                return OK

    # -----------------------------------------------------------------------------------------------------------
    def View_Descr_Text(self, TRstrCode, GRcombo):
        TRcode = int(TRstrCode)
        TR_Full_Code = self.Data.Get_TR_Codes_Full(-1)
        TRfullRec = Get_List_Record(TR_Full_Code, iTR_Ful_TRcode, TRcode, [])
        if not TRfullRec:
            return
        self.Txt_TR_Code.Set_Text(TRcode)
        self.Txt_GR_Code.Set_Text(TRfullRec[iTR_Ful_GRcode])
        self.Txt_CA_Code.Set_Text(TRfullRec[iTR_Ful_CAcode])
        self.Txt_TR_Desc.Set_Text(TRfullRec[iTR_Ful_TRdesc])
        self.Txt_StrToSerc.Set_Text(TRfullRec[iTR_Ful_TRsearc])
        self.Txt_StrFullDesc.Set_Text(TRfullRec[iTR_Ful_TRful])
        self.Txt_CA_Code.Set_Text(TRfullRec[iTR_Ful_CAcode])
        self.Txt_CAdesc.Set_Text(TRfullRec[iTR_Ful_CAdesc])
        GRdesc = TRfullRec[iTR_Ful_GRdesc]
        GRcombo.SetSelText(GRdesc)

    # -------------------------------------------------------------------------------------------------------
    def Clear_Only_Text_Widg(self):
        self.Txt_StrFullDesc.Set_Text('')
        self.Txt_StrToSerc.Set_Text('')
        self.Txt_TR_Desc.Set_Text('')
        self.Txt_TR_Code.Set_Text('')
        self.Txt_GR_Code.Set_Text('')
        self.Txt_CA_Code.Set_Text('')

        self.Txt_TR_Code.Set_Text(0)
        self.Txt_GR_Code.Set_Text(0)
        self.Txt_CA_Code.Set_Text(0)

    # ============================================================================================================
