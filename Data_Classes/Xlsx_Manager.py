# ========================================================================== #
#               -----   xlsx_Mngr.py   -----                                 #
#              class  for  xlsx file managiging                              #
#  for more informations see Data_Organization.txt                           #
# ========================================================================== #

from Data_Classes.Codes_DB import *
from openpyxl import load_workbook
from Common.Common_Functions import *
from datetime import datetime

class Xlsx_Manager(Codes_db):
    def __init__(self):
        super().__init__()

        self._Tot_RowsList  = [0, 0, 0]
        self._Tot_OK        = 0
        self._Tot_Rows = 0
        self._Tot_NOK  = 0

        # the lists for xlsx file   -----------------------------------------
        self.Contab = None                       # the rows of xls file
        self.Valuta = None
        self.Des1   = None
        self.Accr   = None
        self.Addeb  = None
        self.Des2   = None
        #                  nRow Contab Valuta TR_Desc Accred Addeb TRcode
        #                #   x    1       2      x       4     5     6
        self.ItemToCheck = [99,   1,      2,    99,      4,    5,    6]
        self.strList     = ['Row.    ',  'Contab: ', 'Valuta: ', 'Descr:  ', 'Accr:   ', 'Addeb:  ', '']

        #                                     A      B      C      D      E     F
        self._XLSX_Rows_From_Sheet  = []  # Contab Valuta Descr1 Accred Addeb Descr2
        self._XLSX_Rows_Desc_Compact = []
        self._Xlsx_Rows_NOK_List     = []
        #
        self._With_Code_Tree_List   = []  # nRow Contabile Valuta TRdesc Accred Addeb TRcode
        self._Wihtout_Code_Tree_List= []  # nRow Valuta Descr

    # -----------------------------------------------------------------------------------


    # ----------------------------------------------------------------------------------- #
    #            ----------------      public   methods   -----------------               #
    # ----------------------------------------------------------------------------------- #
    def Get_WithCodeList(self):
        return self._With_Code_Tree_List

    def Get_WithoutCodeList(self):
        return self._Wihtout_Code_Tree_List

    def Get_XLSX_Rows_From_Sheet(self):
        return self._XLSX_Rows_From_Sheet

    def Xlsx_Conto_Year_Month_Setup(self, Action):
        # FIDEU_2024_01.xlsx
        if not Action:
            self._Xlsx_Conto = None
            self._Xlsx_Year  = None
            self._Xlsx_Month = None
        else:
            # Here Codes tables  are OK and the xlsx_finame too
            FullFilename = self.Get_Txt_Member(Ix_Xlsx_File)
            if FullFilename != UNKNOWN:
                filename = Get_File_Name(FullFilename)
                self._Xlsx_Conto = filename[0:5]
                self._Xlsx_Year  = int(filename[6:10])
                self._Xlsx_Month = int(filename[11:13])

    # -------------------------------------------------------------------------------------------------
    # The case of two identical records (Dates, value, Code etc.)
    # (for example ATM withdrawals at the same day for the same values)
    # Xlsx must be adjustad manually; i.e. for two 100€ Xlsx must be modified manually:
    # in 99.99 and 100.1
    # nRow    Contab    Valuta    TR_Desc   Accred   Addeb   TRcode
    #   x        1         2         x         3       4        5
    # -------------------------------------------------------------------------------------------------
    def Check_For_Multiple_Record_OnWitCodeList(self, RecToCheck):
        nFound = 0
        for Rec in self._With_Code_Tree_List:
            Index = -1
            Found = True
            for Item in Rec:
                Index += 1
                indexToCheck = self.ItemToCheck[Index]
                if indexToCheck == 99:
                    pass
                else:
                    if Item == '' or Item == ' ':
                        pass
                    else:
                        if Item != RecToCheck[indexToCheck]:
                            Found = False
            if Found:
                nFound += 1

        if nFound == 1:
            return ''
        else:
            Messg = 'Found record:\n'
            Index = -1
            for Item in RecToCheck:
                Index += 1
                Messg += self.strList[Index]
                Messg += str(Item) + '\n'
            Messg += '\n\nfound in more records WitCode List\nAdjust records in Xlsx\nExit '
            return Messg

    # -----------------------------------------------------------------------------------
    def Transact_Year_Setup(self, Action):
        # Transact_2023.db
        if not Action:
            self._Transact_Year = None
        else:
            # Here Codes tables  are OK and the xlsx_finame too
            FullFilename = self.Get_Txt_Member(Ix_Transact_File)
            if FullFilename != UNKNOWN:
                filename = Get_File_Name(FullFilename)
                self._Transact_Year  = int(filename[9:13])



    # ---------------------   O L D  ---------------------------------
    def Load_Xlsx_Lists(self):
        self._Tot_OK                 = 0
        self._XLSX_Rows_From_Sheet   = []  # nRow Contab Valuta  Descr1  Accred Addeb Descr2
        self._XLSX_Rows_Desc_Compact  = []
        self._With_Code_Tree_List     = []  # nRow Contab Valuta TRcode TRdesc  Accred  Addeb
        self._Wihtout_Code_Tree_List  = []  # nRow Valuta  Descr

        Result = self._Load_XLS_Rows_From_Sheet()     # get rows from sheet
        if Result != OK:
            return Result
        Result = self._Create_Xlsx_Lists()   # build lists for trees
        if Result != OK:
            return Result
        #                    [Ix__Tot_OK,   Ix_Tot_WithCode,    Ix_Tot_Without_Code]
        self._Tot_RowsList = [self._Tot_OK, len(self._With_Code_Tree_List), len(self._Wihtout_Code_Tree_List)]
        return OK

    def Get_Total_Rows(self):
        return self._Tot_RowsList


    # =========================================================================================
    # The xlsx file contains Rows that are loaded in    self._XLSX_Rows_From_Sheet
    # used on Top_Xlsx_Rows_View
    # Then are created   -  self._With_Code_Tree_List   -  self._Wihtout_Code_Tree_List
    # used to insert Transactions on database
    # ==========================================================================================
    def Load_Xlsx_Rows_FromSheet(self):
        Result = self._Load_XLS_Rows_From_Sheet()
        self._Files_Loaded[Ix_Xlsx_Rows_Loaded] = False
        if Result == OK:
            self._Files_Loaded[Ix_Xlsx_Rows_Loaded] = True
            return self._XLSX_Rows_From_Sheet
        else:
            return Result

    # -----------------------------------------------------------------------------------------
    def Load_Xlsx_Lists_FromData(self):
        self._Files_Loaded[Ix_Transact_Loaded] = False
        Result = self.Load_Xlsx_Rows_FromSheet()
        if Result != OK:
            return Result
        else:
            Result = self._Load_XLS_Rows_From_Sheet()
            if Result == OK:
                self._Files_Loaded[Ix_Transact_Loaded] = True
                return self._XLSX_Rows_From_Sheet
            else:
                return Result

    # -------------------------------------  Get rows from sheet ----------------------------
    def _Load_XLS_Rows_From_Sheet(self):
        self.XLSX_Rows_From_Sheet   = []
        self._XLSX_Rows_Desc_Compact= []
        self._Xlsx_Rows_NOK_List     = []
        self.iYear_List              = []

        self._Tot_OK   = 0
        self._Tot_NOK  = 0
        self._Tot_Rows = 0

        self._Get_Work_Sheet_Rows()  # set  _Tot_Rows = -1 on ERROR of Loadind Rows
        self._Files_Loaded[Ix_Xlsx_Rows_Loaded]  = False
        self._Files_Loaded[Ix_Xlsx_Lists_Loaded] = False

        if self._Tot_Rows < 0:
            return 'Error on loading Work sheet rows'
        if self._Tot_Rows <= 1:
            return 'No rows on the sheet'

        for nRow in range(1, self._Tot_Rows+1):
            self._Get_xlsx_Row(nRow)
            Des1Comp = Compact_Descr_String(self.Des1)
            Des2Comp = Compact_Descr_String(self.Des2)

            XLS_Row_List    = [int(nRow), self.Contab, self.Valuta,       # as it is in File
                              self.Des1,  self.Accr,   self.Addeb, self.Des2]
            XLS_Row_Compact = [int(nRow), self.Contab, self.Valuta,       # Desc1 & Desc2  compacted
                              Des1Comp,   self.Accr,   self.Addeb, Des2Comp]

            Checked_Row_List = self._Check_Values(XLS_Row_Compact)
            if not Checked_Row_List:
                self._Tot_NOK += 1
                self._Xlsx_Rows_NOK_List.append(XLS_Row_List)
            else:
                self._Tot_OK += 1
                self._XLSX_Rows_Desc_Compact.append(Checked_Row_List)    # Descriptions compacted
                Data_Contab = Checked_Row_List[iRow_Contab]
                Data_Valuta = Checked_Row_List[iRow_Valuta]
                myRow = []
                Item = -1
                for Val in XLS_Row_List:
                    Item += 1
                    if Item == iRow_Contab:
                        myRow.append(Data_Contab)
                    elif Item == iRow_Valuta:
                        myRow.append(Data_Valuta)
                        iYear = int(Data_Valuta[0:4])
                        if iYear in self.iYear_List or len(self.iYear_List) >= 2:
                            pass
                        else:
                            self.iYear_List.append(iYear)
                    else:
                        myRow.append(Val)
                self.XLSX_Rows_From_Sheet.append(myRow)          # Descripritions as in Sheet, Date is str
        if self._Tot_OK == 0:
            return 'any row with significant data'
        if self._Xlsx_Conto == FLASH or self._Xlsx_Conto == AMBRA or self._Xlsx_Conto == POSTA:
            self._Adjust_Xlsx_Rows_ForFLASH()   # adjust rows as in FLASH or in AMBRA
        elif self._Xlsx_Conto == POSTA:
            pass                                # """     "   "  "  POSTA
        else:
            pass                                # NOT identified leave as FIDEU
        # -------------
        if not self._XLSX_Rows_Desc_Compact:
            return 'xlsx file contains any row with significant data'
        else:
            self._Files_Loaded[Ix_Xlsx_Rows_Loaded] = True
            return OK

    # ----------------------  Set tree rows list   ---------------------------------------  #
    def _Create_Xlsx_Lists(self):
        self.iYear_List              = []
        self._Wihtout_Code_Tree_List = []
        self._With_Code_Tree_List    = []
        Tot_Rows_WithCode            = 0
        Tot_Rows_WithoutCode         = 0
        self._Files_Loaded[Ix_Xlsx_Lists_Loaded] = False

        for Row in self._XLSX_Rows_Desc_Compact:
            Row_Without_Code = []
            Row_With_Code    = []
            Full_Desc        = self.Description_Select(Row[iRow_Descr1], Row[iRow_Descr2])
            Row[iRow_Descr1] = Full_Desc

            Result = self._Find_StrToSearc_InFullDesc(Row)
            if Result[0] == NOK:
                if not Result[1]:
                    Tot_Rows_WithoutCode += 1
                    Row_Without_Code.append(Row[iRow_nRow])       # nRow
                    Row_Without_Code.append(Row[iRow_Valuta])     # Valuta
                    Row_Without_Code.append(Full_Desc)            # Full_Desc
                    self._Wihtout_Code_Tree_List.append(Row_Without_Code)
                else:
                    self._Wihtout_Code_Tree_List = []
                    self._With_Code_Tree_List = []
                    self._Tot_OK   = 0
                    self._Tot_Rows = 0
                    return Result[1]

            else:
                Rec_Found = Result[1]
                Tot_Rows_WithCode += 1
                Row_With_Code.append(int(Row[iRow_nRow]))    # nRow
                Row_With_Code.append(Row[iRow_Contab])       # Contabile
                Row_With_Code.append(Row[iRow_Valuta])       # Valuta
                Row_With_Code.append(Rec_Found[iTR_TRdesc])  # TRdesc
                Row_With_Code.append(Row[iRow_Accr])         # Accred
                Row_With_Code.append(Row[iRow_Addeb])        # Addeb
                Row_With_Code.append(Rec_Found[iTR_TRcode])  # TRcode
                self._With_Code_Tree_List.append(Row_With_Code)
        self._Files_Loaded[Ix_Xlsx_Rows_Loaded] = True
        return OK

    # --------------------------------------------------------------------------------------------
    # List_For_XLSX_Row_Control = [
    # [iRow_nRow,   INTEGER],
    # [iRow_Contab, DATE],    [iRow_Valuta, DATE],   [iRow_Descr1, STRING],
    # [iRow_Accr,   NUMERIC], [iRow_Addeb, NUMERIC], [iRow_Descr2, STRING]]
    def _Check_Values(self, XLS_Row_List):
        XLS_Row_List_Checked = []
        for Item_ToCheck in List_For_XLSX_Row_Control:
            Value = XLS_Row_List[Item_ToCheck[0]]
            Type = Item_ToCheck[1]
            ItemChecked = self._Check_Val(Value, Type)
            if ItemChecked is None:
                return []
            else:
                XLS_Row_List_Checked.append(ItemChecked)
        return XLS_Row_List_Checked  # as in Xlsx Rows
                                     # XLS_Row_List : nRow    Contab    Valuta    Descr1   Accred   Addeb   Descr2
    # -----------------------------------------------------------------------------------
    def _Check_Val(self, Item, Type):
        # List_For_XLSX_Row_Control = [
        # [iRow_nRow, INTEGER],
        # [iRow_Contab, DATE],  [iRow_Valuta, DATE],   [iRow_Descr1, STRING],
        # [iRow_Accr, NUMERIC], [iRow_Addeb, NUMERIC], [iRow_Descr2, STRING]  ]
        ItemType  = type(Item)
        if Type == STRING:            #   ---  String   -----  (Descriptions)
            if ItemType is str:
                return Item
            else:
                return ' '
        elif Type == INTEGER:         #   ---  Integer  -----   (Row Id number)
            if ItemType is int:
                return Item
            if ItemType is None:
                return 0
        elif Type == NUMERIC:         #   ---  Numeric  -----  (Accred  Addeb)
            if ItemType is float:
                if not Item:
                    return ' '
                return Item
            elif ItemType is int:
                if Item == 0:
                    return ' '
                return float(Item)
            # if ItemType is None:
            # return ' '
            return ' '
        elif Type == DATE:            #   ---  Date    -----
            Ckd_Date = self._Verify_Date(Item)
            if Ckd_Date:
                return Ckd_Date
            else:
                return None

    # -----------------------------------------------------------------------------------
    def _Get_xlsx_Row(self, nRow):
        if self._Xlsx_Conto == FIDEU:                                # Get columns for FIDEU
            self.Contab = self._Work_Sheet['A' + str(nRow)].value
            self.Valuta = self._Work_Sheet['B' + str(nRow)].value
            self.Des1   = self._Work_Sheet['C' + str(nRow)].value
            XlsxAccr   = self._Work_Sheet['D' + str(nRow)].value
            XlsxAddeb  = self._Work_Sheet['E' + str(nRow)].value
            self.Des2   = self._Work_Sheet['F' + str(nRow)].value
            # ----------   Credits and Debits  type are :  float   -------
            self.Accr  = Convert_To_Float(XlsxAccr)
            self.Addeb = Convert_To_Float(XlsxAddeb)

        elif self._Xlsx_Conto == FLASH or self._Xlsx_Conto == AMBRA:  # Get columns for Flash/AMBRA
            self.Contab = self._Work_Sheet['A' + str(nRow)].value
            self.Valuta = self._Work_Sheet['B' + str(nRow)].value
            self.Des1   = self._Work_Sheet['C' + str(nRow)].value
            XlsxAccr    = self._Work_Sheet['E' + str(nRow)].value
            XlsxAddeb   = self._Work_Sheet['G' + str(nRow)].value
            self.Des2   = ''
            # ----------   Credits and Debits  type are :  float   -------
            self.Accr  = Convert_To_Float(XlsxAccr)
            self.Addeb = -Convert_To_Float(XlsxAddeb)
            typeContab = type(self.Contab)
            typeValuta = type(self.Valuta)

            if typeContab is datetime and typeValuta is datetime:
                pass
            elif typeContab is datetime:
                self.Valuta = self.Contab
            elif typeValuta is datetime:
                self.Contab = self.Valuta

        elif self._Xlsx_Conto == POSTA:                              # Get columns for POSTA
            self.Contab = self._Work_Sheet['A' + str(nRow)].value
            self.Valuta = self._Work_Sheet['B' + str(nRow)].value
            self.Des1   = ''  #self.Work_Sheet['C' + str(nRow)].value
            self.Accr   = self._Work_Sheet['D' + str(nRow)].value
            self.Addeb  = self._Work_Sheet['C' + str(nRow)].value
            self.Des2   = self._Work_Sheet['E' + str(nRow)].value
            if type(self.Addeb) is float or type(self.Addeb) is int:
                self.Addeb  = -self.Addeb
            typeContab = type(self.Contab)
            typeValuta = type(self.Valuta)
            if typeContab is datetime and typeValuta is datetime:
                pass
            elif typeContab is datetime:
                self.Valuta = self.Contab
            elif typeValuta is datetime:
                self.Contab = self.Valuta

        elif self._Xlsx_Conto == AMBRA:                              # Get columns for AMBRA
            pass

    # ---------------------------------------------------------------
    def _Adjust_Xlsx_Rows_ForFLASH(self):
        Copy1 = self.XLSX_Rows_From_Sheet.copy()
        self.XLSX_Rows_From_Sheet = []
        Copy2 = self._XLSX_Rows_Desc_Compact
        self._XLSX_Rows_Desc_Compact = []
        Index = self._Tot_OK -1
        for j in range(0, self._Tot_OK):
            Row1 = Copy1[Index]
            self.XLSX_Rows_From_Sheet.append(Row1)
            Row2 = Copy2[Index]
            self._XLSX_Rows_Desc_Compact.append(Row2)
            Index -= 1

    # --------------------------------------------------------------------------------- #
    #  Workbook is the container of all Worksheets                                      #
    #  while the Worksheet is the container of Data of one Sheet                        #
    # --------------------------------------------------------------------------------- #
    def _Get_Work_Sheet_Rows(self):
        XlsName          = self._Xlsx_Filename
        # Work_Book = None
        try:
            Work_Book = load_workbook(XlsName)
        except:
            self._Tot_Rows = -1
            return
        self.SheetName   = Work_Book.sheetnames[0]   # always the first sheet
        self.Update_Txt_File(self.SheetName, Ix_Sheet_Name)
        self._Work_Sheet = Work_Book.get_sheet_by_name(self.SheetName)
        self._Tot_Rows    = self._Work_Sheet.max_row
        pass

    # -----------------------------------------------------------------------------------
    @classmethod
    def _Verify_Date(cls, DateToCheck):
        Type = type(DateToCheck)
        if Type is datetime:
            strDate = str(DateToCheck)
            myDate  = strDate[:10]
            return myDate
            # return DateToCheck
        DateTemplate = 'DD?MM?YYYY'
        if Type is not str:
            return []
        if len(DateToCheck) != 10:
            return []
        for i in range(0, 10):
            if DateTemplate[i] == '?':
                pass
            else:
                if not DateToCheck[i].isdecimal():
                    return []
        dateobject = datetime.strptime(DateToCheck, '%d/%m/%Y').date()
        return dateobject

    # -----------------------------------------------------------------------------------
    def Description_Select(self, Desc1, Desc2):
        self.Dummy = 1
        Typ1 = type(Desc1)
        Typ2 = type(Desc2)
        Len1  = 0
        Len2  = 0
        if Typ1 is str:
            Len1 = len(Desc1)
        if Typ2 is str:
            Len2 = len(Desc2)
        if not Len1 and not Len2:
            return ''
        if Len1 > Len2:
            return Desc1
        else:
            return Desc2

    # ------------------------------------------------------------------------------------
    def Check_The_Row(self, FullDesc, TRcode):
        for Desc in self.XLSX_Rows_From_Sheet:
            if Desc[iRow_nRow] == 96:
                pass
                for Rec in self._TR_Codes_Table:
                    if Rec[iTR_TRcode] == TRcode:
                        PRINT(FullDesc+ '   Record: ' + Rec)
                pass
# =======================================================================================
