# ***************************************************************************************
#                                        Tree_Widg.py                                   *
#     ----------------     The  class  for  Frame Scroll and Tree        -------------  *
# ***************************************************************************************

import tkinter as tk
from tkinter import ttk
from Common.Constants import *
from Widgt.Dialogs import Message_Dlg

class TheFrame(tk.LabelFrame):
    def __init__(self, Parent, PosX, PosY, Click_On_Tree):
        super().__init__(Parent)
        self.configure(background=BakGnd, foreground='white',)
        self.configure(width=1, height=1,)
        self.configure(text='  ', labelanchor='n', padx=4, pady=4,
                       font=('Arial', 12, 'bold'))
        self.PosX = PosX
        self.PosY = PosY
        self.Clk_On_Tree = Click_On_Tree

        self.place(x=xyToHide, y=xyToHide)
        self.Tree_Scroll = ttk.Scrollbar(self)

        self.Tree_Scroll.pack(side='right', fill='y')

        self.Dummy       = None
        self.Loaded_List = []
        self.iFocus      = NoFocus
        self.iLast_Row   = 0

        self.Reply       = 0
        self.Nrows     = 1
        self.nColToVis = 1
        self.Headings  = []
        self.Anchor    = []
        self.Width     = []

        self.Tree = ttk.Treeview(self,
                                 yscrollcommand=self.Tree_Scroll.set, selectmode="browse",
                                 style="mystyle.Treeview")  # , height=1)
        self.Tree.pack()
        self.Tree_Scroll.config(command=self.Tree.yview)

        # ---------------------  Bind to Click on one row of Tree      ------------------
        # self.my_tree.bind('<Double-1>', self.DobClk_OnTree)
        self.Tree.bind('<ButtonRelease-1>', self.click_on_tree)

    # -----------------------------------------------------------------------------------
    def Frame_PosXY(self, Xpos, Ypos):
        self.place(x=Xpos, y=Ypos)

    # -----------------------------------------------------------------------------------
    def Frame_Title(self, Title):
        self.configure(text=Title)
    # -------------------------------------------
    def Frame_View(self):
        self.place(x=self.PosX, y=self.PosY)
    # -------------------------------------------
    def Frame_Hide(self):
        self.place(x=xyToHide, y=xyToHide)
    # -------------------------------------------
    def click_on_tree(self, arg):
        self.Dummy = arg
        strId = self.Tree.focus()
        if strId:
            RowValues = self.Tree.item(strId, 'values')
            self.Clk_On_Tree(RowValues)

    def Get_Index_Of_Click(self):
        strId = self.Tree.focus()
        if strId:
            return int(strId)
        return 0

    # -------------------------------------------
    def Tree_Setup(self, Form_List):
        self.Delete_All_Rows()
        self.Nrows       = Form_List[iTreeNrows]
        self.nColToVis   = Form_List[iTreeNcol]
        self.Headings    = Form_List[iTreeHead]
        self.Anchor      = Form_List[iTreeAnch]
        self.Width       = Form_List[iTreeWidth]
        self.Tree.configure(height=self.Nrows)

        self.Tree['columns'] = list(range(self.nColToVis))
        self.Tree.heading("#0", text="", anchor='w')
        self.Tree.column("#0", width=0, stretch=False)
        for jj in range(1, self.nColToVis + 1):
            self.Tree.column(f'#{jj}', width=self.Width[jj], anchor=self.Anchor[jj])
            self.Tree.heading(f'#{jj}', text=self.Headings[jj], anchor=self.Anchor[jj])

        self.Tree.tag_configure("oddrow", background="white", )
        self.Tree.tag_configure("evenrow", background="lightblue", )

    def Heading_Setup(self, Headings):
        for jj in range(1, self.nColToVis + 1):
            self.Headings = Headings[jj]
            self.Tree.heading(f'#{jj}', text=self.Headings[jj])
            pass

    # ----------------------------------  Load Values of Rows  --------------------------
    def Load_Row_Values(self, List):
        self.Tree_Scroll.pack(side='right', fill='y')
        self.Loaded_List = List
        self.Delete_All_Rows()
        count = 0
        for Row in List:
            TreeRow = []
            for i in range(0, self.nColToVis):
                Val = str(Row[i]).replace('\n', '', 5)
                if Val == 'None':
                    Val = ''
                TreeRow.append(Val)
            Tag = "evenrow"
            if count % 2:
                Tag = "oddrow"
            self.Tree.insert('', 'end', text='', iid=str(count),
                             values=TreeRow[0:], tags=Tag)
            count += 1
        if self.iFocus != NoFocus:
            self.Set_Focus(self.iFocus)

    # -------------------------------  Delete Last Row on Tree    -----------------------
    def Delete_Tree_Last_Row(self):
        List = []
        Len = len(self.Loaded_List)
        Last_Index = Len-1
        LastRec = self.Loaded_List[Last_Index]

        for i in range(0, Last_Index):
            List.append(self.Loaded_List[i])
        self.iFocus    = Last_Index-1
        self.Load_Row_Values(List)
        Mess = 'Deleted Last Record    Id:  ' + str(Last_Index)  + '\n'
        for Val in LastRec:
            Mess += str(Val)
            Mess += '     '
        Msg_Dlg = Message_Dlg(MsgBox_Info, Mess)
        Msg_Dlg.wait_window()
    #
    # -----------------------------  Inseert Record  on End   ---------------------------
    def Add_ToEnd_Tree_Values(self, Row_Rec):
        List = self.Loaded_List
        Len = len(self.Loaded_List)
        Last_Index = Len
        List.append(Row_Rec)

        iLast_Row = len(List) -1
        self.iFocus    = iLast_Row
        self.Load_Row_Values(List)
        Mess = 'Added Record    Id:     ' + str(Last_Index)  + '\n'
        for Val in Row_Rec:
            Mess += str(Val)
            Mess += '   '
        Mess += '\nat the end'
        Msg_Dlg = Message_Dlg(MsgBox_Info, Mess)
        Msg_Dlg.wait_window()

    # -----------------------------------  Update  Values  ------------------------------
    def Update_Tree_Values(self, Val_Rec_ToUpdate):
        strId = self.Tree.focus()
        if strId:
            self.iFocus = int(strId)
            RowVal = self.Tree.item(strId, 'values')
            self.Loaded_List[self.iFocus] = Val_Rec_ToUpdate
            List   = self.Loaded_List
            List[self.iFocus] = Val_Rec_ToUpdate
            self.Load_Row_Values(List)
            Mess = 'Updated Record    Id:  ' + strId + '\n'
            for Val in RowVal:
                Mess += str(Val)
                Mess += '     '
            Mess += '\n'
            for Val in Val_Rec_ToUpdate:
                Mess += str(Val)
                Mess += '     '
            Msg_Dlg = Message_Dlg(MsgBox_Info, Mess)
            Msg_Dlg.wait_window()
        else:
            Msg_Dlg = Message_Dlg(MsgBox_Info, 'NO Row Selected')
            Msg_Dlg.wait_window()

    # ----------------------------    Get / Set Focus    --------------------------------
    def Set_Focus(self, nRow):   # startig from #0
        self.Clear_Focus()
        AllRows = self.Tree.get_children()
        LenAll  = len(AllRows)
        if nRow > LenAll:
            nRow = LenAll - 1
        Id = AllRows[nRow]
        self.Tree.selection_set(Id)
        self.Tree.focus(str(Id))

    def Set_Selection(self, Sel):   # startig from #0
        self.Clear_Focus()
        self.Tree.selection_set(Sel)

    def Get_Selection(self):
        return self.Tree.selection()

    def Clear_Focus(self):
        Sel = self.Tree.selection()
        self.Tree.selection_remove(Sel)

    # def Get_Line_From_Tree(self, Ncol, Value):
    #     for Line in self.Loaded_List:
    #         if Line[Ncol] == Value:
    #             return Line
    #     return []

    # -------------------------------------------------------------------------------
    def Set_List_For_Focus(self, Start):
        myStart = Start
        newList = []
        Len = len(self.Loaded_List)
        for Index in range(0, Len):
            Rec = self.Loaded_List[myStart]
            newList.append(Rec)
            myStart += 1
            if myStart >= Len:
                myStart = 0
        self.Load_Row_Values(newList)
        self.Set_Focus(0)

    # -----------------------------------  Delete ALL Rows    ---------------------------
    def Delete_All_Rows(self):
        AllRows = self.Tree.get_children()
        for Row in AllRows:
            self.Tree.delete(Row)
# =======================================================================================
