import requests
from bs4 import BeautifulSoup
import json
import time
import re # 导入正则表达式库

def scrape_douban_top250():
    """
    爬取豆瓣电影 Top 250 的数据，并进入详情页获取更详细的信息。
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8' # 明确请求中文内容
    }
    
    all_movies = []
    
    for start_num in range(0, 250, 25):
        list_url = f'https://movie.douban.com/top250?start={start_num}&filter='
        print(f"正在爬取列表页 (第 {start_num // 25 + 1} 页)...")
        
        try:
            response = requests.get(list_url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'lxml')
            movie_items = soup.find_all('div', class_='item')
            
            for item in movie_items:
                detail_url = item.find('div', class_='hd').find('a')['href']
                
                print(f"  -> 正在进入详情页...")
                try:
                    detail_response = requests.get(detail_url, headers=headers)
                    detail_response.raise_for_status()
                    detail_soup = BeautifulSoup(detail_response.text, 'lxml')

                    # --- 👇 全新的、更可靠的解析逻辑 ---
                    title = detail_soup.find('span', property='v:itemreviewed').get_text(strip=True)
                    cover_url = detail_soup.find('div', id='mainpic').find('img')['src']
                    
                    description_tag = detail_soup.find('span', property='v:summary')
                    description = description_tag.get_text(strip=True) if description_tag else "暂无简介"

                    info_div = detail_soup.find('div', id='info')
                    
                    # 提取上映日期
                    release_date_tag = info_div.find('span', string=re.compile(r'上映日期'))
                    release_date = release_date_tag.next_sibling.strip() if release_date_tag else "1900-01-01"
                    
                    # 提取片长
                    duration_tag = info_div.find('span', string=re.compile(r'片长'))
                    duration_text = duration_tag.next_sibling.strip() if duration_tag else "0"
                    duration_match = re.search(r'\d+', duration_text)
                    duration_mins = int(duration_match.group(0)) if duration_match else 0
                    # --- 👆 解析逻辑结束 ---

                    movie_data = {
                        "name": title,
                        "cover": cover_url,
                        "description": description,
                        "release_date": release_date.split('(')[0], # 清理地区信息
                        "duration_mins": duration_mins
                    }
                    all_movies.append(movie_data)
                    
                    time.sleep(1) 

                except requests.RequestException as e_detail:
                    print(f"    !! 爬取详情页失败: {e_detail}")
                except Exception as e_parse:
                    print(f"    !! 解析详情页失败: {e_parse}, URL: {detail_url}")

        except requests.RequestException as e_list:
            print(f"!! 爬取列表页失败: {e_list}")
            break
            
    final_data = {"movies": all_movies}
    
    try:
        with open('seed_data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        print(f"\n成功！共爬取 {len(all_movies)} 部电影的详细数据，已写入到 seed_data.json 文件。")
    except IOError as e_write:
        print(f"写入文件失败: {e_write}")

if __name__ == '__main__':
    scrape_douban_top250()
