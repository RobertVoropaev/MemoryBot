import Algorithmia

apiKey = 'simIVvEvW9njMmOIYwAtYFdxtFe1'
client = Algorithmia.client(apiKey)


dir =  client.dir("data://.algo/deeplearning/ColorfulImageColorization/temp/")

for file in dir.files():
    print(file.url)
    t800File = client.file("data://.my/robots/T-800.png").getFile()