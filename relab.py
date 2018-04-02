#!/usr/bin/python
# -*- coding: utf-8 -*-
# Filename: relab.py
# Author: Pedro H. A. Hasselmann

# Escrevendo em python3 e usando python2.6:
from __future__ import print_function, unicode_literals, absolute_import, division

### GLOBAL IMPORT
import pandas as pd
from os import path, makedirs
import cPickle as pkl
home = path.expanduser("~")

class Relab:
  '''
     RELAB data tool.
     ================
     
     Documentation:
     
     0. Recreate a working folder
     1. Download Relab spectra library at http://www.planetary.brown.edu/relabdata/    
     2. install pandas, xlrd and matplotlib python packages
     
     Attributes:
               __init__([[path_to_catalog]])
               retrieve_from(link, fmt)
               dataframe(filename, missing, indexid, extract)
               retrieve_spectra(extract)
               query(field, value)
               locate(sampleid)
               show_spectra()
    
     Example:
       from relab import Relab
     
       # Open Library
       relab = Relab(library=PATH_TO_CATALOG)
       
       # Query into the Master Catalogue by Columns
       relab.query("GeneralType1","Synthetic", extract=True)
       print(relab.search)
       
       # Query into the Master Catalogue by SampleID
       relab.locate("AA-A1S-001", extract=True) # Or extract=False if you prefer not to save all selected spectra.
       print(relab.search)
       
       # Plot your spectra
       relab.show_spectra()  
  '''

  def __init__(self, library=path.join("D:\\","Catalogues","RelabDB2017Dec31.zip")):
     '''
        1. Open zipped library
        2. Load and Convert Sample_Catalogue.xls
        3. Load and Convert Spectra_Catalogue.xls
        4. Merge both excel sheets into Master Catalogue
     '''
     import zipfile
     # Create a ZipFile Object for Relab Database:
     self.db = zipfile.ZipFile(library)
     self.cat = self.retrieve_from("catalogues/", fmt="xls")
     
     if not path.exists(path.join('catalogues','Master_catalogue.pkl')):
       samplecat    =  self.dataframe("Sample_Catalogue", extract=True)
       spectracat   = self.dataframe("Spectra_Catalogue", extract=True)
       self.fullcat = pd.merge(samplecat, spectracat, left_index=True, right_index=True)
       self.fullcat.index.name = "SampleID"
       self.fullcat.to_csv(path.join('catalogues','Master_catalogue.dat'), sep=str("\t"), encoding='utf-8', na_rep="-")
       self.fullcat.to_pickle(path.join('catalogues','Master_catalogue.pkl'))
     else:
       self.fullcat = pd.read_pickle(path.join('catalogues','Master_catalogue.pkl'))
       
       
     print('Master Catalogue Colunms: ')
     print(self.fullcat.head())
     print(self.fullcat.columns)

  def retrieve_from(self, link, fmt):
     ''' 
        Retrieve paths of Excel catalogues.
     '''     
     link = link.split("/")[0:-1]
     retrieve = dict()
     n = True     
     
     for pth in self.db.namelist():
         
        pth2 = pth.split("/")[0:-1]
        filename = pth.split("/")[-1][:-4]
        pth_ft = pth[-3:]
        
        if pth2 == link and n == True:
          if pth_ft == fmt: 
            retrieve[filename] = pth
          n = True
          
        elif pth2 != link and n == False:
          n = False
          break
      
     return retrieve
           

  def dataframe(self, catname, missing=["   "], indexid="SampleID", extract=True):
     '''
        Convert excel sheet to pandas.dataframe.
        catname --> catalogue name
        indexid --> Main column of the catalogue
        extract --> extract from zipfile (True/False=Yes/No)
        
     '''
     from numpy import genfromtxt, loadtxt
     import xlrd as excel

     #makedirs(filename[0:-4].replace("/","\ "))
         
     if extract: self.db.extract(self.cat[catname], '.')
     
     loadexcel = excel.open_workbook(self.cat[catname].replace("/","\\"), on_demand=True)
     sheet = loadexcel.sheet_by_name(loadexcel.sheet_names()[0])
     print(sheet.ncols, sheet.nrows)

     f = pd.read_excel(
                       self.cat[catname].replace("/","\\"), 
                       loadexcel.sheet_names()[0], 
                       header=0,
                       index_col=indexid,
                       na_values=missing,
                       )
     return f
  
  ### SPECTRA ###   
  def retrieve_spectra(self,extract=True):
     '''
        Get Spectra.
        
        self.spec : dictionary of spectra
        extract : Boolean, choose to extract the selected spectra or not.
     '''
     sampleid = self.search.index
     spectrumid = self.search["SpectrumID"]
     print(sampleid.values, spectrumid.values)

     out = open("specta_list_query.txt",'w+')    
     self.spec = dict()
     for n, s in enumerate(spectrumid):
       f = sampleid[n].lower().split("-")    
       path = '/'.join(["data",f[1],f[0],s.lower()+'.txt'])  
       self.spec[path] = self.db.open(path, 'r')      
       out.write('{0}\n'.format(path))
       
       if extract==True:
         self.db.extract(path, ".")

  def show_spectra(self,**args):
     '''
        Plot your queried spectra.
     '''
     import matplotlib.pyplot as plt
     from numpy import loadtxt
     
     for s in self.spec.values():
       data = loadtxt(s, skiprows=2, delimiter='\t', comments='\r')
       plt.scatter(data[:,0], data[:,1])
       plt.xlabel("Wavelength")
       plt.ylabel("Reflectance")
       plt.show()

  ### QUERIES ###
  def query(self, field, value, extract=True):
     if field in self.fullcat.columns:
       q = self.fullcat[self.fullcat[field] == value]
       self.search = q       
       self.retrieve_spectra(extract)
  
  def locate(self, sampleid, extract=True):
     self.search = self.fullcat.loc[sampleid]
     self.retrieve_spectra(extract)

if __name__ == '__main__':
  #relab = Relab()
  #relab.locate("RS-CMP-012", False)
  #relab.show_spectra()
  pass
# END