# ============================================================================= #
#               -----   Transact_DB.py   -----                                  #
#              last child class  of data chainse                                #
#                                                                               #
#    ----------------------------------                                         #
#     Modul_Mngr    = Modules_Manager()                                         #
#     Data_Manager  = Transact_DB()                                             #
#    ----------------------------------                                         #
#     are istanced on Startup and will NEVER destroyed                          #
#  for more informations see Data_Organization.txt                              #
# ============================================================================= #

import os
import sqlite3
from Common.Common_Functions import *
from Data_Classes.Xlsx_Manager import Xlsx_Manager

# ------------------------------------------------------------------------------
class Transact_Db(Xlsx_Manager):
    def __init__(self):
        super().__init__()
        self._Transact_Table = []
        self.Connect = None
        self.Cursor  = None
        self.Dummy   = 0

        self._tTransact_Year  = None
        self._tTransact_Table = []

        self._Transact_xMonth_List_ForInsert = [[], [], [], [], [], [], [], [], [], [], [], []]
        self._Transact_xMonth_List_Empty     = [False, False, False, False, False, False,
                                                False, False, False, False, False, False]
    # --------------------------------------------------------------------------------------
    def Get_Xlsx_Transact_Ident(self):
        return [self._Xlsx_Conto, self._Xlsx_Year, self._Xlsx_Month, self._Transact_Year]

    # --------------------------------------------------------------------------------------
    def Load_Transact_Table(self, TransacFilename):
        self._tTransact_Table = []
        Transact_Name      = TransacFilename
        if TransacFilename == ON_SELECTIONS:
            Transact_Name = self.Get_Selections_Member(Ix_Transact_File)

        Result = self._Load_Transact_Table(Transact_Name)
        if Result == OK:
            self._Files_Loaded[Ix_Transact_Loaded] = True
            return OK
        else:
            return Result

    # -----------------------------------------------------------------------------------
    def _Load_Transact_Table(self, TransacFilename):
        self._tTransact_Year = Get_Transactions_Year(TransacFilename)
        connect = sqlite3.connect(TransacFilename)
        cursor  = connect.cursor()
        try:
            cursor.execute("SELECT * FROM TRANSACT")
            self._tTransact_Table = cursor.fetchall()   # _tTransact_Table  temporary table
            connect.close()
        except sqlite3.Error as e:                      # in case of error nothing change
            strErr = Db_Error(e)
            MsgErr = 'ERROR on loading Transactions Table:\n' + str(strErr)
            return MsgErr
        finally:
            if connect:
                connect.close()

            self._Transact_Table = self._tTransact_Table    # table with new values
            self._Transact_Year  = self._tTransact_Year     # new Year

            # the Selections are upadated because TransacFilename can be origened from Sarch on TRANSACTIONS
            self.Update_Selections(TransacFilename, Ix_Transact_File)
            return OK


    # ---------------------------------------------------------------------------------------
    def Clear_Transact_Year(self):
        self._Transact_Year = None

    # ---------------------------------------------------------------------------------------
    def _Set_Transact_Year(self):
        # Transact_2023.db
        FullFilename = self.Get_Selections_Member(Ix_Transact_File)
        if FullFilename != UNKNOWN:
            filename = Get_File_Name(FullFilename)
            self._tTransact_Year = int(filename[9:13])
        else:
            self._tTransact_Year = None

    # ---------------------------------------------------------------------------------------
    #                      0      1       2       3       4       5        6      7
    # List_Transact_DB :  nRow  Conto  Contab  Valuta  TR_Desc  Accred   Addeb  TRcode
    # ---------------------------------------------------------------------------------------
    def Get_Transact_Table(self):
        Transact_Descr_OK = []
        for Rec in self._Transact_Table:
            RecList = list(Rec)
            TRcode = RecList[iTransact_TRcode]
            TRdesc = self.Get_TrDesc_FromCode(TRcode)
            RecList[iTransact_TRdesc] = TRdesc
            Transact_Descr_OK.append(RecList)
        return Transact_Descr_OK

    # ---------------------------------------------------------------------------------------
    def Get_Len_Transact_Table(self):
        return len(self._Transact_Table)

    # ---------------------------------------------------------------------------------------
    def Create_TRansact_Filename(self, Year):
        Xlsx_CommonDir = self.Get_Xls_CommonDir()
        Fullname       = Xlsx_CommonDir + '/' + TRANSACTIONS + '/' + Transact_ + str(Year) + '.db'
        return Fullname

    # ---------------------------------------------------------------------------------------
    # used in Top_Insert()
    def Create_Transact_DB_File(self, FullName):
        Filename    = ''
        File_Exists = os.path.isfile(FullName)
        if File_Exists:
            Result = self._Load_Transact_Table(FullName)
            if Result == OK or Result == EMPTY:
                Filename = Get_File_Name(FullName)
                ErrList = [1, [Filename + '   Già esistente']]
                return ErrList
            else:
                Filename = Get_File_Name(FullName)
                ErMessg = [0, ['Errore nel caricare  ' + Filename + '\nappena trovato']]
                return ErMessg

        DirName = Get_Dir_Name(FullName)
        if not os.path.isdir(DirName):
            os.mkdir(DirName)
        connect    = None
        try:
            connect = sqlite3.connect(FullName)
            cursor = connect.cursor()
            cursor.execute(
                "CREATE TABLE TRANSACT (nRow   INTEGER, "
                                       "Conto  TEXT, "
                                       "Contab TEXT, "
                                       "Valuta TEXT, "
                                       "TRdesc TEXT, "
                                       "Accred FLOAT, "
                                       "Addeb  FLOAT ,"
                                       "TRcode INTEGER)" )
            connect.commit()
        except sqlite3.Error as e:
            strErr    = Db_Error(e)
            ErMessg = [ 0, ['Errore nel creare  ' + Filename + '\n' + str(strErr)]]
            return ErMessg
        finally:
            if connect:
                connect.close()
            if not self._Load_Transact_Table(FullName):
                ErMessg = [0, ['Errore nel caricare  ' + Filename + '\nappena creato']]
                return ErMessg
        self.Update_Selections(FullName, Ix_Transact_File)
        self._Set_Transact_Year()
        return [-1, [OK]]

    # ---------------------------------------------------------------------------------------------
    def OpenClose_Transactions_Database(self, Open, Transact_Filename):
        if Open:
            try:
                self.Connect = sqlite3.connect(Transact_Filename)
                self.Cursor = self.Connect.cursor()
            except sqlite3.Error as e:
                if self.Connect:
                    self.Connect.close()
                strErr = Db_Error(e)
                ErMessg = [0, ['Errore on opening  ' + Transact_Filename + '\n' + str(strErr)]]
                return ErMessg

            finally:
                return OK
        else:
            if self.Connect:
                self.Connect.close()

    # --------------------------------------------------------------------------------------------------
    #                      0        1         2         3         4        5        6      7
    # List_Transact_DB :  nRow    Conto    Contab    Valuta    TR_Desc   Accred   Addeb  TRcode
    # ---------------------------------------------------------------------------------------------------
    def Insert_Transact_Record(self, Record_List):
        nRow   = Record_List[iTransact_nRow]
        Conto  = Record_List[iTransact_Conto]
        Contab = Record_List[iTransact_Contab]
        Valuta = Record_List[iTransact_Valuta]
        TRdesc = Record_List[iTransact_TRdesc]
        Accred = Record_List[iTransact_Accred]
        Addeb  = Record_List[iTransact_Addeb]
        TRcode = Record_List[iTransact_TRcode]
        # self.Connect(TransactDB_Filename) made before the loop for insert
        try:
            self.Cursor.execute("""
                             INSERT INTO TRANSACT (nRow, Conto, Contab, Valuta, TRdesc, Accred, Addeb, TRcode)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                             (nRow, Conto, Contab, Valuta, TRdesc, Accred, Addeb, TRcode))
            self.Connect.commit()
            pass
        except sqlite3.Error as e:
            if self.Connect:
                self.Connect.close()
            strErr = Db_Error(e)
            MsgErr = ('ERROR on inserting:\n\n' + TRdesc + '\n\n'
                      'in Codes Table:\n\n') + str(strErr)
            return MsgErr
        finally:
            # if self.Connect:
            #     self.Connect.close()  made at the end of loop for insert
            return OK

    # --------------------------------------------------------------------------------------------------
    #                      0        1         2         3         4        5        6      7
    # List_Transact_DB :  nRow    Conto    Contab    Valuta    TR_Desc   Accred   Addeb  TRcode
    # ---------------------------------------------------------------------------------------------------
    def Fetch_OneYear_Values(self):
        Connct = sqlite3.connect(self._Transact_DB_Filename)
        Cursor = Connct.cursor()
        Cursor.execute("SELECT * FROM TRANSACT")
        self._Transact_Table = Cursor.fetchall()
        Connct.commit()
        Connct.close()

    # --------------------------------------------------------------------------------------------------
    #                              nRow Not check                                   '' only on WithCode
    # be careful : Record to insert :  [nRow, Conto, Contab, Valuta, TRdesc, Accr, Addeb, TRcode,   '']
    #              Record on Database: [nRow, Conto, Contab, Valuta, TRdesc, Accr, Addeb, TRcode]
    #              Id may be different
    # --------------------------------------------------------------------------------------------------
    def Check_IfTransactRecord_InDatabase(self, RecToInsert):
        for Transact_Rec in self._Transact_Table:
            ListOnDb = list(Transact_Rec)
            if ListOnDb[iTransact_Conto]  == RecToInsert[iTransact_Conto]  and \
               ListOnDb[iTransact_Contab] == RecToInsert[iTransact_Contab] and \
               ListOnDb[iTransact_Valuta] == RecToInsert[iTransact_Valuta] and \
               ListOnDb[iTransact_Accred] == RecToInsert[iTransact_Accred] and \
               ListOnDb[iTransact_Addeb]  == RecToInsert[iTransact_Addeb]:
                return True
        return False

    # -------------------------------------------------------------------------------------------------------------
    def Create_Transact_Month_List_Empty(self):
        self._Transact_xMonth_List_Empty     = [True, True, True, True, True, True,
                                                True, True, True, True, True, True]
        for Rec in self._Transact_Table:
            YearMonthV = Get_YearMonthDay(Rec[iTransact_Valuta])
            Year  = YearMonthV[0]
            Month = YearMonthV[1] -1
            if Year == self._Transact_Year:
                self._Transact_xMonth_List_Empty[Month] = False
            YearMonthC = Get_YearMonthDay(Rec[iTransact_Contab])
            Year = YearMonthC[0]
            Month = YearMonthC[1] -1
            if Year == self._Transact_Year:
                self._Transact_xMonth_List_Empty[Month] = False
        return self._Transact_xMonth_List_Empty

    # -------------------------------------------------------------------------------------------------------------
    def Get_Transact_Year_ListInData(self):
        Full_Transact_filename = self._Selections_List[Ix_Transact_File]
        if Full_Transact_filename == UNKNOWN:
            return [0, []]
        Directory  = Get_Dir_Name(Full_Transact_filename)
        Files_List = os.listdir(Directory)
        Years_List = []
        for Filename in Files_List:
            if Transact_ in Filename:
                # Transact_2024.db
                strYear = Filename[9:13]
                if CheckInteger(strYear):
                    iYear = int(strYear)
                    Years_List.append(iYear)
        SelectedFile = Get_File_Name(Full_Transact_filename)
        strYear = SelectedFile[9:13]
        return [strYear, Years_List]

# ===========================================================================================

# ========================== #
#                            #
Data_Manager = Transact_Db() #
#                            #
# ========================== #
