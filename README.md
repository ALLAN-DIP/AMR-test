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

If you have a test file containing several AMRs, please refer to DAIDE/Diplomacy/README.md to parse it from AMR to DAIDE.

