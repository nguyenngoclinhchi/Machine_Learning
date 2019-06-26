import bs4
import future.backports.urllib.request
import pandas as pd
import pandas.io.common
import urllib


def save_xls(list_dfs, xls_path):
    with pd.ExcelWriter(xls_path) as writer:
        for n, dframe in enumerate(list_dfs):
            dframe.to_excel(writer, 'sheet%s' % n)
        writer.save()


def get_bs_obj(href):
    request = future.backports.urllib.request.Request(href, headers={'User-Agent': 'Mozilla/5.0'})
    web_page = pandas.io.common.urlopen(request)
    bs_obj = bs4.BeautifulSoup(web_page.read(), features="lxml")
    return bs_obj


def get_detail(category, course_list_link):
    try:
        bs_obj = get_bs_obj(course_list_link)
        articles = bs_obj.find_all('article', attrs={'class': 'dc-card dc-card--interactive dc-global-search-result'})
        for article in articles:
            item = article.find('div', attrs={'class': 'dc-global-search-result__content'})
            name = item.find('h4').text.strip()
            href = "https://www.datacamp.com" + article.find('a').attrs['href']
            print(name, href)
            if '/courses/' in href:
                if name not in course_list:
                    course_list.append(name)
                    get_course_detail(category, "Course", name, href)
            else:
                if name not in course_list:
                    course_list.append(name)
                    get_course_detail(category, "Project", name, href)
    except urllib.error.HTTPError as err:
        print(err.code)
        if err.code == 404:
            get_detail(category, course_list_link)
        else:
            pass


def get_course_detail(category, code, name_course, link_course):
    bs_obj = get_bs_obj(link_course)
    if '/courses/' in link_course:
        table = bs_obj.find('ul', attrs={'class': 'course__prerequisites'})
    else:
        table = None
    items = bs_obj.find('ul', attrs={'class': 'header-hero__stats'})
    if items is not None:
        info = [item.text.strip() for item in items.find_all('li')]
        detail_list = [i for i in info if i]
        detail = ", ".join(i for i in detail_list)
    else:
        detail = " "
    if table is not None:
        for course in table.find_all('li'):
            name = course.text.strip()
            href = "https://www.datacamp.com" + course.find('a').attrs['href']
            print('\t', name, href)
    else:
        name = " "
        href = " "
    data_list.append([category, code, name_course, detail, link_course, name, href])


data_list = list()
course_list = list()
link = "https://www.datacamp.com/search?utf8=%E2%9C%93&q=&tab=courses&facets%5Btechnology%5D%5B%5D=Python&facets%5Btopic%5D%5B%5D="
types = ['Programming', 'Importing+%26+Cleaning+Data', 'Data+Manipulation', 'Data+Visualization', 'Data+Visualization',
         'Data+Visualization', 'Probability+%26+Statistics', 'Machine+Learning', 'Applied+Finance', 'Case+Studies',
         'Other']
for ele in types:
    get_detail(ele.replace('+', ' ').replace('%26', 'and'), link + ele)

print('------------------------------------------- Data retrieval: Done --------------------------------------------')
raw = pd.DataFrame(data_list)
raw.to_excel('raw.xlsx')

df = pd.DataFrame(data_list,
                  columns=['Topic', 'Code', 'Course', 'Detail', 'Link', 'Prerequisite Course Name',
                           'Prerequisite Course Link'])
df = df[['Code', 'Topic', 'Course', 'Detail', 'Link', 'Prerequisite Course Name', 'Prerequisite Course Link']]
df = df.sort_values(['Code']).drop_duplicates()
df = df.reset_index(drop=True)
df.to_excel('Demo - Copy.xlsx', index=False)

df_sorted = pd.DataFrame(data_list,
                         columns=['Topic', 'Code', 'Course', 'Detail', 'Link', 'Prerequisite Course Name',
                                  'Prerequisite Course Link'])
df_sorted = df_sorted[
    ['Code', 'Topic', 'Course', 'Detail', 'Link', 'Prerequisite Course Name', 'Prerequisite Course Link']]
df_sorted = df_sorted.sort_values(['Code'])
df_sorted.reset_index(drop=True)
df_sorted.set_index(['Code', 'Topic', 'Course', 'Detail', 'Link', 'Prerequisite Course Name'], inplace=True)
df_sorted.drop_duplicates()
df_sorted.to_excel('Demo.xlsx', index=True)
