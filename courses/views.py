from django.shortcuts import render, redirect
from django.contrib import messages, auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q


# Create your views here.
@login_required(login_url='login')
def list_courses(request):
    page_obj = None
    try:
        courses = Courses.objects.all().order_by('-id')
        paginator = Paginator(courses, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'courses': page_obj
        }
    except Exception as e:
        pass
    return render(request, 'courses/courses_list.html', context)


@login_required(login_url='login')
def add_new_course(request):
    if request.method == 'POST':
        title = request.POST['title']
        subtitle = request.POST['subtitle']

        description = request.POST['desc']
        status = request.POST.get('status', True)

        if not title or len(title.strip()) == 0:
            messages.error(request, 'Title should not be empty')
            return redirect(add_new_course)

        elif Courses.objects.filter(title=title).exists():
            messages.error(request, 'Title should be unique')
            return redirect(add_new_course)

        elif not subtitle or len(subtitle.strip()) == 0:
            messages.error(request, 'Subtitle should not be empty')
            return redirect(add_new_course)

        elif Courses.objects.filter(subtitle=subtitle).exists():
            messages.error(request, 'Subtitle should be unique')
            return redirect(add_new_course)

        elif not request.FILES:
            messages.error(request, 'Please add an image')
            return redirect(add_new_course)

        elif not description or len(description.strip()) == 0:
            messages.error(request, 'Please add an description')
            return redirect(add_new_course)

        elif not status:
            messages.error(request, 'Please select the status')
            return redirect(add_new_course)
        
        else:
            image = request.FILES['image']
            course = Courses.objects.create(title=title, subtitle=subtitle, image=image,
                                            description=description, is_available=status)

            amount_values = request.POST.getlist('amount_values[]')
            amount_texts = request.POST.getlist('amount_texts[]')

            for value, text in zip(amount_values, amount_texts):
                amount = Amount.objects.create(value=value, text=text)
                course.amounts.add(amount)
            course.save()

            messages.success(request, f'Course "{title}" added succesfully')
            return redirect(list_courses)

    return render(request, 'courses/add_course.html')


@login_required(login_url='login')
def update_status(request, id):
    try:
        course = Courses.objects.get(id=id)
        course.is_available = not course.is_available
        course.save()
        messages.success(request, 'Status updated succesfully')
    except Courses.DoesNotExist:
        messages.error(request, 'Invalid course')
    return redirect(list_courses)


@login_required(login_url='login')
def edit_course(request, id=None):

    if request.method == 'POST':
        title = request.POST['title']
        subtitle = request.POST['subtitle']
        try:
            course = Courses.objects.get(id=id)
            course.title = title
            course.subtitle = subtitle

            if request.FILES:
                image = request.FILES['image']
                course.image = image

            if len(request.POST['desc'].strip()) > 0:
                description = request.POST['desc']
                course.description = description

            course.save()
            messages.success(request, 'Course updated succesfully')
            return redirect(list_courses)
        except Courses.DoesNotExist:
            messages.warning(request, 'Invalid course')
            return redirect(list_courses)

    try:
        course = Courses.objects.get(id=id)
        context = {'course': course}
        return render(request, 'courses/edit_course.html', context)
    except Courses.DoesNotExist:
        messages.error(request, 'Invalid course')
        return redirect(list_courses)


@login_required(login_url='login')
def delete_course(request, id):
    try:
        course = Courses.objects.get(id=id)
        course.delete()
        messages.success(request, 'Course deleted succesfully')
    except Courses.DoesNotExist:
        messages.error(request, 'Invalid course')
    return redirect(list_courses)


@login_required(login_url='login')
def search_course(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']

        if keyword:
            courses = Courses.objects.order_by('-id').filter(
                Q(title__icontains=keyword) | Q(subtitle__icontains=keyword) | Q(description__icontains=keyword))

    context = {
        'courses': courses,
    }
    return render(request, 'courses/courses_list.html', context)
