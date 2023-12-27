# Lightweight Video-Based Respiration Rate Detection Algorithm: An Application Case on Intensive Care 🪡 (IEEE Transactions on Multimedia 2023)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) 
<a href="https://pytorch.org/get-started/locally/"><img alt="PyTorch" src="https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white"></a>

By [Menghan Hu](https://faculty.ecnu.edu.cn/_s15/hmh/main.psp), [Xudong Tan](https://scholar.google.com/citations?user=6wfIBLgAAAAJ&hl=zh-CN&oi=sra)

If you have any questions, please contact Menghan Hu(mhhu@ce.ecnu.edu.cn) or Xudong Tan(shawntannnn@gmail.com).

## Important Links
- dataset: [LBRD-IC-Dataset](https://github.com/ShawnTan86/LBRD-IC-Dataset) 🌟🌟🌟
- demo link: [Scene 1](https://www.youtube.com/watch?v=rpBcFdN-Pbw&t=2s), [Scene 2](https://www.youtube.com/watch?v=tb_ixhTzqvs) 🔥🔥🔥
- paper: [Lightweight Video-Based Respiration Rate Detection Algorithm: An Application Case on Intensive Care](https://ieeexplore.ieee.org/abstract/document/10158936)  🎉🎉🎉

## A Gentle Introduction
This is a lightweight non-contact respiratory signal detection algorithm suitable for daily use and applicable in ICU scenarios.
![image](https://github.com/ShawnTan86/Lightweight-Video-based-Respiration-Rate-Detection-Algorithm/blob/main/lmagesFolderForReadMe/Application%20diagram.png)

## Getting Started
```bash
conda create -n IOF python=3.9
pip install opencv-python==4.8.0
pip install numpy==1.24.1
pip install scipy==1.11.3
pip install matplotlib==3.7.2
```
cd [Your installation directory]

```bash
python main.py --video-path ./test2.mp4
```
![image](https://github.com/ShawnTan86/Lightweight-Video-based-Respiration-Rate-Detection-Algorithm/blob/main/lmagesFolderForReadMe/test2_result.png)

## Citation
If you use our code for your paper, please cite:
```
@ARTICLE{10158936,
  author={Tan, Xudong and Hu, Menghan and Zhai, Guangtao and Zhu, Yan and Li, Wenfang and Zhang, Xiao-Ping},
  journal={IEEE Transactions on Multimedia}, 
  title={Lightweight Video-Based Respiration Rate Detection Algorithm: An Application Case on Intensive Care}, 
  year={2023},
  volume={},
  number={},
  pages={1-15},
  doi={10.1109/TMM.2023.3286994}}
```
