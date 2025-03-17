import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
def search_engine(keyword, site_url):
    """
    简单搜索引擎函数
    :param keyword: 搜索关键词
    :param site_url: 要搜索的网站URL
    :return: 搜索结果列表
    """
    # 处理关键词中的中文字符，避免URL编码问题
    encoded_keyword = quote(keyword)
    # 构造搜索URL，这里以百度为例
    search_url = f"{site_url}/search?q=={encoded_keyword}"
    
    try:
        # 发送HTTP请求获取网页内容
        response = urllib.request.urlopen(search_url)
        html_content = response.read().decode('utf-8')
        
        # 使用BeautifulSoup解析网页内容
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 查找搜索结果
        results = []
        for item in soup.find_all('div', class_='result'):
            title = item.find('h3').get_text()
            link = item.find('a')['href']
            results.append({'title': title, 'link': link})
        
        return results
    
    except Exception as e:
        print(f"搜索过程中出现错误: {e}")
        return []

if __name__ == "__main__":
    keyword = input("请输入搜索关键词: ")
    site_url = "http://www.bing.com"  # 这里以百度为例
    search_results = search_engine(keyword, site_url)
    
    if search_results:
        print("搜索结果如下：")
        for idx, result in enumerate(search_results, 1):
            print(f"{idx}. 标题: {result['title']}\n   链接: {result['link']}\n")
    else:
        print("未找到相关搜索结果。")


