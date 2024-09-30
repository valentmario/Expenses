# ----------------------------------------------------------------------------#
#               *****     Common_Functions.py      *****                      #
# ----------------------------------------------------------------------------#

from Common.Constants import *

# --------- get  ['Dir_Name', 'Filename']  from a generic path ----------------
def Get_Dir_Name(Full_Name):
    iLastBar = int(Full_Name.rfind("/") + 1)
    return Full_Name[:iLastBar]

def Get_File_Name(Full_Name):
    iLastBar = int(Full_Name.rfind("/") + 1)
    return Full_Name[iLastBar:]

def Get_intMonth_FromStr(nameStr):
    intMonth = -1       # 0-11
    for Name in Month_Names:
        intMonth += 1
        if Name == nameStr:
            return intMonth
    return 0

# -----------------------------------------------------------------------------
def Compact_Descr_String(Descr):
    Type = type(Descr)
    if Type is None or Type is not str:
        return ''
    # if Descr is None:
    #     return ' '
    myStr = ''
    nSpace = 0
    for Char in Descr:
        if Char == ' ':
            if not nSpace:
                myStr += ' '
                nSpace += 1
        else:
            nSpace = 0
            if '0' <= Char <= '9':
                myStr += Char
            elif 'A' <= Char <= 'Z':
                myStr += Char
            elif 'a' <= Char <= 'z':
                myStr += Char.upper()
            elif Char == '#':
                myStr += Char
    return myStr

def CheckInteger(strInt):
    for Digit in strInt:
        if Digit < '0' or Digit > '9':
            return False
    return True

def Check_strYear(strYear, Min, Max):
    for Digit in strYear:
        if Digit < '0' or Digit > '9':
            return False
    intYear = int(strYear)
    if intYear < Min or intYear > Max:
        return False
    return True

def Check_strMonth(strMonth):
    for Digit in strMonth:
        if Digit < '0' or Digit > '9':
            return False
    intMonth = int(strMonth)
    if intMonth < 1 or intMonth > 12:
        return False
    return True

# -----------------------------------------------------------------------------
def List_Order(List, index):
    List_ord = List
    TotRow = len(List)
    Order = True
    while Order:
        Found = False
        for i in range(0, TotRow - 1):
            Row0  = List_ord[i]
            Row1  = List_ord[i + 1]
            Text0 = Row0[index]
            Text1 = Row1[index]
            if Text0 > Text1:
                List_ord[i] = Row1
                List_ord[i + 1] = Row0
                Found = True
        if not Found:
            Order = False
    return List_ord
# -----------------------------------------------------------------------------
def Print_Received_Message(Txtr, Recvr, Request, Values_List):
    strToPrint = '*** '
    strToPrint += 'TXMTR: '+Txtr+'   RECVR: '+Recvr+'   REQUEST: '+Request
    strToPrint += '   VALUES: ' + str(Values_List)
    PRINT(strToPrint)

# -------------------------------------------------------------------------------------
def Get_List_Index(List, Ncol_For_Find, ValueToFind, default):
    index = -1
    for Rec in List:
        index += 1
        if Rec[Ncol_For_Find] == ValueToFind:
            return index
    return default

def Get_List_Item(List, Ncol_For_Find, ValueToFind, Ncol_To_Get, default):
    index = -1
    for Rec in List:
        index += 1
        if Rec[Ncol_For_Find] == ValueToFind:
            return Rec[Ncol_To_Get]
    return default

def Get_List_Record(List, Ncol_For_Find, ValueToFind, default):
    index = -1
    for Rec in List:
        index += 1
        Value = Rec[Ncol_For_Find]
        if Value == ValueToFind:
            return Rec
    return default

# -----------------------------------------------------------------------------
def Get_Xlsx_Year(Xlsx_Name):
    Filename = Get_File_Name(Xlsx_Name)
    Year = Filename[6:10]
    return int(Year)

def Get_Transactions_Year(Transact_Filenae):
    Filename = Get_File_Name(Transact_Filenae)
    return int(Filename[9:13])

def Get_YearMonthDay(TheDate):
    iYear  = int(TheDate[:4])
    iMonth = int(TheDate[5:7])
    iDay   = int(TheDate[8:10])
    return [iYear, iMonth, iDay]

def Conv_En_To_It_Date(Eng_Date):
    # 2023/01/31
    # 0123456789
    Day   = Eng_Date[8:10]    # 31
    Month = Eng_Date[5:7]     # 05
    Year  = Eng_Date[2:4]     # 24
    Italian_Date = Day + '/' + Month + '/' + Year
    return Italian_Date

# ----------------------------------------------------------------------------#
def TestForSign(Sign, FoundNotZ):
    if Sign and FoundNotZ == 1:
        return '-'
    else:
        return ''

# -------------------------------------------------------------------------------------------------------------
def Convert_To_Float(Value):
    Type = type(Value)
    if Type is float:
        return Value
    if Type is int:
        return float(Value)
    return 0.00

# ---------------------------------------------------------------------------------------
def Float_ToString_Setup(Val):
    Digit_List = []
    strValue = ''
    if Val == '' or Val == ' ' or Val == 0.0:
        return ' '
    Value = round(Val)
    AbsValue = abs(Value)
    if AbsValue < 15.0 or AbsValue > 10000.0:
        print(Value)

    mySign = False
    flPositValue = Value
    # if type(Value) is not float:
    #     return

    if Value < 0:
        mySign = True
        flPositValue = -Value
    Intx100_Value = int((flPositValue + 0.005) *100.0)     # Truncated at 2 decimal

    if Intx100_Value >= 10000000000:
        Intx100_Value = 9999999999
    #         10.000.000,00
    Divisor = 1000000000
    for iDigit in range(0,10):
        Significant = int(Intx100_Value / Divisor)
        Digit_List.append(Significant)
        Intx100_Value = Intx100_Value - Significant*Divisor
        Divisor = int(Divisor/10)

    for iDigit in range(0,10):          # create 00.000.000,00
        strValue += str(Digit_List[iDigit])
        if iDigit == 1 or iDigit == 4:
            strValue += '.'
        if iDigit == 7:
            strValue += ','

    strValCompact = ''
    FoundNotZ = 0
    for iChar in range(0, 13):
        CurrChar = strValue[iChar]
        if CurrChar == '.':
            if FoundNotZ:
                strValCompact += '.'
        elif CurrChar == ',':  # <<<<<<<<<<<<<<<<<<<<<<
            break
            # strValCompact += ','
            # FoundNotZ += 1
        elif iChar == 9:
            if CurrChar != '0':
                FoundNotZ += 1
                strValCompact += TestForSign(mySign, FoundNotZ)
                mySign = False
                strValCompact += CurrChar
            else:
                FoundNotZ = 1
                strValCompact += TestForSign(mySign, FoundNotZ)
                mySign = False
                strValCompact += '0'
        else:
            if CurrChar != '0':
                FoundNotZ += 1
                strValCompact += TestForSign(mySign, FoundNotZ)
                mySign = False
                strValCompact += CurrChar
            else:
                if FoundNotZ:
                    strValCompact += CurrChar
                else:
                    strValCompact += ' '
    return strValCompact

    # Digit_List = []
    # strValue = ''
    # if Val == '' or Val == ' ' or Val == 0.0:
    #     return ' '
    # Value = round(Val)
    # AbsValue = abs(Value)
    # if AbsValue < 15.0 or AbsValue > 10000.0:
    #     print(Value)
    #
    # mySign = False
    # flPositValue = Value
    # # if type(Value) is not float:
    # #     return
    #
    # if Value < 0:
    #     mySign = True
    #     flPositValue = -Value
    # Intx100_Value = int((flPositValue + 0.005) *100.0)     # Truncated at 2 decimal
    #
    # if Intx100_Value >= 10000000000:
    #     Intx100_Value = 9999999999
    # #         10.000.000,00
    # Divisor = 1000000000
    # for iDigit in range(0,10):
    #     Significant = int(Intx100_Value / Divisor)
    #     Digit_List.append(Significant)
    #     Intx100_Value = Intx100_Value - Significant*Divisor
    #     Divisor = int(Divisor/10)
    #
    # for iDigit in range(0,10):          # create 00.000.000,00
    #     strValue += str(Digit_List[iDigit])
    #     if iDigit == 1 or iDigit == 4:
    #         strValue += '.'
    #     if iDigit == 7:
    #         strValue += ','
    #
    # strValCompact = ''
    # FoundNotZ = 0
    # for iChar in range(0, 13):
    #     CurrChar = strValue[iChar]
    #     if CurrChar == '.':
    #         if FoundNotZ:
    #             strValCompact += '.'
    #     elif CurrChar == ',':  # <<<<<<<<<<<<<<<<<<<<<<
    #         break
    #         # strValCompact += ','
    #         # FoundNotZ += 1
    #     elif iChar == 9:
    #         if CurrChar != '0':
    #             FoundNotZ += 1
    #             strValCompact += TestForSign(mySign, FoundNotZ)
    #             mySign = False
    #             strValCompact += CurrChar
    #         else:
    #             FoundNotZ = 1
    #             strValCompact += TestForSign(mySign, FoundNotZ)
    #             mySign = False
    #             strValCompact += '0'
    #     else:
    #         if CurrChar != '0':
    #             FoundNotZ += 1
    #             strValCompact += TestForSign(mySign, FoundNotZ)
    #             mySign = False
    #             strValCompact += CurrChar
    #         else:
    #             if FoundNotZ:
    #                 strValCompact += CurrChar
    #             else:
    #                 strValCompact += ' '
    # return strValCompact

# -----------------------------------------------------------------------------
def GetStrList_ForFind(strToFind):
    if strToFind[0:1] != '#':
        return [strToFind]
    strList = []
    index = 0
    nextStr = ''
    for Char in strToFind[index+1:]:
        index +=1
        if Char != '#':
            nextStr += Char
        else:
            strList.append(nextStr)
            nextStr = ''
            if index >= len(strToFind):
                break
    return strList

# -----------------------------------------------------------------------------
# def StrForSearc_in_Fulldescr(strToFind, String):
#     strList = GetStrList_ForFind(strToFind)
#     if not strList:
#         return False
#     index = 0
#     CurrString = String
#     for Item in strList:
#         FirstOccurence = CurrString.find(Item)
#         if FirstOccurence == -1:
#             return False
#         index += FirstOccurence
#         CurrString = String[index:]
#     return True

def StrForSearc_in_Fulldescr(strToFind, String):
    strList = GetStrList_ForFind(strToFind)
    if not strList:
        return False
    index = 0
    CurrString = String
    for Item in strList:
        FirstOccurence = CurrString.find(Item)
        if FirstOccurence == -1:
            return False
        index += FirstOccurence
        CurrString = String[index:]
    return True

# -------------------------------------------------------------------------------------
def PRINT(message):
    if PRINT_ENABLED:
        print(message)

# =======================================================================================
