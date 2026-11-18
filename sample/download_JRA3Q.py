#! /usr/bin/env python3

"""
JRA3Qの海面境界条件データをダウンロードするサンプルスクリプト
"""

from datetime import datetime
from pathlib import Path

import climdatapy

print(f"climdatapy version = {climdatapy.__version__}")

# JRA3Q管理クラスを取得
manager = climdatapy.get_manager("JRA3Q")

download_kw = {
    "stats_type": ["monthly"],
    "data_kind": ["bnd_ocean125"],
    "near_realtime": ["false"],
    "std": ["true"],
    "var": ["all"],
}

# 2020年1-5月のbnd_ocean125をダウンロード
manager.download(
    start_time=datetime(2020, 1, 1, 0),
    end_time=datetime(2020, 5, 31, 23),
    download_kw=download_kw,
    data_dir=Path("./data"),
    log_file_path=Path("./download_jra3q.log"),
    exist_ok=True,
)

# または、download_allメソッドで、ダウンロード可能なすべてのファイルを取得する。
"""manager.download_all(
    start_time=datetime(2020, 1, 1, 0),
    end_time=datetime(2020, 5, 31, 18),
    data_dir=Path("./data"),
    log_file_path=Path("./donload_jra3q.log"),
    exist_ok=True,
)"""
