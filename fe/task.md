在fe文件夹下使用streamlit完成如下的任务：
1. 读取data/xhs/json/search_contents_2025-03-19.json中的list，叫做contents_list，
2. 读取data/xhs/json/search_comments_2025-03-19.json中的list，叫做comments_list,
3. 用列表的形式展示contents_list中不同element的"note_id", "title", "desc", "liked_count", "comments_aggregate"字段
4. 其中"comments_aggregate"的获取方法如下：对于contents_list中元素的"note_id": example_note_id, 在comments_list中找到所有element的"note_id"为example_note_id的元素，把"content"聚合起来作为一个列表赋值给"comments_aggregate"