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

        #                                     A      B      C      D      E     F
        self._XLSX_Rows_From_Sheet  = []  # Contab Valuta Descr1 Accred Addeb Descr2
        self.XLSX_Rows_Desc_Compact = []
        self.Xlsx_Rows_NOK_List     = []
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

    def XLSX_Rows_From_Sheet(self):
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

    # -----------------------------------------------------------------------------------------
    def Load_Xlsx_Lists(self):
        # self.Chat.Set_Start_Time()
        self._Tot_OK                 = 0
        self._XLSX_Rows_From_Sheet   = []  # nRow Contab Valuta  Descr1  Accred Addeb Descr2
        self.XLSX_Rows_Desc_Compact  = []
        self._With_Code_Tree_List     = []  # nRow Contab Valuta TRcode TRdesc  Accred  Addeb
        self._Wihtout_Code_Tree_List  = []  # nRow Valuta  Descr

        Result = self._Get_XLS_Rows_From_Sheet()     # get rows from sheet
        if Result != OK:
            return Result
        Result = self._Create_Xlsx_Tree_Rows_List()   # build lists for trees
        if Result != OK:
            return Result
        #                    [Ix__Tot_OK,   Ix_Tot_WithCode,    Ix_Tot_Without_Code]
        self._Tot_RowsList = [self._Tot_OK, len(self._With_Code_Tree_List), len(self._Wihtout_Code_Tree_List)]
        return OK

    def Get_Total_Rows(self):
        return self._Tot_RowsList

    # ----------------------  Set tree rows list   ---------------------------------------  #
    def _Create_Xlsx_Tree_Rows_List(self):
        self.iYear_List             = []
        self._Wihtout_Code_Tree_List = []
        self._With_Code_Tree_List    = []
        Tot_Rows_WithCode           = 0
        Tot_Rows_WithoutCode        = 0
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
                Row_With_Code.append('  ')                   # Space
                self._With_Code_Tree_List.append(Row_With_Code)
        return OK

    # -------------------------------------  Get rows from sheet ----------------------------
    def _Get_XLS_Rows_From_Sheet(self):
        self.XLSX_Rows_From_Sheet   = []
        self._XLSX_Rows_Desc_Compact= []
        self.Xlsx_Rows_NOK_List     = []
        self.iYear_List             = []
        self._Tot_OK  = 0
        self._Tot_NOK = 0
        self._Get_Work_Sheet_Rows()

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
                self.Xlsx_Rows_NOK_List.append(XLS_Row_List)
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
            return 'wny row with significant data'
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
            self.Accr   = self._Work_Sheet['D' + str(nRow)].value
            self.Addeb  = self._Work_Sheet['E' + str(nRow)].value
            self.Des2   = self._Work_Sheet['F' + str(nRow)].value

            # self.Accr  = Float_ToString_Setup(Accr)
            # self.Addeb = Float_ToString_Setup(Addeb)

        elif self._Xlsx_Conto == FLASH or self._Xlsx_Conto == AMBRA:  # Get columns for Flash/AMBRA
            self.Contab = self._Work_Sheet['A' + str(nRow)].value
            self.Valuta = self._Work_Sheet['B' + str(nRow)].value
            self.Des1   = self._Work_Sheet['C' + str(nRow)].value
            self.Accr   = self._Work_Sheet['E' + str(nRow)].value
            self.Addeb  = self._Work_Sheet['G' + str(nRow)].value
            self.Des2   = ''
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
        Work_Book        = load_workbook(XlsName)
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
