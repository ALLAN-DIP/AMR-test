# AMR



Script to map single ENG sentence to DAIDE:

Download the pre-trained model file from:

https://drive.google.com/file/d/1Snne-h_vaO8WcCVGqk4PZRuGacSDyMif/view?usp=drive_link

and put the model under personal/SEN_REC_MODEL/

<details>
<summary>CLI examples</summary>
```
python single.py --english "I propose ally between us" --sender "Russia" --recipient "Turkey"
``` 
</details>

For several sentences, use the following code to parse from English to AMR. Make sure put the file with same syntax under ../AMR/amrlib/amrlib/data/diplomacy/data/test

<details>
<summary>CLI examples</summary>
```
cd ../AMR/amrlib/scripts/33_Model_Parse_XFM\
  
python 10_Collect_AMR_Data.py

python 22_Test_Model.py
``` 
</details>

You can also use a sentence-AMR file to parse from AMR to DAIDE, more detailed information please refer to README.me file in DAIDE/DiplomacyAMR

