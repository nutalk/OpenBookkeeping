[README EN](https://github.com/nutalk/OpenBookkeeping/blob/main/README_EN.md)

OpenBookkeeping是一个利用定期对账来跟踪个人资产负债的开源项目，并且可以绘制丰富的报表，包括资产负债的变化、未来现金流的预测等。
# 主要特点
- 每月对账一次，避免繁琐记账
- 丰富的报表，帮助对当前财务状况进行评估
- 对过往的资产负债情况进行跟踪，并能查看明细
- 对各项资产负债的现金流进行汇总，预测资产负债的变化
- 开源、免费、自部署，支持docker部署
- 基于sqlite的本地数据管理，保证安全与隐私

# 安装方式
## 在debian系linux服务器直接安装

在debian linux服务器上执行以下命令：

```
git clone git@github.com:nutalk/OpenBookkeeping.git
pip install --no-cache-dir -r requirement.txt
sudo apt install -y gettext
sudo mkdir /data
sudo chmod -R 777 /data
bash docker/init_run.sh
```

## 通过docker安装

```
sudo mkdir /path_to_data
sudo chmod -R 777 /path_to_data
docker pull nutalk/bookkeep:main
docker run -p 7788:7788 -v /path_to_data:/data nutalk/bookkeep:main
```

# 安装完成后

打开浏览器，通过http://ip:7788 访问项目主页。

在/path_to_data或者/data目录，你能找到一个db.sqlite3文件，里面是所有的数据文件，记得定期进行备份。

如果希望使用django自带的后台，账号密码如下：
```
user: admin
password:77887788
```

# 截图

账户清单页面
![](https://www.gaopule.tech/upload/%E5%9B%BE%E7%89%87.png)

每月对账页面
![](https://www.gaopule.tech/upload/%E5%9B%BE%E7%89%87-ltha.png)

账户概述报表
![](https://www.gaopule.tech/upload/%E5%9B%BE%E7%89%87-mfgi.png)

资产负债的现金流推演
![](https://www.gaopule.tech/upload/%E5%9B%BE%E7%89%87-cynw.png)
