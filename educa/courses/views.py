from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Course
from django.views.generic.edit import CreateView, UpdateView, \
                                            DeleteView

# Owner mixins allows to define the behaviour of class
class OwnerMixin(object):
    """
    These mixins can be used with
    any models with owner attribute
    """
    def get_querysset(self):
        qs = super(OwnerMixin, self).get_querysset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(OwnerEditMixin, self).form_valid(form)

class OwnerCourseMixin(OwnerMixin):
    model = Course

class OwnerCoursEditMixin(OwnerCourseMixin, OwnerEditMixin):
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')
    template_name = 'courses/manage/course/form.html'

### List view without mixins (concept)
# class ManageCourseListView(ListView):
#     model = Course
#     template_name = 'courses/manage/course/list.html'
#
#     def get_querysset(self):
#         qs = super(ManageCourseListView, self).get_querysset()
#         return qs.filter(owner=self.request.user)

#### Views
class ManageCourseListView(OwnerCourseMixin, ListView): #listview with mixin
    template_name = 'courses/manage/course/list.html'

class CourseCreateView(OwnerCourseEditMixin, CreateView):
    pass

class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    pass

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    success_url = reverse_lazy('manage_course_list')
