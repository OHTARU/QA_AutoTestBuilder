import json

def save_to_json(filepath, url, steps):
    """URL과 스텝 데이터를 JSON으로 저장"""
    try:
        data = {"url": url, "steps": steps}
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Save Error: {e}")
        return False

def load_from_json(filepath):
    """JSON 파일을 읽어서 URL과 스텝 데이터 반환"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("url", ""), data.get("steps", [])
    except Exception as e:
        print(f"Load Error: {e}")
        return None, []