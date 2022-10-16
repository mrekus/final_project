# final_project
Norint siųsti užsakymus į paštą reikia config.ini suvesti paštą kam norima siųsti, bei iš kokio pašto, įvedus paštą, bei sugeneruotą gmail app id.

Programoje naudojamos technologijos:
* Tkinter
* SQLAlchemy

Programa skirta gamybos pajėgumo, žaliavų, produktų bei užsakymų sekimui. Užsakymų pridėjimui, bei istorijai.

Paleidus programą sukuriami visi pagrindiniai programos laukai, programa kreipiasi į API ir iš config.ini esančių valiutų porų paima dabartinį kursą su EUR. Jei API neveikia ar config.ini suvesti blogi duomenys užkrauna tik default EUR. Į kairėje pusėje esantį combobox sudedami visi užkrauti kursai, pats combobox read-only. Ant visų meniu mygtukų sudedmas spalvų pasikeitimas ant jų užvedus pelę. Meniu scroll mygtukai kurie keičia meniu mygtukus ir automatiškai išsijungia pasiekus meniu viršų ar apačią. Viršuje kontekstinis menu, su kuriuo galima atstatyti pradinę programos būseną, arba išeiti iš programos.

![image](https://user-images.githubusercontent.com/113506949/196032326-06a232ad-f855-4ad5-aa3d-52495bb7794a.png)

## 1) Process:

Paspaudus <ins>Process</ins> mygtuką sukuriama treeview lentelė su duomenų bazės Process lentelės duomenimis, įrašų pasirinkimas ribojamas iki 1. Sukuriamas Edit ir išjungtas Delete mygtukai.

![image](https://user-images.githubusercontent.com/113506949/196007216-82889608-d7f9-472e-aeb0-b65532922424.png)
	
- Paspaudus <ins>Edit</ins> mygtuką nepasirinkus įrašo į <ins>Project_error_log</ins> failą įrašomas warning, jog bandoma editinti nepasirinkus įrašo. Paspaudus <ins>Edit</ins> mygtuką pasirinkus įrašą to įrašo ID paimamas į atmintį su kintamuoju, užkraunami 3 entry fields ir 3 labels. Į entry fields iš kart įrašomi dabartiniai pasirinkto įrašo duomenys. Pačio <ins>Edit</ins> mygtuko tekstas pakeičiamas į <ins>Save changes</ins>, o funkcija pakeičiama į įrašo išsaugojimą. Pridedmas <ins>Cancel</ins> mygtukas. Mygtuko <ins>Save changes</ins> pelės užvedimo spalvos pasikeitimas pakeičiamas į žalią, o mygtuko <ins>Cancel</ins> į raudoną.

	![image](https://user-images.githubusercontent.com/113506949/196007232-6346ac99-9582-4ef4-8f0c-af8a7741340b.png)

- Paspaudus <ins>Save changes</ins> yra tikrinami įrašai iš entry fields. Tikrinamas ar įrašas <ins>Name</ins> yra originalus - su .strip() pašalinami trailing ir leading spaces, su regex pasikartojantys tarpai keičiami į vienus, tada ignoruojant case su .lower() lyginama su duomenų bazės process įrašais. Jei randamas sutapimas, kviečiama <ins>ErrorWindow</ins> klasė kuri iššaukia Error langą, ir įrašymas yra atmetamas. Įrašas su savim nelyginamas, ir galima keisti tik jo šriftą. Tokie patys tikrinimai atliekami <ins>Material</ins> laukui lyginant įrašą su duomenų bazės <ins>Materials</ins> įrašais. <ins>Efficiency</ins> lauke tikrinama ar skaičius yra teigiamas ir ar didesnis už 0. Jei ne kviečiamas atitinkamas Error ir įrašymas yra atmetamas. Praėjus visus patikrinimus <ins>Name</ins> ir <ins>Efficiency</ins> pakeičiami duomenų bazės <ins>Process</ins> lentelėje, <ins>Material</ins> <ins>Materials</ins> lentelėje. Atstatomas <ins>Edit</ins> mygtukas, pašalinamas <ins>Cancel</ins> mygtukas, atnaujinama lentelė.

- Paspaudus <ins>Cancel</ins> mygtuką pašalinami ir išvalomi visi <ins>Edit</ins> sukurti laukai, grąžinamas <ins>Edit</ins> mygtuko tekstas bei funkcija.

## 2) Recipies:

Paspaudus <ins>Recipies</ins> mygtuką sukuriama treeview lentelė su duomenų bazės <ins>Recipies</ins> lentelės duomenimis (materials kiekiai yra vieneto dalimis), įrašų pasirinkimo kiekis ribojamas iki 1. Tikrinamas įrašų kiekis. Lentelėje talpinami 8 įrašai, jei įrašų yra daugiau nei 8 - pridedamas scrollbar lentelės dešinėje pusėje. Aktyvuojamas <ins>Delete</ins> mygtukas ir nuspalvinamas raudonai. Pridedami <ins>Edit</ins> ir <ins>Add Recipe</ins> mygtukai.

![image](https://user-images.githubusercontent.com/113506949/196007240-64eee697-f895-4fb7-b675-c59352115f2d.png)

- Paspaudus <ins>Edit</ins> mygtuką nepasirinkus įrašo į <ins>Project_error_log</ins> failą įrašomas warning, jog bandoma editinti nepasirinkus įrašo. Paspaudus <ins>Edit</ins> mygtuką pasirinkus įrašą to įrašo ID paimamas į atmintį su kintamuoju, užkraunami 6 entry fields ir 6 labels. Į juos įrašomi dabartiniai įrašo duomenys. Pačio <ins>Edit</ins> mygtuko tekstas pakeičiamas į <ins>Save changes</ins>, o funkcija pakeičiama į įrašo išsaugojimą. Pridedamas <ins>Cancel</ins> mygtukas. Išjungiamas <ins>Delete</ins> mygtukas. Mygtuko <ins>Save changes</ins> pelės užvedimo spalvos pasikeitimas pakeičiamas į žalią, o mygtuko <ins>Cancel</ins> į raudoną.

	![image](https://user-images.githubusercontent.com/113506949/196007244-ea94d7d6-5457-4c9e-922d-b0714e88bfeb.png)

- Paspaudus <ins>Save changes</ins> mygtuką <ins>Name</ins> laukas tikrinamas tokiu pačiu principu kaip ir <ins>Process</ins> lentelėje. Kiti laukai tikrinami ar yra teigiami, ar mažiau arba lygūs 1, ir ar jų suma lygi 1. Leidžiama nedidelė 0.0004 paklaida iki 1. Jei tikrinimai praeina, įrašas yra redaguojamas duomenų bazėje pagal ankščiau paimta įrašo ID. Atstatomi <ins>Edit</ins>, <ins>Add Recipe</ins> bei <ins>Delete</ins> mygtukai, atnaujinama lentelė, atnaujinamas <ins>Add an Order</ins> receptų pasirinkimo combobox.

- Paspaudus <ins>Cancel</ins> mygtuką pašalinami ir išvalomi visi <ins>Edit</ins> sukurti laukai, grąžinamas <ins>Edit</ins> mygtuko tekstas bei funkcija, bei <ins>Add Recipe</ins> mygtukas.

- Paspaudus <ins>Add Recipe</ins> mygtuką sukuriami 6 labels bei 6 entry field laukai. Visi tikrinimai atliekami tokie patys kaip ir redaguojant įrašą. Praėjus patikrinimus įrašas įrašomas į duomenų bazės <ins>Recipies</ins> lentelę ir atnaujinama treeview lentelė programoje tikrinant įrašų kiekį. Jei įrašų yra daugiau nei 8 - pridedamas scrollbar lentelės dešinėje pusėje. Mygtuko <ins>Save changes</ins> pelės užvedimo spalvos pasikeitimas pakeičiamas į žalią, o mygtuko <ins>Cancel</ins> į raudoną.

- Paspaudus <ins>Delete</ins> mygtuką nepasirinkus įrašo į <ins>Project_error_log</ins> failą įrašomas warning, jei pasirinktas - pasirinktas įrašas yra ištrinamas ir lentelė atnaujinama tikrinant įrašų kiekį. Jei įrašų yra daugiau nei 8 - pridedamas scrollbar lentelės dešinėje pusėje, atnaujinamas <ins>Add an Order</ins> receptų pasirinkimo combobox..

## 3) Storage:

Paspaudus <ins>Storage</ins> mygtuką sukuriama treeview lentelė su duomenų bazės <ins>Storage</ins> duomenimis. Pridedami <ins>Edit</ins>, bei išjungtas <ins>Delete</ins> mygtukai.

![image](https://user-images.githubusercontent.com/113506949/196007255-d6e9fb21-a59d-413e-b0f5-d3fcb7162e5f.png)

- Paspaudus <ins>Edit</ins> mygtuką nepasirinkus įrašo į <ins>Project_error_log</ins> failą įrašomas warning, jog bandoma editinti nepasirinkus įrašo. Paspaudus <ins>Edit</ins> mygtuką pasirinkus įrašą to įrašo ID paimamas į atmintį su kintamuoju, užkraunami 2 entry fields ir 2 labels. Į entry fields iš kart įrašomi dabartiniai pasirinkto įrašo duomenys. Pačio <ins>Edit</ins> mygtuko tekstas pakeičiamas į <ins>Save changes</ins>, o funkcija pakeičiama į įrašo išsaugojimą. Pridedmas <ins>Cancel</ins> mygtukas. Mygtuko <ins>Save changes</ins> pelės užvedimo spalvos pasikeitimas pakeičiamas į žalią, o mygtuko <ins>Cancel</ins> į raudoną.

	![image](https://user-images.githubusercontent.com/113506949/196007260-e0f12f59-539a-4776-8178-e3f165947913.png)

- Paspaudus <ins>Save changes</ins> mygtuką <ins>Name</ins> bei <ins>Amount</ins> laukai tikrinami tokiu pačiu būdų kaip ir <ins>Process</ins> lentelėje. Praėjus tikrinimus įrašas pagal prieš tai paimtą įrašo ID yra redaguojamas duomenų bazės <ins>Storage</ins> lentelėje. Atstatomas <ins>Edit</ins> mygtukas, pašalinamas <ins>Cancel</ins> mygtukas, atnaujinama lentelė.

- Paspaudus <ins>Cancel</ins> mygtuką pašalinami ir išvalomi visi <ins>Edit</ins> sukurti laukai, grąžinamas <ins>Edit</ins> mygtuko tekstas bei funkcija.

## 4) Materials:

Paspaudus <ins>Materials</ins> mygtuką sukuriama treeview lentelė su duomenų bazės <ins>Materials</ins> duomenimis. Pridedami <ins>Edit</ins>, bei išjungtas <ins>Delete</ins> mygtukai. Lentelės <ins>Price/kg</ins> stulpelis yra automatiškai apsakičiuojamas pagal pasirinktą valiutą. Lentelės atsinaujinimas pririšamas su <ins>Event</ins> prie valiutų combobox pasikeitimo ir pasikeitus įrašui perskaičiuojama kaina.

![image](https://user-images.githubusercontent.com/113506949/196007267-535abdb7-8219-4537-b594-e403df369ee8.png)

- Paspaudus <ins>Edit</ins> mygtuką nepasirinkus įrašo į <ins>Project_error_log</ins> failą įrašomas warning, jog bandoma editinti nepasirinkus įrašo. Paspaudus <ins>Edit</ins> mygtuką pasirinkus įrašą to įrašo ID paimamas į atmintį su kintamuoju, užkraunami 2 entry fields ir 2 labels. Į entry fields iš kart įrašomi dabartiniai pasirinkto įrašo duomenys. Pačio <ins>Edit</ins> mygtuko tekstas pakeičiamas į <ins>Save changes</ins>, o funkcija pakeičiama į įrašo išsaugojimą. Pridedmas <ins>Cancel</ins> mygtukas. Mygtuko <ins>Save changes</ins> pelės užvedimo spalvos pasikeitimas pakeičiamas į žalią, o mygtuko <ins>Cancel</ins> į raudoną.

	![image](https://user-images.githubusercontent.com/113506949/196007275-428ea0aa-a8d5-4ca8-94f1-df2c99ad3fa9.png)

- Paspaudus <ins>Save changes</ins> mygtuką <ins>Name</ins> bei <ins>Amount</ins> laukai tikrinami tokiu pačiu būdų kaip ir <ins>Process</ins> lentelėje. Praėjus tikrinimus įrašas pagal prieš tai paimtą įrašo ID yra redaguojamas duomenų bazės <ins>Storage</ins> lentelėje. Atstatomas <ins>Edit</ins> mygtukas, pašalinamas <ins>Cancel</ins> mygtukas, atnaujinama lentelė.

- Paspaudus <ins>Cancel</ins> mygtuką pašalinami ir išvalomi visi <ins>Edit</ins> sukurti laukai, grąžinamas <ins>Edit</ins> mygtuko tekstas bei funkcija.

## 5) Orders:

Paspaudus <ins>Orders</ins> mygtuką sukuriama treeview lentelė su duomenų bazės <ins>Orders</ins> duomenimis. Pridedamas išjungtas <ins>Edit</ins> mygtukas, išjungtas <ins>Delete</ins> mygtukas, bei <ins>Filter</ins> mygtukas. Užvedus pelę ant <ins>Filter</ins> mygtuko jis nuspalvinamas pilka spalva. Lentelės atsinaujinimas pririšamas prie valiutų combobox pasikeitimo ir kiekvieną kartą pasikeitus atnaujinama lentelė ir perskaičiuojami <ins>Manufacturing cost</ins> ir <ins>Selling price</ins> stulpeliai pagal tos valiutos kursą.

![image](https://user-images.githubusercontent.com/113506949/196007278-4b32c3cb-8150-4ffb-bc57-40ab3bd7c8de.png)

- Paspaudus <ins>Filter</ins> mygtuką pridedamos etiketės bei combobox filtravimui. Į stulpelio <ins>From</ins> combobox sudedama data 2022-01-01, o į stulpelio <ins>To</ins> combobox sudedama dabartinė data kuri atsinaujina automatiškai. Taip pat pridedamas <ins>Period profit</ins> stulpelis kuriame automatiškai apskaičiuojama visos lentelės įrašų <ins>Selling price</ins> - <ins>Manufacturing price</ins>. Visi datų combobox pririšami prie lentelės įrašų atnaujinimo metodo pagal pasirinktą datų ruožą. Kiekvieną kartą pakeitus bet kurį combobox jų vertės paimamos, ir pagal tai dinamiškai išfiltruojami lentelės įrašai, atnaujinamas <ins>Period profit</ins> stulpelis. <ins>Filter</ins> mygtukas pakeičiamas į <ins>Cancel</ins> ir jo pelės užvedimo spalva pakeičiama į raudoną.

	![image](https://user-images.githubusercontent.com/113506949/196007299-b412e31a-f79b-4b38-87b1-3ecdc35d1dce.png)

- Paspaudus <ins>Send to Email</ins> mygtuką visi tuo metu išfiltruoti lentelės įrašai yra sudedami į laišką, kurios <ins>Subject</ins> yra pasirinkta data <ins>From</ins> - <ins>To</ins> iš combobox, o turinys visi lentelės įrašai, bei <ins>Period profit</ins>. Duomenys naudojami siųsti laiškui paimami iš <ins>config.ini</ins> failo įrašant kam siunčiama, bei iš kokio email siunčiama priimant to email login bei gmail app key. Jei laiško išsiųsti nepavyksta metamas <ins>Error</ins> langas.

- Paspaudus <ins>Cancel</ins> mygtuką pašalinami ir išvalomi filtravimo laukai, grąžinamas <ins>Filter</ins> mygtukas ir jo pelės užvedimo spalva, atstatomas išjungtas <ins>Edit</ins> mygtukas.

## 6) Add an Order:

Paspaudus <ins>Add an Order</ins> mygtuką pridedamas combobox kuris yra užpildomas duomenų bazės <ins>Recipies</ins> lentelės pavadinimais, <ins>entry field</ins>, bei du mygtukai <ins>Confirm Order</ins> ir <ins>Cancel Order</ins>.

![image](https://user-images.githubusercontent.com/113506949/196007317-a03ec294-222a-4abe-b9fd-8fc9809c2993.png)

- Paspaudus <ins>Confirm Order</ins> mygtuką yra tikrinama ar į <ins>amount entry field</ins> įrašytas skaičius, tada ar pasirinktas receptas, tada ar įrašytas skaičius didesnis už 0. Jeigu ne, meta atitinkamą error, jei patikrinimai praeina, paimamas receptas pagal pagal combobox pasirinkimą ir pagal receptui reikiamą žaliavų kiekį ir įrašytą užsakymo kiekį skaičiuojama ar užteks žaliavų užsakymui įvykdyti. Jei taip, užsakymas įrašomas į duomenų bazę, į <ins>orders.txt</ins> failą įrašoma užsakymo informacija, iš <ins>Storage</ins> lentelės nurašomi žaliavų kiekiai kurių reikėjo užsakymui įvykdyti, tada tikrinima ar <ins>Mail orders</ins> combobox pasirinkimas yra YES. Jei taip, nusiunčiamas laiškas imant paštą, bei adresatą iš <ins>config.ini</ins> failo, su atlikto užsakymo informacija. Jei žaliavų užsakymui įvykdyti nepakanka, pagal duomenų bazės <ins>Processes</ins> lentelės <ins>efficiency</ins> skaičiuojama kiek darbo valandų reikėtų, kad būtų pagaminta pakankamai žaliavos užsakymui įvykdyti. Tada metamas <ins>Error</ins> langas su šia informacija, įrašomas Error į <ins>Process_error_log failą</ins>.

- Paspaudus <ins>Cancel Order</ins> mygtuką pašalinami sukurti langai, išvalomas <ins>Amount in kg</ins> entry field, bei <ins>Recipe</ins> combobox.
