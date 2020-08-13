## A Military Knowledge Graph Using Baidu Relation Extraction Baseline System
### Reference  
[2020语言与智能技术竞赛：关系抽取任务](https://aistudio.baidu.com/aistudio/competition/detail/31?isFromCcf=true)

### Environments  
Python3 + Paddle Fluid 1.5 (please confirm your Python path in scripts).  
Dependencies are listed in `./requirements.txt`

Or execute the following command to install: 
<br>GPU版本 `pip install paddlepaddle==1.5.2 -i https://mirror.baidu.com/pypi/simple`
<br>CPU版本 `pip install paddlepaddle-gpu==1.5.2.post107 -i https://mirror.baidu.com/pypi/simple`

### Download pre-trained ERNIE model  
Download ERNIE1.0 Base（max-len-512）model and extract it into `./pretrained_model/`  
```
cd ./pretrained_mdoel/
wget --no-check-certificate https://ernie.bj.bcebos.com/ERNIE_1.0_max-len-512.tar.gz
tar -zxvf ERNIE_1.0_max-len-512.tar.gz
```

### DataSet
We crawled about 4,000 military reports from Sina.com and Sohu.com of the past months, and labeled 300 corpus from them. The corpus contains 3 kinds of relationships:

|predicate|subject|subject_type|object|object_type|
|:-:|:-:|:-:|:-:|:-:|
|拥有|巴基斯坦|国家|第16“黑豹”中队|部队|
|研发|巴基斯坦|国家|JF-17B战斗机|武器|
|配备|黑豹中队|部队|JF-17B战斗机|武器|	

run`python get_corpus.py`to get un-tagged corpus.
### Training  
```
sh ./script/train.sh
```
By default the checkpoints will be saved into `./checkpoints/`  
Multi-gpu training is supported after `LD_LIBRARY_PATH` is specified in the script:  
```
export LD_LIBRARY_PATH=/your/custom/path:$LD_LIBRARY_PATH
```
**Accuracy** (token-level and example-level) is printed during the during the training procedure.

### Get structured-data corpus
Gett existing knowledge form [中华网](https://www.china.com/), run:`python get_structured_data.py`

### Visualization demonstration
...

### Update Knowledge Graph
run:
`python update_KG.py`

### To do list
- [x] Train the model 
- [x] Visualization demonstration
- [ ] Expand relation tables and corpus
- [ ] Synonyms problem
- [ ] Speed up
