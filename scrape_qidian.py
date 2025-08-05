# 导入所需的库
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# --- 配置 ---
URL = "https://www.qidian.com/rank/signnewbook/chn21/"
TIMEOUT = 10
OUTPUT_FILE = "scraped_books.txt"

def scrape_book_names():
    """
    以无头模式启动浏览器，访问起点榜单，抓取书名，并保存到文件。
    """
    driver = None
    try:
        print("正在配置无头模式浏览器...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        print("正在初始化浏览器驱动...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"正在打开页面: {URL}")
        driver.get(URL)
        
        print("等待页面动态内容加载完成...")
        wait = WebDriverWait(driver, TIMEOUT)
        wait.until(EC.presence_of_element_located((By.ID, "rank-view-list")))
        print("内容加载成功！")
        
        book_title_elements = driver.find_elements(By.CSS_SELECTOR, "div.book-info h4 a")
        
        if not book_title_elements:
            print("错误：未能找到任何书名。网站的页面结构可能已经改变。")
            return

        print(f"正在将结果写入文件: {OUTPUT_FILE}")
        # 修正了这里的语法错误
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            f.write("--- 起点签约新书榜（玄幻分类）---\n")
            for index, element in enumerate(book_title_elements, 1):
                f.write(f"{index}. {element.text}\n")
        
        print(f"\n抓取完成！结果已保存到 {OUTPUT_FILE}")

    except Exception as e:
        print(f"在执行过程中发生了错误: {e}")
        
    finally:
        if driver:
            print("操作结束，正在关闭浏览器...")
            driver.quit()

if __name__ == "__main__":
    scrape_book_names()
