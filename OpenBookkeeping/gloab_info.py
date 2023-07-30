prop_type_items = ['固定资产', '流动资产', '长期负债', '短期负债']

prop_type_ids = {item: idx for idx, item in enumerate(prop_type_items)}

liability_currency_types = ['等额本息', '先息后本', '等额本金', '到期还本付息']

liability_currency_ids = {item: idx for idx, item in enumerate(liability_currency_types)}


query_prop_by_name="""
select * from prop where  name={}
"""

query_prop_table = """
select name, type, start_date, currency, sum(amount) from prop LEFT outer join prop_details
on prop.id = prop_details.target_id group by name;
"""


create_prop_table = """
CREATE TABLE "prop" (
    "id"	INTEGER NOT NULL,
    "name"	text NOT NULL,
    "type"	INTEGER NOT NULL,
    "start_date"	text NOT NULL,
    "term_month" INTEGER,
    "rate" INTEGER,
    "currency"	INTEGER NOT NULL,
    "ctype" INTEGER,
    "comment" text,
    PRIMARY KEY("id" AUTOINCREMENT)
);
"""


create_prop_detail_table = """
CREATE TABLE "prop_details" (
    "id"	INTEGER NOT NULL,
    "target_id"	INTEGER NOT NULL,
    "occur_date"	text NOT NULL,
    "amount"	INTEGER NOT NULL,
    "notes"	TEXT,
    PRIMARY KEY("id" AUTOINCREMENT)
);
"""
