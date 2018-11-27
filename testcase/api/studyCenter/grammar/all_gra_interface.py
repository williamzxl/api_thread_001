from testcase.api.studyCenter.grammar.mulChoice.get_mul_choice_all_answer import GetAllMulChoiceAnswers
from testcase.api.studyCenter.grammar.mulChoice.post_all_mul_choice_answer import PostAllMulChoiceAnswers
from testcase.api.studyCenter.grammar.graFill.get_all_gra_fill_answer import GetAllGraFillnAnswers
from testcase.api.studyCenter.grammar.graFill.post_all_gra_fill_answer import PostAllGraFillAnswers


class AllGraInterface(GetAllMulChoiceAnswers, PostAllMulChoiceAnswers, GetAllGraFillnAnswers, \
                      PostAllGraFillAnswers):
    pass