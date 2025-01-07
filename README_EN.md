OpenBookkeeping is an open-source tool that tracks personal assets and liabilities through regular reconciliations. It also generates rich reports, including changes in assets and liabilities, future cash flow predictions, and more.

# Key Features
- Reconciliation once a month, avoiding the hassle of detailed bookkeeping.
- Rich reports that help assess current financial status.
- Tracks past assets and liabilities, with the ability to view detailed records.
- Summarizes cash flows for each asset and liability, predicting changes in assets and liabilities.
- Open-source, free, and self-hosted, with Docker support for deployment.
- Local data management based on SQLite, ensuring security and privacy.

# Installation Methods
## Direct installation on Debian-based Linux servers

Execute the following commands on your Debian Linux server:

```
git clone git@github.com:nutalk/OpenBookkeeping.git
pip install --no-cache-dir -r requirement.txt
sudo apt install -y gettext
sudo mkdir /data
sudo chmod -R 777 /data
bash docker/init_run.sh
```
## Installation via Docker
```
sudo mkdir /path_to_data
sudo chmod -R 777 /path_to_data
docker pull nutalk/bookkeep:main
docker run -p 7788:7788 -v /path_to_data:/data nutalk/bookkeep:main
```
# After Installation
Open a browser and visit the project homepage via http://ip:7788.

In the /path_to_data or /data directory, you will find a file named db.sqlite3 which contains all the data. Remember to back it up regularly.

If you'd like to use the built-in Django admin panel, the login credentials are as follows:
```
Username: admin
Password: 77887788
```
# Screenshots
Account List Page
![accounts](https://www.gaopule.tech/upload/%E5%9B%BE%E7%89%87-nbes.png "")

Monthly Reconciliation Page
![](https://www.gaopule.tech/upload/%E5%9B%BE%E7%89%87-gsuv.png)

Account Overview Report
![](https://www.gaopule.tech/upload/%E5%9B%BE%E7%89%87-ayva.png)

Cash Flow Projection for Assets and Liabilities
![](https://www.gaopule.tech/upload/%E5%9B%BE%E7%89%87-oqpj.png)