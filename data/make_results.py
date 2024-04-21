from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_results():
    names_lst = []

    search_xpath = ('/html/body/div[4]/div/div[1]/div[3]/div[1]/form/div[3]/fieldset'
                    '/section[1]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div/input')
    sch_btn_xpath = ('/html/body/div[4]/div/div[1]/div[3]/div[1]/form/div[3]/fieldset/'
                     'section[1]/div[2]/div[1]/div/div[1]')
    sch_1357_xpath = ('/html/body/div[4]/div/div[1]/div[3]/div[1]/form/div[3]/fieldset/section[1]'
                      '/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div[512]')
    pages_num_xpath = ('/html/body/div[4]/div/div[1]/div[3]/div[1]/form/div[3]/fieldset'
                       '/section[1]/div[3]/div[6]/div/div/ul/li[5]')
    next_page_selector = ('#step_1 > section.visual.visual_1 > div.esz-result-block > '
                          'div.esz-pagination-block > div > div > ul > li.next')

    check_xpath_first = ('/html/body/div[4]/div/div[1]/div[3]/div[1]/form/div[3]/'
                         'fieldset/section[1]/div[2]/div[4]/div/div')

    check_selector_second = ('body > div.popup.popup_messagebox.temp.modal-content > div > di'
                             'v.messagebox-body > div > form > div > div:nth-child(1) > div')

    check_selector_third = ('body > div.popup.popup_messagebox.temp.modal-content > div > '
                            'div.messagebox-body > div > div.esz-modal__footer.esz-pt_16 > '
                            'div.esz-modal__footer-item.js-modal-save > div')

    driver = webdriver.Chrome()

    url = 'https://www.mos.ru/pgu/ru/app/dogm/077060701/#step_1'
    driver.get(url)

    sch_btn = driver.find_element(By.XPATH, sch_btn_xpath)
    sch_btn.click()

    sch = driver.find_element(By.XPATH, search_xpath)
    sch.send_keys('ГБОУ Школа № 1357')
    time.sleep(3)

    sch_1357 = driver.find_element(By.XPATH, sch_1357_xpath)
    sch_1357.click()
    time.sleep(3)
    check_btn_first = driver.find_element(By.XPATH, check_xpath_first)
    check_btn_first.click()
    time.sleep(3)
    check_btn_second = driver.find_element(By.CSS_SELECTOR, check_selector_second)
    check_btn_second.click()
    time.sleep(3)
    check_btn_third = driver.find_element(By.CSS_SELECTOR, check_selector_third)
    check_btn_third.click()
    time.sleep(3)

    button = driver.find_element(By.ID, 'startSearchButton')
    button.click()

    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    driver.implicitly_wait(10)
    # pages_num = int(driver.find_element(By.XPATH, pages_num_xpath).text)
    for i in range(2):
        time.sleep(1)
        names = (driver.find_element(By.CLASS_NAME, 'esz-result-sections')
                 .find_elements(By.CLASS_NAME, 'esz-section-block'))
        for n, name in enumerate(names, 1):
            links_lst = []
            for link in name.find_elements(By.XPATH, './/a'):
                links_lst.append(link.get_attribute('href'))
            names_dict = {'topic': name.find_element(
                By.XPATH, f'//*[@id="step_1"]/section[1]/div[3]/div[5]/div/div[{n}]/div[1]').text,
                          'name_': name.find_element(
                              By.XPATH, f'//*[@id="step_1"]/section[1]/div[3]/div[5]/div/div[{n}]/h3[1]').text,
                          'age': name.find_element(
                              By.XPATH, f'//*[@id="step_1"]/section[1]/div[3]/div[5]/div/div[{n}]/div[2]/div/div[4]'
                          ).text,
                          'cost': name.find_element(
                              By.XPATH, f'//*[@id="step_1"]/section[1]/div[3]/div[5]/div/div[{n}]/h3[2]').text,
                          'link': links_lst[1]}
            names_lst.append(names_dict)
        if i != 1:
            next_page_btn = driver.find_element(By.CSS_SELECTOR, next_page_selector)
            next_page_btn.click()
    driver.close()
    driver.quit()
    return names_lst
