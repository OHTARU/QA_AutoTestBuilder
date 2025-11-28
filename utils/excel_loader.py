import pandas as pd
import os

def get_excel_columns(filepath):
    """엑셀 파일의 컬럼(헤더) 목록만 가져오기"""
    try:
        if not os.path.exists(filepath): return []
        df = pd.read_excel(filepath, nrows=0) # 데이터는 안 읽고 헤더만 읽음
        return list(df.columns)
    except Exception as e:
        print(f"Excel Read Error: {e}")
        return []

def load_excel_data(filepath):
    """엑셀 데이터를 리스트(Dictionary List) 형태로 반환"""
    try:
        # NaN(빈값)은 빈 문자열("")로 변환
        df = pd.read_excel(filepath).fillna("")
        # 각 행을 딕셔너리로 변환하여 리스트에 담음
        return df.to_dict(orient='records')
    except Exception as e:
        print(f"Data Load Error: {e}")
        return []