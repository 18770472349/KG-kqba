import re
import sys
import os
import jieba.posseg

from question_classification import Question_classify
from question_template import QuestionTemplate

# # 将自定义字典写入文件
# result = []
# with(open("./data/userdict.txt","r",encoding="utf-8")) as fr:
#     vocablist=fr.readlines()
#     for one in vocablist:
#         if str(one).strip()!="":
#             temp=str(one).strip()+" "+str(15)+" nr"+"\n"
#             result.append(temp)
# with(open("./data/userdict2.txt","w",encoding="utf-8")) as fw:
#     for one in result:
#         fw.write(one)


class Question:
    def __init__(self):
        # # 读取词汇表
        # with(open("./data/vocabulary.txt","r",encoding="utf-8")) as fr:
        #     vocab_list=fr.readlines()
        # vocab_dict={}
        # vocablist=[]
        # for one in vocab_list:
        #     word_id,word=str(one).strip().split(":")
        #     vocab_dict[str(word).strip()]=int(word_id)
        #     vocablist.append(str(word).strip())
        # # print(vocab_dict)
        # self.vocab=vocab_dict

        # 训练分类器
        self.classify_model = Question_classify()

        # 读取问题模板
        self.question_mode_dict = {}
        with open("./data/question_classification.txt", "r", encoding="utf-8") as f:
            for mode in f.readlines():
                mode_id, mode_str = str(mode).strip().split(":")
                self.question_mode_dict[int(mode_id)] = str(mode_str).strip()

        # 创建问题模板对象
        self.questiontemplate = QuestionTemplate()

    def question_process(self, question):
        # 接收问题
        question_raw = str(question).strip()
        # 对问题进行词性标注
        quesiton_pos = self._question_posseg(question_raw)
        # 得到问题的模板
        question_template = self._get_question_template()
        # 查询图数据库,得到答案
        answer = self._query_template(quesiton_pos, question_template)
        return answer

    def _question_posseg(self, raw_question):
        jieba.load_userdict("./data/userdict.txt")
        clean_question = re.sub("[\s+\.\!\/_,$%^*(+\"')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+", "", raw_question,)
        self.clean_question = clean_question
        question_seged = jieba.posseg.cut(str(clean_question))
        result = []
        question_word, question_flag = [], []
        for w in question_seged:
            temp_word = f"{w.word}/{w.flag}"
            result.append(temp_word)
            # 预处理问题
            word, flag = w.word, w.flag
            question_word.append(str(word).strip())
            question_flag.append(str(flag).strip())
        assert len(question_flag) == len(question_word)
        self.question_word = question_word
        self.question_flag = question_flag
        print(result)
        return result

    def _get_question_template(self):
        # 抽象问题
        for item in ["nr", "nm", "ng"]:
            while item in self.question_flag:
                ix = self.question_flag.index(item)
                self.question_word[ix] = item
                self.question_flag[ix] = item + "ed"
        # 将问题转化字符串
        str_question = "".join(self.question_word)
        print("抽象问题为：", str_question)
        # 通过分类器获取问题模板编号
        question_template_num = self.classify_model.predict(str_question)
        print("使用模板编号：", question_template_num)
        question_template = self.question_mode_dict[question_template_num]
        print("问题模板：", question_template)
        question_template_id_str = str(question_template_num) + "\t" + question_template
        return question_template_id_str

    # 根据问题模板的具体类容，构造cql语句，并查询
    def _query_template(self, quesiton_pos, question_template):
        # 调用问题模板类中的获取答案的方法
        try:
            answer = self.questiontemplate.answer(quesiton_pos, question_template)
        except:
            answer = "你问的问题我也还不知道！"
        # answer = self.questiontemplate.answer(quesiton_pos, question_template)
        return answer


if __name__ == '__main__':
    qusetion = Question()
    # Test case for each template
    # TODO
    print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
    # print(qusetion.question_process('卧虎藏龙的评分是多少？'))
