from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import ItemListing, Category, Location, ListingImage
from .forms import AdSubmissionForm


def home(request):
    listings = ItemListing.objects.filter(status='ACTIVE').select_related(
        'category', 'location', 'seller', 'seller__profile'
    ).prefetch_related('images')

    # 1. Search Query
    q = request.GET.get('q', '').strip()
    if q:
        listings = listings.filter(
            Q(title__icontains=q) | Q(description__icontains=q)
        )

    # 2. Category Filter
    category_slug = request.GET.get('category', '').strip()
    if category_slug:
        listings = listings.filter(category__slug=category_slug)

    # 3. Location Filter
    location_id = request.GET.get('location', '').strip()
    if location_id:
        listings = listings.filter(location_id=location_id)

    # 4. Condition Filter
    condition = request.GET.get('condition', '').strip()
    if condition:
        listings = listings.filter(condition=condition)

    # 5. Verified Sellers Filter
    verified_only = request.GET.get('verified', '').strip()
    if verified_only == '1':
        listings = listings.filter(seller__profile__is_verified=True)

    # 6. Price Sorting (Featured items stay prioritized by default)
    price_sort = request.GET.get('price', '').strip()
    if price_sort == 'lowest':
        listings = listings.order_by('-is_featured', 'price', '-created_at')
    elif price_sort == 'highest':
        listings = listings.order_by('-is_featured', '-price', '-created_at')
    else:
        listings = listings.order_by('-is_featured', '-created_at')

    # Pagination (8 items per page)
    paginator = Paginator(listings, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': Category.objects.all(),
        'locations': Location.objects.all(),
    }
    return render(request, 'listings/home.html', context)


def listing_detail(request, pk):
    ad = get_object_or_404(ItemListing, pk=pk, status='ACTIVE')
    return render(request, 'listings/detail.html', context={'ad': ad})


@login_required(login_url='accounts:login')
def create_ad(request):
    if request.method == 'POST':
        form = AdSubmissionForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')  # Extract all uploaded images
        
        if form.is_valid():
            ad = form.save(commit=False)
            ad.seller = request.user
            ad.status = 'ACTIVE'
            ad.save()

            # Save each image linked to the listing
            for index, file in enumerate(files):
                ListingImage.objects.create(
                    listing=ad,
                    image=file,
                    is_primary=(index == 0)
                )

            messages.success(request, "Your ad has been posted successfully!")
            return redirect('listings:detail', pk=ad.pk)
    else:
        form = AdSubmissionForm()

    return render(request, 'listings/create_ad.html', {'form': form})


@login_required(login_url='accounts:login')
def seller_dashboard(request):
    user_ads = ItemListing.objects.filter(seller=request.user).order_by('-created_at')
    
    context = {
        'user_ads': user_ads,
    }
    return render(request, 'listings/dashboard.html', context)


@login_required(login_url='accounts:login')
def toggle_sold_status(request, pk):
    ad = get_object_or_404(ItemListing, pk=pk, seller=request.user)
    if ad.status == 'ACTIVE':
        ad.status = 'SOLD'
        messages.success(request, f"'{ad.title}' has been marked as Sold.")
    else:
        ad.status = 'ACTIVE'
        messages.success(request, f"'{ad.title}' has been reactivated.")
    ad.save()
    return redirect('listings:dashboard')


@login_required(login_url='accounts:login')
def delete_ad(request, pk):
    ad = get_object_or_404(ItemListing, pk=pk, seller=request.user)
    if request.method == 'POST':
        ad.delete()
        messages.success(request, "Your ad has been deleted.")
        return redirect('listings:dashboard')
    return render(request, 'listings/delete_confirm.html', {'ad': ad})


@login_required(login_url='accounts:login')
def edit_ad(request, pk):
    ad = get_object_or_404(ItemListing, pk=pk, seller=request.user)
    
    if request.method == 'POST':
        form = AdSubmissionForm(request.POST, request.FILES, instance=ad)
        files = request.FILES.getlist('images')

        if form.is_valid():
            updated_ad = form.save()

            # If new images were uploaded during edit, add them
            if files:
                for index, file in enumerate(files):
                    ListingImage.objects.create(
                        listing=updated_ad,
                        image=file,
                        is_primary=False  # Keep existing primary image unless managed
                    )

            messages.success(request, f"'{updated_ad.title}' has been successfully updated!")
            return redirect('listings:dashboard')
    else:
        form = AdSubmissionForm(instance=ad)

    context = {
        'form': form,
        'ad': ad,
    }
    return render(request, 'listings/edit_ad.html', context)


def seller_store_view(request, username):
    seller = get_object_or_404(User, username=username)
    # Corrected from Ad.objects to ItemListing.objects
    seller_ads = ItemListing.objects.filter(seller=seller).order_by('-created_at')
    
    context = {
        'profile_seller': seller,
        'seller_ads': seller_ads,
    }
    return render(request, 'listings/seller_store.html', context)