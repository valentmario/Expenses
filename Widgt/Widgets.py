# ***************************************************************************************
#                                          Widgets.py                                   *
#     -------------------          WIDGETS  CLASSES     231003        ---------------   *
# ***************************************************************************************

from Common.Constants import *
from tkinter import ttk
import tkinter as tk

# =======================================================================================
# *****                      S T Y L E S                                            *****
# *****         Stand alone object: The styles are global                           *****
# =======================================================================================
class Widgets_Styles:
    def __init__(self):
        self.style = ttk.Style()

        # ====================   Default Style  TheButton   green    ====================
        self.style.map("DEF.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'white'), ('active', 'white'),
                        ('disabled', '#f66151')], )
        self.style.configure(style="DEF.TButton", background="#00A671",
                             foreground="white", borderwidth=1, font=("Arial", 12),
                             padding=6, relief="raised")

        # =====================  Colored  Style   TheButton  brown ======================
        self.style.map("COL.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'white'), ('active', 'white'),
                        ('disabled', '#f66151')], )
        self.style.configure(style="COL.TButton", background="#9141ac",
                             foreground=ForGnd, borderwidth=1, font=("Arial", 12),
                             padding=6, relief="raised")

        # ======================   Bold Style  TheButton   ==============================
        self.style.map("BOL.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'white'), ('active', 'white')], )
        self.style.configure(style="BOL.TButton", background='#0eaa64',
                             foreground=ForGnd,
                             borderwidth=3, font=("Arial", 13, 'bold'),
                             padding=7, relief="raised")

        # ====================   Default Style for Messages    =========================
        self.style.map("MSG.TButton",
            foreground=[('pressed', 'black'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'white'), ('active', 'white')], )
        self.style.configure(style="MSG.TButton", background='#gray',   #  "#00A671",
                             foreground='white',
                             borderwidth=1, font=("Arial", 12,),
                             padding=10, relief="raised")

        # ====================      Default Style  TheLable      ========================
        self.style.configure(style='INFO.TLabel', background='white', foreground='blue',
                             font=('Arial', 13, 'bold'), padding=4, anchor='c',
                             relief='sunken', borderwidth=3)
        self.style.configure(style='ERR.TLabel', background='#CFD956', foreground='red',
                             font=('Arial', 13, 'bold'), padding=4, anchor='c',
                             relief='sunken', borderwidth=3)

        # ========================   Style   TheTreeView       ==========================
        self.style.configure("mystyle.Treeview", highlightthickness=0,
                             bd=0, font=('Calibri', 10))
        self.style.configure("mystyle.Treeview.Heading", font=('Calibri', 10, 'bold'))
        # Remove the borders ----------------------
        self.style.layout("mystyle.Treeview",
                          [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])



# =======================================================================================
# =====================                 W I D G T E S                       =============
# =======================================================================================


# ==============================       T K      T E X T     =============================
class TheTextPoints(tk.Text):
    def __init__(self, Parent, Style, PosX, PosY, Nchar, Nrows, Texto, Points):
        super().__init__(Parent)
        self.Texto = Texto
        if Style == Txt_Disab:
            self.configure(background="#559CC2", fg='#E1E2FF', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "disabled"
        elif Style == Txt_DisBlak:
            self.configure(background="#559CC2", fg='black', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "normal"
        elif Style == Txt_Enab:    # Enabled to Insert data
            self.configure(background=Col_Mustard, fg='black', relief="sunken")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "normal"
        elif Style == Txt_MsgWhite:
            self.configure(background=Col_Mustard, fg='white', relief="sunken")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "normal"
        elif Style == Txt_MsgErr:
            self.configure(background='gray', fg='yellow', relief="sunken")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "normal"
        else:
            self.configure(background="#559CC2", fg='#E1E2FF', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "disabled"
            self.Texto = 'Text Code NOT found'

        self.Set_Text(self.Texto)
        # self.configure(padx=2,
        self.config(width=Nchar, height=Nrows)
        self.place(x=PosX, y=PosY)

    def Clear_Text(self):
        self.configure(state="normal")
        self.delete("1.0", "end")
        if self.State != "normal":
            self.configure(state='disabled')
    # ----------------------------------------------
    def Set_Text(self, myText):
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.insert('end', myText)
        if self.State != "normal":
            self.configure(state='disabled')
    # ----------------------------------------------
    def Get_Text(self, Type):
        Texto = self.get('1.0', 'end')
        if Type == INTEGER:
            if Texto == '\n' or not self.Test_Dec(Texto):
                return 0
            else:
                intTxt = Texto.replace('\n', '', 5)
            return int(intTxt)
        else:
            return Texto
    @classmethod
    def Test_Dec(cls, Texto):
        for Digit in Texto:
            if '0' <= Digit <= '9' or Digit == '\n':
                pass
            else:
                return False
        return True

# ----------------------------------------------------------------------------------------
class TheText(tk.Text):
    def __init__(self, Parent, Style, PosX, PosY, Nchar, Nrows, Texto):
        super().__init__(Parent)
        if Style == ANY:
            self.configure(state='disabled')
            self.config(width=1, height=1)
            self.place(x=xyToHide, y=xyToHide)
            return

        self.Pos_X  = PosX
        self.Pos_Y  = PosY
        self.Texto = Texto
        Points     = 11
        if Style == Txt_Disab:
            self.configure(background="#559CC2", fg='#E1E2FF', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "disabled"
        elif Style == Txt_DisBlak:
            self.configure(background="#559CC2", fg='black', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "normal"
        elif Style == Txt_Enab:    # Enabled to Insert data
            self.configure(background=Col_Mustard, fg='black', relief="sunken")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "normal"
        elif Style == Txt_MsgWhite:
            self.configure(background=Col_Mustard, fg='white', relief="sunken")
            self.configure(padx=4, pady=4, font=('Courier', Points))
            self.State = "normal"
        elif Style == Txt_MsgErr:
            self.configure(background='gray', fg='yellow', relief="sunken")
            self.configure(padx=4, pady=4, font=('Courier', Points))
            self.State = "normal"
        else:
            self.configure(background="#559CC2", fg='#E1E2FF', relief="raised")
            self.configure(padx=4, pady=4, font=('Arial', Points))
            self.State = "disabled"
            self.Texto = 'Text Code NOT found'

        self.Set_Text(self.Texto)
        # self.configure(padx=2,
        self.config(width=Nchar, height=Nrows)
        self.place(x=self.Pos_X, y=self.Pos_Y)

    def Clear_Text(self):
        self.configure(state="normal")
        self.delete("1.0", "end")
        if self.State != "normal":
            self.configure(state='disabled')
    # ----------------------------------------------
    def Set_Text(self, myText):
        self.configure(state="normal")
        self.delete("1.0", "end")
        self.insert('end', myText)
        if self.State != "normal":
            self.configure(state='disabled')
    # ----------------------------------------------
    def Get_Text(self, Type):
        Texto = self.get('1.0', 'end')
        if Type == INTEGER:
            if Texto == '\n' or not self.Test_Dec(Texto):
                return 0
            else:
                intTxt = Texto.replace('\n', '', 5)
            return int(intTxt)
        else:
            return Texto
    @classmethod
    def Test_Dec(cls, Texto):
        for Digit in Texto:
            if '0' <= Digit <= '9' or Digit == '\n':
                pass
            else:
                return False
        return True

    def PosX(self, Position_X):
        self.place(x=Position_X)

    def PosXY(self, PosX, PosY):
        self.place(x=PosX, y=PosY)

    def Text_View(self):
        self.place(x=self.Pos_X, y=self.Pos_Y)
    # -------------------------------------------
    def Text_Hide(self):
        self.place(x=xyToHide, y=xyToHide)







# ============================    T T K     L A B E L     ===============================
class TheLable(ttk.Label):
    def __init__(self, Parent, Style, PosX, PosY, nChar, Title):
        super().__init__(Parent)
        if Style == Lab_Blue:
            self.configure(style='INFO.TLabel')
        elif Style == Lab_FileSel:
            pass
        elif Style == Lab_Err:
            self.configure(style='ERR.TLabel')
        self.place(x=PosX, y=PosY)
        self.configure(width=nChar, text=Title)
    def Set_Title(self, newTitle):
        self.configure(text=newTitle)


# ===============================     T T K      B U T T O N S     ======================
class TheButton(ttk.Button):
    def __init__(self, Parent, Style, PosX, PosY, Nchar, Name, Command):
        super().__init__(Parent)
        self.PosX = PosX
        self.PosY = PosY
        self.Btn_Text = ''
        if Style == Btn_Def_Dis or Style == Btn_Def_En:
            self.config(style="DEF.TButton")
        elif Style == Btn_Col_Dis or Style == Btn_Col_En:
            self.config(style="COL.TButton")
        elif Style == Btn_Bol_Dis or Style == Btn_Bol_En:
            self.config(style="BOL.TButton")
        elif Style == Btn_Msg:
            self.configure(style='TButton')
        else:
            pass

        if Style == Btn_Def_Dis or Style == Btn_Col_Dis or Style == Btn_Bol_Dis:
            self.configure(state='disabled')
        else:
            self.configure(state='normal')

        self.Btn_Text = Name
        self.configure(text=Name, command=Command, width=Nchar)
        self.place(x=PosX, y=PosY)

    def Set_Btn_State(self, Status):
        if Status == Btn_Disab:
            self.configure(state='disabled')
        else:
            self.configure(state='normal')

    def Btn_Enable(self):
        self.configure(state='normal')

    def Btn_Disable(self):
        self.configure(state='disabled')

    def Place(self, toPlace):
        if not toPlace:
            self.place(x=xyToHide, y=xyToHide)
        else:
            self.place(x=self.PosX, y=self.PosY)
    def SetX(self, Posx):
        self.place(x=Posx)

    def Get_Text(self):
        return self.Btn_Text

    def Set_Text(self, Name):
        self.Btn_Text = Name
        self.configure(text=Name)


# ==============================     T T K     C O M B O      ===========================
class TheCombo(ttk.Combobox):
    def __init__(self, Parent, StrVar, PosX, PosY, Heigth, Nchar, List, strText, clk_Call):
        super().__init__(Parent)
        self.Dummy = 0
        self.clk_Call = clk_Call
        style = ttk.Style()
        style.theme_settings("default", {
                    "TCombobox": {
                        "configure": {"padding": 3, "borderwidth": 3},
                        "map": {
                            "background":      [("active", "white"),       # down arrow
                                                ("readonly", "green")],
                            "fieldbackground": [("readonly", "#559CC2")],  # Inside the combo
                            "foreground":      [("focus", "black"),
                                                ("readonly", "black")]
                        }
                    }},)

        self.configure(style='TCombobox', textvariable=StrVar)
        self.configure(state="readonly", values=List)
        self.configure(font=("Arial", 11), height=Heigth, width=Nchar)
        self.bind('<<ComboboxSelected>>', self.clk_Combo)
        self.SetSelText(strText)
        self.place(x=PosX, y=PosY)
        self.Dummy = 0

    def clk_Combo(self, *arg):
        self.Dummy = arg
        SelectedVal = self.get()
        self.SetSelText(SelectedVal)
        self.clk_Call(SelectedVal)

    def PosX(self, PosX):
        self.place(x=PosX)

    def SetSelText(self, Val1):
        self.set("")
        self.set(Val1)

    def SetValues(self, Values):
        self.configure(values=[' '])
        self.configure(values=Values)

    def GetValue(self):
        return self.get()
# =======================================================================================
