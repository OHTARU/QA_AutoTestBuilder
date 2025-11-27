import re

class PageScanner:
    def determine_locator(self, el):
        """요소 분석 및 최적 식별자 반환 (소셜 로그인 버튼 최적화)"""
        el_id = el.get_attribute("id")
        el_text = el.text.strip()
        el_placeholder = el.get_attribute("placeholder")
        el_class = el.get_attribute("class")
        el_name = el.get_attribute("name")
        
        # [핵심] 링크(a)와 이미지(img)의 강력한 고유 속성 가져오기
        el_title = el.get_attribute("title")
        el_alt = el.get_attribute("alt")
        
        el_data_test = el.get_attribute("data-test") or el.get_attribute("data-testid") or el.get_attribute("data-qa")
        tag = el.tag_name

        # 0순위: Data-* 속성 (가장 강력함)
        if el_data_test:
            return "CSS", f"[data-test='{el_data_test}']", f"Data-Test: {el_data_test}"

        # 1순위: ID (동적인지 체크)
        if el_id and not self._is_dynamic_string(el_id):
            return "ID", el_id, f"ID: {el_id}"
        
        # [핵심] 2순위: Title 속성 (구글 버튼의 <a> 태그)
        if el_title:
            # CSS Selector: [title='값']
            return "CSS", f"[title='{el_title}']", f"Title: {el_title}"

        # [핵심] 3순위: Alt 속성 (구글 버튼의 <img> 태그)
        if el_alt:
            return "XPATH", f"//*[@alt='{el_alt}']", f"Alt: {el_alt}"

        # 4순위: Name
        if el_name:
            return "NAME", el_name, f"Name: {el_name}"
        
        # 5순위: Placeholder
        if el_placeholder:
            return "XPATH", f"//{tag}[@placeholder='{el_placeholder}']", f"Placeholder: {el_placeholder}"
        
        # [핵심] 6순위: Class (동적 클래스 필터링 적용)
        if el_class:
            classes = el_class.split()
            # 이상한 문자열(__, --, 긴 숫자)이 포함된 클래스는 제거
            valid_classes = [c for c in classes if not self._is_dynamic_class(c)]
            
            if valid_classes:
                css_selector = "." + ".".join(valid_classes)
                return "CSS", css_selector, f"Class: {css_selector}"
        
        # 7순위: Text (클래스가 없거나 이상하면 텍스트로 잡음)
        if el_text and len(el_text) < 50:
            # 작은따옴표 처리
            safe_text = el_text.replace("'", "")
            return "XPATH", f"//*[contains(text(), '{safe_text}')]", f"Text: {el_text}"
        
        # 8순위: 최후의 수단
        return "XPATH", f"//{tag}", f"Tag: {tag}"

    def _is_dynamic_class(self, class_name):
        """동적 클래스(난수) 판별: __, --, 혹은 긴 숫자 조합"""
        if "__" in class_name or "--" in class_name: return True
        if len(class_name) > 10 and any(char.isdigit() for char in class_name): return True
        return False

    def _is_dynamic_string(self, text):
        """ID가 동적인지 체크 (숫자 3개 이상 연속)"""
        return bool(re.search(r'\d{3,}', text))

    def create_step_data(self, element):
        l_type, l_value, l_name = self.determine_locator(element)
        tag = element.tag_name
        
        action = "click" 
        if tag == "input": action = "input"
        elif tag in ["iframe", "frame"]: action = "switch_frame"

        return {
            "name": f"[{tag}] {l_name}",
            "type": l_type,
            "locator": l_value,
            "action": action,
            "value": ""
        }

    def create_text_validation_step(self, text):
        safe_text = text.replace("'", "") 
        locator = f"//*[contains(text(), '{safe_text}')]"
        return {
            "name": f"[검증] {text[:15]}...",
            "type": "XPATH",
            "locator": locator,
            "action": "check_text",
            "value": text
        }

    def create_url_validation_step(self, url):
        return {
            "name": f"[URL 확인] {url[-30:]}...",
            "type": "Browser",
            "locator": "Current URL",
            "action": "check_url",
            "value": url
        }