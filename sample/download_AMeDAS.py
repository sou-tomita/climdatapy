#! /usr/bin/env python3

"""
AMeDASをダウンロードするサンプルスクリプト
"""

from datetime import datetime
from pathlib import Path
import climdatapy


# AMeDAS管理クラスを取得
manager = climdatapy.get_manager("AMeDAS")

manager.download(
    start_time=datetime(2026, 4, 25),
    end_time=datetime(2026, 4, 30),
    data_dir=Path("/DATA/DATA/PUBLIC_DATA/AMeDAS"),
    download_kw={"stats_type":["all"]},
    exist_ok=True,
)