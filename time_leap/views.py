from django.shortcuts import render
from django.http import HttpResponse
import os
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
from .siggraph17 import *
from .util import *
import time
import os

os.environ['KMP_DUPLICATE_LIB_OK']='True'


# Create your views here.

def index(request):
    return HttpResponse("Hello world !!!")


def image_upload(request):
    image_dict = {'image_uploads': False,"upload_image":{"url":""},"iscolored":False, "initialLoad":None, 'img_size':0}
    if request.method=='POST':
        image_files = request.FILES
        image = image_files["imagefile"]
        directory = os.getcwd()
        filedir=directory + '/static/images/'+image.name
#         filedir= 'static/images/'+image.name

        fs = FileSystemStorage()
        filename = fs.save(filedir, image)
        print("***********************************************************************")
        # print("image",image.name,filedir,image_list[0].upload_image.name)
        test=colorizer(filedir,image.name)
        if test:
            image_dict['image_uploads']=True
            image_dict['iscolored']=True
            image_dict['upload_image']['url']="http://127.0.0.1:8080/static/img_out/"+"siggraph17_"+image.name
            image_dict['img_size'] = int(os.path.getsize("static/img_out/"+"siggraph17_"+image.name)/1024)
            image_dict['initialLoad']=False
            return render(request, 'index.html',context=image_dict)
        print("***********************************************************************,test",test)
    else:
        image_dict['initialLoad']=True

    return render(request, 'index.html',context=image_dict)



def colorizer(img_path,name):
    time.sleep(5)
    try:
        colorizer_siggraph17 = siggraph17(pretrained=True).eval()
        img = load_img(img_path)
        (tens_l_orig, tens_l_rs) = preprocess_img(img, HW=(256,256))
        # tens_l_rs = tens_l_rs.cuda()
        img_bw = postprocess_tens(tens_l_orig, torch.cat((0*tens_l_orig,0*tens_l_orig),dim=1))
        out_img_siggraph17 = postprocess_tens(tens_l_orig, colorizer_siggraph17(tens_l_rs).cpu())

        directory = os.getcwd()
        imgoutput=directory + '/static/img_out/'+"siggraph17_"+name
        plt.imsave(imgoutput, out_img_siggraph17)
        return True
    except Exception as e:
        print("error:",str(e))
        return False
