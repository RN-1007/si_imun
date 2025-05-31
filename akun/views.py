# from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth import get_user_model

from django.contrib.auth import logout
from django.shortcuts import redirect

from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponseForbidden

from .models import JadwalImunisasi
from .forms import JadwalImunisasiForm

User = get_user_model()

def landing_view(request):
    return render(request,'landing_page/index.html')   

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')  # ganti sesuai URL tujuan setelah login
        else:
            messages.error(request, 'Username atau password salah.')
    return render(request, 'page/login.html')

def dashboard_view(request):
    context = {
        'nama': request.user.nama,
        'role': request.user.role,
    }

    if request.user.role == 'admin':
        # Admin melihat semua user kecuali dirinya
        users = User.objects.exclude(id=request.user.id)
        context['users'] = users

    else:
        # USER biasa: bisa tambah jadwal
        if request.method == 'POST':
            form = JadwalImunisasiForm(request.POST)
            if form.is_valid():
                jadwal = form.save(commit=False)
                jadwal.user = request.user
                jadwal.save()
                return redirect('dashboard')  # redirect agar tidak mengirim ulang form
        else:
            form = JadwalImunisasiForm()

        # Tampilkan daftar jadwal user tersebut
        jadwal_list = JadwalImunisasi.objects.filter(user=request.user).order_by('-tanggal')
        context['form'] = form
        context['jadwal_list'] = jadwal_list

    return render(request, 'page/dashboard.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')  # setelah logout, redirect ke halaman login

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        nama = request.POST['nama']  # ambil dari input
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username sudah digunakan.')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.nama = nama  # simpan ke field model
            user.role = 'user'  # set default role
            user.save()
            messages.success(request, 'Registrasi berhasil. Silakan login.')
            return redirect('login')

    return render(request, 'page/register.html')

def toggle_user_status(request, user_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Hanya admin yang dapat mengubah status pengguna.")
    
    user = get_object_or_404(User, id=user_id)

    if user != request.user:
        user.is_active = not user.is_active
        user.save()

    return redirect('dashboard') 

def delete_user(request, user_id):
    if request.method == 'POST':
        if request.user.is_authenticated and request.user.is_superuser:
            user = get_object_or_404(User, id=user_id)
            if user != request.user:
                user.delete()
                messages.success(request, 'User berhasil dihapus.')
            else:
                messages.error(request, 'Tidak bisa menghapus akun Anda sendiri.')
        else:
            messages.error(request, 'Tidak punya izin.')
    return redirect('dashboard')

def view_user_jadwal(request, user_id):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Hanya admin yang dapat melihat jadwal pengguna lain.")
    
    user = get_object_or_404(User, id=user_id)
    jadwal_list = JadwalImunisasi.objects.filter(user=user).order_by('-tanggal')

    context = {
        'target_user': user,
        'jadwal_list': jadwal_list,
    }
    return render(request, 'page/jadwal_user.html', context)



# tabel user semua bang ------------------------------------------
def tambah_jadwal(request):
    if request.method == 'POST':
        form = JadwalImunisasiForm(request.POST)
        if form.is_valid():
            jadwal = form.save(commit=False)
            jadwal.user = request.user
            jadwal.save()
            return redirect('dashboard')
    else:
        form = JadwalImunisasiForm()

    return render(request, 'page/tambah_jadwal.html', {'form': form})

def edit_jadwal(request, jadwal_id):
    jadwal = get_object_or_404(JadwalImunisasi, id=jadwal_id, user=request.user)
    if request.method == 'POST':
        form = JadwalImunisasiForm(request.POST, instance=jadwal)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = JadwalImunisasiForm(instance=jadwal)
    return render(request, 'page/edit_jadwal.html', {'form': form, 'jadwal': jadwal})


def hapus_jadwal(request, jadwal_id):
    jadwal = get_object_or_404(JadwalImunisasi, id=jadwal_id, user=request.user)
    if request.method == 'POST':
        jadwal.delete()
        return redirect('dashboard')
    return render(request, 'page/konfirmasi_hapus.html', {'jadwal': jadwal})
def toggle_status(request, jadwal_id):
    jadwal = get_object_or_404(JadwalImunisasi, id=jadwal_id, user=request.user)
    jadwal.selesai = not jadwal.selesai
    jadwal.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))