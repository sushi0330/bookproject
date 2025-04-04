from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Book, Review
from django.db.models import Avg
from django.core.paginator import Paginator
from .consts import ITEMS_PER_PAGE

class ListBookView(LoginRequiredMixin, ListView):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        ListView (_type_): _description_
    """
    model = Book
    template_name = 'book/book_list.html'
    paginate_by = ITEMS_PER_PAGE
      
class DetailBookView(LoginRequiredMixin, DetailView):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        DetailView (_type_): _description_
    """
    model = Book
    template_name = 'book/book_detail.html'

class CreateBookView(LoginRequiredMixin, CreateView):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        CreateView (_type_): _description_

    Returns:
        _type_: _description_
    """
    model = Book
    template_name = 'book/book_create.html'
    fields = ['title', 'text', 'category', 'thumbnail']
    success_url = reverse_lazy('list-book')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
class DeleteBookView(LoginRequiredMixin, DeleteView):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        DeleteView (_type_): _description_

    Raises:
        PermissionDenied: _description_

    Returns:
        _type_: _description_
    """
    model = Book
    template_name = 'book/book_confirm_delete.html'
    success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj

class UpdateBookView(LoginRequiredMixin, UpdateView):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        UpdateView (_type_): _description_

    Raises:
        PermissionDenied: _description_

    Returns:
        _type_: _description_
    """
    model = Book
    template_name = 'book/book_update.html'
    fields = ['title', 'text', 'category', 'thumbnail']
    # success_url = reverse_lazy('list-book')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # print(f'obj: {obj}')
        if obj.user != self.request.user:
            raise PermissionDenied
        
        return obj
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.object.pk})

class CreateReviewView(LoginRequiredMixin, CreateView):
    """_summary_

    Args:
        LoginRequiredMixin (_type_): _description_
        CreateView (_type_): _description_

    Returns:
        _type_: _description_
    """
    model = Review
    template_name = 'book/review_form.html'
    fields = ('book', 'title', 'text', 'rate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        # print(context)
        return context 
    
    def form_valid(self, form):
        form.instance.user = self.request.user

        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk': self.kwargs['book_id']})
    
def index_view(request):
    """_summary_

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    object_list = Book.objects.order_by('-id')
    ranking_list = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')

    paginator = Paginator(ranking_list, ITEMS_PER_PAGE)
    page_number = request.GET.get('page',1)
    page_obj = paginator.page(page_number)
    
    return render(request, 
                'book/index.html', 
                {'object_list':object_list, 'ranking_list':ranking_list, 'page_obj':page_obj,})