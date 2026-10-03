#! /usr/bin/env python3

"""
CERESをダウンロードするサンプルスクリプト
"""

from datetime import datetime
from pathlib import Path

import climdatapy


# CERES管理クラスを取得
manager = climdatapy.get_manager("CERES")

manager.download(
    start_time=datetime(2000, 3, 1),
    end_time=datetime(2022, 3, 1),
    data_dir=Path("/DATA/DATA/PUBLIC_DATA/CERES"),
    exist_ok=True,
)