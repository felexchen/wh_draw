wh_draw
========

Repository for plotting and table-making utilities combining the flexibility of analysis_code's simple and flexible string-based plotting with the speed of ra4_macros' "looping" scripts.

#### Code documentation
Doxygen-based documentation is available at [Adam's UCSB-HEP webpage](http://hep.ucsb.edu/people/ald77/documentation/doc_ra4_draw/).

#### Setup and compilation
Compilation requires c++11 and ROOT, but not CMSSW. To compile, simply run

    ./compile.py

#### Making histograms
An example script is available under src/test.cxx. To execute, compile and then run

    ./run/core/test.exe
    
Another example for WH is here:
    ```
    ./run/wh/plot_datamc.exe
    ```
##### Adding branches

The list of branches available for plotting must be specified in txt/variables/full

Then, at compile-time, a baby file will be generated to load/set addresses for all of the variables listed.
Modifying this file should cause the whole repository to be recompiled.



Higgs Tag SF Instructions
========
```
~$ cd
~$ export VO_CMS_SW_DIR=/cvmfs/cms.cern.ch
~$ source $VO_CMS_SW_DIR/cmsset_default.sh
```

#### For more information on how to set up wh_draw: https://github.com/heller3/wh_draw
#### For more information on how to set up WH_studies: https://github.com/danbarto/WH_studies

#### For input distributions:

#### Clone and go to correct branch
```
~$ cd
~$ cmsrel CMSSW_8_0_20
~$ cd CMSSW_8_0_20/src
~$ cmsenv
~$ git clone https://github.com/felexchen/wh_draw.git wh_draw
~$ cd wh_draw
~$ git checkout newBabies
```

#### Make necessary directories 
```
~$ cd plots/mistag/mT/FatJet_pT
~$ chmod +x makedir.sh
~$ ./makedir.sh
~$ cd ../ANsignal/FatJet_pT
~$ cd plots/mistag/mT/ANsignal/FatJet_pT
~$ chmod +x makedir.sh
~$ ./makedir.sh
~$ cd ../../../../..
```

#### Compile and run
```
~$ ./compile.py
~$ ./run/wh/plot_datamcSF_2020_05_27_babies_withSMWH.exe
~$ ./run/wh/plot_datamcSF_2020_07_16_babies_ANsignal.exe
```

#### Organize files
```
~$ cd plots/mistag/mT/FatJet_pT
~$ chmod +x categorize.sh
~$ ./categorize.sh
~$ cd ../ANsignal/FatJet_pT
~$ cd plots/mistag/mT/ANsignal/FatJet_pT
~$ chmod +x categorize.sh
~$ ./categorize.sh
```

#### For mistags and SFs:

#### Clone and go to correct branch
```
~$ cd
~$ cmsrel CMSSW_10_2_9
~$ cd CMSSW_10_2_9/src
~$ cmsenv
~$ git clone https://github.com/felexchen/WH_studies.git WH_studies
~$ cd WH_studies/Analysis/python/mistag
~$ git checkout scaleFactors
```

#### Make necessary directories 
```
~$ mkdir -p plots/mT/ANsignal/FatJet_pT/Gen_H
~$ mkdir -p plots/mT/FatJet_pT/SM_WH
```

#### Plot mistags and SFs
```
~$ python plot_mistag_noSplitBkgSupport.py --combineYears --combineJets --combineBkgs --SMWH
~$ python ANsignal_mistag.py --combineBkgs --combineJets --Gen
```

#### To view them:

Follow these intructions: https://github.com/danbarto/tW_scattering/tree/master/plots

and then

```
~$ cd 
~$ cd public_html/WH_studies
~$ cp ~/CMSSW_10_2_9/src/WH_studies/Analysis/python/mistag/makedir.sh .
~$ chmod +x makedir.sh
~$ ./makedir.sh
~$ cp ~/CMSSW_10_2_9/src/WH_studies/Analysis/python/mistag/copy.sh .
~$ chmod +x copy.sh
~$ ./copy.sh
```

The plots should now be available at http://uaf-10.t2.ucsd.edu/~your_uaf_username/WH_studies/
