# =========================================================================== #
#               -----   Codes_DB.py   -----                                   #
#          class  for Transactions Codes Database                             #
#  for more informations see Data_Organization.txt                            #
# =========================================================================== #

import sqlite3

from Data_Classes.Filesnames_Mngr import Files_Names_Manager
from Common.Common_Functions import *
from Common.Common_Functions import Compact_Descr_String

# ---------------------------------------------------------------------------------
class Codes_db(Files_Names_Manager):
    def __init__(self):
        super().__init__()
        self.Dummy = 0

        # ==================================================================================================== #
        #                                     0      1        2       3     4         5       6        7
        self._TR_Codes_Table      = []  # TRCode GRcode SPcode  TRdesc StrToSear FullDesc
        self._TR_Codes_Full       = []  # TRcode GRcode CAcode  TRdesc GRdesc    CAdesc StrToSear FullDesc
        self._GR_Codes_Table      = []  # GRcode GRdescr  CAcode
        self._CA_Codes_Table      = []  # CAcode CAdescr

        self._GRdescr_Ordered_List = []
        self._CA_Codes_Ordered     = []

        self._Multiple_Maching_List = []  # full descriptions matching with the same StrToSearch


    # ----------------------   Check the database  codes table   --------------------------------
    # for each code record to check verify if in the restant code records
    # exists a record that has a fullDescr that match with the strToSearch to check
    # -------------------------------------------------------------------------------------------
    def Check_Codesdatabase(self):
        self._Multiple_Maching_List = []
        for Rec_To_Check in self._TR_Codes_Table:
            StrToCek = Rec_To_Check[iTR_TRserc]
            for Rec in self._TR_Codes_Table:
                if Rec == Rec_To_Check:
                    pass
                else:
                    FullDescr = Rec[iTR_TRfullDes]
                    if StrForSearc_in_Fulldescr(StrToCek, FullDescr):
                        self._Multiple_Maching_List.append(Rec)
        return self._Multiple_Maching_List
    # -------------------------------------------------------------------------------------- #
    #      public methods invoked outside from  Top_Codes  classes                           #
    # -------------------------------------------------------------------------------------- #
    def Load_Codes_Table(self):
        Result = self._Load_Codes_Tables()
        if Result != OK:
            self._Files_Loaded[Ix_Codes_Loaded] = False
            return Result
        self._Files_Loaded[Ix_Codes_Loaded] = True
        return OK

    def Get_Codes_Table(self):
        return self._TR_Codes_Table

    def Get_TR_Codes_Table_Len(self):
        return len(self._TR_Codes_Table)

    def Get_TrDesc_FromCode(self, TRcde):
        for Rec in self._TR_Codes_Table:
            if Rec[iTR_TRcode] == TRcde:
                return Rec[iTR_TRdesc]
        return -1

    def Get_TR_Codes_Full(self, Index):
        if Index == -1:
            return self._TR_Codes_Full
        else:
            return self._TR_Codes_Full[Index]

    def Create_CodesTable_FromTR(self, TRlist):
        List = []
        for Rec in self.Tree_Codes_View_List:
            if Rec[iView_TRdesc] in TRlist:
                List.append(Rec)
        return List


    def Get_GR_Codes_Table(self):
        return self._GR_Codes_Table

    def Get_CA_Codes_Table(self):
        return self._CA_Codes_Table

    def Get_CA_Codes_Ordered(self):
        return self._CA_Codes_Ordered

    # ----------------------------------------------------------------------------------------
    def Get_New_Code(self):
        Max_Code = 0
        Tot_Codes = 0
        for Rec in self._TR_Codes_Table:
            Tot_Codes += 1
            if Rec[0] > Max_Code:
                Max_Code = Rec[0]
        New_Code = Max_Code + 1
        return [New_Code, Tot_Codes]

    # ----------------------------------------------------------------------------------------
    def Get_Last_TRrec(self):
        Index = -1
        for TRrecord in self._TR_Codes_Table:
            self.Dummy = TRrecord
            Index += 1
        return self._TR_Codes_Table[Index]

    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def Check_Codes_Record_Is_OK(cls, TR_RecToCheck):
        TR_CodeToCheck  = TR_RecToCheck[iTR_TRcode]
        TR_strTo_Search = TR_RecToCheck[iTR_TRserc]
        TR_FullDesc     = TR_RecToCheck[iTR_TRfullDes]
        GR_CodeToCheck  = TR_RecToCheck[iTR_GRcode]
        TR_DescToCheck  = TR_RecToCheck[iTR_TRdesc]
        if TR_FullDesc.find('nRow=') == -1:
            return 'Full Description NOT OK\nnRow=  fails'
        elif TR_CodeToCheck == 0 or GR_CodeToCheck == 0:
            return 'a TR or GR code is zero'
        elif len(TR_DescToCheck) < 3:
            return 'TR description too short'
        elif len(TR_strTo_Search) < 3:
            return 'String to search too short'
        elif TR_strTo_Search == 'Enter a String To Search':
            return 'Enter a correct string to search'
        elif TR_DescToCheck == 'Set Transaction Description':
            return 'Enter a correct Transaction description'
        if not StrForSearc_in_Fulldescr(TR_strTo_Search, TR_FullDesc):
            return 'String To Search:\n' + TR_strTo_Search + '\ndoes not match with Full Desription:\n' + TR_FullDesc
        return OK


    # -------------------------------------------------------------------------------------- #
    #      private  _methods invoked only inside  the data classes  chain                    #
    # -------------------------------------------------------------------------------------- #
    def _Load_Codes_Tables(self):
        self._TR_Codes_Table  = []  # TRCode GRcode   SPcode   TRdesc  StrToSear  FullDesc
        self._GR_Codes_Table  = []  # GRcode GRdescr  CAcode
        self._CA_Codes_Table  = []  # CAcode CAdescr

        self.Tree_Codes_View_List         = []
        self.Tree_Codes_View_List_Ordered = []

        self.GR_Codes_Ordered  = []
        self._CA_Codes_Ordered = []

        try:
            sqlite3.connect(self._Codes_DB_Filename)
            pass
        except:
            return 'Please mount data drive'

        connect = sqlite3.connect(self._Codes_DB_Filename)   # self.Files_Mngr.Codes_DB_Filename)
        cursor = connect.cursor()
        try:
            cursor.execute("SELECT * FROM TRANSACT_CODES")
            self._TR_Codes_Table = cursor.fetchall()
        except:
            connect.close()
            return 'Transations Codes ERROR'
        try:
            cursor.execute("SELECT * FROM GROUP_CODES")
            self._GR_Codes_Table = cursor.fetchall()
        except:
            connect.close()
            return 'Groups table ERROR'
        try:
            cursor.execute("SELECT * FROM CATEGORY_CODES")
            self._CA_Codes_Table = cursor.fetchall()
        except:
            connect.close()
            return 'Categories table ERROR'
        connect.close()

        if not self._TR_Codes_Table or not self._GR_Codes_Table or not self._CA_Codes_Table:
            return 'Codes tables EMPTY'

        # Create the TR_Code_Table with TRcode, TRdrsc , GRcode as in Codes_DB_yyyy-mm-dd.db
        # then update GRdesc, CAcode, CAdesc as in GR_Table and in CA_Table

        Index = -1
        self._TR_Codes_Full = []
        for Rec in self._TR_Codes_Table:
            Index += 1
            TRlist = list(Rec)
            TRcode = Rec[iTR_TRcode]
            TRdesc = Rec[iTR_TRdesc]
            GRcode = Rec[iTR_GRcode]

            GRrec = self._GR_Codes_Table[GRcode]
            GRdesc = GRrec[iGR_GRdesc]
            CAcode = self._Get_CA_Code_From_GR_Code(GRcode)

            CArec  = self._CA_Codes_Table[CAcode]
            CAdesc = CArec[iCA_CAdesc]

            TRlist[iTR_CAcode] = CAcode
            self._TR_Codes_Table[Index] = TRlist

            TR_Cod_Full = [ TRcode, GRcode, CAcode,
                            TRdesc, GRdesc, CAdesc,
                            TRlist[iTR_TRserc], TRlist[iTR_TRfullDes] ]
            self._TR_Codes_Full.append(TR_Cod_Full)
        self._Set_TR_View_List()
        self._GR_CA_Lists_Order()
        return OK

    # -----------------------------------------------------------------------
    def _GR_CA_Lists_Order(self):
        GR_Codes_List_Copy    = self._GR_Codes_Table.copy()
        self.GR_Codes_Ordered = List_Order(GR_Codes_List_Copy, iGR_GRdesc)
        CA_Codes_Table_Copy   = self._CA_Codes_Table.copy()
        self._CA_Codes_Ordered = List_Order(CA_Codes_Table_Copy, iCA_CAdesc)

    # -------------------------------------------------------------------------
    def _Set_TR_View_List(self):
        #  TRcode  TRDesc    GRdesc    CAdesc   StrToSear
        self.Tree_Codes_View_List = []
        for Rec in self._TR_Codes_Table:
            #     0       1         2        3         4
            #  TRcode  TRDesc    GRdesc    CAdesc   StrToSear
            TRcode = Rec[iTR_TRcode]
            GRcode = Rec[iTR_GRcode]
            GRrec  = self._GR_Codes_Table[GRcode]
            GRdesc = GRrec[iGR_GRdesc]
            CAcode = GRrec[iGR_CAcode]
            CAdesc = self._Get_CA_Descr(CAcode)
            List_View_Codes = [TRcode,              # 0
                               Rec[iTR_TRdesc],     # 1 ----------------------------------|
                               GRdesc,              # 2                                   |
                               CAdesc,              # 3                                   |
                               Rec[iTR_TRserc]]     # 4                                   |
            self.Tree_Codes_View_List.append(List_View_Codes)              #              |
            self.Tree_Codes_View_List_Ordered.append(List_View_Codes)      #              !
        self.Tree_Codes_View_List_Ordered = List_Order(self.Tree_Codes_View_List_Ordered, 1)

        self._GRdescr_Ordered_List = []
        for Rec in self._GR_Codes_Table:
            self._GRdescr_Ordered_List.append(Rec[iGR_GRdesc])
        self._GRdescr_Ordered_List.sort()

        self.CAdescr_Ordered = []
        for Rec in self._CA_Codes_Table:
            self.CAdescr_Ordered.append(Rec[iCA_CAdesc])
        self.CAdescr_Ordered.sort()

    # ----------  delete the las transaction codes record ------------------------
    def Delete_Last_TR_Code(self, Last_Code):
        Connect   = sqlite3.connect(self._Codes_DB_Filename)  # self.Files_Mngr.Codes_DB_Filename)
        Cursor    = Connect.cursor()
        try:
            Cursor.execute("DELETE FROM TRANSACT_CODES WHERE TR_Code==?", (Last_Code,))
            Connect.commit()
            Connect.close()
            return OK
        except:
            Connect.close()
            errMessage = 'ERROR on DELETING\nlast code record  '
            errMessage += str(Last_Code)
            return errMessage

    # -----------------------------------------------------------------------------------------------------------------
    def Add_TR_Record(self, Record):
        Connect = sqlite3.connect(self._Codes_DB_Filename)
        cursor  = Connect.cursor()
        TR      = Record[iTR_TRcode]
        GR      = Record[iTR_GRcode]
        CA      = self._Get_CA_Code_From_GR_Code(iGR_CAcode)
        Desc         = Record[iTR_TRdesc]
        StrToSearch  = Compact_Descr_String(Record[iTR_TRserc])
        Full_Descrip = Record[iTR_TRfullDes]
        try:
            cursor.execute("""
                     INSERT INTO TRANSACT_CODES (TR_Code, GR_Code, SP_Code, TR_Descr, Str_To_Search, Str_Full_Descrip)
                             VALUES (?, ?, ?, ?, ?, ?)""", (TR, GR, CA, Desc, StrToSearch, Full_Descrip))
            Connect.commit()
            Connect.close()
            return OK
        except:
            Connect.close()
            return 'ERROR on Codes database:\for record INSERT'

    # --------------   update a codes record on data base  --------------------------------
    def Update_DB_TR_Codes(self, Record):
        Connect  = sqlite3.connect(self._Codes_DB_Filename)   # self.Files_Mngr.Codes_DB_Filename)
        Cursor   = Connect.cursor()
        TR   = Record[iTR_TRcode]
        GR   = Record[iTR_GRcode]
        CA   = Record[iTR_CAcode]
        Desc = Record[iTR_TRdesc]
        StrToSearch  = Compact_Descr_String(Record[iTR_TRserc])
        Full_Descrip = Record[iTR_TRfullDes]

        sql = "UPDATE TRANSACT_CODES SET GR_Code=?, SP_Code=?, TR_Descr=?, Str_To_Search=?, Str_Full_Descrip=? WHERE TR_Code==?"
        sql_data = (GR, CA, Desc, StrToSearch, Full_Descrip, TR)
        try:
            Cursor.execute(sql, sql_data)
            Connect.commit()
            Connect.close()
            return OK
        except:
            Connect.close()
            return 'ERROR on Codes Database\nTR Record UPDATE'

    # --------------   update Group codes record on data base  --------------------------------------------------------
    def Update_GR_CA_Rec(self, List):
        Connect  = sqlite3.connect(self._Codes_DB_Filename)  # self.Files_Mngr.Codes_DB_Filename)
        Cursor   = Connect.cursor()
        GRcode   = List[0]
        GRdesc   = List[1]
        CAcode   = List[2]

        sql = "UPDATE GROUP_CODES SET GR_Code=?, GR_Descr=?, CA_Code=? WHERE GR_Code==?"
        sql_data = (GRcode, GRdesc, CAcode, GRcode)
        try:
            Cursor.execute(sql, sql_data)
            Connect.commit()
            Connect.close()
            return self._Load_Codes_Tables()
        except:
            Connect.close()
            return 'ERROR on Codes Database\nGR Record UPDATE'

    # -----------------------------------------------------------------------------------------------------------------
    def Check_If_Code_Exist(self, TRcode):
        for Rec in self._TR_Codes_Table:
            if Rec[iTR_TRcode] == TRcode:
                return True
        return False

    # -----------------------------------------------------------------------------------------------------------------
    def _Get_CA_Code_From_GR_Code(self, GR_Code):
        for Rec in self._GR_Codes_Table:
            if Rec[iGR_Grcode] == GR_Code:
                return Rec[iGR_CAcode]
        return 0

    def _Get_CA_Descr(self, CA_Code):
        for Rec in self._CA_Codes_Table:
            if Rec[iCA_CAcode] == CA_Code:
                return Rec[iCA_CAdesc]
        return ''

    # -----------------------------------------------------------------------------------------------------------------
    def Get_GR_CA_desc_From_TRdesc(self, TRDesc):
        GRdesc = ''
        CAdesc = ''
        for Code_Rec in self._TR_Codes_Table:
            if Code_Rec[iTR_TRdesc] == TRDesc:
                Code_GR = Code_Rec[iTR_GRcode]
                for GrRec in self._GR_Codes_Table:
                    if GrRec[iGR_Grcode] == Code_GR:
                        GRdesc = GrRec[iGR_GRdesc]
                        CAcode = GrRec[iGR_CAcode]
                        for CArec in self._CA_Codes_Table:
                            if CArec[iCA_CAcode] == CAcode:
                                CAdesc = CArec[iCA_CAdesc]
                                break
        return [GRdesc, CAdesc]

    # -----------------------------------------------------------------------------------------------------------------
    def Get_TR_GR_CA_desc_From_TRcode(self, TRcode):
        TRdesc = ''
        GRdesc = ''
        CAdesc = ''
        for Code_Rec in self._TR_Codes_Table:
            if Code_Rec[iTR_TRcode] == TRcode:
                TRdesc = Code_Rec[iTR_TRdesc]
                Code_GR = Code_Rec[iTR_GRcode]
                for GrRec in self._GR_Codes_Table:
                    if GrRec[iGR_Grcode] == Code_GR:
                        GRdesc = GrRec[iGR_GRdesc]
                        CAcode = GrRec[iGR_CAcode]
                        for CArec in self._CA_Codes_Table:
                            if CArec[iCA_CAcode] == CAcode:
                                CAdesc = CArec[iCA_CAdesc]
                                break
        return [TRdesc, GRdesc, CAdesc]


    # ---------------------------------------------------------------------------------------------
    def _Find_StrToSearc_InFullDesc(self, Row):  # nRow Contab Valuta   Full_Desc ....
        Full_Desc   = Row[iRow_Descr1]
        nFound      = 0
        Found_List  = []
        for TRrecord in self._TR_Codes_Table:
            StrToSearc = TRrecord[iTR_TRserc]

            # if self.ChecK_StrToSearch(StrToSearc, Full_Desc):
            if StrForSearc_in_Fulldescr(StrToSearc, Full_Desc):
                nFound += 1
                Found_List.append(TRrecord)

        if nFound == 1:
            return [OK, Found_List[0]]
        elif nFound == 0:
            return [NOK, []]
        else:
            print(Row)
            ErrMsg = ('In Xlsx file on:\n\nRow: ' + str(Row[iRow_nRow]) + '  Contab: ' + str(Row[iRow_Contab]))
            ErrMsg += '\nDescription:\n' + Row[iRow_Descr2] + '\n\nFound:\n'
            for Rec in Found_List:
                #print(Rec)
                strCode = str(Rec[iTR_TRcode])
                Texto = 'Code: ' + strCode + ' Descr: ' + Rec[iTR_TRdesc] + '\n'  + 'string for search: ' + Rec[iTR_TRserc] + '\n\n' #  strCode + '  Descr: ' + Rec[iTR_TRdesc] + '\nFor search: ' + Rec[iTR_TRserc] + '\n' )
                ErrMsg += Texto
                pass
            return [NOK, ErrMsg]
# ==============================================================================================================
