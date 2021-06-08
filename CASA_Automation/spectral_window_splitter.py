#To split off spectral windows from a calibrated dataset, open CASA in the working directory of the data set and use this script. 
#Ensure that there are no other measurement sets in that working directory or they will be deleted

#Change the following parameters
fitsf = 'J1058+0443_A_C_PE2_12B-230' #uvfits name
spectral_windows_to_split = '0~4' #selected spectral windows
pseudo_band = 'CS' #pseudo_band; required for naming, give spectral window if not selecting a sub-band

#general variable naming for the various measurement sets created by CASA
split_name = fitsf + pseudo_band + '.ms'
uvfits_name = fitsf + pseudo_band
myvis = 'temp_vis.ms'


importuvfits(fitsfile=fitsf,vis=myvis) #import the uvfits file to a CASA measurement set
split(vis=myvis, field = '0', spw=spectral_windows_to_split, outputvis = split_name, correlation='RR,LL',datacolumn='data'); #split off the selected spectral window
exportuvfits(vis=split_name,fitsfile=uvfits_name,datacolumn='data',padwithflags=True,overwrite=True)    #export the data 

os.system('rm -rfv *.ms*') #clear all of the measurement sets created in the process





