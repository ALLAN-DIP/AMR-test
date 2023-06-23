# AMR



Script to map single ENG sentence to DAIDE:
Download the pre-trained model file from:
and put the model in 

<details>
<summary>CLI examples</summary>
```
python single.py --english "I propose ally between us" --sender "Russia" --recipient "Turkey"
``` 
</details>

<details>
<summary>jsonl output format</summary>

jsonl output example line:
```
{"id": "dip_0001.1", "snt": "Austria", "amr": "(c / country :name (n / name :op1 \"Austria\"))", "daide-status": "Full-DAIDE", "daide": "AUS"}
```
</details>
