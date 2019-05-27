# 英雄联盟角色头像识别
## 一、数据
1. hero_index_name.csv 文件存储的是英雄全称及其对应序号
2. lol_icon_index 文件夹存储的是分类基准头像图片（从直播截图中挑选）并且图片名字是用序号命名
3. 如果要添加新的英雄，就在csv文件末尾添加序号和全称，并且在lol_icon_index文件夹添加相应的以序号命名的头像图片
## 二、脚本
1. orbClassification.py 是包含orb分类method的class
2. lol_hero_classification.py 相当于main.py 包含整个工作流程。需要注意，在运行前，可能需要修改以下变量
+ src_dir = "img"
+ image_dir = "lol_hero_icon"
+ standard_dir = "standard_sample" 
