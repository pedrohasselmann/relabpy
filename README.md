# relabpy
Easily query through the RELAB Spectral Library.

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
