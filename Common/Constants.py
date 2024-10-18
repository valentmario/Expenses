# ------------------------------------------------------------#
#           *****     Constants.py      *****                 #
#        Contains Constants Definition   23-11-11             #
# ------------------------------------------------------------#

# ------------------   Constants  for Widgets  ----------------
BakGnd    = '#567688'     # for all widgets
ForGnd    = "white"       # for all   " "
PRINT_ENABLED = False     # To print or NOT

DUAL_DISPLAY  = False
if DUAL_DISPLAY:
    Main_Wind_geometry     = '330x310+1580+1'     # '330x310+1700+10'
    Settings_geometry      = '330x400+1580+390'    # 330x400+1700+370
    Top_Mngr_geometry      = '660x1000+1000+10'    # 660x1000+2100+10
    Top_View_geometry      = '840x1000+2000+10'
    Top_View_geom_reduced  = '840x1000+350+200'
    Top_View_Mess_geometry = '450x470+600+10'
    Top_GRcodes_geometry   = '830x1000+1600+10'
    Top_Xlsx_View_geometry = '820x1000+1300+10'   # '820x1000+2040+10'
    Top_Insert_geometry    = '740x1000+2200+10'  # '610x1000+2870+10'
    Top_TrView_geometry    = '820x1000+3000+10'
    #                             1 Frame               2 Frames           3 Frames
    Top_Query_geometry     = ['630x1000+3200+10', '1080x1000+640+10', '1500x1000+200+10']
                           # ['630x1000+1060+10', '1060x1000+640+10', '1500x1000+200+10']
else:
    Main_Wind_geometry     = '330x310+1580+1'
    Settings_geometry      = '330x390+1580+360'
    Top_Mngr_geometry      = '660x1000+1000+1'
    Top_View_geometry      = '840x1000+350+1'
    Top_View_geom_reduced  = '840x470+350+200'
    Top_GRcodes_geometry   = '830x1000+20+1'
    Top_Xlsx_View_geometry = '820x1000+10+1'
    Top_View_Mess_geometry = '450x470+600+10'
    Top_Insert_geometry    = '740x1000+900+1'
    Top_TrView_geometry    = '820x1000+10+1'
    #                         one frame           two frames          three frames
    Top_Query_geometry     = ['630x1000+1020+10', '1080x1000+570+10', '1520x1000+130+10']

# ---------------------------   for queries  ----------------------------------------------------------------
# on the panel for queries can appear the following frames depending on Month and Total Months
# the frames used are three:  Frame1             Frame2             Fraame 3
# the months inserted are     1 (Jan-Dec)
#
VIEW_WITHCODE = 'View with Frames With Codes'
VIEW_WITHOUT  = 'View Frame Without Codes'

SELTR  = 'Scegli un codice'
ALLTR  = 'ogni codice'
ALLGR  = 'ogni gruppo'
ALLCA  = 'ogni categoria'

JAN   = 'Gennaio'
FEB   = 'Febbraio'
MARCH = 'Marzo'
APR   = 'Aprile'
MAY   = 'Maggio'
JUNE  = 'Giugno'
JULY  = 'Luglio'
AUG   = 'Agosto'
SEPT  = 'Settembre'
OCT   = 'Ottobre'
NOV   = 'Novembre'
DEC   = 'Dicembre'

Month_Names    = (JAN, FEB, MARCH, APR, MAY, JUNE, JULY, AUG, SEPT, OCT, NOV, DEC)
Month_Names_Compact = ('Gen  ','Feb  ','Mar  ','Apr  ','Mag  ','Giu  ','Lug  ','Ago  ','Set ','Ott  ','Nov  ','Dic')

ONE_MONTH     = '1  mese'
TWO_MONTHS    = '2  mesi'
THREE_MONTHS  = '3  mesi'
FOUR_MONTHS   = '4  mesi'
SIX_MONTHS    = '6  mesi'
TWELVE_MONTHS = '12 mesi'

MONTH_INT     = {JAN: 1, FEB:2, MARCH:3, APR:4, MAY:5, JUNE:6, JULY:7, AUG:8, SEPT:9, OCT:10, NOV:11, DEC:12}

TOT_MONTH_INT = {ONE_MONTH:1, TWO_MONTHS:2, THREE_MONTHS:3, FOUR_MONTHS:4, SIX_MONTHS:6, TWELVE_MONTHS:12}

LIST_TOT_12 = [ONE_MONTH, TWO_MONTHS, THREE_MONTHS, FOUR_MONTHS, SIX_MONTHS, TWELVE_MONTHS]
LIST_TOT_6  = [ONE_MONTH, TWO_MONTHS, THREE_MONTHS, FOUR_MONTHS, SIX_MONTHS]
LIST_TOT_4  = [ONE_MONTH, TWO_MONTHS, THREE_MONTHS, FOUR_MONTHS]
LIST_TOT_3  = [ONE_MONTH, TWO_MONTHS, THREE_MONTHS]
LIST_TOT_2  = [ONE_MONTH, TWO_MONTHS]
LIST_TOT_1  = [ONE_MONTH]
Queries_Tot_Dict = {JAN:  LIST_TOT_12, FEB: LIST_TOT_6,  MARCH: LIST_TOT_6, APR: LIST_TOT_6,
                    MAY: LIST_TOT_6,   JUNE: LIST_TOT_6, JULY:LIST_TOT_6,   AUG: LIST_TOT_4,
                    SEPT: LIST_TOT_4,  OCT: LIST_TOT_3,  NOV: LIST_TOT_2,   DEC: LIST_TOT_1}

xyToHide    = 10000
# ----------------------------------   queries :  trees, months, geomety  -----------------------------------
# Frames in view :   Frame1   Frame1-Frame2  Frame1-Frame2 -Frame3
#                          Frame geometry index per total Months   (see Top_Query_geometry)
Queries_Geometry_Index  = {ONE_MONTH:0, TWO_MONTHS:1, THREE_MONTHS:2, FOUR_MONTHS:1, SIX_MONTHS:2, TWELVE_MONTHS:2}


# Widgets (Text, Button, Combo) position for  1, 2 or 3 frames
#                               0   one Frame            1        two Frames       2  three Frames
Queries_Frames_PosX = [ [10, xyToHide, xyToHide, 465], [10, 455, xyToHide, 910], [10, 455, 900, 1350] ]
Widgets_PosY        = [450, 880, 1310]
#                          total frames per total months
Queries_nFrames     = {ONE_MONTH:1, TWO_MONTHS:2, THREE_MONTHS:3, FOUR_MONTHS:2, SIX_MONTHS:3, TWELVE_MONTHS:3}

#                          total months per frame
Queries_nMonts_xTree = {ONE_MONTH:1, TWO_MONTHS:1, THREE_MONTHS:1, FOUR_MONTHS:2, SIX_MONTHS:2, TWELVE_MONTHS:4}


# =========================================================== #
#       CHAT for  echanging   DATA between classes            #
# =========================================================== #
MAIN_WIND        = 'Main_Window     '
MODULES_MNGR     = 'Modules Manager'       # Top_Level Launcher
FILES_NAMES_MNGR = 'Files_Names_Mngr'    # .txt .db .xlsx files names manager
CODES_CLASS      = 'Codes_Class     '    # Codes Manager
XLSX_CLASS       = 'Xlsx_Class      '    # xlsx File Manager
TRANSACT_CLASS   = 'Transact_Class  '    # Transactions DB Manager
DATA_CLASS       = 'Data_Class'          # Class derived from all Data_Classe

TOP_SETTINGS     = 'Top_Settings    '      # Toplevel for Settings
TOP_CODES_MNGR   = 'Top_Codes_Mngr  '      # Toplevel TR Codes Manager
TOP_CODES_VIEW   = 'Top_Codes_View  '      # Toplevel Codes Viewer
TOP_GR_MNGR      = 'Top_GR_Manager  '      # Toplevel GR Codes Manager
TOP_XLSX_VIEW    = 'Xlsx Rows View  '      # Toplevel  xlsx File Viewer
TOP_INS          = 'Top_Ins_Tansact '      # Toplevel Insert Transactions on DB
TOP_VIEW_TRANSACT= 'Top View Transact'   # Topleveel view transactions
TOP_QUERY        = 'Top_Queries     '      # Toplevel for Queries
TOP_VIEW_MESS    = 'Top show messages '    # Toplevel to shaw messages
ANY              = 'All Modules     '

# Checkes to be maade before a Tolevel launch
CEK_CODES      = 'Check codes DB     '
CEK_CODES_TRUE = 'Check codes DB if OK'
CEK_XLSX_LIST  = 'Check xlsx lists   '
CEK_XLSX_TRUE  = 'Check xlsx if OK   '

CEK_TOP_INSERT = 'Check for Top_Insert '
CEK_TOP_QUERIES= 'Check for Top_Queries '

LAUNCH_CHECKOUT = [ [TOP_SETTINGS,      []],
                    [TOP_CODES_MNGR,    [CEK_CODES,      CEK_XLSX_LIST]],
                    [TOP_CODES_VIEW,    [CEK_CODES]],
                    [TOP_GR_MNGR,       [CEK_CODES]],
                    [TOP_XLSX_VIEW,     [CEK_CODES,       CEK_XLSX_LIST]],
                    [TOP_INS,           [CEK_CODES_TRUE,  CEK_XLSX_TRUE, CEK_TOP_INSERT]],
                    [TOP_VIEW_TRANSACT, [CEK_CODES_TRUE,  CEK_TOP_QUERIES]],
                    [TOP_QUERY,         [CEK_CODES_TRUE,  CEK_TOP_QUERIES]],
                    [TOP_VIEW_MESS,     []] ]

# Participants_List  [<class name>,  Name]
Ix_TopClass = 0
Ix_TopName  = 1

# Requests Code for Messages between classes
CODE_TO_CLOSE        = 'Close window'
CODE_SHOW_PARTIC_LIST= 'Show Participants List'     # Show Chat Participants List

UPDATE_FILES_NAME   = 'Update Selections'           # only for Main_Widow Set_Selections()
CODE_CLK_ON_TR_CODES= 'Clicked Row with TR Codes'   # Clkd on Codes_DB Record Values = [TRcode]
CODE_CLIK_ON_XLSX   = 'Clkded On_Xlsx_Tree  '       # Clkd on Xlsx Row  Value = [nRow, Data_Valuta]
CODE_CLEAR_FOCUS    = 'Clear Focus   '
CODES_DB_UPDATED    = 'Codes database update'
XLSX_UPDATED        = 'Xlsx ists created'
XLSX_ROWS_LOADED    = 'Xlsx rows loaded'
TRANSACT_UPDATED    = 'Transactions updated'
MULTI_MATCH         = 'Multple StrToSearc matching'

CODE_CLIK_ONTREE    = 'Code_Clkd_on_Tree'            # For Testing ONLY

ON_SELECTIONS       = 'Filename in Selections'

# =========================================================== #
#             FILES  PARAMETERS                               #
# =========================================================== #
# Files Types Identifier
Id_File_DBcodes  = 'Codes DB'
Id_File_xlsx     = 'Xlsx file'
Id_File_Transact = 'Transactions DB'
Id_File_Any      = 'Any'

UNKNOWN          = 'unknown'
NEW  = 'New file created'
YES  = 'YES'
NO   = 'NO'
NONE = 'None'
OK     = 'OK'
NOK    = 'NOK'
LOADED = 'Loaded'   # it means that the file or Db are Loaded but can contains error
EMPTY  = 'Empty'

ALL_CODES   = 'All codes'
ALL_GROUPS  = 'All groups'
ALL_CAT     = 'All categories'

Selections_Dir_Name    = '/home/mario/aExp_Selections'
Selections_Full_Name   = '/home/mario/aExp_Selections/Selections'
Default_Init_Dir       = '/home/mario/bFiles'
#Default_Init_Dir       = '/home/mario/bXLSX_Files/FIDEU/FIDEU_2023'

# Txt File Items Indexes  ----------------------------
Ix_Codes_File    = 0
Ix_Xlsx_File     = 1
Ix_Sheet_Name    = 2
Ix_Transact_File = 3
Ix_Query_List    = 4
Ix_TOP_ToStart   = 5

# insert/Queries Indexes  ----------------------------
Ix_Query_Conto     = 0
Ix_Query_Month     = 1
Ix_Query_TotMonths = 2
Ix_Query_TRsel     = 3
Ix_Query_GRsel     = 4
Ix_Query_CAsel     = 5

# Used on Modules Mananager To Load Files only once
# at startup or after a file selection
Ix_Codes_Loaded      = 0
Ix_Xlsx_Lists_Loaded = 1
Ix_Transact_Loaded   = 2

# =============================================================
#             WIDGETS  CONSTANTS                              =
# =============================================================
# xyToHide    = 10000
Lab_Blue    = 1
Lab_FileSel = 2
Lab_Err     = 3

Btn_Def_En  = 1      # Button Default greeen     Enabled
Btn_Col_En  = 2      # Button Colored (brown)
Btn_Bol_En  = 3      # Button green bold
Btn_Def_Dis = 4      # Button Default greeen     Disabled
Btn_Col_Dis = 5      # Button Colored (brown)
Btn_Bol_Dis = 6      # Button green bold
Btn_Msg     = 7      # Button for Message

Btn_Disab  = 1      # Button Disabled
Btn_Enab   = 2      # Button Enabled (normal)

MsgBox_Info = 'Info message'
MsgBox_Ask  = 'Ask message'
MsgBox_Err  = 'Err message'

FileBox_Codes    = 'Codes file'
FileBox_Xlsx     = 'Xlsx file'
FileBox_Transact = 'Transact file'

Txt_Enab     = 'Txt_Enab'      # Text enable     Black on Mustard
Txt_Disab    = 'Txt_Disab'     # Text disabled   White on Light Blue
Txt_DisBlak  = 'Txt_DisBlak'   # Text Disabled   Black on Light Blue
Txt_MsgWhite = 'Txt_MsgWhite'  # Text for MsgBox White on Mustard
Txt_MsgErr   = 'Txt_MsgErr'    # Text for MsgBox Red on Mustard

Col_Mustard  = '#749D5F'
Col_BluLit   = 0

TxtBkgDisab = '#559CC2'     # sky blue
TxtBkgEnab  = '#749D5F'     # gray yellow

iTreeNrows = 0      # Tree number of columns to view
iTreeNcol  = 1
iTreeHead  = 2
iTreeAnch  = 3
iTreeWidth = 4

NoFocus    = -1

VIEW_ALPHAB    = 'alfabeticamente'
VIEWxCODE      = 'ordine per codice'
VIEW_SEARCH    = 'Stringa chiave'
CODES_VIEW_SEL = [VIEW_ALPHAB, VIEWxCODE, VIEW_SEARCH]

# =========================================================== #
#             DATA BASES  STRUCTURE                           #
# =========================================================== #
VIEW_ONLY_ERROR  = 1
VIEW_OKand_ERROR = 2

CHECK_DBCODES_LOADED = 1
CHECK_TEMT_DBCODES   = 2
ISSTRING             = 1
ISLIST               = 2

#   -----  Database  Codes_DB_yyy-mm-dd.db -----------------
# TABLE  TRANSACT_CODES
Len_Codes_Filename_Min  = 22
Ident_DB_Filename   = 'Codes_DB/Codes_DB_20'
iTR_TRcode    = 0  # UNIC TR CODE
iTR_GRcode    = 1
iTR_CAcode    = 2  # Must be selected fro GROUPS_TABLE
iTR_TRdesc    = 3
iTR_TRstrToFind    = 4
iTR_TRfullDes = 5
TR_Rec_Default = [0, 0, 0, 'Desc', 'Search', 'Full_Desc']

iTR_Ful_TRcode  = 0
iTR_Ful_GRcode  = 1
iTR_Ful_CAcode  = 2
iTR_Ful_TRdesc  = 3
iTR_Ful_GRdesc  = 4
iTR_Ful_CAdesc  = 5
iTR_Ful_TRfind  = 6
iTR_Ful_TRful   = 7

MAX_TR_CODE_NUM = 500
MAX_GR_CODE_NUM = 50

# TABLE  GROUP_CODES
iGR_Grcode = 0
iGR_GRdesc = 1
iGR_CAcode = 2
GR_Rec_Deafault = [0, 'GR Decr', 0]

# TABLE  CATEGORY_CODES
iCA_CAcode = 0
iCA_CAdesc = 1
CA_Rec_Deafault = [0, 'CA descr']

# Default TR GR CA  Codes
Def_TRcode = 0
Def_GRcode = 0
Def_CAcode = 0

#   -----  Database  /TRNSACTIONS/Transact_2024.db  ----------
TRANSACTIONS = 'TRANSACTIONS'
Transact_    = 'Transact_'
TRANSACT_ID  = 'TRANSACTIONS/Transact_'
Len_Transact_Filename = 16
iTransact_nRow   = 0
iTransact_Conto  = 1
iTransact_Contab = 2
iTransact_Valuta = 3
iTransact_TRdesc = 4
iTransact_Accred = 5
iTransact_Addeb  = 6
iTransact_TRcode = 7

Ix_Xlsx_Conto    = 0
Ix_Xlsx_Year     = 1
Ix_Xlsx_Month    = 2
Ix_Transact_Year = 3

FIDEU       = 'FIDEU'      # Fideuram Account    Must be 5 chars length
FLASH       = 'FLASH'      # Flash Card          Must be 5 chars length
FIDFLHBP    = 'FID+FLH+BP' # FIDEU/FLASH/POSTA   Doesn't matter
POSTA       = 'POSTA'      # Poste Italiane      Must be 5 chars length
AMBRA       = 'AMBRA'      # Credit Card Ambra   Must be 5 chars length
Conto_List  = [FIDEU, FLASH, FIDFLHBP, POSTA, AMBRA]

# -----------------------------------------------------------------------------------------------------------
#                      0        1         2         3         4        5        6      7
# List_Transact_DB :  nRow    Conto    Contab    Valuta    TR_Desc   Accred   Addeb  TRcode

# =====================================       Trees  Lists        ========================================= #
#                            0      1          2         3       4         5      6                         #
# XLS_Row_List          : nRow    Contab    Valuta    Des1     Accr      Addeb   Des2      as in xlsx File  #
# XLS_Row_Compact       : nRow    Contab    Valuta    Des1Comp Accr      Addeb,  Des2Comp                   #
# List View Codes       : TRcode  TR_Desc   GR_Desc   CA_Desc  StrToSear                                    #
# List_Rows_WithoutCode : nRow    Date      FullDesc                                                        #
# List_Rows_WithCode    : nRow    Contab    Valuta    TR_Desc   Accred   Addeb   TRcode                     #
# Query_View_List       : Date    TR_Desc   Accred    Addeb                                                 #
# ========================================================================================================= #
Ix_Tot_OK           = 0
Ix_Tot_WithCode     = 1
Ix_Tot_Without_Code = 2

Len_Xlsx_Filename_Min = 18
# XLS_Row_List
iRow_nRow   = 0
iRow_Contab = 1
iRow_Valuta = 2
iRow_Descr1 = 3
iRow_Accr   = 4
iRow_Addeb  = 5
iRow_Descr2 = 6

# List_WithCode
iNoCode_nRow     = 0
iNoCode_Date     = 1
iNoCode_Addeb    = 2
iNoCode_FullDesc = 3

# List_WithCode
iWithCode_nRow     = 0
iWithCode_Contab   = 1
iWithCode_Valuta   = 2
iWithCode_TR_Desc  = 3
iWithCode_Accr     = 4
iWithCode_Addeb    = 5
iWithCode_TRcode   = 6
iWithCode_FullDesc = 7

# List_View_Codes
iView_TRcode    = 0
iView_TRdesc    = 1
iView_GRdesc    = 2 # these constants are not used
iView_CAdesc    = 3 # because GRdesc CAdesc StrToFind are
iView_StrToFind = 4 # as on Codes Tables

iQuery_Date     = 0
iQuery_Descr    = 1
iQuery_Accr     = 2
iQuery_Addeb    = 3

# ----------------------  List of Controls  To Check XLS rows Data ------------------------------------------
INTEGER = 'Integer'
NOT_INT = 'String'
NUMERIC = 'Numeric'
DATE    = 'Date'
STRING  = 'String'
VAL_DATE = 'Data valuta'
ACC_DATE = 'Data contabile'

List_For_XLSX_Row_Control = [
    [iRow_nRow,   INTEGER],
    [iRow_Contab, DATE],    [iRow_Valuta, DATE],   [iRow_Descr1, STRING],
    [iRow_Accr,   NUMERIC], [iRow_Addeb, NUMERIC], [iRow_Descr2, STRING]]

# -----------------------------------------------------------------------------------------------------------
                        #   --- Items ---
Default_Selections_List = [UNKNOWN,                           # 0 Ix_Codes_File
                           UNKNOWN,                           # 1 Ix_Xlsx_File
                          'Sheet Name',                       # 2 Ix_Sheet_Name    ----- Elements  -----
                           UNKNOWN,                           # 3 Ix_Transact_File [Year,Conto, Mon,Tot,
                          [FIDEU, JAN, ONE_MONTH,             # 4 Query  [Conto, Month, Tot, ...
                           ALL_CODES, ALL_GROUPS, ALL_CAT],   #   TR GR CA  selected]
                          [] ]                                # 5 Top to start

# ===========================================================================================================
