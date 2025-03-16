from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()

try:
    driver.get('https://yz.chsi.com.cn/zsml/')

    # 1. 搜索专业
    print("🔍 正在搜索专业：软件工程")
    input_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='请输入专业名称']"))
    )
    input_box.send_keys("软件工程")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'ivu-btn-primary') and .//span[text()='查询']]"))
    ).click()

    # 2. 选择专业（默认第一个）
    results = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//div[@class='zy-item']"))
    )
    print("\n📑 找到以下专业：")
    for i, result in enumerate(results, 1):
        code = result.find_element(By.XPATH, ".//div[@class='zy-name']").text.split()[0]
        print(f"{i}. {code} 软件工程")
    choice = int(input("请选择专业："))
    print(f"👉 选择第 {choice} 个专业")
    results[choice - 1].find_element(By.XPATH, ".//a[contains(@class, 'zy-btn')]").click()

    # 3. 切换窗口并登录
    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[-1])
    input("⏳ 请手动登录后按回车继续...")

    # 4. 展开所有院校（带状态检查）
    print("\n🔄 展开所有院校（最多10所）：")
    schools = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@class='zy-item' and not(contains(@style, 'display: none'))]"))
    )
    for idx, school in enumerate(schools, 1):
        try:
            # 检查展开状态（通过图标class）
            icon = school.find_element(By.XPATH, './/a[@class="show-more"]/i').get_attribute("class")
            if "arrows-down" in icon:  # 未展开
                expand_btn = WebDriverWait(school, 5).until(
                    EC.element_to_be_clickable((By.XPATH, './/a[@class="show-more"]'))
                )
                driver.execute_script("arguments[0].click();", expand_btn)
                print(
                    f"✅ 展开 {idx}/{len(schools)}: {school.find_element(By.XPATH, './/div[@class=\"yx-name\"]').text}")
            else:
                print(f"ℹ️ 跳过 {idx}（已展开）: {school.find_element(By.XPATH, './/div[@class=\"yx-name\"]').text}")
        except Exception as e:
            print(f"⚠️ 展开失败 {idx}: {str(e)[:30]}")

    # 5. 核心提取逻辑（精准科目）
    print("\n📝 开始提取考试科目（格式：院校 > 院系 > 科目）：")
    for school in schools:
        try:
            school_name = WebDriverWait(school, 5).until(
                EC.visibility_of_element_located((By.XPATH, './/div[@class="yx-name"]'))
            ).text.strip()
            print(f"\n🏫 【{school_name}】")

            # 定位表格（带滚动）
            table = WebDriverWait(school, 10).until(
                EC.presence_of_element_located((By.XPATH, './/div[@class="ivu-table-body"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView();", table)
            rows = table.find_elements(By.XPATH, "./table/tbody/tr")

            for row in rows:
                try:
                    # 基础信息
                    department = row.find_element(By.XPATH, ".//td[1]").text.strip()
                    major = row.find_element(By.XPATH, ".//td[3]").text.strip()
                    direction = row.find_element(By.XPATH, ".//td[5]").text.strip()

                    # 处理科目显示（点击查看或默认展开）
                    try:
                        # 点击查看（部分院校需要）
                        view_btn = WebDriverWait(row, 3).until(
                            EC.element_to_be_clickable((By.XPATH, ".//a[contains(., '查看') and @href='javascript:;']"))
                        )
                        driver.execute_script("arguments[0].click();", view_btn)
                        kskm = WebDriverWait(row, 3).until(
                            EC.visibility_of_element_located((By.XPATH, './/div[@class="kskm-detail"]'))
                        )
                    except:
                        # 默认展开
                        kskm = WebDriverWait(row, 3).until(
                            EC.presence_of_element_located((By.XPATH, './/div[@class="kskm-detail"]'))
                        )

                    # 提取科目代码（忽略说明）
                    subjects = [
                        div.text.split('<span')[0].strip()  # 只取代码部分
                        for div in kskm.find_elements(By.XPATH, './div')
                        if any(keyword in div.text for keyword in ['政治', '外语', '业务课'])
                    ]
                    # 补全四科（处理缺失）
                    exam_subjects = subjects[:4] + ['未公布'] * (4 - len(subjects))

                    # 结构化输出
                    print(f"├─ 院系所：{department}")
                    print(f"├─ 专业：{major}")
                    print(f"├─ 研究方向：{direction}")
                    print("└─ 考试科目：")
                    for idx, subject in enumerate(exam_subjects, 1):
                        print(f"   ├─ {['政治', '外语', '业务课一', '业务课二'][idx - 1]}：{subject}")
                    print("─" * 60)

                except Exception as e:
                    print(f"⚠️ 行提取失败：{str(e)[:50]}")
                    continue

        except Exception as e:
            print(f"⚠️ 跳过院校 {school_name}：{str(e)[:50]}")
            continue

except Exception as e:
    print(f"\n❌ 致命错误：{str(e)}")
    driver.save_screenshot("error.png")
finally:
    driver.quit()
    input("按回车结束程序...")
