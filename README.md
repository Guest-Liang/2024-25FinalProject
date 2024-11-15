# 毕设
好像也没什么想说的，就是太麻烦了还有填一堆表格，什么甘特图什么中期目标   
明明一个月就能干完的活…

# 编译
[![wakatime](https://wakatime.com/badge/user/0985cb7f-21b8-4ea5-86a4-5e6ba93cb575/project/3eb63dd6-fb69-469e-a7de-4cd19eb66177.svg)](https://wakatime.com/badge/user/0985cb7f-21b8-4ea5-86a4-5e6ba93cb575/project/3eb63dd6-fb69-469e-a7de-4cd19eb6617.svg)   

backend, 产物在dist:   
```conda
cd backend
conda activate FinalProject
pip install -r requirements.txt
python pyi_auto_pack.py
```

vue前端, 产物在dist:   
```npm
cd frontend
pnpm install
pnpm build-only
```

electron, 产物在build:   
```npm
cd frontend
pnpm electron-builder --win
```

# 运行
windows 安装版，或者免安装版   
无论哪种都需要一个控制台，所以双击启动会有一个无输出的控制台弹出，不要关闭   
通过控制台启动，可以看到错误信息   

ubuntu 免安装版 以0.2.1版本为例      
解压tar.gz   
```bash
mkdir App
tar -zxvf GuestLiangElectronApp-0.2.1.tar.gz -C ./App 
```
在控制台运行
```bash
cd ./App
./guestliang-electron-app --no-sandbox --disable-gpu
```


### 11.7日
![81aab6cfb8d28ac35a775825c98b17b9](https://github.com/user-attachments/assets/5bc0c2d8-e689-4483-9c8e-05b890ea260a)   
