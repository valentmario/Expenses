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

        self._Multi_Codes_Matching_List = []  # full descriptions matching with the same StrToFind
        self.connect                    = None
        self.cursor                     = None

    # ----------------------   Check the database  codes table   --------------------------------
    # for each code record to check verify if in the restant code records
    # exists a record that has a fullDescr that match with the StrToFind to check
    # -------------------------------------------------------------------------------------------
    def Check_Codesdatabase(self, Db_Select):
        if Db_Select == CHECK_DBCODES_LOADED:
            TR_Codes_Table = self._TR_Codes_Table
        else:         # CHECK_TEMT_DBCODES
            TR_Codes_Table = self._tTR_Codes_Table

        self._Multi_Codes_Matching_List = []
        for Rec_To_Check in TR_Codes_Table:
            TR_toCheck = Rec_To_Check[iTR_TRcode]
            if TR_toCheck == 330:
                pass
            if TR_toCheck == 475:
                pass

            StrToCek = Rec_To_Check[iTR_TRstrToFind]
            for Rec in TR_Codes_Table:
                RecInChecking = Rec[iTR_TRcode]
                if RecInChecking == 330:
                    pass
                if RecInChecking == 475:
                    pass
                if Rec == Rec_To_Check:     # it's himself
                    pass
                else:                       # different record
                    FullDescr = Rec[iTR_TRfullDes]
                    if StrToFind_in_Fulldescr(StrToCek, FullDescr):
                        self._Multi_Codes_Matching_List.append(Rec_To_Check)
                        self._Multi_Codes_Matching_List.append(Rec)
        return self._Multi_Codes_Matching_List

    # ----------------------------------------------------------------------------------------
    def Get_Multiple_List(self):
        return self._Multi_Codes_Matching_List

    # -------------------------------------------------------------------------------------- #
    #      public methods invoked outside from  Top_Codes  classes                           #
    # -------------------------------------------------------------------------------------- #
    def Load_Codes_Tables(self, CodesFilename):
        Codes_Name = CodesFilename
        if CodesFilename == ON_SELECTIONS:
            Codes_Name = self._Codes_DB_Filename
        if Codes_Name == UNKNOWN:
            return 'Codes Database file unknown'
        Result = self._Load_Codes_Tables(Codes_Name)
        if Result != OK:
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

    # ----------------------------------------------------------------------------------------
    def Check_StrToFind_Exist_OnCodTable(self, StrToFind, Code):
        for Rec in self._TR_Codes_Table:
            FullDesc = Rec[iTR_TRfullDes]
            if StrToFind_in_Fulldescr(StrToFind, FullDesc):
                if Rec[iTR_TRcode] == Code:
                    pass
                else:
                    ErrMsg = ('New string to find:\n' + StrToFind +
                              '\n\nFound also on Record:\n' +
                              'Code: ' + str(Rec[iTR_TRcode]) + '\n' + FullDesc)
                    return [NOK, ErrMsg]
        return [OK, '']

    # ---------------------------------------------------------------------------------------------------
    @classmethod
    def Check_Codes_Record_Is_OK(cls, TR_RecToCheck):
        TR_CodeToCheck  = TR_RecToCheck[iTR_TRcode]
        TR_strTo_Find  = TR_RecToCheck[iTR_TRstrToFind]
        TR_FullDesc     = TR_RecToCheck[iTR_TRfullDes]
        GR_CodeToCheck  = TR_RecToCheck[iTR_GRcode]
        TR_DescToCheck  = TR_RecToCheck[iTR_TRdesc]
        if TR_FullDesc.find('nRow=') == -1:
            return 'Full Description NOT OK\nnRow=  fails'
        elif TR_CodeToCheck == 0 or GR_CodeToCheck == 0:
            return 'a TR or GR code is zero'
        elif len(TR_DescToCheck) < 3:
            return 'TR description too short'
        elif len(TR_strTo_Find) < 3:
            return 'String to find too short'
        elif TR_strTo_Find == 'Enter a String to find':
            return 'Enter a correct string to find'
        elif TR_DescToCheck == 'Set Transaction Description':
            return 'Enter a correct Transaction description'
        if not StrToFind_in_Fulldescr(TR_strTo_Find, TR_FullDesc):
            return 'String To Find:\n' + TR_strTo_Find + '\ndoes not match with Full Desription:\n' + TR_FullDesc
        return OK


    # -------------------------------------------------------------------------------------- #
    #      private  _methods invoked only inside  the data classes  chain                    #
    #    in case of error on loading TR-GR-CA Tables nothing is changed                      #
    # -------------------------------------------------------------------------------------- #
    def _Load_Codes_Tables(self, CodesFilename):
        self._tTR_Codes_Table  = []  # TRCode GRcode   SPcode   TRdesc  StrToSear  FullDesc
        self._tGR_Codes_Table  = []  # GRcode GRdescr  CAcode
        self._tCA_Codes_Table  = []  # CAcode CAdescr

        self.Tree_Codes_View_List         = []
        self.Tree_Codes_View_List_Ordered = []

        self.CodesFilename = CodesFilename

        try:  # ---------------------------------------------------------- # try connect
            self.connect = sqlite3.connect(CodesFilename)
        except sqlite3.Error as e:  # in case of error nothing change
            strErr = Db_Error(e)
            MsgErr = 'ERROR on connect Transactions Table:\n' + str(strErr)
            return MsgErr
        finally:
            self.cursor = self.connect.cursor()

        try: # ------------------------------------------------------------- # try load Transactions Codes
            self.cursor.execute("SELECT * FROM TRANSACT_CODES")
            self._tTR_Codes_Table = self.cursor.fetchall()
        except sqlite3.Error as e:  # in case of error nothing change
            strErr = Db_Error(e)
            MsgErr = 'ERROR on Loading Codes Table:\n' + str(strErr)
            if self.connect:
                self.connect.close()
            return MsgErr
        finally:
            pass

        try:  # ------------------------------------------------------------- # try load Groups codes
            self.cursor.execute("SELECT * FROM GROUP_CODES")
            self._tGR_Codes_Table = self.cursor.fetchall()
        except sqlite3.Error as e:  # in case of error nothing change
            strErr = Db_Error(e)
            MsgErr = 'ERROR on Loading Codes Table:\n' + str(strErr)
            if self.connect:
                self.connect.close()
            return MsgErr
        finally:
            pass

        try:  # ------------------------------------------------------------- # try load Categories codes
            self.cursor.execute("SELECT * FROM CATEGORY_CODES")
            self._tCA_Codes_Table = self.cursor.fetchall()
        except sqlite3.Error as e:  # in case of error nothing change
            strErr = Db_Error(e)
            MsgErr = 'ERROR on Loading Category Table:\n' + str(strErr)
            if self.connect:
                self.connect.close()
            return MsgErr
        finally:
            if self.connect:
                self.connect.close()

        # Check for multiple matching is made on the calling method
        self._TR_Codes_Table = self._tTR_Codes_Table
        self._GR_Codes_Table = self._tGR_Codes_Table
        self._CA_Codes_Table = self._tCA_Codes_Table

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
                            TRlist[iTR_TRstrToFind], TRlist[iTR_TRfullDes] ]
            self._TR_Codes_Full.append(TR_Cod_Full)
        self._Set_TR_View_List()
        self._GR_CA_Lists_Order()
        return OK

    # -----------------------------------------------------------------------
    def _GR_CA_Lists_Order(self):
        GR_Codes_List_Copy     = self._GR_Codes_Table.copy()
        self.GR_Codes_Ordered  = List_Order(GR_Codes_List_Copy, iGR_GRdesc)
        CA_Codes_Table_Copy    = self._CA_Codes_Table.copy()
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
            List_View_Codes = [TRcode,               # 0
                               Rec[iTR_TRdesc],      # 1 ----------------------------------|
                               GRdesc,               # 2
                               CAdesc,               # 3                                   |
                               Rec[iTR_TRstrToFind]] # 4                                   |
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
        Result = ''
        Connect   = sqlite3.connect(self._Codes_DB_Filename)  # self.Files_Mngr.Codes_DB_Filename)
        Cursor    = Connect.cursor()
        try:
            Cursor.execute("DELETE FROM TRANSACT_CODES WHERE TR_Code==?", (Last_Code,))
            Connect.commit()
            Connect.close()
            return OK
        except sqlite3.Error as e:                      # in case of error nothing change
            strErr = Db_Error(e)
            MsgErr = ('ERROR on deleting:\n\n' + 'Code: ' + str(Last_Code) + '\n\n'
                      ' in Codes Table:\n\n') + str(strErr)
            return MsgErr
        finally:
            if Connect:
                Connect.close()
                Result = self.Load_Codes_Tables(ON_SELECTIONS)
            return Result

    # -----------------------------------------------------------------------------------------------------------------
    def Add_TR_Record(self, Record):
        Connect   = sqlite3.connect(self._Codes_DB_Filename)
        cursor    = Connect.cursor()
        TR        = Record[iTR_TRcode]
        GR        = Record[iTR_GRcode]
        CA        = self._Get_CA_Code_From_GR_Code(iGR_CAcode)
        Desc      = Record[iTR_TRdesc]
        StrToFind = Compact_Descr_String(Record[iTR_TRstrToFind])
        Full_Descrip = Record[iTR_TRfullDes]
        try:
            cursor.execute("""
                     INSERT INTO TRANSACT_CODES (TR_Code, GR_Code, SP_Code, TR_Descr, Str_To_Search, Str_Full_Descrip)
                             VALUES (?, ?, ?, ?, ?, ?)""", (TR, GR, CA, Desc, StrToFind, Full_Descrip))
            Connect.commit()
            Connect.close()
        except sqlite3.Error as e:                      # in case of error nothing change
            strErr = Db_Error(e)
            MsgErr = ('ERROR on inserting:\n\n' + 'Code: ' + str(TR) + '\n\n'
                      ' in Codes Table:\n\n') + str(strErr)
            return MsgErr
        finally:
            if Connect:
                Connect.close()
            Result = self.Load_Codes_Tables(ON_SELECTIONS)
            return Result

    # --------------   update a codes record on data base  --------------------------------
    def Update_DB_TR_Codes(self, Record):
        Connect  = sqlite3.connect(self._Codes_DB_Filename)   # self.Files_Mngr.Codes_DB_Filename)
        Cursor   = Connect.cursor()
        TR   = Record[iTR_TRcode]
        GR   = Record[iTR_GRcode]
        CA   = Record[iTR_CAcode]
        Desc = Record[iTR_TRdesc]
        StrToFind    = Compact_Descr_String(Record[iTR_TRstrToFind])
        Full_Descrip = Record[iTR_TRfullDes]

        sql = "UPDATE TRANSACT_CODES SET GR_Code=?, SP_Code=?, TR_Descr=?, Str_To_Search=?, Str_Full_Descrip=? WHERE TR_Code==?"
        sql_data = (GR, CA, Desc, StrToFind, Full_Descrip, TR)
        try:
            Cursor.execute(sql, sql_data)
            Connect.commit()
            # Connect.close()
            # return OK
        except sqlite3.Error as e:                      # in case of error nothing change
            strErr = Db_Error(e)
            MsgErr = ('ERROR on Updating:\n\n' + 'Code: ' + str(TR) + '\n\n'
                      ' in Codes Table:\n\n') + str(strErr)
            return MsgErr
        finally:
            if Connect:
                Connect.close()
            Result = self.Load_Codes_Tables(ON_SELECTIONS)
            return Result

    # --------------   update Group codes record on data base  --------------------------------------------------------
    def Update_GR_CA_Rec(self, List):
            pass
        # Connect  = sqlite3.connect(self._Codes_DB_Filename)  # self.Files_Mngr.Codes_DB_Filename)
        # Cursor   = Connect.cursor()
        # GRcode   = List[0]
        # GRdesc   = List[1]
        # CAcode   = List[2]
        #
        # sql = "UPDATE GROUP_CODES SET GR_Code=?, GR_Descr=?, CA_Code=? WHERE GR_Code==?"
        # sql_data = (GRcode, GRdesc, CAcode, GRcode)
        # try:
        #     Cursor.execute(sql, sql_data)
        #     Connect.commit()
        # except sqlite3.Error as e:                      # in case of error nothing change
        #     strErr = Db_Error(e)
        #     MsgErr = ('ERROR on Updating:\n\n' + 'GR Code: ' + str(GRdesc) + '\n\n'
        #               ' in Groups Table:\n\n') + str(strErr)
        #     return MsgErr
        # finally:
        #     if Connect:
        #         Connect.close()
        #         Result = self._Load_Codes_Tables(CHECK_DBCODES_LOADED)
        #         return

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
    def _Find_StrToFind_InFullDesc(self, Row, Full_Desc):  # nRow Contab Valuta   Full_Desc ....
        nFound      = 0
        Found_List  = []    # [TRrecord, ..., TRrecord]
        for TRrecord in self._TR_Codes_Table:
            StrToFind = TRrecord[iTR_TRstrToFind]
            if StrToFind == '' and Full_Desc == '':
                pass
            if StrToFind_in_Fulldescr(StrToFind, Full_Desc):
                nFound += 1
                Found_List.append(TRrecord)
                #  TESTING
                # nFound += 1
                # Found_List.append(TRrecord)

        if nFound == 1:                         # Found only one String to find
            return [OK, Found_List[0]]
        elif nFound == 0:                       # String to find NOT found
            return [NOK, []]
        else:                                   # Multiple String_to_Tind matching
            ErrMsg = ('In Xlsx file for:\n\nRow: ' + str(Row[iRow_nRow]) + '  Contab: ' + str(Row[iRow_Contab]))
            ErrMsg += '\nFull Description:\n' + Full_Desc + '\n\nFound:\n'
            CodesFound = '  '
            for Rec in Found_List:
                strCode = str(Rec[iTR_TRcode])
                Texto   = 'Code: ' + strCode + '    Descr: ' + Rec[iTR_TRdesc] + '\n'
                Texto += 'string To find: ' + Rec[iTR_TRstrToFind] + '\n' + Rec[iTR_TRfullDes] + '\n'
                ErrMsg += Texto
                CodesFound += '  --   ' + strCode
            ErrMsg += 'Please Select the correct code:  '  + str(CodesFound)
            return [MULTI, ErrMsg]
# ==============================================================================================================
