import json
import os
from cryptography.fernet import Fernet

KEY_FILE = "secret.key"

def _get_cipher():
    """암호화 키 로드 또는 생성"""
    if not os.path.exists(KEY_FILE):
        # 키가 없으면 새로 생성
        key = Fernet.generate_key()
        with open(KEY_FILE, "wb") as key_file:
            key_file.write(key)
    
    # 키 읽기
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()
    return Fernet(key)

def save_to_json(filepath, url, steps):
    """데이터 저장 (비밀번호는 암호화)"""
    try:
        cipher = _get_cipher()
        steps_to_save = []

        # 깊은 복사 대신 리스트 컴프리헨션으로 처리
        for step in steps:
            new_step = step.copy()
            # 비밀번호 타입인 경우 암호화 수행
            if new_step['action'] == 'input_password' and new_step['value']:
                encrypted_val = cipher.encrypt(new_step['value'].encode()).decode()
                new_step['value'] = f"ENC:{encrypted_val}" # 암호화된 표시(prefix)
            steps_to_save.append(new_step)

        data = {"url": url, "steps": steps_to_save}
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Save Error: {e}")
        return False

def load_from_json(filepath):
    """데이터 로드 (비밀번호 복호화)"""
    try:
        cipher = _get_cipher()
        
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        loaded_steps = []
        for step in data.get("steps", []):
            # 암호화된 비밀번호 복호화
            if step['action'] == 'input_password' and step['value'].startswith("ENC:"):
                try:
                    enc_val = step['value'].replace("ENC:", "")
                    decrypted_val = cipher.decrypt(enc_val.encode()).decode()
                    step['value'] = decrypted_val
                except Exception:
                    step['value'] = "" # 키가 안 맞으면 빈 값 처리
            loaded_steps.append(step)
            
        return data.get("url", ""), loaded_steps
    except Exception as e:
        print(f"Load Error: {e}")
        return None, []