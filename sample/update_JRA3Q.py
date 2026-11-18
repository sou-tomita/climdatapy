#! /usr/bin/env python3

"""
直近に公開されたJRA3Qをダウンロードするサンプルスクリプト
"""

from pathlib import Path

import climdatapy

print(f"climdatapy version = {climdatapy.__version__}")

# JRA3Q管理クラスを取得
manager = climdatapy.get_manager("JRA3Q")

# 直近に公開されたbnd_ocean125をダウンロード
download_kw = {
    "stats_type": ["monthly"],
    "data_kind": ["bnd_ocean125"],
    "near_realtime": ["false"],
    "std": ["true"],
    "var": ["all"],
}

manager.update(
    download_kw=download_kw,
    data_dir=Path("./data"),
    log_file_path=Path("./update_jra3q.log"),
    exist_ok=True,
)

## 直近に公開されたanl_surf125をダウンロード
#manager.update(
#    download_kw={
#        "stats_type": ["instant"],
#        "data_kind": ["anl_suf125"],
#        "near_realtime": ["all"],
#        "stats_type": ["all"],
#        "std": ["true"],
#        "var": ["all"],
#    },
#    data_dir=Path("./data"),
#    log_file_path=Path("./update_jra3q.log"),
#    exist_ok=True,
#)

# または、update_allメソッドで、ダウンロード可能なすべてのファイルを取得する。
"""manager.update_all(
    data_dir=Path("./data"),
    log_file_path=Path("./update_jra3q.log"),
    exist_ok=True,
)"""
