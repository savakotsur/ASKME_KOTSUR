from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate(objects_list, request, per_page=10):
    page = request.GET.get('page', 1)  

    paginator = Paginator(objects_list, per_page)  

    try:
        page_obj = paginator.page(page)  
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj