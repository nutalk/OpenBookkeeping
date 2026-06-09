#!/usr/bin/env python
"""OpenBookkeeping 数据导出脚本

将 SQLite 数据库中的 Prop 和 Detail 数据导出为 JSON 格式，
用于迁移到 my_bookkeep 或其他系统。

用法:
    python export_data.py                          # 默认导出到 ./export.json
    python export_data.py --output /path/to/output.json
    python export_data.py --db /path/to/db.sqlite3
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Django 环境设置
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookkeep.settings")

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def setup_django():
    """初始化 Django"""
    import django
    django.setup()


def export_data(output_path: str):
    """导出所有 Prop 及其关联的 Detail 数据为 JSON"""
    from accounts.models import Prop, Detail

    props_data = []
    for prop in Prop.objects.all().order_by("id"):
        details = Detail.objects.filter(target_id=prop).order_by("id")
        details_data = [
            {
                "id": d.id,
                "occur_date": d.occur_date,
                "amount": d.amount,
                "comment": d.comment or "",
            }
            for d in details
        ]

        props_data.append(
            {
                "id": prop.id,
                "name": prop.name,
                "p_type": prop.p_type,
                "start_date": prop.start_date,
                "term_month": prop.term_month,
                "rate": prop.rate,
                "currency": prop.currency or 0,
                "ctype": prop.ctype,
                "comment": prop.comment or "",
                "activate": prop.activate,
                "details": details_data,
            }
        )

    # 汇总统计
    total_assets = 0
    total_liabilities = 0
    for p in props_data:
        total = sum(d["amount"] for d in p["details"])
        if p["p_type"] <= 1:
            total_assets += total
        else:
            total_liabilities += total

    export_data = {
        "version": "1.0",
        "exported_at": datetime.now().isoformat(),
        "source": "OpenBookkeeping",
        "summary": {
            "total_props": len(props_data),
            "total_details": sum(len(p["details"]) for p in props_data),
            "total_assets": total_assets,
            "total_liabilities": total_liabilities,
            "net_worth": total_assets - total_liabilities,
        },
        "props": props_data,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(export_data, f, ensure_ascii=False, indent=2)

    print(f"✅ 数据已导出到: {output_path}")
    print(f"   - 账户数: {export_data['summary']['total_props']}")
    print(f"   - 明细数: {export_data['summary']['total_details']}")
    print(f"   - 总资产: {total_assets:,}")
    print(f"   - 总负债: {total_liabilities:,}")
    print(f"   - 净资产: {total_assets - total_liabilities:,}")


def main():
    parser = argparse.ArgumentParser(
        description="OpenBookkeeping 数据导出脚本 - 导出为 JSON 格式"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="export.json",
        help="输出文件路径 (默认: export.json)",
    )
    parser.add_argument(
        "--db",
        "-d",
        default=None,
        help="SQLite 数据库文件路径 (默认: 使用 settings.py 中的配置)",
    )
    args = parser.parse_args()

    # 如果指定了数据库路径，覆盖 Django 配置
    if args.db:
        db_path = os.path.abspath(args.db)
        if not os.path.exists(db_path):
            print(f"❌ 数据库文件不存在: {db_path}")
            sys.exit(1)
        os.environ.setdefault("DATABASE_PATH", db_path)

    # 解析输出路径
    output_path = os.path.abspath(args.output)
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    setup_django()
    export_data(output_path)


if __name__ == "__main__":
    main()
