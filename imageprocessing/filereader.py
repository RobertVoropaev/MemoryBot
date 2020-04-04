import Algorithmia

apiKey = 'simIVvEvW9njMmOIYwAtYFdxtFe1'
client = Algorithmia.client(apiKey)

t800File = client.file("data://.algo/deeplearning/ColorfulImageColorization/temp/a006b777f7b74df370efaa0af67ff51f_origin.png").getBytes()
print(t800File)

with open(Э)