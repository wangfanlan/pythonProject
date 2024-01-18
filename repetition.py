import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# 定义两个文本
text1 = "im person."
text2 = "im dog person1."

# 将文本转换为词袋向量
vectorizer = CountVectorizer()
vector1 = vectorizer.fit_transform([text1]).toarray()
vector2 = vectorizer.transform([text2]).toarray()

# 计算两个向量的余弦相似度
similarity = cosine_similarity(vector1, vector2)
print(similarity)