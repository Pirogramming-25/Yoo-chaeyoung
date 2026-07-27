import re

def parse_nutrition_info(text_list):
    if not text_list:
        return {'calories': None, 'carbs': None, 'protein': None, 'fat': None}

    full_text = " ".join(text_list)
    print("=== [OCR 추출 텍스트] ===")
    print(full_text)
    print("=========================")

    nutrition_data = {
        'calories': None,
        'carbs': None,
        'protein': None,
        'fat': None
    }

    try:
        cal_match = re.search(r'(?:열량|칼로리)?\s*(\d+(?:\.\d+)?)\s*(?:kcal|cal)', full_text, re.IGNORECASE)
        if cal_match:
            nutrition_data['calories'] = float(cal_match.group(1))

        def extract_val(keywords, text):
            for kw in keywords:
                pattern = rf'{kw}\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*(g|mg)?'
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    val = float(match.group(1))
                    unit = match.group(2).lower() if match.group(2) else 'g'
                    if unit == 'mg':
                        val = val / 1000.0
                    return round(val, 2)
            return None

        nutrition_data['carbs'] = extract_val(['탄수화물', '탄수'], full_text)
        nutrition_data['protein'] = extract_val(['단백질', '단백'], full_text)
        nutrition_data['fat'] = extract_val(['지방', '지방질'], full_text)

    except Exception as e:
        print(f"❌ 규칙 기반 파싱 중 에러 발생: {e}")

    return nutrition_data