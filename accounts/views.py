from urllib.parse import urlencode

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, ListView

from accounts.forms import LoginForm, CustomUserCreationForm, UserChangeForm, SearchForm
from accounts.models import Account


class LoginView(TemplateView):
    template_name = 'login.html'
    form = LoginForm

    def get(self, request, *args, **kwargs):
        next = request.GET.get('next')
        form_data = {} if not next else {'next': next}
        form = self.form(form_data)
        context = {'login_form': form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form(request.POST)
        if not form.is_valid():
            return redirect('login')
        login_name = form.cleaned_data.get('login')
        password = form.cleaned_data.get('password')
        next = form.cleaned_data.get('next')
        user = authenticate(request, login=login_name, password=password)
        if not user:
            return redirect('login')
        login(request, user)
        if next:
            return redirect(next)
        return redirect('index')


def logout_view(request):
    logout(request)
    return redirect('index')


class RegisterView(CreateView):
    model = get_user_model()
    template_name = 'register.html'
    form_class = CustomUserCreationForm
    success_url = '/'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.login
            user.save()
            login(request, user)
            return redirect('index')
        context = {}
        context['form'] = form
        return self.render_to_response(context)


class ProfileView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile.html'
    context_object_name = 'user_obj'

    def get_context_data(self, **kwargs):
        posts = self.object.posts.order_by('-created_at')
        own_profile = self.request.user
        some_profile = kwargs.get('object')
        kwargs['own_subscribes'] = own_profile.subscriptions.count()
        kwargs['own_subscribers'] = own_profile.subscribers.count()
        kwargs['some_subscribes'] = some_profile.subscriptions.count()
        kwargs['some_subscribers'] = some_profile.subscribers.count()
        kwargs['posts'] = posts
        kwargs['search_form'] = SearchForm()
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        subscribe_to = request.GET.get('subscribe_to')
        if subscribe_to:
            request.user.subscriptions.add(subscribe_to)
        subscribe_of = request.GET.get('subscribe_of')
        if subscribe_of:
            request.user.subscriptions.remove(subscribe_of)
        return super().get(request, *args, **kwargs)


class UserChangeView(UpdateView):
    model = get_user_model()
    form_class = UserChangeForm
    template_name = 'user_change.html'
    context_object_name = 'user_obj'

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})


class ProfilesView(ListView):
    template_name = 'profiles.html'
    model = get_user_model()
    context_object_name = 'profiles'
    queryset = Account.objects.all()

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')
        return None

    def get_queryset(self):
        queryset = super().get_queryset().all()
        print(queryset)
        if self.search_value:
            query = Q(email__icontains=self.search_value) | Q(login__icontains=self.search_value) | Q(
                first_name__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({'search': self.search_value})
        return context
