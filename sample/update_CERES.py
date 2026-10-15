#! /usr/bin/env python3

"""
CERESを更新するサンプルスクリプト
"""

from pathlib import Path
import climdatapy

print(f"climdatapy version = {climdatapy.__version__}")

# CERES管理クラスを取得
manager = climdatapy.get_manager("CERES")

# 最新のCERESデータをダウンロード
manager.update(
    data_dir=Path("/DATA/DATA/PUBLIC_DATA/CERES"),
    log_file_path=Path("/DATA/DATA/PUBLIC_DATA/CERES/update_CERES.log"),
    exist_ok=True,
)
