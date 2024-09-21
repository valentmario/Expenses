# =========================================================================== #
#            -----   Filesnames_Mngr.py   -----                               #
#   files names managed:                                                              #
#      Files_Names.txt                                                        #
#      Codes_DB.db                                                            #
#      Xlsx_filex.xlsx                                                        #
#      Transact.db                                                            #
#  Classes inheritance:                                                       #
#  Files_Names_Mngr <-- Codes_DB <-- Xlsx_Manager <-- Transact_DB             #
#  Data = Transact_DB()                                                       #
#                                                                             #
#  for more informations see Data_Organization.txt                            #
# =========================================================================== #

import os
import tkinter as tk
from tkinter import filedialog
from Common.Common_Functions import *
from datetime import datetime

# ---------------------------------------------------------------------------------------
class Files_Names_Manager:
    def __init__(self):
        self.Dummy = 0   # to avoid @classmethod
        # '/home/mario/aExpen_Init/Selections'
        self._Selections_List    = []
        self._Codes_DB_Filename  = UNKNOWN
        self._Xlsx_Filename      = UNKNOWN
        self.Sheet_Name          = UNKNOWN
        self._Work_Sheet         = None
        self._Transact_DB_Filename = UNKNOWN
        self._Files_Loaded       = [False, False, False, False] # Codes_Db, Xlsx_Rows, Xlsx_Lists, Transact_Db

        self._Xlsx_Conto    = None  # or on selecting new file  FIDEU_2024_01.xlsx
        self._Xlsx_Year     = None  # they are  calculated on startup
        self._Xlsx_Month    = None
        self._Transact_Year = None  # or on selecting new file  Transact_2024

        self.Curr_Year  = datetime.now().year    # to max years history setup
        self.Curr_Month = datetime.now().month
        self.Min_Year = self.Curr_Year - 9
        self.Max_Year = self.Curr_Year + 1

    # -------------------------------------------------------------------------------------
    def Get_Files_Loaded_Stat(self, Index):
        return self._Files_Loaded[Index]

    def Set_Files_Lodad(self, Index, Status):
        self._Files_Loaded[Index] = Status
        pass

    # ----------------------------------------------------------------------------------- #
    #            ----------------      public   methods   -----------------               #
    # ----------------------------------------------------------------------------------- #
    def Check_Create_Selections(self):
        if not os.path.exists(Selections_Full_Name):
            if not os.path.isdir(Selections_Dir_Name):
                os.mkdir(Selections_Dir_Name)
            Selections = open(Selections_Full_Name, "w")
            Selections.write("")
            Selections.close()
            Selections = open(Selections_Full_Name, "a")
            # Casting the list to a string before writing
            Selections.write(str(Default_Selections_List))  # Write default Files_Names.txt
            Selections.close()
            self._Selections_List = Default_Selections_List
            return NEW
        else:  # ---  Files_Names.txt exists ----
            self._Read_Selections()
            return OK

    def Get_Selections_Member(self, Index):
        return self._Selections_List[Index]

    def Get_TopToStart_List(self):
        return self._Selections_List[Ix_TOP_ToStart]

    def Read_Selections(self):        # used only on Settings
        self._Read_Selections()
        return self._Selections_List

    # -----------------------------------------------------------------------------------
    def Update_Selections(self, Value, Index):     # Update an Item
        self._Update_Selections(Value, Index)
        pass

    # -----------------------------------------------------------------------------------
    def Update_Query_List(self, Value, Index):
        Query_List = self._Selections_List[Ix_Query_List]
        Query_List[Index]            = Value
        self._Selections_List[Ix_Query_List] = Query_List
        self._Update_Selections(Query_List, Ix_Query_List)

    # ----------------------------------------------------------------------------------
    def Sel_Codes_OnData(self, Parent):
        Init_Directory = Default_Init_Dir
        if self._Codes_DB_Filename != UNKNOWN:
            Init_Directory = Get_Dir_Name(self._Codes_DB_Filename)
        # -----------------------------------------------------
        Full_filename = tk.filedialog.askopenfilename(parent=Parent,
            title='Select codes database',
            filetypes=[('db file', '*.db')],
            initialdir=Init_Directory)
        # -----------------------------------------------------
        if not Full_filename:
            return ''
        return Full_filename

    # ----------------------------------------------------------------------------------
    def Sel_Xlsx_OnData(self, Parent):
        Init_Directory = Default_Init_Dir
        if self._Xlsx_Filename != UNKNOWN:
            Init_Directory = Get_Dir_Name(self._Xlsx_Filename)



        # -----------------------------------------------------
        Full_filename = tk.filedialog.askopenfilename(parent=Parent,
            title='Select xlsx file',
            filetypes=[('xlsx file', '*.xlsx')],
            initialdir=Init_Directory)
        # -----------------------------------------------------
        if not Full_filename:
            return ''
        return Full_filename

    # ----------------------------------------------------------------------------------
    def Sel_Transact_OnData(self, Parent):
        Init_Directory = Default_Init_Dir
        if self._Transact_DB_Filename != UNKNOWN:
            Init_Directory = Get_Dir_Name(self._Transact_DB_Filename)
        # -----------------------------------------------------
        Full_filename = tk.filedialog.askopenfilename(parent=Parent,
            title='Select transactions database',
            filetypes=[('db file', '*.db')],
            initialdir=Init_Directory)
        # -----------------------------------------------------
        if not Full_filename:
            return ''
        return Full_filename

    # -------------------------------------------------------------------------------------
    def Get_Xls_CommonDir(self):
        nSlash = []
        Count  = -1
        for Char in self._Xlsx_Filename:
            Count = Count + 1
            if Char == '/':
                nSlash.append(Count)
        Len_nSlash = len(nSlash)
        if Len_nSlash < 4:
            return False
        IndexCommon = nSlash[Len_nSlash-3]
        CommonXlsx = self._Xlsx_Filename[0:IndexCommon]
        return CommonXlsx

    # -------------------------------------------------------------------------------------
    def Get_Transact_CommonDir(self):
        nSlash = []
        Count  = -1
        for Char in self._Transact_DB_Filename:
            Count = Count + 1
            if Char == '/':
                nSlash.append(Count)
        Len_nSlash = len(nSlash)
        if Len_nSlash < 4:
            return False
        IndexCommon = nSlash[Len_nSlash-2]
        CommonTransact = self._Transact_DB_Filename[0:IndexCommon]
        return CommonTransact


    # ----------------------------------------------------------------------------------- #
    #            ----------------      internal  methods   ---------------                #
    # ----------------------------------------------------------------------------------- #
    def _Read_Selections(self):
        self._Selections_List = []
        Selection_File = open(Selections_Full_Name)  # default is 'r'
        for Line in Selection_File:
            self._Selections_List = eval(Line)
        Selection_File.close()
        self._Codes_DB_Filename = self._Selections_List[Ix_Codes_File]
        self._Xlsx_Filename     = self._Selections_List[Ix_Xlsx_File]
        self.Sheet_Name         = self._Selections_List[Ix_Sheet_Name]
        self._Transact_DB_Filename = self._Selections_List[Ix_Transact_File]
        self.Top_ToStart        = self._Selections_List[Ix_TOP_ToStart]
        pass
    # ------------------------------------------------------------------------------------
    def _Update_Selections(self, Value, Index):
        self._Selections_List = self.Read_Selections()
        self._Selections_List[Index] = Value
        Selections = open(Selections_Full_Name, "w")  #
        Selections.write("")
        Selections.close()
        Selections = open(Selections_Full_Name, "a")
        # Casting the list to a string before writing
        Selections.write(str(self._Selections_List))
        Selections.close()
        self._Read_Selections()


# =======================================================================================
