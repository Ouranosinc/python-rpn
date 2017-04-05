#!/usr/bin/env python
# -*- coding: utf-8 -*-
# . s.ssmuse.dot /ssm/net/hpcs/201402/02/base \
#                /ssm/net/hpcs/201402/02/intel13sp1u2 \
#                /ssm/net/rpn/libs/15.2 \
#                /ssm/net/cmdn/tests/vgrid/6.0.0-a4/intel13sp1u2
# Author: Stephane Chamberland <stephane.chamberland@canada.ca>
# Copyright: LGPL 2.1

"""
Module burpc is a ctypes import of burp_c's library (libburp_c_shared.so)
 
The burpc.proto python module includes ctypes prototypes for 
burp_c's libburp_c C functions.

Warning:
    Please use with caution.
    The functions in this module are actual C funtions and must thus be called
    as such with appropriate argument typing and dereferencing.
    It is highly advised in a python program to prefer the use of the
    python wrapper found in
    * rpnpy.burpc.base

Notes:
    The functions described below are a very close ''port'' from the original
    [[Cmda_tools#Librairies.2FAPI_BURP_CMDA|burp_c]] package.<br>
    You may want to refer to the [[Cmda_tools#Librairies.2FAPI_BURP_CMDA|burp_c]] documentation for more details.

See Also:
    rpnpy.burpc.brpobj
    rpnpy.burpc.base
    rpnpy.burpc.const

Details:
    See Source Code

##DETAILS_START
== Functions C Prototypes ==

<source lang="python">

 ## c_vgd_construct():
 ##    Returns a NOT fully initialized VGridDescriptor instance
 ##    Proto:
 ##       vgrid_descriptor* c_vgd_construct();
 ##    Args:
 ##       None
 ##    Returns:
 ##       POINTER(VGridDescriptor) : a pointer to a new VGridDescriptor object

</source>
##DETAILS_END
"""

import ctypes as _ct
import numpy  as _np
import numpy.ctypeslib as _npc

from . import libburpc
from rpnpy.burpc import const as _cst

def brp_filemode(filemode='r'):
    """
    #TODO: desc
    """
    if filemode in _cst.BRP_FILEMODE2FST_INV.keys():
        filemode = _cst.BRP_FILEMODE2FST_INV[filemode]
    try:
        fstmode, brpmode = _cst.BRP_FILEMODE2FST[filemode]
    except:
        raise ValueError('Unknown filemode: "{}", should be one of: {}'
                        .format(filemode, repr(_cst.BRP_FILEMODE2FST.keys())))
    return fstmode, brpmode, _cst.BRP_FILEMODE2FST_INV[brpmode]


class BURP_RPT(_ct.Structure):
    """
    Python Class equivalenet of the burp_c's BURP_RPT C structure to hold
    the BURP report data

    typedef struct {
        int  *buffer;
        int  handle;
        int  nsize;
        int  temps;
        int  flgs;
        char stnid[10];
        int  idtype;
        int  lati;
        int  longi;
        int  dx;
        int  dy;
        int  elev;
        int  drnd;
        int  date;
        int  oars;
        int  runn;
        int  nblk;
        int  *sup;
        int  nsup;
        int  *xaux;
        int  nxaux;
        int  lngr;
        int  init_hdr; /* for internal use only */
    } BURP_RPT ;


    To get an instance of a pointer to this class you may use the
    provided functions:

    myBURP_RPTptr = rpnpy.burpc.proto.c_brp_newrpt()

    See Also:
       c_brp_newrpt
       c_brp_newblk
       BURP_BLK
   """
    _fields_ = [
        ("buffer", _ct.POINTER(_ct.c_int)),
        ("handle", _ct.c_int),
        ("nsize",  _ct.c_int),
        ("temps",  _ct.c_int),
        ("flgs",   _ct.c_int),
        ("stnid",  _ct.c_char * _cst.BRP_STNID_STRLEN),
        ("idtype", _ct.c_int),
        ("lati",   _ct.c_int),
        ("longi",  _ct.c_int),
        ("dx",     _ct.c_int),
        ("dy",     _ct.c_int),
        ("elev",   _ct.c_int),
        ("drnd",   _ct.c_int),
        ("date",   _ct.c_int),
        ("oars",   _ct.c_int),
        ("runn",   _ct.c_int),
        ("nblk",   _ct.c_int),
        ("sup",   _ct.POINTER(_ct.c_int)),
        ("nsup",   _ct.c_int),
        ("xaux",  _ct.POINTER(_ct.c_int)),
        ("nxaux",  _ct.c_int),
        ("lngr",   _ct.c_int),
        ("init_hdr", _ct.c_int)  ## for internal use only
        ]
    
    ## def __str__(self):
    ##    return self.__class__.__name__ + str([x[0] + '=' + str(self.__getattribute__(x[0])) for x in self._fields_])
    ##    ## s = self.__class__.__name__ + '('
    ##    ## l = [y[0] for y in self._fields_]
    ##    ## l.sort()
    ##    ## for x in l:
    ##    ##     s += x + '=' + str(self.__getattribute__(x)) + ', '
    ##    ## s += ')'
    ##    ## return s

    def __repr__(self):
       ## return self.__class__.__name__ + repr([x[0] + '=' + repr(self.__getattribute__(x[0])) for x in self._fields_])
       return self.__class__.__name__ + '(' + \
           repr(dict([(x[0], self.__getattribute__(x[0])) for x in self._fields_])) + ')'


class BURP_BLK(_ct.Structure):
    """
    Python Class equivalenet of the burp_c's BURP_BLK C structure to hold
    the BURP block data

    typedef struct {
        int    bkno;
        int    nele;
        int    nval;
        int    nt;
        int    bfam;
        int    bdesc;
        int    btyp;
        int    bknat;
        int    bktyp;
        int    bkstp;
        int    nbit;
        int    bit0;
        int    datyp;
        char   store_type;
        int    *lstele;
        int    *dlstele;
        int    *tblval;
        float  *rval;
        double *drval;
        char   *charval;
        int    max_nval, max_nele, max_nt;
        int    max_len;
    } BURP_BLK ;


    To get an instance of a pointer to this class you may use the
    provided functions:

    myBURP_BLKptr = rpnpy.burpc.propo.c_brp_newblk()

    See Also:
       c_brp_newrpt
       c_brp_newblk
       BURP_RPT
   """
    _fields_ = [
        ("bkno",  _ct.c_int),
        ("nele",  _ct.c_int),
        ("nval",  _ct.c_int),
        ("nt",    _ct.c_int),
        ("bfam",  _ct.c_int),
        ("bdesc", _ct.c_int),
        ("btyp",  _ct.c_int),
        ("bknat", _ct.c_int),
        ("bktyp", _ct.c_int),
        ("bkstp", _ct.c_int),
        ("nbit",  _ct.c_int),
        ("bit0",  _ct.c_int),
        ("datyp", _ct.c_int),
        ("store_type", _ct.c_char),
        ("lstele",  _ct.POINTER(_ct.c_int)),
        ("dlstele", _ct.POINTER(_ct.c_int)),
        ("tblval",  _ct.POINTER(_ct.c_int)),
        ("rval",  _ct.POINTER(_ct.c_float)),
        ("drval",  _ct.POINTER(_ct.c_double)),
        ("charval",  _ct.c_char_p),
        ("max_nval", _ct.c_int),
        ("max_nele", _ct.c_int),
        ("max_nt", _ct.c_int),
        ("max_len", _ct.c_int),
        ]
    
    ## def __str__(self):
    ##    return self.__class__.__name__ + str([x[0] + '=' + str(self.__getattribute__(x[0])) for x in self._fields_])
    ##    ## s = self.__class__.__name__ + '('
    ##    ## l = [y[0] for y in self._fields_]
    ##    ## l.sort()
    ##    ## for x in l:
    ##    ##     s += x + '=' + str(self.__getattribute__(x)) + ', '
    ##    ## s += ')'
    ##    ## return s

    def __repr__(self):
       ## return self.__class__.__name__ + repr([x[0] + '=' + repr(self.__getattribute__(x[0])) for x in self._fields_])
       return self.__class__.__name__ + '(' + \
           repr(dict([(x[0], self.__getattribute__(x[0])) for x in self._fields_])) + ')'


## /*
##  * Macros for getting values of a Report
##  * acces to field in the BURP_RPT structure should be accessed
##  * through these Macros Only
##  * access without these macros would be at your own risk
##  * current definition do not cover all available field
##  * since they are not used by anyone yet.
##  */
RPT_HANDLE = lambda rpt: rpt[0].handle
RPT_NSIZE  = lambda rpt: rpt[0].nsize
RPT_TEMPS  = lambda rpt: rpt[0].temps
RPT_FLGS   = lambda rpt: rpt[0].flgs
RPT_STNID  = lambda rpt: rpt[0].stnid
RPT_IDTYP  = lambda rpt: rpt[0].idtype
RPT_LATI   = lambda rpt: rpt[0].lati
RPT_LONG   = lambda rpt: rpt[0].longi
RPT_DX     = lambda rpt: rpt[0].dx
RPT_DY     = lambda rpt: rpt[0].dy
RPT_ELEV   = lambda rpt: rpt[0].elev
RPT_DRND   = lambda rpt: rpt[0].drnd
RPT_DATE   = lambda rpt: rpt[0].date
RPT_OARS   = lambda rpt: rpt[0].oars
RPT_RUNN   = lambda rpt: rpt[0].runn
RPT_NBLK   = lambda rpt: rpt[0].nblk
RPT_LNGR   = lambda rpt: rpt[0].lngr


## /*
##  * Macros for setting values of a Report
##  * acces to field in the BURP_RPT structure should be accessed
##  * through these Macros Only
##  * access without these macros would be at your own risk
##  * current definition do not cover all available field
##  * since they are not used by anyone yet.
##  */
## /* for internal use only */
## extern  void       brp_setstnid( BURP_RPT *rpt, const char *stnid );
libburpc.brp_setstnid.argtypes = (_ct.POINTER(BURP_RPT), _ct.c_char_p)
libburpc.brp_setstnid.restype = None
c_brp_setstnid = libburpc.brp_setstnid

def RPT_SetHANDLE(rpt, val): rpt[0].handle = val
def RPT_SetTEMPS (rpt, val): rpt[0].temps = val
def RPT_SetFLGS  (rpt, val): rpt[0].flgs
def RPT_SetSTNID (rpt, val): c_brp_setstnid(rpt, val)
def RPT_SetIDTYP (rpt, val): rpt[0].idtype = val
def RPT_SetLATI  (rpt, val): rpt[0].lati = val
def RPT_SetLONG  (rpt, val): rpt[0].longi = val
def RPT_SetDX    (rpt, val): rpt[0].dx = val
def RPT_SetDY    (rpt, val): rpt[0].dy = val
def RPT_SetELEV  (rpt, val): rpt[0].elev = val
def RPT_SetDRND  (rpt, val): rpt[0].drnd = val
def RPT_SetDATE  (rpt, val): rpt[0].date = val
def RPT_SetOARS  (rpt, val): rpt[0].oars = val
def RPT_SetRUNN  (rpt, val): rpt[0].runn = val


## /*
##  * Macros for getting values of a Block
##  * acces to field in the BURP_BLK structure should be accessed
##  * through these Macros Only
##  * access without these macros would be at your own risk
##  */

BLK_BKNO  = lambda blk: blk[0].bkno
BLK_NELE  = lambda blk: blk[0].nele
BLK_NVAL  = lambda blk: blk[0].nval
BLK_NT    = lambda blk: blk[0].nt
BLK_BFAM  = lambda blk: blk[0].bfam
BLK_BDESC = lambda blk: blk[0].bdesc
BLK_BTYP  = lambda blk: blk[0].btyp
BLK_BKNAT = lambda blk: blk[0].bknat
BLK_BKTYP = lambda blk: blk[0].bktyp
BLK_BKSTP = lambda blk: blk[0].bkstp
BLK_NBIT  = lambda blk: blk[0].nbit
BLK_BIT0  = lambda blk: blk[0].bit0
BLK_DATYP = lambda blk: blk[0].datyp
BLK_Data  = lambda blk: blk[0].data
BLK_DLSTELE= lambda blk,e : blk[0].dlstele[e]
BLK_LSTELE = lambda blk,e : blk[0].lstele[e]
BLK_TBLVAL = lambda blk,e,v,t: blk[0].tblval[e + blk[0].nele*(v + (blk[0].nval)*t)]
BLK_RVAL   = lambda blk,e,v,t: blk[0].rval[e + blk[0].nele*(v + (blk[0].nval)*t)]
BLK_DVAL   = lambda blk,e,v,t: blk[0].drval[e + blk[0].nele*(v + (blk[0].nval)*t)]
BLK_CHARVAL= lambda blk,l,c: blk[0].charval[l * blk[0].nt + c]
BLK_STORE_TYPE = lambda blk: blk[0].store_type

## /*
##  * Macros for setting values of a Block
##  * acces to field in the BURP_BLK structure should be accessed
##  * through these Macros Only
##  * access without these macros would be at your own risk
##  */
def BLK_SetNELE (blk, val): blk[0].nele = val
def BLK_SetNVAL (blk, val): blk[0].nval = val
def BLK_SetNT   (blk, val): blk[0].nt = val
def BLK_SetBKNO (blk, val): blk[0].bkno = val
def BLK_SetBFAM (blk, val): blk[0].bfam = val
def BLK_SetBDESC(blk, val): blk[0].bdesc = val
def BLK_SetBTYP (blk, val): blk[0].btyp = val
def BLK_SetBKNAT(blk, val): blk[0].bknat = val
def BLK_SetBKTYP(blk, val): blk[0].bktyp = val
def BLK_SetBKSTP(blk, val): blk[0].bkstp = val
def BLK_SetNBIT (blk, val): blk[0].nbit = val
def BLK_SetDATYP(blk, val): blk[0].datyp = val
def BLK_SetDVAL(blk,e,v,t,val):
    blk[0].drval [e + blk[0].nele * (v + blk[0].nval * t)] = val
def BLK_SetTBLVAL(blk,e,v,t,val):
    blk[0].tblval[e + blk[0].nele * (v + blk[0].nval * t)] = val
def BLK_SetRVAL(blk,e,v,t,val):
    blk[0].rval[e + blk[0].nele * (v + blk[0].nval * t)] = val
def BLK_SetCVAL(blk,l,c,val):
    blk[0].charval[l * blk[0].nt + c] = val;
def BLK_SetLSTELE(blk,i,val):
    blk[0].lstele[i] = val
def BLK_SetDLSTELE(blk,i,val):
    blk[0].dlstele[i] = val
def BLK_SetSTORE_TYPE(blk,val):
    blk[0].store_type = val

## /*
##  * allocators and constructors
##  */
    
## extern  BURP_BLK  *brp_newblk( void );
libburpc.brp_newblk.argtypes = None
libburpc.brp_newblk.restype = _ct.POINTER(BURP_BLK)
c_brp_newblk = libburpc.brp_newblk

## extern  BURP_RPT  *brp_newrpt( void );
libburpc.brp_newrpt.argtypes = None
libburpc.brp_newrpt.restype = _ct.POINTER(BURP_RPT)
c_brp_newrpt = libburpc.brp_newrpt

## extern  void       brp_allocrpt( BURP_RPT *rpt, int  nsize );
libburpc.brp_allocrpt.argtypes = (_ct.POINTER(BURP_RPT), _ct.c_int)
libburpc.brp_allocrpt.restype = None
c_brp_allocrpt = libburpc.brp_allocrpt

## extern  void       brp_allocblk( BURP_BLK *blk, int  nele, int nval, int nt );
libburpc.brp_allocblk.argtypes = (_ct.POINTER(BURP_BLK),
                                  _ct.c_int, _ct.c_int, _ct.c_int)
libburpc.brp_allocblk.restype = None
c_brp_allocblk = libburpc.brp_allocblk

## /*
##  *  find elements
##  */

## extern  int        brp_searchdlste( int  code, BURP_BLK *blk );

## /*
##  * destructors and deallocators
##  */

## extern  void       brp_freeblk( BURP_BLK *blk );
libburpc.brp_freeblk.argtypes = (_ct.POINTER(BURP_BLK), )
libburpc.brp_freeblk.restype = None
c_brp_freeblk = libburpc.brp_freeblk

## extern  void       brp_freerpt( BURP_RPT *rpt );
libburpc.brp_freerpt.argtypes = (_ct.POINTER(BURP_RPT), )
libburpc.brp_freerpt.restype = None
c_brp_freerpt = libburpc.brp_freerpt

## /* for internal use only */
## extern  void       brp_freebuf(BURP_RPT *rpt);
## extern  void       brp_freedata( BURP_BLK *blk );

## /*
##  * reinitializers
##  */
## extern  void       brp_clrblk( BURP_BLK  *blk );
libburpc.brp_clrblk.argtypes = (_ct.POINTER(BURP_BLK), )
libburpc.brp_clrblk.restype = None
c_brp_clrblk = libburpc.brp_clrblk

## extern  void       brp_clrblkv(BURP_BLK  *bblk, float val);
libburpc.brp_clrblkv.argtypes = (_ct.POINTER(BURP_BLK), _ct.c_int)
libburpc.brp_clrblkv.restype = None
c_brp_clrblkv = libburpc.brp_clrblkv

## extern  void       brp_clrrpt( BURP_RPT *rpt );
libburpc.brp_clrrpt.argtypes = (_ct.POINTER(BURP_RPT), )
libburpc.brp_clrrpt.restype = None
c_brp_clrrpt = libburpc.brp_clrrpt


## /* reset blk and rpt headers to default as initialised
##  * in brp_newblk and brp_newblk
##  */

## extern  void       brp_resetrpthdr( BURP_RPT *rpt );
libburpc.brp_resetrpthdr.argtypes = (_ct.POINTER(BURP_RPT), )
libburpc.brp_resetrpthdr.restype = None
c_brp_resetrpthdr = libburpc.brp_resetrpthdr

## extern  void       brp_resetblkhdr( BURP_BLK *blk );
libburpc.brp_resetblkhdr.argtypes = (_ct.POINTER(BURP_BLK), )
libburpc.brp_resetblkhdr.restype = None
c_brp_resetblkhdr = libburpc.brp_resetblkhdr

## /*
##  * converters
##  */

## extern  int        brp_encodeblk( BURP_BLK  *blk );
libburpc.brp_encodeblk.argtypes = (_ct.POINTER(BURP_BLK), )
libburpc.brp_encodeblk.restype = _ct.c_int
c_brp_encodeblk = libburpc.brp_encodeblk

## extern  int        brp_safe_convertblk( BURP_BLK  *blk, int mode );
libburpc.brp_safe_convertblk.argtypes = (_ct.POINTER(BURP_BLK), _ct.c_int)
libburpc.brp_safe_convertblk.restype = _ct.c_int
c_brp_safe_convertblk = libburpc.brp_safe_convertblk

## extern  int        brp_convertblk( BURP_BLK  *blk, int mode );
libburpc.brp_convertblk.argtypes = (_ct.POINTER(BURP_BLK), _ct.c_int)
libburpc.brp_convertblk.restype = _ct.c_int
c_brp_convertblk = libburpc.brp_convertblk

## /*
##  * find report and block before reading them
##  */

## extern  int        brp_findblk( BURP_BLK  *blk, BURP_RPT  *rpt );
libburpc.brp_findblk.argtypes = (_ct.POINTER(BURP_BLK), _ct.POINTER(BURP_RPT))
libburpc.brp_findblk.restype = _ct.c_int
c_brp_findblk = libburpc.brp_findblk

## extern  int        brp_findrpt( int iun, BURP_RPT *rpt );
libburpc.brp_findrpt.argtypes = (_ct.c_int, _ct.POINTER(BURP_RPT))
libburpc.brp_findrpt.restype = _ct.c_int
c_brp_findrpt = libburpc.brp_findrpt

## /*
##  * read in data
##  */

## extern  int        brp_getrpt( int iun, int handle, BURP_RPT  *rpt );
libburpc.brp_getrpt.argtypes = (_ct.c_int, _ct.c_int, _ct.POINTER(BURP_RPT))
libburpc.brp_getrpt.restype = _ct.c_int
c_brp_getrpt = libburpc.brp_getrpt

## extern  int        brp_safe_getblk(int bkno, BURP_BLK  *blk, BURP_RPT  *rpt);
libburpc.brp_safe_getblk.argtypes = (_ct.c_int, _ct.POINTER(BURP_BLK), _ct.POINTER(BURP_RPT))
libburpc.brp_safe_getblk.restype = _ct.c_int
c_brp_safe_getblk = libburpc.brp_safe_getblk

## extern  int        brp_getblk(int bkno, BURP_BLK  *blk, BURP_RPT  *rpt);
libburpc.brp_getblk.argtypes = (_ct.c_int, _ct.POINTER(BURP_BLK), _ct.POINTER(BURP_RPT))
libburpc.brp_getblk.restype = _ct.c_int
c_brp_getblk = libburpc.brp_getblk

## /* brp_readblk same as brp_getblk() but the BLK_RVAL(blk,e,v,t) values
##    are not available as conversion are not done. function to use when readig burp and
##    there is no need to work with real values
## */

## extern  int        brp_readblk(int bkno, BURP_BLK  *blk, BURP_RPT  *rpt, int);
libburpc.brp_readblk.argtypes = (_ct.c_int, _ct.POINTER(BURP_BLK), _ct.POINTER(BURP_RPT), _ct.c_int)
libburpc.brp_readblk.restype = _ct.c_int
c_brp_readblk = libburpc.brp_readblk


## /*
##  * read only header
##  */

## extern  int        brp_rdrpthdr(int handle, BURP_RPT *rpt);
libburpc.brp_rdrpthdr.argtypes = (_ct.c_int, _ct.POINTER(BURP_RPT))
libburpc.brp_rdrpthdr.restype = _ct.c_int
c_brp_rdrpthdr = libburpc.brp_rdrpthdr

## extern  int        brp_rdblkhdr(int bkno, BURP_BLK  *blk, BURP_RPT  *rpt);
libburpc.brp_rdblkhdr.argtypes = (_ct.c_int, _ct.POINTER(BURP_BLK), _ct.POINTER(BURP_RPT))
libburpc.brp_rdblkhdr.restype = _ct.c_int
c_brp_rdblkhdr = libburpc.brp_rdblkhdr

## /* prepare a report for writing */
## extern  int        brp_initrpthdr( int iun, BURP_RPT *rpt );
libburpc.brp_initrpthdr.argtypes = (_ct.c_int, _ct.POINTER(BURP_RPT))
libburpc.brp_initrpthdr.restype = _ct.c_int
c_brp_initrpthdr = libburpc.brp_initrpthdr

## /* prepare a report for writing alias of brp_initrpthdr */
## extern  int        brp_putrpthdr( int iun, BURP_RPT *rpt );
libburpc.brp_putrpthdr.argtypes = (_ct.c_int, _ct.POINTER(BURP_RPT))
libburpc.brp_putrpthdr.restype = _ct.c_int
c_brp_putrpthdr = libburpc.brp_putrpthdr

## /* add new blocks into a report */
## extern  int        brp_putblk( BURP_RPT *rpt, BURP_BLK *blk );
libburpc.brp_putblk.argtypes = (_ct.POINTER(BURP_RPT), _ct.POINTER(BURP_BLK))
libburpc.brp_putblk.restype = _ct.c_int
c_brp_putblk = libburpc.brp_putblk

## /* write out to a file */
## extern  int        brp_writerpt( int iun, BURP_RPT *rpt, int where );
libburpc.brp_writerpt.argtypes = (_ct.c_int, _ct.POINTER(BURP_RPT), _ct.c_int)
libburpc.brp_writerpt.restype = _ct.c_int
c_brp_writerpt = libburpc.brp_writerpt

## /* modify only the header of a report */
## extern  int        brp_updrpthdr( int iun, BURP_RPT *rpt );
libburpc.brp_updrpthdr.argtypes = (_ct.c_int, _ct.POINTER(BURP_RPT))
libburpc.brp_updrpthdr.restype = _ct.c_int
c_brp_updrpthdr = libburpc.brp_updrpthdr

## /*
##  * return the floating point constant used for missing values
##  */
## extern  float      brp_msngval(void);
## libburpc.brp_msngval.argtypes = None
libburpc.brp_msngval.restype = _ct.c_float
c_brp_msngval = libburpc.brp_msngval

## /*
##  * utilities
##  */

## /*  copy rpt header */
## extern void        brp_copyrpthdr( BURP_RPT * dest, const BURP_RPT *source);
libburpc.brp_copyrpthdr.argtypes = (_ct.POINTER(BURP_RPT), _ct.POINTER(BURP_RPT))
c_brp_copyrpthdr = libburpc.brp_copyrpthdr

## /*  copy the whole rpt  */
## extern void        brp_copyrpt( BURP_RPT * dest, const BURP_RPT *source);
libburpc.brp_copyrpt.argtypes = (_ct.POINTER(BURP_RPT), _ct.POINTER(BURP_RPT))
c_brp_copyrpt = libburpc.brp_copyrpt

## /*  resize the  rpt with newsize to add blocks  */
## extern void        brp_resizerpt( BURP_RPT * dest, int NewSize);
libburpc.brp_resizerpt.argtypes = (_ct.POINTER(BURP_RPT), _ct.c_int)
c_brp_resizerpt = libburpc.brp_resizerpt

## /* duplicate block */
## extern void        brp_copyblk( BURP_BLK *dest, const BURP_BLK *source);
libburpc.brp_copyblk.argtypes = (_ct.POINTER(BURP_BLK), _ct.POINTER(BURP_BLK))
c_brp_copyblk = libburpc.brp_copyblk

## /* resize  block */
## extern void        brp_resizeblk( BURP_BLK *source,int NEW_ele, int NEW_nval, int NEW_nt);
libburpc.brp_resizeblk.argtypes = (_ct.POINTER(BURP_BLK),
                                   _ct.c_int, _ct.c_int, _ct.c_int)
c_brp_resizeblk = libburpc.brp_resizeblk

## extern void        brp_resizeblk_v2( BURP_BLK **source ,int nele, int nval, int nt);
#TODO: brp_resizeblk_v2
## libburpc.brp_resizeblk_v2.argtypes = (_ct.POINTER(_ct.POINTER(BURP_BLK)),
##                                       _ct.c_int, _ct.c_int, _ct.c_int)
## c_brp_resizeblk_v2 = libburpc.brp_resizeblk_v2

## /*
##  * Opening files
##  */

## extern  int        brp_open(int  iun, const char *filename, char *op);
libburpc.brp_open.argtypes = (_ct.c_int, _ct.c_char_p, _ct.c_char_p)
libburpc.brp_open.restype = _ct.c_int
c_brp_open = libburpc.brp_open

## extern  int        brp_close(int iun);
libburpc.brp_close.argtypes = (_ct.c_int, )
libburpc.brp_close.restype = _ct.c_int
c_brp_close = libburpc.brp_close

## /*
##  * deleting reports and blocks
##  */

## extern  int        brp_delblk(BURP_RPT *rpt, const BURP_BLK * blk);
libburpc.brp_delblk.argtypes = (_ct.POINTER(BURP_RPT), _ct.POINTER(BURP_BLK))
libburpc.brp_delblk.restype = _ct.c_int
c_brp_delblk = libburpc.brp_delblk

## extern  int        brp_delrpt(BURP_RPT *rpt);
libburpc.brp_delrpt.argtypes = (_ct.POINTER(BURP_RPT), )
libburpc.brp_delrpt.restype = _ct.c_int
c_brp_delrpt = libburpc.brp_delrpt

## /*
##  * burp rpn option functions
##  */

## extern  int        brp_SetOptFloat(char* opt, float val);
libburpc.brp_SetOptFloat.argtypes = (_ct.c_char_p, _ct.c_float)
libburpc.brp_SetOptFloat.restype = _ct.c_int
c_brp_SetOptFloat = libburpc.brp_SetOptFloat

## extern  int        brp_SetOptChar (char* opt, char * val);
libburpc.brp_SetOptChar.argtypes = (_ct.c_char_p, _ct.c_char_p)
libburpc.brp_SetOptChar.restype = _ct.c_int
c_brp_SetOptChar = libburpc.brp_SetOptChar

## extern  float      brp_msngval (void);
libburpc.brp_msngval.argtypes = None
libburpc.brp_msngval.restype = _ct.c_float
c_brp_msngval = libburpc.brp_msngval

## /*
##  * burp rpn functions
##  */
#Note: these are avail in librmn... should we add them here too? Will there be an SQL version for these too?
## extern  int        c_mrfmxl ( int iun );
## extern  int        c_mrfnbr ( int iun );
## extern  int        c_mrbdel ( int *buf, int bkno);


if __name__ == "__main__":
    pass #print burpc version 
    
# -*- Mode: C; tab-width: 4; indent-tabs-mode: nil -*-
# vim: set expandtab ts=4 sw=4:
# kate: space-indent on; indent-mode cstyle; indent-width 4; mixedindent off;
