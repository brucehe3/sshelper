import re
import time
from selenium import webdriver
from selenium.common import exceptions
from app.models import UserCaseStep, UserCaseResult
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

XPATH_PATTERN = re.compile("\(([\s\S]*?)\)\[([0-9]+)\]")


def get_element(driver, xpath):
    if xpath[:5] == 'xpath':
        results = re.findall(XPATH_PATTERN, xpath)
        if results:
            result = results[0]
            pos = int(result[1])
            # 下标减一
            pos -= 1
            elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, result[0]))
            )
            return elements[pos]

    elif xpath[:2] == 'id':

        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, xpath[3:]))
        )

    else:
        return WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )


def run_test_case_steps(driver, user_case):
    steps = user_case.steps.all()
    assert_success_num = 0

    for step in steps:
        element = None
        if step.step_type == UserCaseStep.STEP_TYPE_OPEN:
            # 打开网页
            driver.get(step.xpath)
        else:
            element = get_element(driver, step.xpath)

        if step.step_type == UserCaseStep.STEP_TYPE_CLICK:
            element.click()
        elif step.step_type == UserCaseStep.STEP_TYPE_INPUT:
            element.clear()
            element.send_keys(step.step_text)
        elif step.step_type == UserCaseStep.STEP_TYPE_ASSERT:

            result = WebDriverWait(driver, 10).until(
                EC.text_to_be_present_in_element((By.XPATH, step.xpath), step.step_text)
            )
            if not result:
                pass
            else:
                assert_success_num += 1

        if step.pause_seconds:
            time.sleep(step.pause_seconds)

    return assert_success_num


def running_test_case(result_id):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # define headless

    driver = webdriver.Chrome(chrome_options=chrome_options)

    result = UserCaseResult.objects.get(pk=result_id)
    try:
        result.status = 1
        result.save()

        user_case = result.user_case
        # 统计匹配点数
        result.assert_num = UserCaseStep.objects.filter(
            user_case=user_case,
            step_type=UserCaseStep.STEP_TYPE_ASSERT).count()

        result.assert_success_num = run_test_case_steps(driver, user_case)
        result.status = 3

        result.save()

    except exceptions.WebDriverException as e:
        result.fail_reason = e.msg
        result.status = 2

        result.save()

    # code = options.get('code')[0]
    # self.run_test_case(code)

    driver.quit()
