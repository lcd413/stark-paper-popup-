from stark.service import v1
from crm import models
from django.conf.urls import url
from django.shortcuts import redirect,HttpResponse
from django.utils.safestring import mark_safe
class DepartmentConfig(v1.StarkConfig):
    list_display = ['title','code']
v1.site.register(models.Department,DepartmentConfig)

class UserInfoConfig(v1.StarkConfig):

    show_add_btn = True

    show_search_form = True
    search_fields = ['name__contains', 'email__contains']
    edit_link = ['name']

    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return '性别'

        # return obj.gender
        return obj.get_gender_display()

    def display_depart(self,obj=None,is_header=False):
        if is_header:
            return '部门'
        return obj.depart.title



    comb_filter = [
        v1.FilterOption('gender', is_choice=True),
        v1.FilterOption('depart',)
    ]
    list_display = ['name', 'username','email',display_gender,display_depart]
v1.site.register(models.UserInfo,UserInfoConfig)

class CourseConfig(v1.StarkConfig):
    list_display = ['name']

v1.site.register(models.Course,CourseConfig)


class SchoolConfig(v1.StarkConfig):
    list_display = ['title']

v1.site.register(models.School,SchoolConfig)

class ClassListConfig(v1.StarkConfig):
    def display_teachers(self, obj=None, is_header=False):
        if is_header:
            return '任课老师'

        html = []
        teacher_list = obj.teachers.all()
        for teacher in teacher_list:
            html.append(teacher.name)

        return ",".join(html)
    comb_filter = [
        v1.FilterOption('school', ),
        v1.FilterOption('course', )
    ]

    list_display = ['school','course','semester','price','start_date','graduate_date','memo',display_teachers,'tutor']


v1.site.register(models.ClassList,ClassListConfig)


class CustomerConfig(v1.StarkConfig):




    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return '性别'
        return obj.get_gender_display()

    def display_education(self,obj=None,is_header=False):
        if is_header:
            return '学历'
        return obj.get_education_display()

    def display_course(self,obj=None,is_header=False):
        if is_header:
            return '咨询课程'
        course_list = obj.course.all()
        html = []
        # self.request.GET
        # self._query_param_key
        # 构造QueryDict
        # urlencode()
        for item in course_list:
            temp = "<a style='display:inline-block;padding:3px 5px;border:1px solid blue;margin:2px;' href='/stark/crm/customer/%s/%s/dc/'>%s <span class='glyphicon glyphicon-remove'></span></a>" %(obj.pk,item.pk,item.name)
            html.append(temp)

        return mark_safe("".join(html))

    def display_status(self,obj=None,is_header=False):
        if is_header:
            return '状态'
        return obj.get_status_display()

    def record(self,obj=None,is_header=False):
        if is_header:
            return '跟进记录'
        # /stark/crm/consultrecord/?customer=11
        return mark_safe("<a href='/stark/crm/consultrecord/?customer=%s'>查看跟进记录</a>" %(obj.pk,))

    list_display = ['qq','name',display_gender,display_education,display_course,display_status,record]




    def delete_course(self,request,customer_id,course_id):
        """
        删除当前用户感兴趣的课程
        :param request:
        :param customer_id:
        :param course_id:
        :return:
        """
        customer_obj = self.model_class.objects.filter(pk=customer_id).first()
        customer_obj.course.remove(course_id)
        # 跳转回去时，要保留原来的搜索条件
        return redirect(self.get_list_url())

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        patterns = [
            url(r'^(\d+)/(\d+)/dc/$', self.wrap(self.delete_course), name="%s_%s_dc" %app_model_name),
        ]
        return patterns
v1.site.register(models.Customer,CustomerConfig)

class ConsultRecordConfig(v1.StarkConfig):
    list_display = ['customer','consultant','date','note']

v1.site.register(models.ConsultRecord,ConsultRecordConfig)

class PaymentRecordConfig(v1.StarkConfig):
    list_display = ['customer','class_list','pay_type','paid_fee','turnover','quote','note','date','consultant']

v1.site.register(models.PaymentRecord,PaymentRecordConfig)


class StudentConfig(v1.StarkConfig):
    list_display = ['customer','username','password','emergency_contract','class_list','company','location','position','salary','welfare','date','memo']

v1.site.register(models.Student,StudentConfig)

class CourseRecordConfig(v1.StarkConfig):
    list_display = ['class_obj','day_num','teacher','date','course_title','course_memo','has_homework','homework_title','homework_memo','exam']

v1.site.register(models.CourseRecord,CourseRecordConfig)

class StudyRecordConfig(v1.StarkConfig):
    list_display = ['course_record','student','record','score','homework_note','note','homework','stu_memo','date']
v1.site.register(models.StudyRecord,StudyRecordConfig)

