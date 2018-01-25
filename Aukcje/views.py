from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.urls import reverse
from django.contrib.auth.models import Group

from .models import Aukcja, Kategoria, Komentarz, PodKategoria
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from .forms import AukcjaForm, SignUpForm, EditProfileForm, KomentarzForm, SubCategoryForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_admin_or_moderator(user):
    return user.groups.filter(name__in=['Admin', 'Moderator']).exists()

def auction_list(request):
    auctions = Aukcja.objects.all().order_by('-published_date')
    return render(request, 'Aukcje/auction_list.html', {'auctions': auctions})
def auction_in_category(request, pk):
    auctions = Aukcja.objects.filter(kategoria=pk)

    return render(request,'Aukcje/category.html', {'auctions': auctions})

def auction_detail(request, pk):
    aukcja = get_object_or_404(Aukcja, pk=pk)
    return render(request, 'Aukcje/aukcja_detail.html', {'aukcja': aukcja})
@login_required
def auction_new(request):
    if request.method == "POST":
        form = AukcjaForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('auction_detail', pk=post.pk)
    else:
        form = AukcjaForm()
    return render(request, 'Aukcje/auction_edit.html', {'form': form})

@login_required
def auction_edit(request, pk):
    post = get_object_or_404(Aukcja, pk=pk)
    if request.method == "POST":
        form = AukcjaForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('auction_detail', pk=post.pk)
    else:
        form = AukcjaForm(instance=post)
    return render(request, 'Aukcje/auction_edit.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_moderator)
def auction_edit_admin(request, pk):
    post = get_object_or_404(Aukcja, pk=pk)
    if request.method == "POST":
        form = AukcjaForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('admin_auction_list', pk=post.pk)
    else:
        form = AukcjaForm(instance=post)
    return render(request, 'Aukcje/auction_edit.html', {'form': form})

@login_required
def auction_remove(request, pk):
    post = get_object_or_404(Aukcja, pk=pk)
    post.delete()
    return redirect('auction_list')

@login_required
@user_passes_test(is_admin_or_moderator)
def auction_remove_admin(request, pk):
    post = get_object_or_404(Aukcja, pk=pk)
    post.delete()
    return redirect('admin_auction_list')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            group = Group.objects.get(name='User')
            user.groups.add(group)
            login(request, user)
            return redirect('auction_list')
    else:
        form = SignUpForm()
    return render(request, 'Aukcje/singup.html', {'form': form})

def profilePk(request, pk):
    user = get_object_or_404(User,pk=pk)
    auctions = Aukcja.objects.filter(author=user)
    opinions = Komentarz.objects.filter(komentowany=user, zatwierdzony=True)
    return render(request,'Aukcje/profile.html', {'user':user,'auctions':auctions, 'opinions': opinions})

def profile(request):
    user = get_object_or_404(User,pk=request.user.pk)
    auctions = Aukcja.objects.filter(author=user)
    opinions = Komentarz.objects.filter(komentowany=user, zatwierdzony=True)
    return render(request,'Aukcje/profile.html', {'user':user,'auctions':auctions, 'opinions': opinions})

def show_category(request,pk):
    kategoria =Kategoria.objects.get(kategoria=pk)
    auctions = Aukcja.objects.filter(kategoria=kategoria.pk)
    subCategories = PodKategoria.objects.filter(kategoria=kategoria)
    return render(request, 'Aukcje/auctionsInCategory.html', {'auctions': auctions, 'subCategories':subCategories})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was updated successfully!')  # <-
            return redirect('settings:password')
        else:
            messages.warning(request, 'Please correct the error below.')  # <-
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Aukcje/change_password.html', {'form': form})
@login_required
def edit_profile(request):
    if request.method =='POST':
        form  = EditProfileForm(request.POST, instance = request.user)

        if form.is_valid():
            form.save()
            return redirect('profile', request.user.pk)

    else:
        form = EditProfileForm(instance=request.user)
        return render(request, 'Aukcje/update_profile.html', {'form': form})
@login_required
def user_auctions(request):
    user = User.objects.get(pk=request.user.pk)
    auctions = Aukcja.objects.filter(author=user).order_by('-published_date')
    return render(request, 'Aukcje/user_auctions.html', {'auctions': auctions})

@login_required
def add_opinion(request,pk):
    user = User.objects.get(pk=pk)
    if request.method == "POST":
        form = KomentarzForm(request.POST)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.autor = request.user
            opinion.komentowany = user
            opinion.save()
            return redirect('profilePk', pk)
    else:
        form = KomentarzForm()
    return render(request, 'Aukcje/add_opinion.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_moderator)
def approve_opinions(request):
    opinions = Komentarz.objects.filter(zatwierdzony=False)
    return render(request, 'Aukcje/approve_opinions.html', {'opinions':opinions})

@login_required
@user_passes_test(is_admin_or_moderator)
def opinion_remove(request, pk):
    opinion = get_object_or_404(Komentarz, pk=pk)
    opinion.delete()
    return redirect('approve_opinions')

@login_required
@user_passes_test(is_admin_or_moderator)
def opinion_approved(request, pk):
    opinion = get_object_or_404(Komentarz, pk=pk)
    opinion.zatwierdz()
    return redirect('approve_opinions')

@login_required
@user_passes_test(is_admin_or_moderator)
def admin_auction_list(request):
    auctions = Aukcja.objects.all().order_by('-published_date')
    return render(request, 'Aukcje/auction_list_admin.html', {'auctions': auctions})
@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = User.objects.all()
    return render(request, 'Aukcje/users.html', {'users': users})
@login_required
@user_passes_test(is_admin_or_moderator)
def admin_panel(request):
    return render(request,'Aukcje/admin.html')

@login_required
def opinions(request):
    opinions = Komentarz.objects.all().order_by('-data')
    return render(request,'Aukcje/opinion_list.html',{'opinions':opinions})

@login_required
@user_passes_test(is_admin)
def change_group(request, pk, old_group, new_group):
    user = User.objects.get(pk=pk)
    oldGroup = Group.objects.get(name=old_group)
    newGroup = Group.objects.get(name=new_group)
    user.groups.remove(oldGroup)
    user.groups.add(newGroup)
    return redirect('user_list')

@login_required
def user_opinions(request):
    user = request.user
    opinions = Komentarz.objects.filter(komentowany=user, zatwierdzony=True)
    return render(request,'Aukcje/user_opinions.html',{'opinions':opinions})

@login_required
def user_made_opinions(request):
    user = request.user
    opinionsApproved = Komentarz.objects.filter(autor=user, zatwierdzony=True)
    opinionsNotApproved = Komentarz.objects.filter(autor=user, zatwierdzony=False)
    return render(request, 'Aukcje/user_made_opinions.html', {'opinionsApproved': opinionsApproved, 'opinionsNotApproved':opinionsNotApproved})

def show_subcategory(request, pk, subC):
    subCat = PodKategoria.objects.get(pk=subC)
    auctions = Aukcja.objects.filter(podkategoria=subCat).order_by('-published_date')
    subCategories = PodKategoria.objects.filter(kategoria=pk)
    return render(request,'Aukcje/category_subcategory.html', {'auctions':auctions,'subCat':subCat,'subCategories':subCategories})

@login_required
@user_passes_test(is_admin)
def show_subcategories(request):
    subCategories = PodKategoria.objects.all()
    return render(request,'Aukcje/subcategories.html', {'subCategories':subCategories})

@login_required
def opinion_edit(request, pk, pkO):
    opinion = get_object_or_404(Komentarz, pk=pk)
    user = User.objects.get(pk=pkO)
    if request.method == "POST":
        form = KomentarzForm(request.POST, instance=opinion)
        if form.is_valid():
            opinion=form.save(commit=False)
            opinion.zatwierdzony=False
            opinion.autor=request.user
            opinion.komentowany=user
            opinion.save()
            return redirect('user_made_opinions')
    else:
        form = KomentarzForm(instance=opinion)
    return render(request, 'Aukcje/opinion_edit.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def subCategories(request):
    subCategories=PodKategoria.objects.all()
    return render(request, 'Aukcje/subcategories_list.html', {'subCategories':subCategories})

@login_required
@user_passes_test(is_admin)
def edit_subcategory(request, pk):
    subCateogry = get_object_or_404(PodKategoria, pk=pk)
    if request.method == "POST":
        form = SubCategoryForm(request.POST, instance=subCateogry)
        if form.is_valid():
            opinion = form.save(commit=False)
            opinion.save()
            return redirect('subCategories')
    else:
        form = SubCategoryForm(instance=subCateogry)
    return render(request, 'Aukcje/add_subCategory.html', {'form': form})

@login_required
@user_passes_test(is_admin)
def new_subcategory(request):
    if request.method == "POST":
        form = SubCategoryForm(request.POST)
        if form.is_valid():
            subcategory = form.save(commit=False)
            subcategory.save()
            return redirect('subCategories')
    else:
        form = SubCategoryForm()
    return render(request, 'Aukcje/add_subCategory.html', {'form': form})