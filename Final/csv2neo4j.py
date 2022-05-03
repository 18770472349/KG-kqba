import os

from py2neo import Graph, Node, Relationship


# 链接neo4j
print("Connect to database...")
if os.path.exists('config.py'):
    from config import Config
    graph = Graph(Config.url, user=Config.user, password=Config.password)
else:
    graph = Graph("http://localhost:7474")


# 清空数据库
print("Clean database...")
graph.delete_all()


# 导入节点 电影类型  == 注意类型转换
print('Load gener...')
cypher = """LOAD CSV WITH HEADERS  FROM "https://docs.google.com/spreadsheets/d/e/2PACX-1vTNIZ6v2-AbLrVIPa4lm6sy-oFmynIlq__YRinuZiCVO46cDFvWDLyDf4vMoJd_2CB_JGxFX6VMJ5l5/pub?gid=1996397084&single=true&output=csv" AS line
            MERGE (p:Genre{gid:toInteger(line.genre_id),name:line.genre_name})"""
graph.run(cypher)

# 导入节点 演员信息
print('Load person...')
cypher = """LOAD CSV WITH HEADERS FROM 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRQL2-i72yb96epYrw0cSEeuvTfDZ4hPLSmqcVNG9OXr5qhUiyoEKMJdUhtFKQcRve2dudTwIOv4Xen/pub?gid=1472103528&single=true&output=csv
' AS line
MERGE (p:Person { pid:toInteger(line.person_id)}) 
ON CREATE SET p.birth = line.person_birth_day, p.biography = line.person_biography
ON MATCH SET p.birth = line.person_birth_day, p.biography = line.person_biography
ON CREATE SET p.death = line.person_death_day,p.eng_name =line.person_english_name
ON MATCH SET p.death = line.person_death_day, p.eng_name =line.person_english_name
ON CREATE SET p.birthplace = line.birthplace, p.pname = line.person_name
ON MATCH SET p.birthplace = line.birthplace, p.pname = line.person_name
"""
graph.run(cypher)


# 导入节点 电影信息
print('Load movie...')
cypher = """LOAD CSV WITH HEADERS  FROM "https://docs.google.com/spreadsheets/d/e/2PACX-1vSWbeiZQoK5YsjwJYBL2fIgFS8VX9blVGMap9wWVb6kuMUIoRzN8psHH8fHexzXO-KxK3MDHbg8yMyN/pub?gid=1702166074&single=true&output=csv
" AS line    
MERGE (p:Movie{mid:toInteger(line.movie_id),title:line.movie_title})
ON CREATE SET p.introduction = line.movie_introduction, p.movie_releasedate = line.movie_releasedate, p.rating=toFloat(line.movie_rating)
ON MATCH SET p.introduction = line.movie_introduction, p.movie_releasedate = line.movie_releasedate, p.rating=toFloat(line.movie_rating)
"""
graph.run(cypher)

## 导入关系 actedin  电影是谁参演的 1对多
print('Load person_to_movie...')
print('Part1...')
cypher = """LOAD CSV WITH HEADERS FROM "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO9UHxmJ6r-Cv01Gp2NK5npo3M1-M4GN26CjCYP89uLtVxx0JRbePN-W7N4uyJ_sw938CrpR17nDpb/pub?gid=2041541949&single=true&output=csv
" AS line
match (from:Person{pid:toInteger(line.person_id)}),(to:Movie{mid:toInteger(line.movie_id)})
merge (from)-[r:actedin{pid:toInteger(line.person_id),mid:toInteger(line.movie_id)}]->(to)
"""
res = graph.run(cypher, timeout=60000)
print('Part2..')
cypher = """LOAD CSV WITH HEADERS FROM "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO9UHxmJ6r-Cv01Gp2NK5npo3M1-M4GN26CjCYP89uLtVxx0JRbePN-W7N4uyJ_sw938CrpR17nDpb/pub?gid=1718766297&single=true&output=csv
" AS line
match (from:Person{pid:toInteger(line.person_id)}),(to:Movie{mid:toInteger(line.movie_id)})
merge (from)-[r:actedin{pid:toInteger(line.person_id),mid:toInteger(line.movie_id)}]->(to)
"""
res = graph.run(cypher, timeout=60000)
print('Part3..')
cypher = """LOAD CSV WITH HEADERS FROM "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO9UHxmJ6r-Cv01Gp2NK5npo3M1-M4GN26CjCYP89uLtVxx0JRbePN-W7N4uyJ_sw938CrpR17nDpb/pub?gid=1802311097&single=true&output=csv
" AS line
match (from:Person{pid:toInteger(line.person_id)}),(to:Movie{mid:toInteger(line.movie_id)})
merge (from)-[r:actedin{pid:toInteger(line.person_id),mid:toInteger(line.movie_id)}]->(to)
"""
res = graph.run(cypher, timeout=60000)





# 导入关系  电影是什么类型 == 1对多
print('Load movie_to_gener...')
cypher = """LOAD CSV WITH HEADERS FROM "https://docs.google.com/spreadsheets/d/e/2PACX-1vQAk5ASF0GUEyVAKsHKVQ3DvoBb8nBTY19P0eE_MJm5tYMfbQBJGuLubb3jb2BkmXMTQRiWEHPzvkUY/pub?gid=1626965039&single=true&output=csv
" AS line  
match (from:Movie{mid:toInteger(line.movie_id)}),(to:Genre{gid:toInteger(line.genre_id)})    
merge (from)-[r:is{mid:toInteger(line.movie_id),gid:toInteger(line.genre_id)}]->(to)  
"""
graph.run(cypher)

print('Load finished!')


# 查询relationship的语句
cypher = "match (n)-[r]-(b) return n,r,b limit 10"
graph.run(cypher)

"""
-- 问：章子怡都演了哪些电影？  
match(n:Person)-[:actedin]->(m:Movie) where n.pname='章子怡' return m.title  
  
--  删除所有的节点及关系  
MATCH (n)-[r]-(b)  
DELETE n,r,b  
"""

pass
