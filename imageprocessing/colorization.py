import Algorithmia

apiKey = 'simIVvEvW9njMmOIYwAtYFdxtFe1'
client = Algorithmia.client(apiKey)

model = 'deeplearning/ColorfulImageColorization/1.1.13'
algo = client.algo(model)

image_url = "https://roadheroes.storage.yandexcloud.net/a006b777f7b74df370efaa0af67ff51f_origin.jpg"
input = {"image": image_url}
print(algo.pipe(input).result['output'])