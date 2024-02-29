# Molecfit-Compatible-Input-Files
This repository has the code to convert CARMENES input data files into a FITS BINTABLE file as to make it compatible with Molecfit GUI. The trick is to add an additional HEADER files called "HIERARCH ESO PRO CATG" and putting that as "SCIENCE", as for Molecfit to read it as an input file. Since, CARMENES is not yet recognised by Molecfit as an instrument, change the HEADER "INSTRUME" to "ANY". Additionally, looking at the efficiency of Molecfit, use data from only one spectral order, as Molecfit tends to crash if it's more than that.

Written with the help of Georgia Mraz.
