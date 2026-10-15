#! /usr/bin/env python3

from datetime import datetime
from pathlib import Path
from typing import Any

from ...util import Dataset
from . import dl


class CERES(Dataset):

    def __init__(self) -> None:
        super().__init__()

        self.min_time = datetime(2000, 3, 1)
        self.max_time = datetime(2022, 3, 1)

    def get_request_key(
        self,
        download_kw: dict[str, list[str]],
        **kwargs,
    ) -> list[dict[str, Any]]:

        return [{"": None}]

    def get_request_time_range(
        self,
        start_time: datetime,
        end_time: datetime,
        request_kw: dict[str, Any],
    ) -> tuple[datetime, datetime]:

        request_start_time = max(start_time, self.min_time)
        request_end_time = min(end_time, self.max_time)

        if request_start_time > request_end_time:
            raise ValueError(
                "Requested period is outside the available CERES period "
                "(2000-03-01 to 2022-03-01)."
            )

        return request_start_time, request_end_time

    def get_all_download_key(self) -> dict[str, list[str]]:

        return {"": [""]}

    def dl_file(
        self,
        start_time: datetime,
        end_time: datetime,
        request_kw: dict[str, Any],
        data_dir: Path,
        exist_ok: bool = False,
    ) -> None:

        dl.ceres_download(
            data_dir=data_dir,
            exist_skip=exist_ok,
        )

    def get_newest_time(
        self,
        request_kw: dict[str, list[Any]],
    ) -> datetime:

        return self.max_time