import os
import falcon
import mimetypes
from wsgiref import simple_server
from os import walk
import subprocess


def cutVideo(id, cut, path, duration):	
	def formatRec(path):
		file=path.split("/")
		ext=file[len(file)-1].split(".")
		return ext[len(ext)-1]
	def countVideos(path):
		videos=[]
		for (dirpath, dirnames, filenames) in walk(path):
		    videos.extend(filenames)
		return len(videos)
	def createFolder(path):
		if not os.path.exists(path):
			os.mkdir(path , 0755 );
	def findVideo(path,id):		
		videos=[]
		for (dirpath, dirnames, filenames) in walk(path):
		    videos.extend(filenames)
		for i in range(0,len(videos)):
			video=videos[i].split(".")			
			if video[0]==id:						 
				fin=path+".".join(video)
				return fin
		return None

	path=path.replace("\\","/")	
	path=path+"/"
	fin=findVideo(path,id)	
	if fin==None:
		return "Failed Request your video doesn't exist!"
	else:
		ext=formatRec(fin)		
		fout=path+"Processed/"
		createFolder(path+"Processed/")
		createFolder(path+"Processed/"+id+"/")
		fout=path+"Processed/"+id+"/action_"+str(countVideos(path+"Processed/"+id+"/"))+"."+ext	
		start=float(cut)-(int(duration)/2)		
		cut="ffmpeg -ss "+ str(start) +" -i " + fin + " -t " + str(duration)+" -c copy "+fout		
		process = subprocess.Popen(cut.split(), stdout=subprocess.PIPE)
		output = process.communicate()[0]
		return "Your video has been cutted!"

	path=rep.replace("\\","/")
	html=head(html)
	html=body(html,getSubdir(path+"Processed"),path,getVideos(path))
	writeHtml(html)
	return html


class Cut:
    def on_get(self, req, res, id, cut, rep, duration):
        res.status = falcon.HTTP_200                     
        res.body = cutVideo(id,cut,rep,duration)


app = falcon.API()
app.add_route("/cut&id={id}&cut={cut}&rep={rep}&dur={duration}", Cut())


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8000
    httpd = simple_server.make_server(host, port, app)
    print "Serving on %s:%s" % (host, port)
    httpd.serve_forever()
