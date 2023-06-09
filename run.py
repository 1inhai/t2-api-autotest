#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pytest
import click
import traceback

from utils.commons.mail_control import MailSender
from utils import logger
from utils.case_process.create_case_control import TestCaseAutoCreate


@click.command()
@click.option('--mark', '-m', default='', help='传入被标记的case套件, 例: -m login')
def run(mark):
    logger.info("""

               开始执行项目...
               """)
    TestCaseAutoCreate.create_case()  # 自动生成用例，可注释
    try:
        pytest.main(['test_cases', f'-m={mark}', '--clean-alluredir', '--alluredir=allure-results'])
        os.system("allure generate -c -o allure-report")
    except Exception:
        err = traceback.format_exc()
        MailSender().send_email(
            subject='接口自动化错误报告',
            body=err
        )
        logger.error(f'程序运行异常，已发送错误邮件')
        raise


if __name__ == '__main__':
    run()
