# -------------------------------------------------------------------------------------- #
#                                 Dialogs.py                                             #
#     -------------------     Messsages   Dialog      ---------------                    #
# -------------------------------------------------------------------------------------- #

import tkinter as tk
from Widgt.Widgets import TheText
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheCombo

# =======================   M E S S A G E      D I A L O G       ========================
#  1...44      1 line       1..22 \n  one line

class Message_Dlg(tk.Toplevel):
    def __init__(self, Option, Texto):
        super().__init__()
        self.resizable(False, False)
        self.geometry('470x650') # +100+500')

        self.title('Modal  Dialog')
        self.configure(bg='lightblue')
        self.Texto = ''
        self.data  = ' '
        self.MaxChar_xLine = 46     #  VERY IMPORTANT for nLines count

        if Texto[-1] == '\n':
            self.Txt = Texto[:-1]
        else:
            self.Txt = Texto

        self.Nchar_xLine      = self.MaxChar_xLine
        self.nLine            = 1
        self.nCharCount_xLine = 0

        for Char in self.Txt:
            self.Texto += Char
            self.nCharCount_xLine += 1
            if self.nCharCount_xLine >= self.MaxChar_xLine:    # self.Nchar_xLine:
                self.nCharCount_xLine = 0
                self.nLine += 1
            if Char == '\n':
                self.nCharCount_xLine = 0
                self.nLine           += 1
                if self.nLine        > 80:
                    break
        self.nLine += 2
        VertFlot  = float(self.nLine) * 14.5
        Vert_Delt = int(VertFlot)
        Btn_Xpos  = 280
        Btn_Ypos  = 60  + Vert_Delt
        VertYgeo  = 120 + Vert_Delt
        self.geometry('450x' + str(VertYgeo)+'+900+50')

        if Option == MsgBox_Info:
            self.title('Info Message')
            TheText(self, Txt_MsgWhite, 10, 10, self.MaxChar_xLine, self.nLine, self.Texto)
            TheButton(self, Btn_Def_En, Btn_Xpos, Btn_Ypos, 15, 'OK', self.Clk_OK)

        elif Option == MsgBox_Err:
            self.title('E R R O R   Message')
            TheText(self, Txt_MsgErr,   10, 10, self.MaxChar_xLine, self.nLine, self.Texto)
            TheButton(self, Btn_Def_En, Btn_Xpos, Btn_Ypos, 15, 'OK', self.Clk_OK)

        elif Option == MsgBox_Ask:
            self.title('YES  NO  Selection Request')
            self.Texto += ' ?'
            TheText(self, Txt_MsgWhite, 10, 10, self.MaxChar_xLine, self.nLine, self.Texto)
            # TheText(self, Txt_MsgWhite,  self.MaxChar_xLine, self.MaxChar_xLine, self.Texto)
            TheButton(self, Btn_Def_En, Btn_Xpos, Btn_Ypos, 15, 'YES', self.Clk_YES)
            TheButton(self, Btn_Def_En,  20, Btn_Ypos,  15, 'NO', self.Clk_NO)

        else:
            self.title('FATAL ERROR\n!!!  Message type unknown   !!!')
            TheText(self,   Txt_MsgErr,  43, 20, self.Nchar_xLine, self.nLine, 'Message Code NOT FOUND')
            TheButton(self, Btn_Def_En, 260, Btn_Ypos, 15, 'OK', self.Clk_OK)
        self.wait_visibility()
        self.grab_set()
        self.transient()
        pass

    def Clk_OK(self):
        self.data = OK
        self.grab_release()
        self.destroy()

    def Clk_YES(self):
        self.data = YES
        self.grab_release()
        self.destroy()

    def Clk_NO(self):
        self.data = NO
        self.grab_release()
        self.destroy()

# ================================================================================= #
#                  *****      Top_View_Message.py      *****                        #
# ================================================================================= #

import tkinter as tk

from Common.Common_Functions import *
from Chat import Ms_Chat
from Widgt.Widgets import TheButton
from Widgt.Widgets import TheTextPoints


class View_Message(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.Chat = Ms_Chat

        self.Chat.Attach([self, TOP_XLSX_VIEW])
        self.protocol('WM_DELETE_WINDOW', self.Call_OnClose)

        self.resizable(False, False)
        self.geometry(Top_View_Mess_geometry)
        self.title('***   Show  message   *** ')
        self.configure(background=BakGnd)
        Messg = List[0]
        if len(List) > 1:
            pass
        self.Txt1 = TheTextPoints(self, Txt_Disab,  20, 20, 50, 20, Messg, 11)
        TheButton(self, Btn_Def_En, 270, 410, 16, 'E X I T ', self.Call_OnClose)
        pass

    # ----------------------------------------------------------------------------- #
    def Call_OnClose(self):
        self.Chat.Detach(TOP_XLSX_VIEW)
        self.destroy()

    def Share_Msg_on_Chat(self, Transmitter_Name, Request_Code, Values_List):
        pass


# =======================   C O M B O       D I A L O G       ========================
class Combo_Dlg(tk.Toplevel):
    def __init__(self, List):
        super().__init__()
        self.resizable(False, False)
        self.title('Combo  Dialog')
        self.configure(bg='lightblue')
        self.data = 'None'
        self.geometry('440x130+900+400')
        self.title('Combo Dialog')
        TheText(self, Txt_Disab, 80, 25, 17, 1, 'Make a selection')
        self.StrVar = tk.StringVar()
        self.Combo = TheCombo(self, self.StrVar, 260, 25, 20, 14, List, ' Select year  ', self.Clk_Combo)
        TheButton(self, Btn_Def_En, 260, 65, 15, 'OK', self.Clk_OK)

        self.wait_visibility()
        self.grab_set()
        self.transient()

    # -------------------------------------------------------------------------
    def Clk_OK(self):
        self.grab_release()
        self.destroy()

    def Clk_Combo(self, Val):
        self.data = Val

# =================================================================================

from Data_Classes.Transact_DB import Data_Manager

# =======================   F I L E     D I A L O G       ========================
class File_Dialog(tk.Toplevel):
    def __init__(self, Option):
        super().__init__()
        self.resizable(False, False)
        self.geometry('500x380+800+100')
        self.title('File Select  Dialog')
        self.configure(bg='white')
        self.Data = Data_Manager

        self.FileName = ''
        if Option == FileBox_Codes:
            Full_filename = self.Data.Sel_Codes_OnData(self)
            self.FileName = Full_filename

        elif Option == FileBox_Xlsx:
            Full_filename = self.Data.Sel_Xlsx_OnData(self)
            self.FileName = Full_filename

        elif Option == FileBox_Transact:
            Full_filename = self.Data.Sel_Transact_OnData(self)
            self.FileName = Full_filename

        self.destroy()
        return

# ==============================================================================