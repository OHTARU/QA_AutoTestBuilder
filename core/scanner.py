class PageScanner:
    def determine_locator(self, el):
        """요소 속성을 분석하여 최적의 식별자 반환 (Data 속성 우선)"""
        el_id = el.get_attribute("id")
        el_text = el.text.strip()
        el_placeholder = el.get_attribute("placeholder")
        el_class = el.get_attribute("class")
        el_data_test = el.get_attribute("data-test") or el.get_attribute("data-testid") or el.get_attribute("data-qa")
        
        tag = el.tag_name

        # 0순위: Data-* 속성
        if el_data_test:
            return "CSS", f"[data-test='{el_data_test}']", f"Data-Test: {el_data_test}"

        # 1순위: ID
        if el_id:
            return "ID", el_id, f"ID: {el_id}"
        
        # 2순위: Placeholder
        if el_placeholder:
            return "XPATH", f"//{tag}[@placeholder='{el_placeholder}']", f"Placeholder: {el_placeholder}"
        
        # 3순위: Class (CSS Selector)
        if el_class:
            css_selector = "." + el_class.strip().replace(" ", ".")
            return "CSS", css_selector, f"Class: {el_class}"
        
        # 4순위: Text
        if el_text and len(el_text) < 30:
            return "XPATH", f"//{tag}[contains(text(), '{el_text}')]", f"Text: {el_text}"
        
        # 5순위: Tag
        return "XPATH", f"//{tag}", f"Tag: {tag}"

    def create_step_data(self, element):
        """일반 요소 스캔"""
        l_type, l_value, l_name = self.determine_locator(element)
        tag = element.tag_name
        
        action = "input" if tag == "input" else "click"

        return {
            "name": f"[{tag}] {l_name}",
            "type": l_type,
            "locator": l_value,
            "action": action,
            "value": ""
        }

    def create_text_validation_step(self, text):
        """[NEW] 드래그된 텍스트로 검증 스텝 생성"""
        # XPath에서 작은따옴표 문제 방지
        safe_text = text.replace("'", "") 
        
        # 텍스트가 포함된 요소를 찾는 범용 XPath
        locator = f"//*[contains(text(), '{safe_text}')]"
        
        return {
            "name": f"[검증] {text[:15]}...", # 이름은 적당히 잘라서 표시
            "type": "XPATH",
            "locator": locator,
            "action": "check_text", # 자동으로 검증 모드
            "value": text # 확인하고 싶은 값 자동 입력
        }