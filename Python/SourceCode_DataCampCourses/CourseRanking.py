import pandas as pd


# PARENT = CHILD + 1
def set_parent(child_index):
    return child_index + 1


# CHILD = PARENT - 1
def set_child(parent_index):
    return parent_index - 1


def get_prerequisite(start_node, path_list):
    start_node = str(start_node)
    path_list = path_list + [start_node] if start_node not in path_list else path_list
    if start_node is '':
        return path_list
    if start_node not in graph.keys():
        graph[start_node] = ''
        df.append({start_node: ['', '', 1]}, ignore_index=True)
        get_prerequisite(start_node, path_list)
    for item in graph[start_node]:
        path_list = get_prerequisite(item, path_list)
    return path_list


raw = pd.read_excel('Demo - Copy.xlsx').drop_duplicates()
raw.sort_values('Code')
df = raw[raw['Code'] == 'Course']
df = df[['Course', 'Prerequisite Course Name']]
raw = raw.drop_duplicates()
course_detail = raw[['Topic', 'Code', 'Course', 'Detail', 'Link']].drop_duplicates()
prerequisite = raw[['Prerequisite Course Name', 'Prerequisite Course Link']].drop_duplicates()
prerequisite.columns = ['Path', 'Path Link']
df['Checked'] = 0
df.drop_duplicates()
idx = pd.IndexSlice
path = []
graph = dict()

for name in df['Course'].unique():
    graph[name] = df[df['Course'] == name]['Prerequisite Course Name'].tolist()
keys = graph.keys()
key_list = list()
path_key_list = list()
for key in df['Course'].unique():
    if key not in path:
        path = []
        path = get_prerequisite(key, path)
        print(key, path.__len__())
        for ele in path:
            if (ele != 'nan') or path.__len__() == 2:
                if ele == 'nan':
                    ele = ''
                if ele != key:
                    key_list.append(key)
                    path_key_list.append(ele)
course_detail.to_excel('Course_detail.xlsx', index=False)
for i in path_key_list:
    if i not in key_list:
        if i != 'nan' and i != '':
            print(i)
            key_list.append(i)
            path_key_list.append('')
result = zip(key_list, path_key_list)
result = pd.DataFrame(result, columns=['Course', 'Path']).drop_duplicates()
result.to_excel("Result.xlsx", index=False)

merged = pd.merge(course_detail, result, how='outer', on='Course')
merged = pd.merge(merged, prerequisite, how='outer', on='Path')
merged = merged.drop_duplicates()
merged = merged.sort_values(['Topic', 'Course']).drop_duplicates()
merged = merged.reset_index(drop=True)
for course in merged[merged['Topic'] == 'Machine Learning']['Path']:
    merged[merged['Path'] == course]['Path Topic'] = merged[merged['Course'] == course]['Topic']
merged.to_excel("Merged.xlsx", index=False)

temp = merged
course_pivot = temp[['Topic', 'Path']].pivot_table(columns=['Path'], aggfunc='count')
df_count = pd.DataFrame(course_pivot.unstack())
df_count.columns = ['Topic']
df_count = df_count.sort_values('Topic', ascending=False).unstack()
df_count['Topic'].to_excel('count.xlsx')