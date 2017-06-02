#coding:utf-8
from collections import OrderedDict
from operator import itemgetter

critics={'Lisa Rose':{'Lady in the Water':2.5,'Snakes on a Plane':3.5,'Just My Luck':3.0,'Superman Returns':3.5,'You,Me and Dupree':2.5,'The Night Listener':3.0},
         'Gene Seymour':{'Lady in the Water':3.0,'Snakes on a Plane':3.5,'Just My Luck':1.5,'Superman Returns':5.0,'You,Me and Dupree':3.5,'The Night Listener':3.0},
         'Michael Phillips':{'Lady in the Water':2.5,'Snakes on a Plane':3.0,'Superman Returns':3.5,'The Night Listener':4.0},
         'Claudia Puig':{'Snakes on a Plane':3.5,'Just My Luck':3.0,'Superman Returns':4.0,'You,Me and Dupree':2.5,'The Night Listener':4.5},
         'Mick LaSalle':{'Lady in the Water':3.0,'Snakes on a Plane':4.0,'Just My Luck':2.0,'Superman Returns':3.0,'You,Me and Dupree':2.0,'The Night Listener':3.0},
         'Jack Mattews':{'Lady in the Water':3.0,'Snakes on a Plane':4.0,'Superman Returns':5.0,'You,Me and Dupree':3.5,'The Night Listener':3.0},
         'Toby':{'Snakes on a Plane':4.5,'You ,Me and Dupree':1.0,'Superman Returns':4.0}}

from math import *

#返回一个有关person1与person2的基于距离的相似度评价
def sim_distance(prefs,person1,person2):
    #得到shared_items的列表
    si={}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item]=1

            #如果两者没哟共同之处，则返回0
    if len(si)==0:
        return 0
    #计算所有差值的平方和
    sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2) for item in prefs[person1] if item in prefs[person2]])

    return 1/(1+sqrt(sum_of_squares))

# print ('sim_distance=',sim_distance(critics,'Lisa Rose','Gene Seymour'))

#返回p1和p2的皮尔逊相关系数
def sim_pearson(prefs,p1,p2):
    #得到双方都曾评价过的物品列表
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item]=1

    #得到列表元素的个数
    n=len(si)
    #如果两者没有共同之处
    if n==0:
        return 1
    #对所有偏好求和
    sum1=sum([prefs[p1][it] for it in si])
    sum2=sum([prefs[p2][it] for it in si])

    #求平方和
    sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq=sum([pow(prefs[p2][it],2) for it in si])
    #求成绩之和
    pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

    #计算皮尔逊评价值
    num=pSum-(sum1*sum2/n)
    den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
    if den==0:
        return 0

    r=num/den

    return r

# print ('sim_pearson=',sim_pearson(critics,'Lisa Rose','Gene Seymour'))

#从反映偏好的字典中返回最为匹配者
def topMatches(prefs,person,n=5,similarity=sim_pearson):
    scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]

    #对列表进行排序，评价值最高者排在最前面
    scores.sort()
    scores.reverse()
    return scores[0:n]

# print topMatches(critics,'Lisa Rose',3,similarity=sim_pearson)
#利用所有他人评价值的加权平均，为某人提供建议
def getRecommendations(prefs,person,similarity=sim_pearson):
    totals={}
    simSums={}
    for other in prefs:
        #不要和自己做比较
        if other==person:
            continue

        sim=similarity(prefs,person,other)

        #忽略评价值为零或小于零的情况
        if sim<=0:
            continue

        for item in prefs[other]:
            #只对自己还未看过的影片进行评价
            if item not in prefs[person] or prefs[person][item]==0:
                #相似度*评价值
                totals.setdefault(item,0)
                totals[item]+=prefs[other][item]*sim
                #相似度之和
                simSums.setdefault(item,0)
                simSums[item]+=sim

        #建立一个归一化的列表
    rankings=[(total/simSums[item],item) for item,total in totals.items()]

        #返回经过排序的列表
    rankings.sort()
    rankings.reverse()
    return rankings

# print getRecommendations(critics,'Toby')

# print ('getRecommendations=',getRecommendations(critics,'Toby',similarity=sim_distance))

def transformPrefs(prefs):
    result={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})

            result[item][person]=prefs[person][item]
    return result

movies=transformPrefs(critics)

U = ['c', 'd', 'e', 'g']
A = ['a', 'b', 'd','e']
B = ['a', 'c', 'f']
C = ['b', 'c', 'g']
D = ['c', 'd', 'e']
E = ['h']
F = []
data = {'U':U,'A': A, 'B': B,'C':C, 'D': D, 'E': E,'F':F}
# print len(set(A)&set(E))
# print len(data['A'])
# print type(data['A'])
def getSimilarity(person1,person2):
    sim=len(set(person1)&set(person2))
    return sim/sqrt(len(person1)*len(person2))

# print getSimilarity(A,B)

# data = {'U':U,'A': A, 'B': B, 'C': C, 'D': D, 'E': E}
# print data['U']


# #将数据集data转换成物品-用户
def transtData(data):
    result = {}
    for u, items in data.items():
        for i in items:
            if i not in result:
                result[i] = []
            result[i].append(u)
    return result
# print transtData(data)


#基于用户的协同过滤，用户相似度根据改进余弦相似度计算(测试)
def userSimilarityTest_test(data,u):#u是一个用户
    max=0
    who=''
    if data[u]==[]:#如果是新用户，什么书都没与收藏
        who=''

    # 将用户-物品列表转换成物品-用户列表
    # item_user = {}
    # for user, item in data.items():
    #     for i in item:
    #         if i not in item_user:
    #             item_user[i] = []
    #         item_user[i].append(user)
    item_user = transtData(data)
    # common_user = []
    # for i in data[u]:
    #     for v in item_user[i]:
    #         if v == u:
    #             continue
    #         if v not in common_user:
    #             common_user.append(v)
    # print common_user

    for k,v in data.items():
        if k == u:
            continue
        if set(v).issubset(data[u]):#排除物品列表被包含在用户u的用户
            continue
        intersection=set(data[u])&set(v)#计算物品的交集
        if len(intersection) == 0:
            continue
        itemOfIntersectionSim = 0
        for i in intersection:
            itemOfIntersectionSim += 1/log(1+len(item_user[i]))
        sim = itemOfIntersectionSim/sqrt(len(data[u])*len(v))
        print k,sim

        if sim>max:
            max = sim
            who = k
    # if who == '':
    #     R = []
    # else:
    #     C = set(data[who]) & set(data[u])
    #     for item in data[who]:
    #         if item in C:
    #             continue
    #         R.append(item)

    return who
# print ('E',userSimilarityTest1(data,'E'))

#基于用户的协同过滤，用户相似度根据改进余弦相似度计算
def userSimilarity(data,u):#u是一个用户
    max=0
    who=''
    if data[u]==[]:#如果是新用户，什么书都没与收藏
        who=''
    # 将用户-物品列表转换成物品-用户列表
    # item_user = {}
    # for user, item in data.items():
    #     for i in item:
    #         if i not in item_user:
    #             item_user[i] = []
    #         item_user[i].append(user)
    item_user = transtData(data)
    common_user = []  #common_user记录和目标用户有交集的用户列表
    for i in data[u]:
        for v in item_user[i]:
            if v == u:
                continue
            if v not in common_user:
                common_user.append(v)
    if common_user ==[]:
        who = ''
    for v in common_user:
        if set(data[v]).issubset(data[u]):#排除物品列表被包含在用户u的用户
            continue
        intersection = set(data[u]) & set(data[v])  # 计算物品的交集
        #itemOfIntersectionSim为公式分子部分
        itemOfIntersectionSim = 0
        for i in intersection:
            itemOfIntersectionSim += 1/log(1+len(item_user[i]))
        sim = itemOfIntersectionSim/sqrt(len(data[u])*len(data[v]))
        print v,sim

        if sim>max:
            max = sim
            who = v

    return who
# print ('E',userSimilarityTest(data,'E'))
# print userSimilarityTest('U',data)
# def getSimilaritytest(u, data):  # u为一个用户感兴趣的物品集  data（字典）为其他所有用户的数据集: {'用户ID':[用户感兴趣的物品列表]}
# 	sim_dct = {}
# 	for k, v in data.items():
# 		set_v = set(v)
# 		set_u = set(u)
# 		if u == v or set_v.issubset(set_u):
# 			continue  # 两个物品列表一样的过滤， 物品v集合属于物品u集合的过滤　
#
# 		intersection = len(set_v & set_u)
# 		if not intersection:
# 			continue  # u 与 v 没有交集的过滤
#
# 		sim = intersection/sqrt(len(u)*len(v))
# 		sim_dct[k] = sim
# 	return OrderedDict(sorted(sim_dct.items(), key=lambda x: x[1])[::-1])
# 	# return OrderedDict(sorted(sim_dct.items(), key=lambda x: x[1][:n])[::-1]) top n （获取前n个）
#
# for k, v in getSimilarity(U, data).items():
# 	print k, v

def recommendationByUserSimilarityToUser(data,person):
    R=[]
    u=userSimilarity(data,person)
    print u,"is best similarity to",person
    if u=='':#如果没有相似的用户
       R=[]
    elif data[person]==[]:#新用户问题
        R=[]
    else:
        C=set(data[u])&set(data[person])
        for item in data[u]:
            if item in C:
                continue
            R.append(item)
    return R
# print getRecommendationUser(data,'U')


#基于物品的推荐算法，计算物品间的相似度，用改进的余弦相似度,用在图书详情页的相关推荐
def itemSimilarity(data,item):
    # #将数据集data转换成物品-用户
    # item_user={}
    # similary_list={}
    # for u,items in data.items():
    #     for i in items:
    #         if i not in item_user:
    #             item_user[i]=[]
    #         item_user[i].append(u)
    # return item_user
    # #将数据集data转换成物品-用户
    item_user=transtData(data)
    similary_list = {}
    #物品之间的相似度进行计算
    print item
    for i,user in item_user.items():
        if i==item:
            continue
            #common为测试物品与其他物品的用户列表的交集
        common=set(user)&set(item_user[item])
        if len(common)==0:
            continue
        userOfCommonSim=0
        for u in common:
            userOfCommonSim+=1/log(1+len(data[u]))
        itemSim=userOfCommonSim/sqrt(len(user)*len(item_user[item]))
        print i,itemSim
        similary_list.setdefault(i,itemSim)
    # print similary_list
    rank=sorted(similary_list.items(),key=lambda d:d[1])
    #r为一个从相似度高低排序的物品列表
    r=[]
    for i in range(len(rank)):
        r.append(rank[i][0])
    r.reverse()
    print r
    return r


#基于物品的推荐算法，计算物品间的相似度，用改进的余弦相似度,实现用户的个性化推荐
def recommendationByItemSimilarityToUser(data,person):
    r = [] #推荐列表
    item_user=transtData(data)#将数据集data转换成物品-用户
    item_user_new = item_user.copy()
    # print item_user
    # print data[person]
    if len(data[person]) == 0:#新用户问题
        r = []
    else:
        for k in data[person]:  #将物品-用户字典中包含在目标用户的物品间键去除
            item_user_new.pop(k)
    # print item_user_new
    # print item_user
    similary_list = {}
    #物品之间的相似度进行计算
    for k in data[person]:
        print k
        for i,user in item_user_new.items():
            # if i == k:
            #     continue
            common=set(user)&set(item_user[k])#common为测试物品与其他物品的用户列表的交集
            if len(common)==0:
                continue
            userOfCommonSim=0
            for u in common:
                userOfCommonSim+=1/log(1+len(data[u]))
            itemSim = userOfCommonSim/sqrt(len(user)*len(item_user[k]))
            print i,itemSim
            if i not in similary_list:
                similary_list.setdefault(i,itemSim)
            else:
                similary_list[i] = similary_list[i] + itemSim
        print ('\n')
    print similary_list
    rank=sorted(similary_list.items(),key=lambda d:d[1])

    for i in range(len(rank)):
        r.append(rank[i][0])
    r.reverse()
    return r

# print ('itemSimilarity(data,\'b\')',itemSimilarityToUser(data,'B'))
# print ('itemSimilarity(data,\'c\')',itemSimilarity(data,'c'))
# print ('itemSimilarity(data,\'g\')',itemSimilarity(data,'g'))

