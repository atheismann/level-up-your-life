from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Journal
from django.views.generic import DetailView
from django.http import HttpResponse

S3_BASE_URL = 'https://s3.us-east-2.amazonaws.com/'
BUCKET = 'levelupyourlife-aplha'
# Define the home view
def home(request):
  return HttpResponse('<h1>Welcome to Level Up Your Life!</h1>')

class JournalCreate(CreateView):
  model = Journal
  fields = ['title', 'author', 'about']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class JournalUpdate(UpdateView):
  model = Journal
  fields = ['title', 'author', 'about']

class JournalDelete(DeleteView):
  model = Journal
  success_url = '/journals/'

def journals_index(request):
  journals = Journal.objects.all()
  return render(request, 'journals/index.html', { 'journals': journals })

def journals_detail(request, journal_id):
  journal = Journal.objects.get(id=journal_id)
  return render(request, 'journals/detail.html', {
    'journal': journal,
  })

def about(request):
  return render(request, 'about.html')

def add_attachment(request, post_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
          s3.upload_fileobj(photo_file, BUCKET, key)
          url = f"{S3_BASE_URL}{BUCKET}/{key}"
          photo = Photo(url=url, post_id=post_id)
          photo.save()
      except:
          print('An error occurred uploading file to S3')
  return redirect('detail', post_id=post_id)