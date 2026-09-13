#! /usr/bin/env python3

import pandas as pd
import time as time_module
from datetime import datetime, timedelta
from pathlib import Path
import urllib.error
# from .param import code_dict
# from ...util import download

prec_list = [
    11,12,13,14,15,16,17,18,19,20,21,22,23,24,
    31,32,33,34,35,36,40,41,42,43,44,45,46,48,49,
    50,51,52,53,54,55,56,57,60,61,62,63,64,65,66,67,68,69,
    71,72,73,74,81,82,83,84,85,86,87,88,91
]


def wind_direction(w_direction_str):
  """風向を文字から数値(16方位)に変換する """
  drection = {
    '静穏': '0', '北北東': '1', '北東': '2', '東北東': '3', '東': '4',
    '東南東': '5', '南東': '6', '南南東': '7', '南': '8', '南南西': '9',
    '南西': '10', '西南西': '11', '西': '12', '西北西': '13',
    '北西': '14', '北北西': '15', '北': '16'
  }
  return drection[w_direction_str] if w_direction_str in drection else w_direction_str


def split_space(value):
  """空白で区切られている文字の左端だけを取り出す """
  s_value = str(value).strip()
  if ' ' in s_value:
    return s_value.split(" ")[0]
  return s_value


def get_tail_time(
    year: int, month: int, dt: timedelta = timedelta(hours=6), **kwargs
) -> datetime:

    tail_time = datetime(year, month + 1, 1) if month < 12 else datetime(year + 1, 1, 1)
    return tail_time - dt


def make_url(date, stats_type, a_type, prec_no, block_no, option):
  """読み込むページのURLを作成する"""
  type_list = {
     "annual" : "annually" , "monthly" : "monthly" ,
     "daily" : "daily" , "hourly" : "hourly" , "10min" : "10min"
  }
  t_type = type_list[stats_type]
  _a_type = a_type if stats_type == "annual" else a_type + "1"

  return (
     f"https://www.data.jma.go.jp/stats/etrn/view/{t_type}_{_a_type}.php"
     f"?prec_no={prec_no}&block_no={block_no}"
     f"&year={date.year}&month={date.month}&day={date.day}&view={option}"
  )


def make_AMeDAS(date, stats_type, prec_no, block_no, obs_no, lat, lon, height):
  """データフレームをダウンロード形式に整える"""

  a_type = 's' if int(block_no) > 10000 else 'a'
  url = make_url(date, stats_type, a_type, prec_no, block_no, 'p1')

  try:
    df = _fetch_AMeDAS(url)

    if stats_type == '10min':
      label_list = ['時分', '現地気圧', '海面気圧', '降水量', '気温', '相対湿度', '平均風速', '平均風向', '最大瞬間風速', '最大瞬間風向', '日照時間']\
        if a_type == 's' else ['時分', '降水量', '気温', '相対湿度', '平均風速', '平均風向', '最大瞬間風速', '最大瞬間風向', '日照時間']
    elif stats_type == 'hourly':
      label_list = ['時', '現地気圧', '海面気圧', '降水量', '気温', '露点温度', '蒸気圧', '湿度', '平均風速', '平均風向', '日照時間', '全天日射量', '降雪', '積雪', '天気', '雲量', '視程']\
        if a_type == 's' else ['時', '降水量', '気温', '露点温度', '蒸気圧', '湿度', '平均風速', '平均風向', '日照時間', '降雪', '積雪']
    elif stats_type == 'daily':
      label_list = ['日', '現地気圧', '海面気圧', '合計降水量', '1時間最大降水量', '10分最大降水量', '平均気温', '最高気温', '最低気温', '平均湿度', '最小湿度', '平均風速', '最大風速', '最大風向', '最大瞬間風速', '最大瞬間風向', '日照時間', '合計降雪', '最深積雪', '天気概要(昼)', '天気概要(夜)']\
        if a_type == 's' else ['日', '合計降水量', '1時間最大降水量', '10分最大降水量', '平均気温', '最高気温', '最低気温', '平均湿度', '最小湿度', '平均風速', '最大風速', '最大風向', '最大瞬間風速', '最大瞬間風向', '最多風向', '日照時間', '合計降雪', '最深積雪']
    elif stats_type == 'monthly' or stats_type == 'annual':
      label_list = ['月', '現地気圧', '海面気圧', '合計降水量', '日最大降水量', '1時間最大降水量', '10分最大降水量', '日平均気温', '日平均最高気温', '日平均最低気温', '最高気温', '最低気温', '平均湿度', '最小湿度', '平均風速', '最大風速', '最大風向', '最大瞬間風速', '最大瞬間風向', '日照時間', '全天日射量', '合計降雪', '日合計の最大降雪',  '最深積雪', '平均雲量', '雪日数', '霧日数', '雷日数']\
        if a_type == 's' else ['月', '合計降水量', '日最大降水量', '1時間最大降水量', '10分最大降水量', '日平均気温', '日平均最高気温', '日平均最低気温', '最高気温', '最低気温', '平均湿度', '最小湿度', '平均風速', '最大風速', '最大風向', '最大瞬間風速', '最大瞬間風向', '日照時間', '合計降雪', '日合計の最大降雪',  '最深積雪']

    df = df.set_axis(label_list, axis=1)
    if stats_type == 'annual':
      df.rename(columns={'月': '年'}, inplace=True)

    t = df.iloc[:, 0]
    df = df.drop(df.columns[0], axis=1)

    block = {
      '観測点番号': [obs_no] * len(df),
      '緯度': [lat] * len(df),
      '経度': [lon] * len(df),
      '標高': [height] *len(df),
    }
    block = pd.DataFrame(block)

    if a_type == 'a':
      pressure = {
        '現地気圧':['-99.0'] * len(df),
        '海面気圧':['-99.0'] * len(df),
      }
      pressure = pd.DataFrame(pressure)
      df = pd.concat([pressure, df], axis=1)

    if stats_type == '10min':
      time = {
        '時': [str(t[j]).split(":")[0] for j in range(len(df))],
        '分': [str(t[j]).split(":")[1] for j in range(len(df))],
      }
      time = pd.DataFrame(time)
    else:
      time = t

    obs_date = {
        '年': [date.year] * len(df),
        '月': [date.month] * len(df),
        '日': [date.day] * len(df)
    }
    obs_date = pd.DataFrame(obs_date)

    if stats_type == 'daily':
      obs_date = obs_date.drop(obs_date.columns[2],axis=1)
    elif stats_type == 'monthly':
      obs_date = obs_date.drop(obs_date.columns[[1, 2]],axis=1)
    elif stats_type == 'annual':
      obs_date = obs_date.drop(obs_date.columns[[0, 1, 2]],axis=1)

    df = pd.concat([obs_date, time, block, df], axis=1)

    if stats_type == 'hourly':
      df = df.drop(columns = ['露点温度'])
      if a_type == 's':
        df = df.drop(columns = ['天気', '雲量', '視程'])
      elif a_type =='a':
        df.insert(17, '全天日射量', ['-99.0'] * len(df))

    elif stats_type == 'daily':
      df = df.drop(columns = ['天気概要(昼)', '天気概要(夜)']) if a_type == 's' else df.drop(columns = ['最多風向'])

    elif stats_type == 'monthly' or stats_type == 'annual':
      if a_type =='a':
        insert_no = 25 if stats_type == 'monthly' else 24
        df.insert(insert_no, '全天日射量', ['-99.0'] * len(df))

        tmp = {
          '平均雲量': ['-99.0'] * len(df),
          '雪日数': ['-99.0'] * len(df),
          '霧日数': ['-99.0'] * len(df),
          '雷日数': ['-99.0'] * len(df),
        }
        df = pd.concat([df, pd.DataFrame(tmp)], axis=1)

    return df

  except TypeError:
    print(f'TypeError,block_no:{block_no},date:{date}')


def _fetch_AMeDAS(url):
    """気象庁WebページからHTMLを読み込み数値のみのデータフレームを作成する（内部用）"""
    flag = 1
    while flag:
        try:
            dfs = pd.read_html(url)
            df = dfs[0]
            df = df.fillna('-99.0')
            for col in df.columns:
                df[col] = df[col].astype(str).apply(split_space)
                df[col] = df[col].astype(str).apply(wind_direction)
            df = df.replace(['///', '--', '×', '#'], '-99.0')
            flag = 0
            return df
        except ValueError:
            flag = 0
            return pd.DataFrame([])
        except urllib.error.HTTPError:
            print("HTTPError", datetime.now())
            time_module.sleep(300)
        except urllib.error.URLError:
            print("URLError", datetime.now())
            time_module.sleep(300)


def get_time_list(
    stats_type: str,
    start_time: datetime,
    end_time: datetime,
    **kwargs,
) -> list[datetime]:
    from dateutil.relativedelta import relativedelta

    if stats_type == "annual":
        return [end_time]

    time_list = []
    date = start_time

    while date <= end_time:
        time_list.append(date)
        if stats_type in ("10min","hourly"):
            date += timedelta(days=1)
        elif stats_type == "daily":
            date += relativedelta(months=1)
        elif stats_type == "monthly":
            date += relativedelta(years=1)

    return time_list


def get_save_fpath(
    base_dir: Path,
    stats_type: str,
    prec_no: int,
    year: int,
    month: int,
    day: int = 1,
    **kwargs,
) -> Path:

    if stats_type in ("10min","hourly"):
        return base_dir /f"{stats_type}/{year}/{year}{month:02}/ame{prec_no}_{day:02}_{month:02}_{year}.txt"
    elif stats_type == "daily":
        return base_dir /f"{stats_type}/{year}/ame{prec_no}_{month:02}_{year}.txt"
    elif stats_type == "monthly" :
        return base_dir /f"{stats_type}/{year}/ame{prec_no}_{year}.txt"
    elif stats_type == "annual" :
        return base_dir /f"A{stats_type}/ame{prec_no}.txt"
    else:
       raise ValueError(f"想定外のstats_type: {stats_type}")


def AMeDAS_download(
    stats_type: str,
    start_time: datetime,
    end_time: datetime,
    base_dir: Path,
    AMeDAS_point_list: list,
    exist_skip: bool = False,
    **kwargs,
) ->None:

    time_list =get_time_list(stats_type,start_time,end_time)

    for date in time_list:
        #保存フォルダを作成
        if stats_type in ("10min", "hourly"):
            (base_dir /f"{stats_type}/{date.year}/{date.year}{date.month:02}").mkdir(parents=True,exist_ok=True)
        elif stats_type in ("daily","monthly"):
            (base_dir /f"{stats_type}/{date.year}").mkdir(parents=True,exist_ok=True)
        else:
            (base_dir /f"{stats_type}").mkdir(parents=True,exist_ok=True)

        i = 0
        entry =AMeDAS_point_list[0]
        access_time =time_module.time()

        for prec_no in prec_list:
            df = pd.DataFrame()
            save_fpath = get_save_fpath(base_dir, stats_type,prec_no,date.year,date.month,date.day)

            while entry[1] == str(prec_no):
                start_AMeDAS = datetime.strptime(entry[7], "%Y/%m/%d")
                end_AMeDAS   = datetime.strptime(entry[8], "%Y/%m/%d")

                in_range =start_AMeDAS <= date <= end_AMeDAS
                skip = exist_skip and save_fpath.exists()

                if in_range and not skip:
                    if stats_type == "10min" and int(entry[3]) > 10000 and date < datetime(2008,6,25):
                        pass #10min　アメダス地点は2008年6月25日以降のみ対応
                    else:
                        if time_module.time() -access_time < 1.5:
                            time_module.sleep(1.5 -(time_module.time() - access_time))
                        access_time = time_module.time()

                        df1 = make_AMeDAS(date,stats_type,prec_no,entry[3],entry[0],entry[4],entry[5],entry[6])
                        df = pd.concat([df,df1],axis=0)

                i += 1
                entry =AMeDAS_point_list[i] if i <len(AMeDAS_point_list) else ["0","0","0","0","0","0","0","0","0"]

            if len(df) != 0 and not (exist_skip and save_fpath.exists()):
                df.to_csv(save_fpath,header=False,index=False,sep=" ")
            else:
                print(f"exist: {save_fpath}")
