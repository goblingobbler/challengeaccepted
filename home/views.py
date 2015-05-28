from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from models import Challenge, Comments

from django.core.signals import request_finished
import django.dispatch
from django.dispatch import receiver

import threading
import time
# Create your views here.

import logging
logger = logging.getLogger('')

def index(request):
    return render(request, 'index.html', {})

def challenges(request):

    objs = Challenge.objects.all()

    return render(request, 'challenge_outer.html', {'objs': objs})

def filter(request):
    objs = Challenge.objects.all()

    return render(request, 'challenge_inner.html', {'objs': objs})


def edit(request):
    if request.method == 'POST':
        title = request.POST['title']
        desc = request.POST['desc']

        ch = Challenge(title = title, desc = desc)
        ch.save()

        return HttpResponseRedirect(reverse('challenges'))

    return render(request, 'edit_form.html')

def comment(request, id):
    if request.method == 'POST':
        link = request.POST['link']
        desc = request.POST['desc']
        ch = Challenge.objects.filter(pk = id).first()
        
        [link, valid] = validateLink(link)
        
        com = Comments(challenge = ch, link = link, desc = desc, valid_video = valid)
        com.save()
        
        return HttpResponseRedirect(reverse('challenge', args=[id]))

    return render(request, 'comment_form.html')

def viewchallenge(request, id):
    ch = Challenge.objects.filter(pk = id).first()
    
    if 'c' in request.GET:
        com = get_object_or_404(Comments, pk=reqeust.GET['c'])
        
        return render(request, 'comment_view.html', {'challenge':ch, 'comment':com})
    
    else:
        return render(request, 'challenge.html', {'challenge':ch})



def validateLink(link):
    str = ''
    if 'iframe' in link:
        #<iframe width="560" height="315" src="https://www.youtube.com/embed/eytE4BU9Atk" frameborder="0" allowfullscreen></iframe>
        for row in link.split(' '):
            if 'src' in row and 'youtube' in row:
                str = row.replace('"','').split('/')[-1]
                
    elif 'youtube' in link:
        if 'watch' in link:
            for row in link.split('?')[-1].split('&'):
                if 'v' == row.split('=')[0]:
                    str = row.split('=')[-1]
        else:
            str = link.split('/')[-1]
    elif 1 not in [c in link for c in ['&','/','?','=']]:
        str = link
        
    
    if str != '':
        return [str,True]
    else:
        return [str,False]
    
    

'''

def score(request, address):
    city = address.split(',', 1)[1]
    address = address.split(',', 1)[0]
    
    metric_list = ['QUALITY','CUISINE VARIETY','PROXIMITY','PRICE VARIETY']
    
    if request.method == 'POST':
        #Call score generator here
        lat = request.POST['lat']
        lng = request.POST['lng']
        
        metrics = {}
        for row in ScoreType.objects.all():
            if row.title in request.POST:
                metrics[row.title] = float(request.POST[row.title])
            else:
                metrics[row.title] = 1
        
        logger.warning(address)
        
        
        test_address = Address.objects.filter(address = address, city = city).last()
        if not test_address or test_address.completed == False:
            if not test_address:
                test_address = Address(address = address, city = city, lat = lat, lng = lng)
                test_address.save()
            
                ScoreThread(test_address,metrics).start()
            #compute_async.send('Address', lat=lat, lng=lng, address=address, city=city, metrics=metrics)
            
            return render(request, 'fail.html', {})
            
        else:
            group = ScoreGroup.objects.filter(max_score__gt = test_address.finalscore()).first()
            
            return render(request, 'score.html', {'test_address':test_address, 'group':group, 'lat':lat, 
                'lng':lng, 'address':address, 'city':city, 'metric_list':metric_list})
    
    else:
        score = {}
        test_address = Address.objects.filter(address = address, city = city).first()
        if test_address:
            for row in test_address.addressscore_set.all():
                score[row.type.title] = row.score
        
        return render(request, 'score_container.html', {'test_address':test_address, 'lat':test_address.lat, 
                                                        'lng':test_address.lng, 'address':address, 'city':city})

    

    
#@receiver(compute_async)
#def computeAsyncScore(sender, **kwargs):
    
class ScoreThread(threading.Thread):
    def __init__(self, address, metrics):
        self.address = address
        self.metrics = metrics
        
        super(ScoreThread, self).__init__()

    def run(self):
        # long running code here
        f = open('score_log.txt', 'a')
        start_time = time.time()
        
        f.write('START: ' + str(time.time() - start_time) + ', ')
        
        score = {}
        raw,restaurants = calcscore(float(self.address.lat), float(self.address.lng), f, start_time)
        
        f.write('SCORE RETURNED: ' + str(time.time() - start_time) + ', ')
        
        score_types = {'final':'final_score','rating':'Nd','price':'Vt_price',
                       'variety':'Vt_cat','distance':'Qd'}
        for key in score_types:
            score[key] = raw[score_types[key]][0] * self.metrics[key]
        
        self.address.score_title = raw['Nat_A'][0]
        self.address.score_desc = raw['Nat_B'][0]
        
        for row in ScoreType.objects.all():
            a = AddressScore(address = self.address, type = row, score = score[row.title], weight = self.metrics[row.title])
            a.save()
        
        f.write('SCORES SAVED: ' + str(time.time() - start_time) + ', ')
        
        ts = []
        for i in restaurants['id']:
            res = Restaurant(owner = self.address, title = restaurants['name'][i], address = restaurants['google_address'][i], 
                        lat = restaurants['lat'][i], lng = restaurants['lon'][i], google_id = restaurants['place_id'][i])
            
            res.save()
            t = ImageThread(res)
            t.start()
            ts.append(t)
            
        for t in ts:
            t.join()
        
        self.address.completed = True
        self.address.save()
        
        f.write('ADDRESS COMPLETED: ' + str(time.time() - start_time) + ', ')
        f.write('\n')
        f.close()
        
    
class ImageThread(threading.Thread):
    def __init__(self, res):
        self.res = res
        super(ImageThread, self).__init__()

    def run(self):
        self.res = get_photos(self.res)
        self.res.save()
        
'''
    
    