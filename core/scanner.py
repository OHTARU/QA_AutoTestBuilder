class PageScanner:
    def determine_locator(self, el):
        el_id = el.get_attribute("id")
        el_text = el.text.strip()
        el_placeholder = el.get_attribute("placeholder")
        el_class = el.get_attribute("class")
        el_name = el.get_attribute("name")
        
        # 링크/이미지 버튼용 속성
        el_title = el.get_attribute("title")
        el_alt = el.get_attribute("alt")

        el_data_test = el.get_attribute("data-test") or el.get_attribute("data-testid") or el.get_attribute("data-qa")
        tag = el.tag_name

        if el_data_test: return "CSS", f"[data-test='{el_data_test}']", f"Data-Test: {el_data_test}"
        if el_id: return "ID", el_id, f"ID: {el_id}"
        if el_name: return "NAME", el_name, f"Name: {el_name}"
        if el_title: return "CSS", f"{tag}[title='{el_title}']", f"Title: {el_title}"
        if el_alt: return "XPATH", f"//*[@alt='{el_alt}']", f"Alt: {el_alt}"
        if el_placeholder: return "XPATH", f"//{tag}[@placeholder='{el_placeholder}']", f"Placeholder: {el_placeholder}"
        if el_class:
            css_selector = "." + el_class.strip().replace(" ", ".")
            return "CSS", css_selector, f"Class: {el_class}"
        if el_text and len(el_text) < 30:
            return "XPATH", f"//{tag}[contains(text(), '{el_text}')]", f"Text: {el_text}"
        
        return "XPATH", f"//{tag}", f"Tag: {tag}"

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
        """URL 검증 스텝 생성"""
        return {
            "name": f"[URL 확인] {url[-30:]}...",
            "type": "Browser",
            "locator": "Current URL",
            "action": "check_url",
            "value": url
        }