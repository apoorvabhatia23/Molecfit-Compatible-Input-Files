# Import the important packages

import numpy as np
from astropy.io import fits
import os


# This function sorts the files according to their MJDs (time of observation in MJD)

def sort_exposure(data_files):
    
    MJD = []

    for file_name in data_files:
        hdu = fits.open(file_name)
        MJD.append(hdu[0].header['MJD-OBS'])

    MJD = np.array(MJD)
    sorting = np.argsort(MJD)
    MJD = MJD[sorting]
    
    # print(MJD[sorting])

    return sorting, MJD


# It reads the data files from the input directory

def read_hdus(input_data_directory, target_name):

    # I have only chosen files which were observed in the NIR Fibre-A 
    data_files = [os.path.join(input_data_directory, x) for x in os.listdir(input_data_directory) if x.endswith('-sci-desj-nir_A.fits')]
    
    data_files = np.array(data_files)
    
    sort, MJD = sort_exposure(data_files)
    
    data_files_sorted = data_files[sort]
    
    # print(data_files_sorted)
    
    hdus = []
    
    for file_name in data_files_sorted:
        
        hdu = fits.open(file_name)

        if hdu[0].header['OBJECT'] == target_name:
            hdus.append(hdu)

            print(file_name)

   
    # data_files_sorted = data_files[time_sorted_exposures_mask]

    return hdus, MJD


# Here you just define the input data directory

input_data_directory = 'V1298/20231210'

# In case your directory has data of other targets as well, you have to define the target name from the FITS file to separate from the rest
target_name = 'V1298Tau' 

data_files, MJD = read_hdus(input_data_directory = input_data_directory, target_name = target_name)

# data_files = np.array(data_files)


# Molecfit is not able to read CARMENES data as it is as the file format is not supported by it. Hence, we convert our input file into the FITS BINTABLE form

# It is also observed that Molecfit crashes if we use data of multiple spectral orders together, hence, for efficiency reasons, we make the FITS BINTABLE file of only one spectra order
order = 5

for file in data_files:
    
    hdul_orig = file

    # date = hdul_orig[0].header['DATE-OBS']

    # print(date)
    
    SPEC = hdul_orig[1].data[order]
    WAVE = hdul_orig[4].data[order]
    ERRS = hdul_orig[3].data[order]
    
    header_orig = (hdul_orig[0].header)
    date = hdul_orig[0].header['DATE-OBS']
    mjd = str(hdul_orig[0].header['MJD-OBS'])
    empty_primary = fits.PrimaryHDU(header = header_orig)

    # Molecfit does not recognise CARMENES as an instrument yet, hence, we change INSTRUMENT name to "ANY"
    empty_primary.header['INSTRUME'] = 'ANY'

    # For Molecfit to read this file as an input, we needs to add an additional header "HIERARCH ESO PRO CATG" and put it as "SCIENCE"
    empty_primary.header['HIERARCH ESO PRO CATG'] = 'SCIENCE'
    empty_primary.header['OBJECT'] = 'V1298T'
    
    col1 = fits.Column(name = 'wavelength', format = '1D', array = WAVE)
    col2 = fits.Column(name = 'flux', format = '1D', array = SPEC)
    col3 = fits.Column(name = 'err_flux', format = '1D', array = ERRS)
    
    hdu = fits.BinTableHDU.from_columns([col1, col2, col3])
    hdul = fits.HDUList([empty_primary, hdu])

    # print(hdul[0].header)
    data_orig = hdul[1].data

    # Save your new input file into the desired Molecfit input data directory
    hdul.writeto('data_dir/reflex_input/molecfit/molecfit/raw/ANY/' + date + '.fits') 