from testcase.api.login.login_all_api import LoginApi
from utils.config import NewConfig

from testcase.api.studyCenter.getServiceInfo_step1 import GetServiceInfo
from testcase.api.studyCenter.getTaskInfo_step2 import GetTaskInfo
from testcase.api.studyCenter.startLearning_step3 import StartLearning
from testcase.api.studyCenter.getTaskInfo_step4 import GetTaskInfo2

from testcase.api.studyCenter.words_lists.all_cihui import AllCihuiInterface
from testcase.api.studyCenter.sysListening.all_listening_interface import AllListenInterface
from testcase.api.studyCenter.reading.all_reading_interface import AllReadInterface
from testcase.api.studyCenter.grammar.all_gra_interface import AllGraInterface
from testcase.api.studyCenter.writing.all_wrt_interface import AllWrtInterface

if __name__ == '__main__':
    cfg_info = NewConfig()
    devices = cfg_info.get_info('vivox6')
    common, headers = cfg_info.get_info("vivox6")
    print(common,headers)
    t = LoginApi()
    access_token = t.get_access_token(common, headers)
    print("access_token:".capitalize(), access_token)
    while True:
        try:
            step1 = GetServiceInfo(common, headers, access_token)
            step1_ids = step1.get_service_id()
            servicesID, _, _, = step1_ids
            print("Step1 return:", step1_ids)
            step2 = GetTaskInfo(common, headers, access_token)
            step2_ids = step2.get_task_id(servicesID)
            print("step2_ids", step2_ids)
            scheduleID, _, all_currStatus = step2_ids
            print("all_currStatus",all_currStatus)
            all_currStatuses = []
            for c in all_currStatus:
                all_currStatuses.append(c.get("currStatus"))
            # if 0 not in all_currStatus:
            #     break
            print(all_currStatuses)
            step3 = StartLearning(common, headers, access_token)
            try:
                steps3_result = step3.start_to_learn(scheduleID)
            except:
                steps3_result = 1
            if steps3_result:
                step4 = GetTaskInfo2(common, headers, access_token)
                steps4_data = step4.get_all_tasks_id(servicesID)
                print("steps4_data", steps4_data)
                # from time import sleep
                # sleep(50)
                for datas in steps4_data:
                    if datas.get("VOC"):
                        print("VOC", datas.get("VOC"))
                        for task in datas.get("VOC"):
                            print(task)
                            practiceType = task.get("practiceType")
                            currStatus = task.get("currStatus")
                            taskID = task.get("taskID")
                            groupID = task.get("groupID")
                            # # if currStatus == 0:
                            print("VOC", practiceType, currStatus, taskID, groupID)
                            words_post = AllCihuiInterface(common, headers, access_token)
                            data_1 = words_post.get_word_list_words(groupID, taskID, practiceType)
                            print("Data",data_1)
                            for star in data_1:
                                print("star ----", star)
                                words_post.put_wordsList_3star(star)
                            d = {"taskID":taskID, "groupID":groupID}
                            words_post.put_all_words_lists_done(d)
                    if datas.get("RID"):
                        for task in datas.get("RID"):
                            practiceType = task.get("practiceType")
                            currStatus = task.get("currStatus")
                            taskID = task.get("taskID")
                            groupID = task.get("groupID")
                            print("RID", practiceType, currStatus, taskID, groupID)
                            if currStatus == 0:
                                if practiceType == 13:
                                    # print(taskID, groupID)
                                    sa = AllReadInterface(common, headers, access_token)
                                    all_answer = sa.get_all_sen_analysis_answer(groupID, taskID)
                                    print("句子分析", all_answer)
                                    if len(all_answer) != 0:
                                        print("a", all_answer)
                                        for a in all_answer:
                                            print("AAAA", a)
                                            sa.post_all_sen_analysis_answer(taskID, a)
                                    sa_words = sa.get_sa_words(groupID, taskID, practiceType)
                                    for star in sa_words:
                                        r = sa.put_sa_words(star)
                                        print(r)
                                    sa_done_data = sa.return_sa_done_data(groupID, practiceType)
                                    sa.put_sa_done(sa_done_data, taskID)
                                if practiceType == 14:
                                    st = AllReadInterface(common, headers, access_token)
                                    all_answer = st.get_all_sec_train_answer(groupID, taskID)
                                    print("all_answer", all_answer)
                                    for a in all_answer:
                                        if "newF" in list(a.keys()):
                                            stars_3 = st.get_sec_train_words(groupID, taskID, practiceType)
                                            for star in stars_3:
                                                ne_re = st.put_sec_train_words(star)
                                            st_data = st.get_sec_train_word_done_data(groupID, taskID, practiceType)
                                            re = st.put_sec_train_words_done(taskID, st_data)
                                        else:
                                            st.post_all_sec_train_answer(taskID, a)
                                if practiceType == 15:
                                    # print(taskID, groupID)
                                    at = AllReadInterface(common, headers, access_token)
                                    all_answer = at.get_all_art_train_answer(groupID, taskID)
                                    print("文章训练", all_answer)
                                    for a in all_answer:
                                        print("A", a)
                                        if "newF" in list(a.keys()):
                                            stars_3 = at.get_article_train_words(groupID, taskID, practiceType)
                                            # print("stars_3", stars_3)
                                            for star in stars_3:
                                                at.put_article_train_words(star)
                                            at_data = at.get_articleTrain_word_done_data(groupID, taskID, practiceType)
                                            # print(at_data)
                                            heheh = at.put_article_train_done(taskID, at_data)
                                            print("H", heheh)
                                        if "newF" not in list(a.keys()):
                                            print("A", a)
                                            print('a.get("stepType") ', a.get("stepType"))
                                            if a.get("stepType") == 3:
                                                at.post_all_art_train_answer(taskID, a)
                                            if a.get("stepType") == 2:
                                                at.post_all_art_train_answer(taskID, a)
                                            # if a.get("stepType") == 1:
                                            #     at.put_article_train_done(taskID, a)
                                            if a.get("stepType") == 4:
                                                at.post_all_art_train_answer(taskID, a)
                                if practiceType == 16:
                                    clozeTest = AllReadInterface(common, headers, access_token)
                                    all_answer = clozeTest.get_all_ClozeTest_answer(groupID, taskID)
                                    print(all_answer)
                                    for a in all_answer:
                                        if "newF" in list(a.keys()):
                                            stars_3 = clozeTest.get_ClozeTest_words(groupID, taskID, practiceType)
                                            for star in stars_3:
                                                clozeTest.put_ClozeTest_words(star)
                                            data = clozeTest.get_ClozeTest_word_done_data(groupID, taskID, practiceType)
                                            print("+++++++++++++++",data)
                                            clozeTest.put_ClozeTest_words_done(taskID, data)
                                        if "newF" not in list(a.keys()):
                                            clozeTest.post_all_clozeTest_answer(taskID, a)
                                if practiceType == 17:
                                    cloze75 = AllReadInterface(common, headers, access_token)
                                    all_answer = cloze75.get_all_Cloze75_answer(groupID, taskID)
                                    print(all_answer)
                                    for a in all_answer:
                                        if "newF" in list(a.keys()):
                                            stars_3 = cloze75.get_Cloze75_words(groupID, taskID, practiceType)
                                            for star in stars_3:
                                                cloze75.put_Cloze75_words(star)
                                            data = cloze75.get_Cloze75_word_done_data(groupID, taskID, practiceType)
                                            print("+++++++++++++++",data)
                                            cloze75.put_Cloze75_words_done(taskID, data)
                                        if "newF" not in list(a.keys()):
                                            try:
                                                data = cloze75.get_Cloze75_word_done_data(groupID, taskID, practiceType)
                                                cloze75.put_Cloze75_words_done(taskID, data)
                                            except:
                                                pass
                                            cloze75.post_all_cloze75_answer(taskID, a)
                            else:
                                pass
                    if datas.get("GRA"):
                        # print(datas.get("GRA"))
                        for task in datas.get("GRA"):
                            if task.get('currStatus') == 0 or task.get('currStatus') == 1:
                                practiceType = task.get("practiceType")
                                currStatus = task.get("currStatus")
                                taskID = task.get("taskID")
                                groupID = task.get("groupID")
                                # print(taskID, groupID,practiceType)
                                if currStatus == 0:
                                    if practiceType == 6:
                                        mul_choice = AllGraInterface(common, headers, access_token)
                                        mul_choice_answers = mul_choice.get_all_mul_choice_answer(groupID, taskID)
                                        # print(mul_choice_answers)
                                        for answer in mul_choice_answers:
                                            post_mul_choice_answer = mul_choice.post_all_mul_choice_answer(taskID, answer)
                                        mul_choice_words = mul_choice.get_mul_choice_words(groupID, taskID, practiceType)
                                        mc_words = mul_choice.get_mul_choice_words(groupID, taskID, practiceType)
                                        for star in mc_words:
                                            r = mul_choice.put_mul_choice_words(star)
                                        mul_choice_done_data = mul_choice.get_mul_choice_done_data(groupID, practiceType)
                                        mul_choice.put_mul_choice_done(mul_choice_done_data, taskID)
                                    if practiceType == 7:
                                        graFill = AllGraInterface(common, headers, access_token)
                                        all_answer = graFill.get_all_gra_fill_answer(groupID, taskID)
                                        print(all_answer)
                                        for a in all_answer:
                                            if "newF" in list(a.keys()):
                                                stars_3 = graFill.get_gra_fill_words(groupID, taskID, practiceType)
                                                for star in stars_3:
                                                    graFill.put_gra_fill_words(star)
                                                data = graFill.get_gra_fill_word_done_data(groupID, taskID, practiceType)
                                                graFill.put_gra_fill_words_done(taskID, data)
                                            if "newF" not in list(a.keys()):
                                                graFill.post_all_gra_fill_answer(taskID, a)
                                if currStatus == 1:
                                    if practiceType == 6:
                                        mul_choice = AllGraInterface(common, headers, access_token)
                                        mul_choice_words = mul_choice.get_mul_choice_words(groupID, taskID, practiceType)
                                        mc_words = mul_choice.get_mul_choice_words(groupID, taskID, practiceType)
                                        for star in mc_words:
                                            if star.get("oldF") == 3:
                                                pass
                                            else:
                                                r = mul_choice.put_mul_choice_words(star)
                    if datas.get("LIS"):
                        print("Begin LIS", datas.get("LIS"))
                        for task in datas.get("LIS"):
                            # print("task:", task)
                            if task.get('currStatus') == 0 or task.get('currStatus') == 1:
                                practiceType = task.get("practiceType")
                                currStatus = task.get("currStatus")
                                taskID = task.get("taskID")
                                groupID = task.get("groupID")
                                print(practiceType, currStatus, taskID, groupID)
                                if currStatus == 0:
                                    if practiceType == 1:
                                        # print(practiceType, currStatus, taskID, groupID)
                                        word_listen = AllListenInterface(common, headers, access_token)
                                        word_listen_answers = word_listen.get_all_dict_answer(groupID, taskID)
                                        for answer in word_listen_answers:
                                            post_word_dict_answer = word_listen.post_all_word_dict_answer(taskID, answer)
                                        word_dict_words = word_listen.get_word_dict_words(groupID, taskID, practiceType)
                                        wd_words = word_listen.get_word_dict_words(groupID, taskID, practiceType)
                                        for star in wd_words:
                                            r = word_listen.put_word_dict_words(star)
                                    if practiceType == 2:
                                        # print(practiceType, currStatus, taskID, groupID)
                                        word_trans_get = AllListenInterface(common, headers, access_token)
                                        word_trans_answers = word_trans_get.get_all_word_tran_answer(groupID, taskID)
                                        for answer in word_trans_answers:
                                            post_word_trans_answer = word_trans_get.post_all_word_tran_answer(taskID, answer)
                                        word_trans_words = word_trans_get.get_word_trans_words(groupID, taskID, practiceType)
                                        wt_words = word_trans_get.get_word_trans_words(groupID, taskID, practiceType)
                                        for star in wt_words:
                                            # print(star)
                                            r = word_trans_get.put_word_tran_words(star)
                                            # print(r)
                                    if practiceType == 3:
                                        sen_fill = AllListenInterface(common, headers, access_token)
                                        sen_fill_answers = sen_fill.get_all_sen_fill_answer(groupID, taskID)
                                        for answer in sen_fill_answers:
                                            # print("Answer", answer)
                                            post_sen_fill_answer = sen_fill.post_all_sen_fill_answer(taskID, answer)
                                        sen_fill_words = sen_fill.get_sen_fill_words(groupID, taskID, practiceType)
                                        sf_words = sen_fill.get_sen_fill_words(groupID, taskID, practiceType)
                                        for star in sf_words:
                                            r = sen_fill.put_sen_fill_words(star)
                                        sf_done_data = sen_fill.get_sen_fill_done_data(groupID, practiceType)
                                        sen_fill.put_sen_fill_done(sf_done_data, taskID)
                                if currStatus == 1:
                                    word_lists_to_3start = AllListenInterface(common, headers, access_token)
                                    if practiceType == 1:
                                        word_dict_words =word_lists_to_3start .get_word_dict_words(groupID, taskID, practiceType)
                                        wd_words = word_lists_to_3start.get_word_trans_words(groupID, taskID, practiceType)
                                        for star in wd_words:
                                            if star.get("oldF") == 3:
                                                pass
                                            else:
                                                 word_lists_to_3start.put_word_tran_words(star)
                                    if practiceType == 2:
                                        word_trans_words = word_lists_to_3start.get_word_trans_words(groupID, taskID,
                                                                                                   practiceType)
                                        wt_words = word_lists_to_3start.get_word_trans_words(groupID, taskID, practiceType)
                                        for star in wt_words:
                                            if star.get("oldF") == 3:
                                                pass
                                            else:
                                                word_lists_to_3start.put_word_tran_words(star)
                                    if practiceType == 3:
                                        sen_fill_words = word_lists_to_3start.get_sen_fill_words(groupID, taskID,
                                                                                                   practiceType)
                                        sf_words = word_lists_to_3start.get_sen_fill_words(groupID, taskID, practiceType)
                                        for star in sf_words:
                                            if star.get("oldF") == 3:
                                                pass
                                            else:
                                                print("+++++++++++++++++++++", star)
                                                word_lists_to_3start.put_sen_fill_words(star)
                    if datas.get("WRI"):
                        print("Begin WRI")
                        for task in datas.get("WRI"):
                            if task.get('currStatus') == 0 or task.get('currStatus') == 1:
                                practiceType = task.get("practiceType")
                                currStatus = task.get("currStatus")
                                taskID = task.get("taskID")
                                groupID = task.get("groupID")
                                if currStatus == 0:
                                    if practiceType == 9:
                                        # print(practiceType, currStatus, taskID, groupID)
                                        word_spell = AllWrtInterface(common, headers, access_token)
                                        word_spell_answers = word_spell.get_all_word_spell_answer(groupID, taskID)
                                        for answer in word_spell_answers:
                                            post_word_spell_answer = word_spell.post_all_word_spell_answer(taskID, answer)
                                        word_spell_words = word_spell.get_word_spell_words(groupID, taskID, practiceType)
                                        ws_words = word_spell.get_word_spell_words(groupID, taskID, practiceType)
                                        for star in ws_words:
                                            r = word_spell.put_word_spell_words(star)
                                    if practiceType == 12:
                                        print("真题写作")
                                        zhenti_xiezuo = AllWrtInterface(common, headers, access_token)
                                        zhenti_xiezuo_answers = zhenti_xiezuo.get_all_zhenti_xiezuo_answer(groupID, taskID)
                                        for answer in zhenti_xiezuo_answers:
                                            print("Answer", answer)
                                            post_word_spell_answer = zhenti_xiezuo.post_all_zhenti_xiezuo_answer(taskID, answer)
                                if currStatus == 1:
                                    word_lists_to_3start = AllWrtInterface(common, headers, access_token)
                                    if practiceType == 9:
                                        word_spell_words = word_lists_to_3start.get_word_spell_words(groupID, taskID,
                                                                                                   practiceType)
                                        ws_words = word_lists_to_3start.get_word_spell_words(groupID, taskID, practiceType)
                                        for star in ws_words:
                                            if star.get("oldF") == 3:
                                                pass
                                            else:
                                                word_lists_to_3start.put_word_spell_words(star)
        except:
            pass

