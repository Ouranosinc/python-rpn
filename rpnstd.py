## Automatically adapted for numpy.oldnumeric Jan 10, 2008 by 

""" module Fstd contains the classes used to access RPN Standard Files (rev 2000)
    class FstKeys   : search tags (nom, type, etiket, date, ip1, ip2, ip3)
    class FstDesc   : auxiliary tags (grtyp, ig1, ig2, ig3, ig4,  dateo, deet, npas, datyp, nbits)
    class FstParms  : combined set of tags (search and auxiliary)
    class FstFile   : a standard file
    clsss FstHandle : pointer to a standard file record
"""
import types
## import numpy.oldnumeric as Numeric
## import numpy.oldnumeric.user_array as UserArray
import numpy
import Fstdc

# primary set of descriptors has two extra items, used to read/scan file
# handle carries the last handle associated with the keys ,
# or -1 if next match, or -2 if match is to start at beginning of file
X__PrimaryDesc={'nom':'    ','type':'  ','etiket':'            ',
                'date':-1,'ip1':-1,'ip2':-1,'ip3':-1,'handle':-2,'nxt':0,'fileref':None}

# descriptive part of the keys, returned by read/scan, needed for write
X__AuxiliaryDesc={'grtyp':'X','dateo':0,'deet':0,'npas':0,
               'ig1':0,'ig2':0,'ig3':0,'ig4':0,'datyp':0,'nbits':0,
               'xaxis':None,'yaxis':None,'xyref':(None,None,None,None,None),'griddim':(None,None)}

# wild carded descriptive part of the keys (non initialized)
W__AuxiliaryDesc={'grtyp':' ','dateo':-1,'deet':-1,'npas':-1,
               'ig1':-1,'ig2':-1,'ig3':-1,'ig4':-1,'datyp':-1,'nbits':-1}

X__Criteres={'nom':['    '],'type':['  '],'etiket':['            '],
        'date':[-1],'ip1':[-1],'ip2':[-1],'ip3':[-1],
        'grtyp':[' '],'dateo':[-1],'deet':[-1],'npas':[-1],
        'ig1':[-1],'ig2':[-1],'ig3':[-1],'ig4':[-1],
        'ni':[-1],'nj':[-1],'nk':[-1],'datyp':[-1],'nbits':[-1]}

Sgrid__Desc={'nom':'    ','type':'  ','etiket':'            ','date':-1,'ip1':-1,'ip2':-1,'ip3':-1,
             'deet':0,'npas':0,'datyp':0,'nbits':0,'dateo':-1}
             
Tgrid__Desc={'grtyp':'X','ig1':-1,'ig2':-1,'ig3':-1,'ig4':-1,'xyref':(None,None,None,None,None),'griddim':(None,None),
             'xaxis':None,'yaxis':None}


X__FullDesc={}
X__FullDesc.update(X__PrimaryDesc)
X__FullDesc.update(X__AuxiliaryDesc)

W__FullDesc={}
W__FullDesc.update(X__PrimaryDesc)
W__FullDesc.update(W__AuxiliaryDesc)

X__DateDebut=-1
X__DateFin=-1
X__Delta=0.0

def Predef_Grids():
#
# Predefined Grid configurations
#
  global Grille_Amer_Nord, Grille_Europe, Grille_Inde, Grille_Hem_Sud, Grille_Canada, Grille_Maritimes
  global Grille_Quebec, Grille_Prairies, Grille_Colombie, Grille_USA, Grille_Global, Grille_GemLam10
  Grille_Amer_Nord=Grid(grtyp='N',ninj=(401,401),ig14=cxgaig('N',200.5,200.5,40000.0,21.0))  # PS 40km
  Grille_Europe=Grid(grtyp='N',ninj=(401,401),ig14=cxgaig('N',200.5,220.5,40000.0,-100.0))   # PS 40km
  Grille_Inde=Grid(grtyp='N',ninj=(401,401),ig14=cxgaig('N',200.5,300.5,40000.0,-170.0))     # PS 40km
  Grille_Hem_Sud=Grid(grtyp='S',ninj=(401,401),ig14=cxgaig('S',200.5,200.5,40000.0,21.0))    # PS 40km
  Grille_Canada=Grid(grtyp='N',ninj=(351,261),ig14=cxgaig('N',121.5,281.5,20000.0,21.0))     # PS 20km
  Grille_Maritimes=Grid(grtyp='N',ninj=(175,121),ig14=cxgaig('N',51.5,296.5,20000.0,-20.0))  # PS 20km
  Grille_Quebec=Grid(grtyp='N',ninj=(199,155),ig14=cxgaig('N',51.5,279.5,20000.0,0.0))       # PS 20km
  Grille_Prairies=Grid(grtyp='N',ninj=(175,121),ig14=cxgaig('N',86.5,245.5,20000.0,20.0))    # PS 20km
  Grille_Colombie=Grid(grtyp='N',ninj=(175,121),ig14=cxgaig('N',103.5,245.5,20000.0,30.0))   # PS 20km
  Grille_USA=Grid(grtyp='N',ninj=(351,261),ig14=cxgaig('N',121.0,387.5,20000.0,21.0))        # PS 20km
  Grille_Global=Grid(grtyp='L',ninj=(721,359),ig14=cxgaig('L',-89.5,180.0,0.5,0.5))          # LatLon 0.5 Deg
  Grille_GemLam10=Grid(grtyp='N',ninj=(1201,776),ig14=cxgaig('N',536.0,746.0,10000.0,21.0))  # PS 10km


def printdaterange():
    global X__DateDebut,X__DateFin,X__Delta
    print 'Debug printdaterange debut fin delta=',X__DateDebut,X__DateFin,X__Delta

def resetdaterange():
    global X__DateDebut,X__DateFin,X__Delta
    X__DateDebut=-1
    X__DateFin=-1
    X__Delta=0.0

def dump_keys_and_values(self):
    result=''
    keynames = self.__dict__.keys()
    keynames.sort()
    for name in keynames:
        result=result+name+'='+repr(self.__dict__[name])+' , '
    return result[:-3]  # eliminate last blank comma blank sequence

def levels_to_ip1(levels,kind):
    return(Fstdc.level_to_ip1(levels,kind))

def cxgaig(grtyp,xg1,xg2,xg3,xg4):
    if (grtyp == None or xg1 == None or xg2 == None or xg3 == None or xg4 == None):
      print 'cxgaig error: missing argument, calling is cxgaig(grtyp,xg1,xg2,xg3,xg4)'
    return(Fstdc.cxgaig(grtyp,xg1,xg2,xg3,xg4))
    
class FstFile:
    """Python Class implementation of the RPN standard file interface
       newfile=FstFile(name='...',mode='...')  open file (fstouv)
           name is a character string containing the file name
           mode is a string containing RND SEQ R/O
       ex: newfile=FstFile('myfile','RND+R/O')
           FstHandle=FstFile[FstParm]       get matching record
           FstHandle=FstFile[0]             get next matching record (fstsui)
           FstRecord=FstFile[FstHandle]     get data associated with handle
           FstFile[FstParm]=array           append/rewrite data and tags to file
           del newfile                      close the file
    """
    def __init__(self,name='total_nonsense',mode='RND+STD') :
        self.filename=name
        self.lastread=None
        self.lastwrite=None
        self.options=mode
        self.iun = Fstdc.fstouv(0,self.filename,self.options)
        if (self.iun == None):
          raise IOError,(-1,'failed to open standard file',self.filename)
        else:
          print 'R.P.N. Standard File (2000) ',name,' is open with options:',mode,' UNIT=',self.iun

    def voir(self,options='NEWSTYLE'):
        Fstdc.fstvoi(self.iun,options)

    def __del__(self):
        if (self.iun != None):
          Fstdc.fstfrm(self.iun)
          print 'file ',self.iun,' is closed, filename=',self.filename
        del self.filename
        del self.lastread
        del self.lastwrite
        del self.options
        del self.iun

    def __getitem__(self,key):              # get record from file
        params = self.info(key)         # 1 - get handle
        if params == None:              # oops !! not found
            return (None,None)
        target = params.handle
        array=Fstdc.fstluk(target)   # 2 - get data
        return (params,array)               # return keys and data arrray

    def edit_dir_entry(self,key):       # edit (zap) directory entry referenced by handle
      return(Fstdc.fst_edit_dir(key.handle,key.date,key.deet,key.npas,-1,-1,-1,key.ip1,key.ip2,key.ip3,
                                key.type,key.nom,key.etiket,key.grtyp,key.ig1,key.ig2,key.ig3,key.ig4,key.datyp))
      
    def info(self,key):                     # get handle associated with key
        if isinstance(key,FstParm):         # fstinf, return FstHandle instance
            if key.nxt == 1:               # get NEXT one thatmatches
                self.lastread=Fstdc.fstinf(self.iun,key.nom,key.type,
                              key.etiket,key.ip1,key.ip2,key.ip3,key.date,key.handle)
            else:                           # get FIRST one that matches
                if key.handle >= 0 :       # handle exists, return it
                    return key
                self.lastread=Fstdc.fstinf(self.iun,key.nom,key.type,
                              key.etiket,key.ip1,key.ip2,key.ip3,key.date,-2)
        elif key==NextMatch:                # fstsui, return FstHandle instance
            self.lastread=Fstdc.fstinf(self.iun,' ',' ',' ',0,0,0,0,-1)
        else:
            raise TypeError   # invalid "index"
        result=FstParms()
        if self.lastread != None:
#            self.lastread.__dict__['fileref']=self
            result.update_by_dict(self.lastread)
            result.fileref=self
#            print 'DEBUG result=',result
        else:
            return None
        return result # return handle

    def __setitem__(self,index,value):      # [re]write data and tags
        if (value == None):
            if (isinstance(index,FstParm)): # set of keys
                target = index.handle
            elif type(index) == type(0):  # handle
                target = index
            else:
                print 'FstFile: index must provide a valid handle to erase a record'
                raise TypeError
            print 'erasing record with handle=',target,' from file'
            self.lastwrite=Fstdc.fsteff(target)
            # call to fsteff goes here
        elif (isinstance(index,FstParms)) and (type(value) == type(numpy.array([]))):
            # call to fstecr goes here with rewrite flag (index=true/false)
            self.lastwrite=0
#            print 'writing data',value.shape,' to file, keys=',index
#            print 'dict = ',index.__dict__
            if (value.flags.farray):
              print 'fstecr Fortran style array'
              Fstdc.fstecr(value,
                         self.iun,index.nom,index.type,index.etiket,index.ip1,index.ip2,
                         index.ip3,index.dateo,index.grtyp,index.ig1,index.ig2,index.ig3,
                         index.ig4,index.deet,index.npas,index.nbits)
            else:
              print 'fstecr C style array'
              Fstdc.fstecr(numpy.reshape(numpy.transpose(value),value.shape),
                         self.iun,index.nom,index.type,index.etiket,index.ip1,index.ip2,
                         index.ip3,index.dateo,index.grtyp,index.ig1,index.ig2,index.ig3,
                         index.ig4,index.deet,index.npas,index.nbits)
        else:
           print 'FstFile write: value must be an array and index must be FstParms'
           raise TypeError

class Grid:
    "Base method to attach a grid description to a fstd field"
    def __init__(self,keysndata=(None,None),(xkeys,xaxis)=(None,None),(ykeys,yaxis)=(None,None),ninj=(None,None),grtyp=None,ig14=(None,None,None,None),vector=None):
      if grtyp != None:           # grid is defined by grtyp,ig1,ig2,ig3,ig4
        ig1,ig2,ig3,ig4 = ig14
        if (ig1==None or ig2==None or ig3==None or ig4==None):
           raise TypeError,'Grid: ig14 tuple (ig1,ig2,ig3,ig4) must be specified'
        lescles=FstParms()
        lescles.xyref=(grtyp,ig1,ig2,ig3,ig4)
        lescles.grtyp=grtyp
        lescles.ig1=ig1
        lescles.ig2=ig2
        lescles.ig3=ig3
        lescles.ig4=ig4
        lescles.griddim=ninj
        ledata=None
      else:
        if keysndata != (None,None) and isinstance(keysndata,tuple):
          (lescles,ledata)=keysndata
          if ((not isinstance(lescles,FstParms)) or (not isinstance(ledata,numpy.ndarray))):
            raise TypeError,'Grid: argument keysndata is not a tuple of type (Fstkeys,data)'
        else:
          raise TypeError,'Grid: argument keysndata is not a tuple of type (Fstkeys,data)'
        if ( (xkeys,xaxis)!=(None,None) and (ykeys,yaxis)!=(None,None) ):       # xaxis any yaxis provided
          lescles.xyref=(xkeys.grtyp,xkeys.ig1,xkeys.ig2,xkeys.ig3,xkeys.ig4)
          lescles.xaxis=xaxis
          lescles.yaxis=yaxis.ravel()
          lescles.griddim=(xaxis.shape[0],yaxis.shape[1])
        else:
          if lescles.grtyp == 'Z' or lescles.grtyp == 'Y':       # get xaxis and yaxis
            (xcles,xdata) = lescles.getaxis('X')
            (ycles,ydata) = lescles.getaxis('X')
          else:                                    # only keysndata, grid defined by grtyp,ig1,ig2,ig3,ig4 from keys
            lescles.xyref=(lescles.grtyp,lescles.ig1,lescles.ig2,lescles.ig3,lescles.ig4)
            if ninj != (None,None):
              lescles.griddim=ninj
            else:
              if ledata == None:
                raise TypeError,'Grid: argument ninj must be specified when data field is missing'
              else:
                lescles.griddim=(ledata.shape[0],ledata.shape[1])
        if vector != None:
          if (lescles.nom=='UU  '):
            (clesvv,champvv) = lescles.fileref[FstKeys(nom='VV',type=lescles.type,date=lescles.date,etiket=lescles.etiket,ip1=lescles.ip1,ip2=lescles.ip2,ip3=lescles.ip3)]
            if clesvv == None:
              print 'Grid error: VV record not found'
              return
            self.keys2 = clesvv
            self.field2 = champvv
        else:
          self.keys2= None
          self.field2=None
#      print 'Grid DEBUG lescles.nom date dateo=',lescles.nom,lescles.date,lescles.dateo
#      print 'Grid DEBUG lescles.xyref=',lescles.xyref
#      print 'Grid DEBUG lescles.griddim=',lescles.griddim
      self.keys = lescles
      self.field = ledata
#      print 'Grid termine'
#      print ' '
    
    def __getitem__(self,tgrid):              # interpolate to target grid
      if isinstance(tgrid,Grid):
        tgrtyp=tgrid.keys.grtyp
        txyref=tgrid.keys.xyref
        tgriddim=tgrid.keys.griddim
        txaxis=tgrid.keys.xaxis
        tyaxis=tgrid.keys.yaxis
      else:
        raise TypeError,'Grid: argument is not a Grid instance'
      xyref=self.keys.xyref
      ks=self.keys
      print 'Debug Grid interpolation for ',self.keys.nom,' from grid',xyref,' griddim=',ks.griddim,' to grid',txyref,' griddim=',tgriddim
      srcflag=ks.xaxis != None
      dstflag=txaxis != None
      vecteur=self.keys2 != None
#      print 'Degug Grid __getitem__ srcflag=',srcflag,' dstflag=',dstflag
      newkeys=FstParms()
      newkeys.update_by_dict_from(self.keys,Sgrid__Desc)
      newkeys.update_by_dict_from(tgrid.keys,Tgrid__Desc)
#      print 'Debug Grid __getitem__ newkeys=',newkeys.nom,newkeys.xyref
      if (tgrid.field == None):
#        print 'Debug Grid __getitem__ creating dummy array'
        dummyarray=numpy.zeros( (2,2) )
        newgrid=Grid((newkeys,dummyarray))
      else:
        newgrid=Grid((newkeys,tgrid.field))
      if vecteur:
        print 'Degug Grid __getitem__ interpolation vectorielle'
        (newarray,newarray2)=Fstdc.ezinterp(self.field,self.field2,ks.griddim,ks.grtyp,xyref,ks.xaxis,ks.yaxis,srcflag,tgriddim,tgrtyp,txyref,txaxis,tyaxis,dstflag,vecteur)
        newgrid.field=newarray
        newgrid.field2=newarray2
        newgrid.keys2=self.keys2
        newgrid.keys2.update_by_dict_from(tgrid.keys,Tgrid__Desc)
      else:
        newarray=Fstdc.ezinterp(self.field,None,ks.griddim,ks.grtyp,xyref,ks.xaxis,ks.yaxis,srcflag,tgriddim,tgrtyp,txyref,txaxis,tyaxis,dstflag,vecteur)
        newgrid.field=newarray
#      print 'newarray info=',newarray.shape,newarray.flags
#      print 'Debug newgrid.keys=',newgrid.keys.nom,newgrid.keys.xyref
#      if newgrid.keys2 != None:
#        print 'Debug newgrid.keys2',newgrid.keys2.nom,newgrid.keys.xyref
      return(newgrid)
      
class FstParm:
    "Base methods for all RPN standard file descriptor classes"
    def __init__(self,model,reference,extra):
        for name in reference.keys():            # copy initial values from reference
            self.__dict__[name]=reference[name]  # bypass setatttr method for new attributes
        if model != None:
            if isinstance(model,FstParm):        # update with model attributes
               self.update(model)
            else:
                print 'FstParm.__init__: model must be an FstParm class instances'
                raise TypeError
        for name in extra.keys():                # add extras using own setattr method
            setattr(self,name,extra[name])

    def update(self,with):
        "Replace Fst attributes of an instance with Fst attributes from another"
        if isinstance(with,FstParm) and isinstance(self,FstParm):  # check if class=FstParm
            for name in with.__dict__.keys():
                if (name in self.__dict__.keys()) and (name in X__FullDesc.keys()):
                    self.__dict__[name]=with.__dict__[name]
        else:
            print 'FstParm.update: can only operate on FstParm class instances'
            raise TypeError

    def update_cond(self,with):
        "Conditional Replace Fst attributes if not wildcard values"
        if isinstance(with,FstParm) and isinstance(self,FstParm):  # check if class=FstParm
            for name in with.__dict__.keys():
                if (name in self.__dict__.keys()) and (name in X__FullDesc.keys()):
                    if (with.__dict__[name] != W__FullDesc[name]):
                        self.__dict__[name]=with.__dict__[name]
        else:
            print 'FstParm.update_cond: can only operate on FstParm class instances'
            raise TypeError

    def update_by_dict(self,with):
        for name in with.keys():
            if name in self.__dict__.keys():
                setattr(self,name,with[name])

    def update_by_dict_from(self,frm,with):
        for name in with.keys():
            if name in self.__dict__.keys():
                setattr(self,name,frm.__dict__[name])

    def __setattr__(self,name,value):   # this method cannot create new attributes
        if name in self.__dict__.keys():                   # is attribute name valid ?
            if type(value) == type(self.__dict__[name]):   # right type (string or int))
                if type(value) == type(''):
                    reflen=len(self.__dict__[name])        # string, remember length
                    self.__dict__[name]=(value+reflen*' ')[:reflen]
                else:
                    self.__dict__[name]=value              # integer
            else:
                if self.__dict__[name] == None:
#                   print 'Debug***** None name=',name
                   self.__dict__[name]=value
                else:
                    print value,'has the wrong type for attribute',name
        else:
            print 'attribute',name,'does not exist for class',self.__class__

    def findnext(self,flag=1):                  # set/reset next match flag
        self.nxt = flag
        return self

    def wildcard(self):                  # reset keys to undefined
        self.update_by_dict(W__FullDesc)

    def __str__(self):
        return dump_keys_and_values(self)

class FstKeys(FstParm):
    "Primary descriptors, used to search for a record"
    def __init__(self,model=None,**args):
        FstParm.__init__(self,model,X__PrimaryDesc,args)

class FstDesc(FstParm):
    "Auxiliary descriptors, used when writing a record or getting descriptors from a record"
    def __init__(self,model=None,**args):
        FstParm.__init__(self,model,X__AuxiliaryDesc,args)

class FstParms(FstKeys,FstDesc):
    "Full set of descriptors, Primary + Auxiliary, needed to write a record, can be used for search"
    def __init__(self,model=None,**args):
        FstKeys.__init__(self)   # initialize Key part
        FstDesc.__init__(self)   # initialize Auxiliary part
        if model != None:
            if isinstance(model,FstParm):
                self.update(model)
            else:
                print 'FstParms: cannot initialize from arg #1'
                raise TypeError
        for name in args.keys(): # and update with specified attributes
            setattr(self,name,args[name])
    
    def getaxis(self,axis):
       if (self.grtyp != 'Z' and self.grtyp != 'Y'):
         print 'getaxis error: can not get axis from grtyp=',self.grtyp
         return(None,None)
       if (self.xaxis == None and self.yaxis == None):
         (xaxiskeys,xaxisdata) = self.fileref[FstKeys(nom='>>',ip1=self.ig1,ip2=self.ig2,ip3=self.ig3)]
         (yaxiskeys,yaxisdata) = self.fileref[FstKeys(nom='^^',ip1=self.ig1,ip2=self.ig2,ip3=self.ig3)]
         if (xaxiskeys == None or yaxiskeys == None):  
           print 'getaxis error: axis grid descriptors (>>,^^) not found'
           return (None,None)
         self.xaxis=xaxisdata
         self.yaxis=yaxisdata
         self.xyref = (xaxiskeys.grtyp,xaxiskeys.ig1,xaxiskeys.ig2,xaxiskeys.ig3,xaxiskeys.ig4)
         ni=xaxisdata.shape[0]
         nj=yaxisdata.shape[1]
         self.griddim=(ni,nj)
       axiskeys=FstParms()
       axiskeys.xyref=self.xyref
       axiskeys.griddim=self.griddim
       if axis == 'X':
         axisdata=self.xaxis
       else: 
         axisdata=self.yaxis.ravel()
       return(axiskeys,axisdata)

class FstCriterias:
    "Base methods for RPN standard file selection criteria input filter classes"
    def __init__(self,reference,exclu,extra):
        self.__dict__['exclu'] = exclu
        for name in reference.keys():            # copy initial values from reference
            self.__dict__[name]=[]+reference[name]  # bypass setatttr method for new attributes
        for name in extra.keys():                # add extras using own setattr method
            setattr(self,name,extra[name])

    def update(self,with):
        "Replace Fst attributes of an instance with Fst attributes from another"
        if isinstance(with,FstCriterias) and isinstance(self,FstCriterias):  # check if class=FstParm
            for name in with.__dict__.keys():
                if (name in self.__dict__.keys()) and (name in X__Criteres.keys()):
                    self.__dict__[name]=with.__dict__[name]
        else:
            print 'FstParm.update: can only operate on FstCriterias class instances'
            raise TypeError

    def update_cond(self,with):
        "Conditional Replace Fst attributes if not wildcard values"
        if isinstance(with,FstCriterias) and isinstance(self,FstCriterias):  # check if class=FstCriterias
            for name in with.__dict__.keys():
                if (name in self.__dict__.keys()) and (name in X__Criteres.keys()):
                    if (with.__dict__[name] != X__Criteres[name]):
                        self.__dict__[name]=with.__dict__[name]
        else:
            print 'FstCriterias.update_cond: can only operate on FstCriterias class instances'
            raise TypeError

    def update_by_dict(self,with):
        for name in with.keys():
            if name in self.__dict__.keys():
                setattr(self,name,with[name])

    def isamatch(self,with):
        "Check attributes for a match, do not consider wildcard values"
        global X__DateDebut,X__DateFin,X__Delta
        if isinstance(with,FstParm) and isinstance(self,FstCriterias):  # check if class=FstParm
            match = 1
            for name in with.__dict__.keys():
                if (name in self.__dict__.keys()) and (name in X__FullDesc.keys()):
                    if (self.__dict__[name] != X__Criteres[name]):      # check if wildcard
                        if (name == 'date'):
                            print 'Debug isamatch name=',name
                            if (X__DateDebut != -1) or (X__DateFin != -1):      # range of dates
                                print 'Debug range de date debut fin delta',X__DateDebut,X__DateFin,X__Delta
                                print 'Debug range with self',name,with.__dict__[name],self.__dict__[name]
                                match = match & Fstdc.datematch(with.__dict__[name],X__DateDebut,X__DateFin,X__Delta)
                            else:
                                print 'Debug check ',name,with.__dict__[name],self.__dict__[name]
                                match = match & (with.__dict__[name] in self.__dict__[name])
                        else:
                            print 'Debug check ',name,with.__dict__[name],self.__dict__[name]
                            match = match & (with.__dict__[name] in self.__dict__[name])
            return match
        else:
            print 'FstCriterias.isamatch: can only operate on FstParm, FstCriterias class instances'
            raise TypeError

    def __setattr__(self,name,values):   # this method cannot create new attributes
        if name in self.__dict__.keys():                   # is attribute name valid ?
            if type(values) == type([]):
                self.__dict__[name]=[]
                for value in values:
                    if type(value) == type(''):
                        reflen=len(X__Criteres[name][0])        # string, remember length
                        self.__dict__[name].append((value+reflen*' ')[:reflen])
                    else:
                        self.__dict__[name].append(value)              # integer
            else:
                self.__dict__[name]=[]
                if type(values) == type(''):
                    reflen=len(X__Criteres[name][0])        # string, remember length
                    self.__dict__[name].append((values+reflen*' ')[:reflen])
                else:
                    self.__dict__[name].append(values)              # integer
        else:
            print 'attribute',name,'does not exist for class',self.__class__

    def __str__(self):
        return dump_keys_and_values(self)

class FstSelect(FstCriterias):
    "Selection criterias for RPN standard file input filter"
    def __init__(self,**args):
        FstCriterias.__init__(self,X__Criteres,0,args)

class FstExclude(FstCriterias):
    "Exclusion criterias for RPN standard file input filter"
    def __init__(self,**args):
        FstCriterias.__init__(self,X__Criteres,1,args)

class FstRecord(numpy.ndarray,FstParms):
    "Standard file record, with data (ndarray class) and full set of descriptors"
    def __init__(self,data=None,ref=None):
        if (type(data) == type(numpy.array(0))) or (type(data) == type([])):  # list or array
            numpy.ndarray.__init__(self,data)
        elif isinstance(data,UserArray.UserArray):   # UserArray (or subclass)
            numpy.ndarray.__init__(self,data.array)
        elif data == None:                           # None means initialize with null array
            numpy.ndarray.__init__(self,[])
        else:
            print 'FstRecord: cannot initialize data from arg #2'
            raise TypeError
        FstParms.__init__(self)  # initialize descriptor part
        if ref != None:          # update with ref tags if supplied
            if isinstance(ref,FstParm):
                self.update(ref)
            elif type(ref) == type({}):
                self.update_by_dict(ref)
            else:
                print 'FstRecord: cannot initialize parameters from arg #3'
                raise TypeError
        
class FstDate:
    "Visual date with word1=YYYYMMDD word2=HHMMSShh"
    def __init__(self,word1,word2=-1):
        if isinstance(word1,FstDate):
            self.stamp = word1.stamp
        elif type(word1) == type(0):    # integer type
            if (word2 == -1):
                self.stamp = word1
            else:
                dummy=0
                (self.stamp,dummy1,dummy2) = Fstdc.newdate(dummy,word1,word2,3)
        else:
            print 'FstDate: cannot initialize date time stamp from arguments'
            raise TypeError

    def __sub__(self,other):
        return(Fstdc.difdatr(self.stamp,other.stamp))

    def incr(self,temps):
        if ((type(temps) == type(1)) or (type(temps) == type(1.0))):
            nhours = 0.0
            nhours = temps
            idate=Fstdc.incdatr(self.stamp,nhours)
            print 'Debug idate=',idate,type(idate)
            return(FstDate(idate,-1))
        else:
            print 'incr: wrong argument type'
            raise TypeError

    def range(self,debut=-1,fin=-1,delta=0.0):
        global X__DateDebut,X__DateFin,X__Delta
        X__DateDebut=debut
        X__DateFin=fin
        X__Delta=delta
        print 'Debug setdaterange',X__DateDebut,X__DateFin,X__Delta
        self.stamp=-2          # stamp = -2 indicates a range for the date

class FstMapDesc:
    "Map Descriptors with lat1,lon1, lat2,lon2, rot"
    def __init__(self,key,xs1=0.,ys1=0.,xs2=0.,ys2=0.,ni=0,nj=0):
        print 'Debug FstMapDesc grtyp ig1-4=',key.grtyp,key.ig1,key.ig2,key.ig3,key.ig4
#        print 'Debug FstMapDesc xs1,ys1,xs2,ys2=',xs1,ys1,xs2,ys2
        if isinstance(key,FstParm):
          print 'Debug FstMapDesc appel a Fstdc.mapdscrpt'
          print 'xs1,ys1,xs2,ys2=',xs1,ys1,xs2,ys2
          self.geodesc=Fstdc.mapdscrpt(xs1,ys1,xs2,ys2,ni,nj,key.grtyp,key.ig1,key.ig2,key.ig3,key.ig4)
#       (self.lat1,self.lon1,self.lat2,self.lon2,self.rot)=Fstdc.mapdscrpt(xs1,ys1,xs2,ys2,key.grtyp,key.ig1,key.ig2,key.ig3,key.ig4)
        else:
            print 'FstMapdesc: invalid key'
            raise TypeError

FirstRecord=FstKeys()
NextMatch=None
Predef_Grids()