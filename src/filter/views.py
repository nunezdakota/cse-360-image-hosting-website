from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.core.files import File
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill, Adjust
from django.conf import settings
from django.contrib.auth.models import User
from dragdrop.models import UploadFile

class FilterImg(ImageSpec):
    processors = Adjust(contrast=1.2, sharpness=1.1, brightness =1.3),
    format     = 'JPEG'
    options    = {'quality': 100} 

#should pass a file
def changeBright(request):
    
    print "changeBright request"
    print "\n"
   
    filename = request.GET['iname']
    filename_split = filename.split(request.user.username+"/")
   
    print "\n\n\nthis is filename_split: %s" % filename_split
    print "\n filname_split[-1]: %s" % filename_split[-1]
   
    filename_original = filename_split[-1]

    inameStr = request.GET['iname']
   
    print  inameStr
   
    inameStr= inameStr.split("8000/media")

    # print source to terminal
    print "\n inameStr: %s" % inameStr[-1]
   
    source_file_path =settings.MEDIA_ROOT+inameStr[-1]
   
    print "source_file :%s" % source_file_path  

    # manipulate image here
    source_file = open(settings.MEDIA_ROOT + inameStr[-1], 'r')
    image_generator = FilterImg(source=source_file)
    result = image_generator.generate()

    
    if settings.MEDIA_ROOT+'/user_'+request.user.username + "/" + filename_original:
        filename_original = filename_split[-1].join("_edit")
        print "\n\n\n\n\nthis file name exists"

    dest = file(settings.MEDIA_ROOT+'/user_'+request.user.username +'/'+filename_original, 'w')
    dest.write(result.read())
    dest.close()
  
    new_file = UploadFile(file = 'user_'+request.user.username +'/'+filename_original)
    new_file.user = request.user
    new_file.save()

    # this is to pass in the data into render_to_response
    # data = {'form': form}

    return render_to_response('filter.html', context_instance=RequestContext(request))