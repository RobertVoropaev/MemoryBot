## MemoryBot
MemoryBot - чат-бот ВКонтакте, который позволяет удивительно легко и быстро загружать фотографии своих родственников-героев Великой отечественной войны на сайт "Дорога Памяти" и делиться историей их подвига с окружающими в сети ВКонтакте. Сервис предоставляет возможности по поиску и добавлению дополнительной информации о подвиге народа и позволяет оживить фотографии с помощью улучшения качества и превращения черно-белых изображений в цветные.
Мы считаем, что это позволит миллионам людей увековечить подвиги их близких!

## VK Bot Demo
<p align="center"><img src="vk-bot-demo.gif" width="320"></p>

## Обработка изображений
### Модуль Colorization
<table>
   <tr>
    <th>До</th>
    <th>После</th>
    <th>До</th>
    <th>После</th>
   </tr>
   <tr>
     <td><img src="/imageprocessing/colorization-example/1.jpg" width="200"></td>
     <td><img src="/imageprocessing/colorization-example/2.jpg" width="200"></td>
     <td><img src="/imageprocessing/colorization-example/3.jpg" width="200"></td>
     <td><img src="/imageprocessing/colorization-example/4.jpg" width="200"></td>
  </tr>
</table>

### Модуль шумоподавления
<img src="/imageprocessing/denoize-example/denoize-example.jpg" width="604">

### Модуль валидации
<table>
   <tr>
      <th><img src="/imageprocessing/validation-example/military_uniform.jpeg" width="150"></th>
      <th>
         military_uniform: 0.90626603<br>
         pickelhaube: 0.08267837<br>
         bearskin: 0.010410854
      </th>
      <th><img src="/imageprocessing/validation-example/military_uniform_2.jpeg" width="150"></th>
      <th>
         military_uniform: 0.036771357<br>
         assault_rifle: 0.3407515<br>
         rifle: 0.27693072
      </th>
      <th><img src="/imageprocessing/validation-example/suit.jpeg" width="150"></th>
      <th>
         suit: 0.68397385<br>
         bassoon: 0.039434254<br>
         cornet: 0.03742094
      </th>
   </tr>
</table>

## Команда MemTeam
* Роберт Воропаев
* Шуана Пирбудагова
* Mikhail Kuznetsov
* Mariia Rumiantceva
* Владимир Филинов
