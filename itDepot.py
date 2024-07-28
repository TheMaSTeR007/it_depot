import json, requests, os, gzip, hashlib
from lxml import html


def req_sender(url: str, method: str):
    _response = requests.request(method=method, url=url)
    if _response.status_code != 200:
        print(f"HTTP Status code: {_response.status_code}")
    else:
        # Request Successful
        return _response


def page_checker(url: str, method: str, path: str) -> str:
    page_hash = hashlib.sha256(url.encode()).hexdigest()
    if os.path.exists(f"{path}/{page_hash}.html.gz"):
        # Page exists
        print("Page exists, reading page...")
        with gzip.open(f"{path}/{page_hash}.html.gz", 'rb') as decompressed_file:
            html_text = decompressed_file.read().decode(errors='backslashreplace')
        # Returning string type text
        return html_text
    else:
        print("Page does not exist, Sending Request...")  # Page does not exist
        _response = req_sender(url=url, method=method)  # Sending HTTP Request
        page_hash = hashlib.sha256(url.encode()).hexdigest()
        print(f'File name is : {page_hash}')

        with gzip.open(f"{path}/{page_hash}.html.gz", 'wb') as file:
            file.write(_response.content)
            print("Page Saved")
        return _response.text


def scraper_func(url: str, method: str, path_to_save_page: str):
    html_response_text = page_checker(url=url, method=method, path=path_to_save_page)  # Getting the html text

    parsed_html = html.fromstring(html=html_response_text)  # Creating a parsed html file for applying Xpath
    xpath_category_link = "//a[@class = 'text-dark']/@href"
    category_link_list = [ url + half_link for half_link in parsed_html.xpath(xpath_category_link)]
    # print(category_results)

    xpath_category_name = "//a[@class = 'text-dark']/text()"  # Getting name of category
    category_name_list = [category_name for category_name in parsed_html.xpath(xpath_category_name)]
    # print(category_name_list)

    final_output = []
    for each_category_link in category_link_list:
        each_category_data = page_checker(url=each_category_link, method=method, 
                                          path="C:/Users/jaimin.gurjar/PycharmProjects/pythonProject/26Jun24/it_depot/it_depot_category_pages")
        xpath_page_count = '//li[last()-2]/a[ contains(@class, "category_page_class") ]/text()'
        parsed_category_page = html.fromstring(each_category_data)
        category_page_count = parsed_category_page.xpath(xpath_page_count)
        xpath_current_category_name = "//h4[@class='font-weight-bold pl-md-2 text-md-left text-center']/text()"
        current_category_name = parsed_category_page.xpath(xpath_current_category_name)[0]
        if len(category_page_count) > 0:
            print(f"Page count: {int(category_page_count[0])} on url: {each_category_link}")
            category_dict = {
                "category_name": current_category_name,
                "category_url": each_category_link,
                "total_page_count": int(category_page_count[0])
            }
        else:
            print(f"Page cout: {1} on url: {each_category_link}")
            category_dict = {
                "category_name": current_category_name,
                "category_url": each_category_link,
                "total_page_count": 1
            }
        # print(category_page_count)
        final_output.append(category_dict)

    # to Save in .txt format
    with open("FINAL_Output.txt", 'w') as final_file:
        final_file.write(str(final_output))
    # to Save in .Json format
    with open("FINAL_Output.json", 'w') as final_file:
        final_file.write(json.dumps(final_output))

    print(final_output)


my_url = "https://www.theitdepot.com/"
my_method = "GET"
my_path = "C:/Users/jaimin.gurjar/PycharmProjects/pythonProject/26Jun24/it_depot"

scraper_func(url=my_url, method=my_method, path_to_save_page=my_path)
