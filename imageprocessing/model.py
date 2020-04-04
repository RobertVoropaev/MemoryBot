import Algorithmia

apiKey = 'simIVvEvW9njMmOIYwAtYFdxtFe1'
client = Algorithmia.client(apiKey)

model = 'deeplearning/ColorfulImageColorization/1.1.13'
algo = client.algo(model)

img_local_url = "data_in/origin.jpg"
file = client.file("data://.my/" + img_local_url).putFile(img_local_url)

input = {"image": image_url}
 print(algo.pipe(input).result['output'])