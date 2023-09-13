import os
import requests, base64
from django.conf import settings
from django.shortcuts import render, redirect
from websets.forms import audioAccept, CreateUserForm
from websets.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.cache import cache_page
from websets.forms import VideoIdForm  
import requests, time, re, os
from django.http import JsonResponse
from pydub import AudioSegment

@cache_page(60 * 1)

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Congratulations ' + user + '!')

                return redirect('login')  

        context = {'form': form}
        return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
       return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect')

        context = {}
        return render(request, 'loginPage.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


def aiModels(request):
    return render(request, 'aiModel.html')


def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        desc = request.POST['desc']

        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        print("The data has been written to the db")

    return render(request, 'contact.html')


def pricing(request):
    return render(request, 'pricing.html')


def mp3_conversion(video_id, api_key, api_host):
    #Setup own youtube API key 
    api_key = settings.API_KEY 
    api_host = settings.API_HOST
    url = f"https://{api_host}/dl?id={video_id}"

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": api_host
    }

    while True:
        response = requests.get(url, headers=headers)
        fetch_response = response.json()

        if fetch_response["status"] == "processing":
            time.sleep(1)
        else:
            return fetch_response


def extract_video_id(url):
    pattern = r"(?:v=|\/videos\/|embed\/|youtu.be\/|\/v\/|\/e\/|watch\?v=|&v=)([\w-]+)"

    match = re.search(pattern, url)

    if match:
        return match.group(1)
    else:
        return None


def convert_mp3(request):
    if request.method == 'POST':
        form = VideoIdForm(request.POST)
        if form.is_valid():
            youtube_url = form.cleaned_data['video_id']
            if not youtube_url.strip():
                return render(request, 'conversion.html', {'success': False, 'message': 'Please enter a YouTube link'})

            video_id = extract_video_id(youtube_url)
            if video_id:
                api_key = settings.API_KEY
                api_host = settings.API_HOST

                response = mp3_conversion(video_id, api_key, api_host)

                if response.get('status') == 'ok':
                    song_title = response.get('title')
                    song_link = response.get('link')
                    converted_audio_url = response.get('converted_audio_link')

                    try:
                        response_head = requests.head(song_link)
                        file_size_bytes = int(response_head.headers['Content-Length'])
                        file_size_mb = file_size_bytes / (1024 * 1024)
                    except:
                        file_size_mb = None
                    
                    return render(request, 'conversion.html', {'success': True,
                                                             'song_title': song_title,
                                                             'song_link': song_link,
                                                             'file_size_mb': file_size_mb,
                                                             'converted_audio_url': converted_audio_url})
                else:
                    error_message = response.get('msg')
                    return render(request, 'conversion.html', {'success': False, 'message': error_message})
                  
    form = VideoIdForm(request.POST)
    if form.is_valid():
        youtube_url = form.cleaned_data['video_id'] 
       
        video_id = extract_video_id(youtube_url)
        
        if video_id:
            api_key = settings.API_KEY
            api_host = settings.API_HOST

            response = mp3_conversion(video_id, api_key, api_host)

            if response.get('status') == 'ok':
                return render(request, 'conversion.html', {'success': True,
                                                         'song_title': response.get('title'),
                                                         'song_link': response.get('link')})
            else:
                return render(request, 'conversion.html', {'success': False, 'message': 'Invalid YouTube URL'})
    else:
        form = VideoIdForm()

    return render(request, 'conversion.html', {'form': form})


def download_converted_audio(request):
    if request.method == 'POST':
        converted_audio_url = request.POST.get('converted_audio_url')
        if converted_audio_url:
            
            save_path = os.path.join(settings.MEDIA_ROOT, 'accepted_audio')
            os.makedirs(save_path, exist_ok=True)

            file_name = f'converted_audio_{int(time.time())}.mp3'
            file_path = os.path.join(save_path, file_name)

            response = requests.get(converted_audio_url)
            if response.ok:
                with open(file_path, 'wb') as f:
                    f.write(response.content)

                success_message = "File Grabbed Successfully and is ready for conversion."

                return render(request, 'conversion.html', {'success_message': success_message})
            else:
                return JsonResponse({'message': 'Failed to download the file'})
        else:
            return JsonResponse({'message': 'No converted audio URL provided'})


def conversion(request):
    if request.method == 'POST':
        form = audioAccept(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.cleaned_data['Audio_File']
            
            uploaded_file_path = os.path.join(settings.MEDIA_ROOT, 'accepted_Audio')
            os.makedirs(uploaded_file_path, exist_ok=True)
            file_name = uploaded_file.name
            file_path = os.path.join(uploaded_file_path, file_name)

            with open(file_path, 'wb') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            uvr_api_url = "http://localhost:7865/run/uvr_convert"
            audio_data = uploaded_file.read()
            base64_audio_data = base64.b64encode(audio_data).decode('utf-8')
            vocal_output_folder = os.path.join(settings.MEDIA_ROOT, 'vocals_Audio')
            os.makedirs(vocal_output_folder, exist_ok=True)
            instru_output_folder = os.path.join(settings.MEDIA_ROOT, 'instru_Audio')
            os.makedirs(instru_output_folder, exist_ok=True)

            payload = {
                "data": [
                    "Hp2_all_vocals",
                    uploaded_file_path,
                    vocal_output_folder,
                    {"name": "uploaded_audio.wav", "data": f"data:@file/octet-stream;base64,{base64_audio_data}"},
                    instru_output_folder,
                    "10",
                    "wav"
                ]
            }
            
            uvr_response = requests.post(uvr_api_url, json=payload).json()
            data = uvr_response["data"]
            
            ai_model = request.POST.get('ai_model')  

            dropdown_api_url = "http://localhost:7865/run/infer_set"
            payload = {
                "data": [
                    ai_model,
                    0.33,
                    0.33,
                ]
            }
           
            dropdown_response = requests.post(dropdown_api_url, json=payload).json()
            dropdown_data = dropdown_response["data"]

            audio_files = []
           
            files = os.listdir(vocal_output_folder)
            
            for file in files:
                if file.endswith(".wav"):
                    audio_files.append(file)

            if audio_files:
                selected_audio_file = audio_files[0]
               
                selected_audio_file_path = os.path.join(vocal_output_folder, selected_audio_file)
                
                convert_api_url = "http://localhost:7865/run/infer_convert_batch"
                with open(selected_audio_file_path, 'rb') as selected_audio_file:
                    vocal_audio_data = selected_audio_file.read()

                base64_vocal_audio_data = base64.b64encode(vocal_audio_data).decode('utf-8')
                converted_output_folder = os.path.join(settings.MEDIA_ROOT, 'converted_Audio')
                os.makedirs(converted_output_folder, exist_ok=True)

                payload = {
                    "data": [
                        0,
                        vocal_output_folder,
                        converted_output_folder,
                        {"name": "uploaded_audio.wav",
                         "data": f"data:@file/octet-stream;base64,{base64_vocal_audio_data}"},
                        0,
                        "rmvpe",
                        "hello world",
                        "logs/guanguanV1.index",
                        1,
                        3,
                        0,
                        1,
                        0.33,
                        "mp3",
                    ]
                }
                
                response = requests.post(convert_api_url, json=payload).json()
                converted_data = response["data"]

                context = {
                    'form': form,
                    'uploaded_file_name': uploaded_file.name if uploaded_file else None,
                    'processed_data': data,
                    'converted_data': converted_data,
                }

                os.remove(file_path)             
                return redirect('combine')

    else:
        form = audioAccept()

    context = {'form': form}
    return render(request, 'conversion.html', context)


def combine(request):
    input_directory_vocal = os.path.join(settings.MEDIA_ROOT, 'converted_Audio')
    input_directory_instru = os.path.join(settings.MEDIA_ROOT, 'instru_Audio')

    vocals_audio = AudioSegment.from_file(os.path.join(input_directory_vocal, "vocal_Dougie.wav_10.wav.wav"))
    instrumental_audio = AudioSegment.from_file(os.path.join(input_directory_instru, "instrument_Dougie.wav_10.wav"))

    min_length = min(len(vocals_audio), len(instrumental_audio))
    vocals_audio = vocals_audio[:min_length]
    instrumental_audio = instrumental_audio[:min_length]

    combined_audio = vocals_audio.overlay(instrumental_audio)

    output_directory = os.path.join(settings.MEDIA_ROOT, 'combined_Audio')

    os.makedirs(output_directory, exist_ok=True)

    output_file_path = os.path.join(output_directory, "combined.mp3")
    combined_audio.export(output_file_path, format="mp3")
    
    return redirect('list_and_download_audio')


def list_and_download_audio(request):
    audio_dir = os.path.join(settings.MEDIA_ROOT, 'combined_audio')

    audio_files = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.mp3')]

    download_links = []
    for audio_file in audio_files:
        audio_path = os.path.join(audio_dir, audio_file)
        download_links.append({'filename': audio_file, 'url': audio_path})

    return render(request, 'player.html', {'download_links': download_links})