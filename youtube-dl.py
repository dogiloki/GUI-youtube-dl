from youtube_dl import YoutubeDL
dl_opts={}
with YoutubeDL(dl_opts) as dl:
    #features=dl.extract_info("https://www.facebook.com/IMVENOM27/videos/829189487797017/",download=False)
    features=dl.extract_info("https://www.youtube.com/watch?v=NJzoBmVPeYw",download=False)
    print(features['formats'][0])