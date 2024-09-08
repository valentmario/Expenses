# =========================================================================== #
#            -----   Filesnames_Mngr.py   -----                               #
#   files names managed:                                                              #
#      Files_Names.txt                                                        #
#      Codes_DB.db                                                            #
#      Xlsx_filex.xlsx                                                        #
#      Transact.db                                                            #
#  Classes inheritance:                                                       #
#  Files_Names_Mngr <-- Codes_DB <-- Xlsx_Manager <-- Transact_DB             #
#  Data = Transact_DB()
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

        # the /home/mario/aTxt_File/Files_Names.txt skeleton -----------------
        self._Txt_List           = []
        self._Codes_DB_Filename  = UNKNOWN
        self._Xlsx_Filename      = UNKNOWN
        self.Sheet_Name          = UNKNOWN
        self._Work_Sheet         = None
        self._Transact_DB_Filename = UNKNOWN

        self._Xlsx_Conto    = None  # or on selecting new file  FIDEU_2024_01.xlsx
        self._Xlsx_Year     = None  # they are  calculated on startup
        self._Xlsx_Month    = None
        self._Transact_Year = None  # or on selecting new file  Transact_2024

        self.Curr_Year  = datetime.now().year    # to max years history setup
        self.Curr_Month = datetime.now().month
        self.Min_Year = self.Curr_Year - 5
        self.Max_Year = self.Curr_Year + 1

    # ----------------------------------------------------------------------------------- #
    #            ----------------      public   methods   -----------------               #
    # ----------------------------------------------------------------------------------- #
    def Check_Create_Txt_File(self):
        if not os.path.exists(Txt_File_Full_Name):
            if not os.path.isdir(Txt_File_Dir_Name):
                os.mkdir(Txt_File_Dir_Name)
            Txt_File = open(Txt_File_Full_Name, "w")
            Txt_File.write("")
            Txt_File.close()
            Txt_File = open(Txt_File_Full_Name, "a")
            # Casting the list to a string before writing
            Txt_File.write(str(Default_TxtFile_List))  # Write default Files_Names.txt
            Txt_File.close()
            self._Txt_List = Default_TxtFile_List
            return NEW
        else:  # ---  Files_Names.txt exists ----
            self._Read_Txt_File()
            return OK

    def Get_Txt_Member(self, Index):
        return self._Txt_List[Index]

    def Get_TopToStart_List(self):
        return self._Txt_List[Ix_TOP_ToStart]

    def Read_Txt_File(self):        # used only on Settings
        self._Read_Txt_File()
        return self._Txt_List

    # -----------------------------------------------------------------------------------
    def Update_Txt_File(self, Value, Index):     # Update an Item
        self._Update_Txt_File( Value, Index)

    # -----------------------------------------------------------------------------------
    def Update_Query_List(self, Value, Index):
        Query_List = self._Txt_List[Ix_Query_List]
        Query_List[Index]            = Value
        self._Txt_List[Ix_Query_List] = Query_List
        self._Update_Txt_File(Query_List, Ix_Query_List)

    # ----------------------------------------------------------------------------------
    def Sel_Codes_OnData(self):
        Init_Directory = Default_Init_Dir
        if self._Codes_DB_Filename != UNKNOWN:
            Init_Directory = Get_Dir_Name(self._Codes_DB_Filename)
        # -----------------------------------------------------
        Full_filename = tk.filedialog.askopenfilename(
            title='Select codes database',
            filetypes=[('db file', '*.db')],
            initialdir=Init_Directory)
        # -----------------------------------------------------
        return Full_filename

    # ----------------------------------------------------------------------------------
    def Sel_Xlsx_OnData(self):
        Init_Directory = Default_Init_Dir
        if self._Xlsx_Filename != UNKNOWN:
            Init_Directory = Get_Dir_Name(self._Xlsx_Filename)
        # -----------------------------------------------------
        Full_filename = tk.filedialog.askopenfilename(
            title='Select xlsx file',
            filetypes=[('xlsx file', '*.xlsx')],
            initialdir=Init_Directory)
        # -----------------------------------------------------
        return Full_filename

    # ----------------------------------------------------------------------------------
    def Sel_Transact_OnData(self):
        Init_Directory = Default_Init_Dir
        if self._Transact_DB_Filename != UNKNOWN:
            Init_Directory = Get_Dir_Name(self._Transact_DB_Filename)
        # -----------------------------------------------------
        Full_filename = tk.filedialog.askopenfilename(
            title='Select transactions database',
            filetypes=[('db file', '*.db')],
            initialdir=Init_Directory)
        # -----------------------------------------------------
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
    def _Read_Txt_File(self):
        self._Txt_List = []
        Txt_File = open(Txt_File_Full_Name)  # default is 'r'
        for Line in Txt_File:
            self._Txt_List = eval(Line)
        Txt_File.close()
        self._Codes_DB_Filename = self._Txt_List[Ix_Codes_File]
        self._Xlsx_Filename     = self._Txt_List[Ix_Xlsx_File]
        self.Sheet_Name         = self._Txt_List[Ix_Sheet_Name]
        self._Transact_DB_Filename = self._Txt_List[Ix_Transact_File]
        self.Top_ToStart        = self._Txt_List[Ix_TOP_ToStart]

    # ------------------------------------------------------------------------------------
    def _Update_Txt_File(self, Value, Index):
        self._Txt_List = self.Read_Txt_File()
        self._Txt_List[Index] = Value
        Txt_File = open(Txt_File_Full_Name, "w")  #
        Txt_File.write("")
        Txt_File.close()
        Txt_File = open(Txt_File_Full_Name, "a")
        # Casting the list to a string before writing
        Txt_File.write(str(self._Txt_List))
        Txt_File.close()
        self._Read_Txt_File()

# =======================================================================================
