#! /usr/bin/env python3

"""
直近に公開されたJRA3Qをダウンロードするサンプルスクリプト
"""

from pathlib import Path
import climdatapy

print(f"climdatapy version = {climdatapy.__version__}")

# AMeDAS管理クラスを取得
manager = climdatapy.get_manager("AMeDAS")

# 直近に公開されたデータをダウンロード
manager.update(
    download_kw={
        "stats_type": ["all"],
    },
    data_dir=Path("/DATA/DATA/PUBLIC_DATA/AMeDAS"),
    log_file_path=Path("DATA/DATA/PUBLIC_DATA/AMeDAS/update_AMeDAS.log"),
    exist_ok=True,
)
