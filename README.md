# OpenBookkeeping
开源个人与家庭财务跟踪软件。

## 主要功能
个人与家庭记账应该关注整体的资产与负债、现金流是否充沛，而各项收支细节记录过于繁琐，且没有很大的用处。

因此，OpenBookkeeping最关注以下功能：
1. 记录各项资产与负债。
2. 每项资产与负债都能计算现金流。
3. 定期核对各项资产与负债的情况。
4. 跟踪整体资产与负债的变化趋势。

另外出于安全性考虑，数据用sqlite在本地保存。

## 安装
### 直接安装
在linux服务器上执行以下命令：

```
get clone git@github.com:nutalk/OpenBookkeeping.git
pip install --no-cache-dir -r requirement.txt
python manage.py runserver 0.0.0.0:7788
```
你就能打开浏览器，通过http://ip:7788 访问了。

在windows上应该也行，但我没有测试过。

### 通过docker安装
```
docker pull nutalk/bookkeep:main
docker run -p 7788:7788 nutalk/bookkeep:main
```

## django账户密码
user: admin
password: 77887788