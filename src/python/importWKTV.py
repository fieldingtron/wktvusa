#!/usr/bin/env python
import glob, os
import re
import io
import frontmatter
import fnmatch
import random
import datetime
from shutil import copyfile
from urllib.parse import unquote

def is_non_zero_file(fpath):  
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0

def writeToMd(filename,post):
    print("writing to " + filename)
    filez = open(filename, 'w',encoding='utf-8')
    from io import BytesIO
    f = BytesIO()
    frontmatter.dump(post, f)
    doc = f.getvalue().decode('utf-8')
    clean_data = re.sub("(</?strong[^>]*>)", "", doc, 0, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    filez.write(clean_data)
    filez.close()

wdir = 'C:\\Users\\fielding\\Documents\\wktvusa.com\\tmp'

count = 1
os.chdir(wdir)
filePattern = "*.md"

## get .md files recursively and remove slug reference and other tags
for path, dirs, files in os.walk(os.path.abspath(wdir)):
    for filename in fnmatch.filter(files, filePattern):
        filepath = os.path.join(path, filename)
        print("\n\nworking on file " + filepath)
        post = frontmatter.load(filepath)   

        baseContentDir = 'C:\\Users\\fielding\\Documents\\wktvusa.com\\content'
        subContentDir = 'misc'  
        
        ## move the post to the correct location based on their category
        meta = post.metadata
        catz = list(meta['categories'])
        if 'NEWS' in catz:
            print("news alert")
            subContentDir = 'news'

        if 'Washington Today' in catz:
            print('video alert')
            subContentDir = 'videos'

        kdir = unquote(post['permalink'])
        # print(kdir)

        cdir =  baseContentDir + "\\" + subContentDir + "\\" + kdir
        cdir_img = baseContentDir+"\\images"   

        if not os.path.exists(cdir):
            os.makedirs(cdir)
            print("creating " + cdir)

        # if not os.path.exists(cdir_img):
        #     os.makedirs(cdir_img)
        #     print("creating " + cdir_img)



        ## test if import image exists and is non zero
        boolWPimageFound = False
 
        if 'image' in post.keys():              
            imagel = post['image']
            simpleImageName=os.path.basename(imagel)
            dirnamez=os.path.dirname(imagel)
            imgDatePrefix = dirnamez.replace('/wp-content/uploads/','').replace('/','-') + "-"
            # print ("import image is " + imagel)
            # print ("base image name is " + simpleImageName)
            imgdir = 'c:\\Users\\fielding\\Documents\\wktvusa.com\\wordpress-old-vagrant\\public'
            wpimg = imgdir+"\\"+imagel
            boolWPimageFound = is_non_zero_file(wpimg) 
            strIMG =  str(post['image'])
            print("import image file found " + str(boolWPimageFound) + " " + strIMG)
        ## test if featured image exists  ? 
        #featuredimg = cdir_img +"\\" + "featured-" + simpleImageName
        newImgName = imgDatePrefix + str(post['id']) + ".jpg"

        featuredimg = cdir_img +"\\" + newImgName

        #print ("featured image name = "+ featuredimg)
        boolFeaturedimageFound = is_non_zero_file(featuredimg)
        print("featured image file found " + str(boolFeaturedimageFound))

        ## copying image over if needed
        if not boolFeaturedimageFound:
            ## and wp image exists
            if boolWPimageFound:
                print ("copy over featured image")
                copyfile(wpimg, featuredimg)  
                post['imagef'] =  newImgName

        ## remove fields not needed

        post['youtube'] = post['wpzoom_post_embed_code']
        post['imagef'] =  newImgName

        ## clean up unused tags
        removelist = ['slug','wpzoom_post_template','wpzoom_post_embed_location','wpzoom_post_embed_self','wpzoom_post_embed_hd','wpzoom_post_embed_skin','guid',
         'categories','layout','wpzoom_post_embed_code',
        'text-retention','ssl-ports','robotsmeta']
        removelist_len = len(removelist)    
        for i in range(0, removelist_len):
            if removelist[i] in post.keys():
                del post[removelist[i]]
                print("removing " + removelist[i])
        
       
        if post['youtube'] == ['']:
           print ("Empty LIST!")
           del post['youtube']
        else:
            yt = str(post['youtube'])
            print (yt)
            regex = re.compile(r'.+?(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?(?P<id>[A-Za-z0-9\-=_]{11})')
            match = regex.match(yt)
            if not match:
                print('no match')
            else:
                print(match.group('id'))
                post['youtube'] = match.group('id')
                post['youtube-url'] = "https://www.youtube.com/watch?v=" + match.group('id')
        ## rename fields in file
        ## parse youtube URL in video
        ## writing the index.md file there
        writeToMd(cdir+"\\index.md",post)                     