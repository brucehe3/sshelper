import time
import re
from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.common import exceptions

from app.models import UserCaseStep, UserCase, UserCaseResult
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

XPATH_PATTERN = re.compile("\(([\s\S]*?)\)\[([0-9]+)\]")


class Command(BaseCommand):
    help = '自动化测试脚本'

    def add_arguments(self, parser):
        # parser.add_argument('code', nargs='-', type=str)
        pass

    def handle(self, *args, **options):

        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # define headless

        self.driver = webdriver.Chrome(chrome_options=chrome_options)

        # 读取最新一条user_case_result处理
        results = UserCaseResult.objects.filter(status=0).order_by('created')
        for result in results:
            try:
                user_case = result.user_case
                # 统计匹配点数
                result.assert_num = UserCaseStep.objects.filter(
                    user_case=user_case,
                    step_type=UserCaseStep.STEP_TYPE_ASSERT).count()

                result.assert_success_num = self.run_test_case(user_case)
                result.status = 3
            except exceptions.WebDriverException as e:
                result.fail_reason = e.msg
                result.status = 2

            result.save()

        # code = options.get('code')[0]
        # self.run_test_case(code)

        self.driver.quit()

    def get_element(self, xpath):

        if xpath[:5] == 'xpath':
            results = re.findall(XPATH_PATTERN, xpath)
            if results:
                result = results[0]
                pos = int(result[1])
                # 下标减一
                pos -= 1
                # return self.driver.find_elements_by_xpath(result[0])[pos]

                elements = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, result[0]))
                )
                # print(elements,pos,len(elements))
                return elements[pos]

        elif xpath[:2] == 'id':
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, xpath[3:]))
            )
            # return self.driver.find_element_by_id(xpath[3:])
        else:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            # return self.driver.find_element_by_xpath(xpath)

    def run_test_case(self, user_case):
        #
        # try:
        #     user_case = UserCase.objects.get(code=code)
        # except UserCase.DoesNotExist:
        #     return False

        steps = user_case.steps.all()
        assert_success_num = 0

        for step in steps:

            self.stdout.write(self.style.SUCCESS('执行步骤：%s' % step.name))
            # self.stdout.write(self.style.SUCCESS('当前的url：%s' % self.driver.current_url))

            element = None
            if step.step_type == UserCaseStep.STEP_TYPE_OPEN:
                # 打开网页
                self.driver.get(step.xpath)
            else:
                element = self.get_element(step.xpath)

            if step.step_type == UserCaseStep.STEP_TYPE_CLICK:
                element.click()
            elif step.step_type == UserCaseStep.STEP_TYPE_INPUT:
                element.clear()
                element.send_keys(step.step_text)
            elif step.step_type == UserCaseStep.STEP_TYPE_ASSERT:

                result = WebDriverWait(self.driver, 10).until(
                    EC.text_to_be_present_in_element((By.XPATH, step.xpath), step.step_text)
                )
                if not result:
                    self.stdout.write(self.style.ERROR('匹配检测失败'))
                else:
                    assert_success_num += 1
                    self.stdout.write(self.style.SUCCESS('匹配检测成功'))

            if step.pause_seconds:
                self.stdout.write(self.style.SUCCESS('暂停 %s 秒' % step.pause_seconds))
                time.sleep(step.pause_seconds)

        return assert_success_num