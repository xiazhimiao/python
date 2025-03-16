from selenium import webdriver

# 创建 Chrome 浏览器实例，无需指定驱动路径
driver = webdriver.Chrome()

try:
    # 打开百度首页
    driver.get('https://www.baidu.com')

    # 打印页面标题
    print(driver.title)

    # 可以在这里添加更多的操作，让程序保持运行
    input("按回车键退出程序并关闭浏览器...")

except Exception as e:
    print(f"程序运行出现错误: {e}")