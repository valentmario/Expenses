# ============================================================================= #
#               -----   Transact_DB.py   -----                                  #
#              last child class  of data chainse                                #
#                                                                               #
#    ----------------------------------                                         #
#     Modul_Mngr = Modules_Manager()                                            #
#     Data       = Transact_DB()                                                #
#    ----------------------------------                                         #
#     are istanced on Startup and will NEVER destoyed                           #
# ============================================================================= #
"""
    the rule is:
    methods and data inside the data chain are underscored (_).
    the private (_) methods and attributes are accessible only inside data chain.
    public methods isn't undscored (_) and can't acces to _attributes
    but they can retrieve _attributes with Get_somthing_method()

    data chain:
    LOW LEVEL       return  OK  or  'Diagnostic'

    Modules_Manager
    MIDDLE LEVEL    return True or display 'Diagnostic' and return False

    Toplevel modules
    HIGH LEVEL      get only True or False

"""
# ===================================================================================
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

    # --------------------------------------------------------------------------
    def Call_OnClose(self):
        self.Chat.Detach(TRANSACT_CLASS)
        del self

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
    def Create_Transact_DB_File(self, Year):      # used in Top_Insert()
        Connect        = None
        Fullname = self.Create_TRansact_Filename(Year)
        try:
            Connect = sqlite3.connect(Fullname)
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
            self.Update_Txt_File(Fullname, Ix_Transact_File)

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
    def Check_IfTransactRecord_InDatabase(self, RecToInsert):
        for Transact_Rec in self._Transact_Table:
            Found = True
            Index = -1
            for Item in Transact_Rec:
                Index += 1
                if Item != RecToInsert[Index]:
                    Found = False
            if Found:
                ListToInsert = [RecToInsert[iTransact_Conto], RecToInsert[iTransact_Valuta], RecToInsert[iTransact_TRdesc],
                                RecToInsert[iTransact_Accred], RecToInsert[iTransact_Addeb]]
                ListInDatabase = [Transact_Rec[iTransact_Conto], Transact_Rec[iTransact_Valuta], Transact_Rec[iTransact_TRdesc],
                                Transact_Rec[iTransact_Accred], Transact_Rec[iTransact_Addeb]]
                return [ListToInsert, ListInDatabase]
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
