# ============================================================================= #
#               -----   Transact_DB.py   -----                                  #
#              last child class  of data chainse                                #
#                                                                               #
#    ----------------------------------                                         #
#     Modul_Mngr = Modules_Manager()                                            #
#     Data       = Transact_DB()                                                #
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
    # --------------------------------------------------------------------------------------
    def Get_Xlsx_Transact_Ident(self):
        return [self._Xlsx_Conto, self._Xlsx_Year, self._Xlsx_Month, self._Transact_Year]

    # --------------------------------------------------------------------------------------
    def Load_Transact_Table(self):
        connect = sqlite3.connect(self._Transact_DB_Filename)
        cursor  = connect.cursor()
        try:
            cursor.execute("SELECT * FROM TRANSACT")
            self._Transact_Table = cursor.fetchall()
            connect.close()
        except:
            connect.close()
            return 'ERROR\non loading Transactions'

        if not self._Transact_Table:
            return EMPTY
        return OK

    # ---------------------------------------------------------------------------------------
    def Get_Transact_Table(self):
        return self._Transact_Table

    # ---------------------------------------------------------------------------------------
    def Get_Transact_ViewInsert_List(self):
        ViewList = []
        for Record in self._With_Code_Tree_List:
            ViewRec = [Record[iWithCode_nRow], Record[iWithCode_Contab], Record[iWithCode_Valuta],
                       Record[iWithCode_TR_Desc], Record[iWithCode_Accr], Record[iWithCode_Addeb],
                       Record[iWithCode_TRcode]]
            # ViewRec = [Record[iTransact_nRow], Record[iTransact_Contab], Record[iTransact_Valuta],
            #            Record[iTransact_TRdesc], Record[iTransact_Accred], Record[iTransact_Addeb],
            #            Record[iTransact_TRcode]]
            ViewList.append(ViewRec)
        return ViewList

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
        self.Dummy = 0
        Connect    = None
        try:
            Connect = sqlite3.connect(FullName)
            Cursor = Connect.cursor()
            Cursor.execute(
                "CREATE TABLE TRANSACT (nRow   INTEGER, "
                                       "Conto  TEXT, "
                                       "Contab TEXT, "
                                       "Valuta TEXT, "
                                       "TRdesc TEXT, "
                                       "Accred FLOAT, "
                                       "Addeb  FLOAT ,"
                                       "TRcode INTEGER)" )
            Connect.commit()
            Connect.close()
        except:
            Connect.close()
            return False
        return True

    # --------------------------------------------------------------------------------------------
    def OpenClose_Transactions_Database(self, Open, Transact_Filename):
        if Open:
            self.Connect = sqlite3.connect(Transact_Filename)
            self.Cursor = self.Connect.cursor()
            pass
        else:
            self.Connect.close()
            pass

    # --------------------------------------------------------------------------------------------------
    #                      0        1         2         3         4        5        6      7
    # List_Transact_DB :  nRow    Conto    Contab    Valuta    TR_Desc   Accred   Addeb  TRcode
    # ---------------------------------------------------------------------------------------------------
    def Insert_Transact_Record(self, Record_List):   # nRow, Cont, Contab, Valuta, Trdesc, Accred, Addeb, TRcode:
        nRow   = Record_List[iTransact_nRow]
        Conto  = Record_List[iTransact_Conto]
        Contab = Record_List[iTransact_Contab]
        Valuta = Record_List[iTransact_Valuta]
        TRdesc = Record_List[iTransact_TRdesc]
        Accred = Record_List[iTransact_Accred]
        Addeb  = Record_List[iTransact_Addeb]
        TRcode = Record_List[iTransact_TRcode]
        Cursor = None
        # self.Connect(TransactDB_Filename) is  made before the loop for insert
        try:
            Connect = sqlite3.connect(self._Transact_DB_Filename)
            Cursor  = Connect.cursor()
            # self.Cursor.execute("""
            Cursor.execute("""
                             INSERT INTO TRANSACT (nRow, Conto, Contab, Valuta, TRdesc, Accred, Addeb, TRcode)
                             VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                             (nRow, Conto, Contab, Valuta, TRdesc, Accred, Addeb, TRcode))
            Connect.commit()
            Cursor.close()
            return True
        except:
            Cursor.close()
            return False

        # self.Connect.commit()
        # self.Connect.close() #  is  made at the end of loop for insert

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
    #                               nRow Not to check                                         only on WithCode
    # be careful : Record to insert :  [nRow, Conto, Contab, Valuta, TRdesc, Accr, Addeb, TRcode,     '']
    #              Record on Database: [nRow, Conto, Contab, Valuta, TRdesc, Accr, Addeb, TRcode]
    #              Id may be different
    # --------------------------------------------------------------------------------------------------
    def Check_IfTransactRecord_InDatabase(self, RecToInsert):
        for Transact_Rec in self._Transact_Table:
            ListOnDb = list(Transact_Rec)
            Found = True
            Index = -1
            for ItemOnDb in ListOnDb:
                Index += 1
                if Index == 0:
                    pass
                else:
                    if ItemOnDb != RecToInsert[Index]:
                        Found = False
                        break
            if Found:
                return [Transact_Rec[iTransact_nRow],   Transact_Rec[iTransact_Conto],
                        Transact_Rec[iTransact_Contab], Transact_Rec[iTransact_Valuta],
                        Transact_Rec[iTransact_TRdesc],
                        Transact_Rec[iTransact_Accred], Transact_Rec[iTransact_Addeb],
                        Transact_Rec[iTransact_TRcode]]
            return []

    # -------------------------------------------------------------------------------------------------------------
    def Get_Transact_Year_ListInData(self):
        Full_Transact_filename = self._Txt_List[Ix_Transact_File]
        if Full_Transact_filename == UNKNOWN:
            return []
        Directory  = Get_Dir_Name(Full_Transact_filename)
        Files_List = os.listdir(Directory)
        Years_List = []
        for Filename in Files_List:
            # Transact_2024.db
            strYear = Filename[9:13]
            if CheckInteger(strYear):
                iYear = int(strYear)
                Years_List.append(iYear)
        return Years_List

# ===========================================================================================

# ========================== #
#                            #
Data = Transact_Db()         #
#                            #
# ========================== #
