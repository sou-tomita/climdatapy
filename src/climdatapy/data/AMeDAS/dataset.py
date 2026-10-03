#! /usr/bin/env python3

from datetime import datetime, timedelta
from pathlib import Path
from typing import Any
from ...util import Dataset
from . import dl


class AMeDAS(Dataset):

    def __init__(self) :
        self.AMeDAS_point_list = None

    def dl_file(self, start_time, end_time, request_kw, data_dir, exist_ok=False):
        # 未読み込みの場合だけ読み込む
        if self.AMeDAS_point_list is None:
            with open(data_dir / "AMeDAS_list.txt", encoding="utf-8") as f:
                AMeDAS_list = [s.rstrip() for s in f.readlines()]
            self.AMeDAS_point_list = [row.split(" ") for row in AMeDAS_list]

        dl.AMeDAS_download(
            request_kw["stats_type"],
            start_time,
            end_time,
            data_dir,
            self.AMeDAS_point_list,
            exist_ok,
        )


    def get_request_key(self, download_kw, **kwargs):
        if "stats_type" not in download_kw:
            download_kw = {"stats_type": ["all"]}

        if "all" in download_kw["stats_type"]:
            download_kw["stats_type"] = ["10min", "hourly", "daily", "monthly", "annual"]

        request_key_list = []
        for stats_type in download_kw["stats_type"]:
            request_key_list.append({
                "stats_type": stats_type,
                "near_realtime": download_kw.get("near_realtime", False),
            })

        return request_key_list


    def get_request_time_range(
        self, start_time: datetime, end_time: datetime, request_kw: dict[str, Any]
    ) -> tuple[datetime, datetime]:

        if request_kw["near_realtime"]:
            min_start_time = datetime(datetime.now().year - 1, 1, 1, 0)
        else:
            min_start_time = datetime(1872, 1, 1, 0)

        request_start_time = (
            start_time if min_start_time < start_time else min_start_time
        )

        last_time = self.get_newest_time(request_kw)
        if end_time < request_start_time:
            request_end_time = request_start_time
        elif end_time > last_time:
            request_end_time = last_time

        else:
            request_end_time = end_time

        return request_start_time, request_end_time


    def get_all_download_key(self) -> dict[str, list[Any]]:

        return {
            "stats_type": ["all"],
        }


    def get_newest_time(self, request_kw: dict[str, list[Any]]) -> datetime:

        if request_kw["near_realtime"]:
            last_time = datetime.now() - timedelta(days=1)
            last_time = datetime(last_time.year, last_time.month, last_time.day, 6)
            #dailyのデータは、毎時5時に更新のため、取得可能な最新更新日時を毎時6時に設定
        else:
            now_time = datetime.now()
            dmonth = 1 if now_time.day >= 4 else 2
            month = now_time.month - dmonth
            year = now_time.year if month > 0 else now_time.year - 1
            month = 12 - month if month < 1 else month

            last_time = dl.get_tail_time(year, month, dt=timedelta(hours=6))

        return last_time
