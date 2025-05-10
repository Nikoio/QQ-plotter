Ниже представлен формат данных, собранных в этой папке.

Данные представляют собой измерения индукции межпланетного 
магнитного поля и скорости солнечного ветра на аппарате WIND.


Источник данных: портал OmniWeb (https://omniweb.gsfc.nasa.gov/)

Чтобы получить эти и аналогичные данные, заходим в:
	-> OmniWeb
	-> Wind 
	-> 1-min, magnetic field and plasma,BSN-shifted 
	-> Plots, listings, subsetted files (откроется сайт: https://omniweb.gsfc.nasa.gov/form/sc_merge_min1.html)
	-> выбираем пункты:
		- Create File
		- 1-min averaged
		- даты начала и конца выборки. Для файла YYYY.txt соответственно YYYY0101-YYYY1231
		- интересующие величины. Для всех файлов это:
			- Scalar B, nT
			- BX, nT (GSE, GSM)
			- BY, nT (GSE)
			- BZ, nT (GSE)
			- Flow speed, km/s
			- Vx Velocity, km/s, GSE
			- Vy Velocity, km/s, GSE
			- Vz Velocity, km/s, GSE
	-> Нажимаем Submit

На выхоте получаем два файла:
	- непосредственно таблица с данными в файле расширения .lst (это просто текст, тоже самое, что и .txt)
	- файл, описывающий формат таблицы, расширения .fmt (пример файла для всех годовых таблиц представлен ниже)

--------------
Пример .fmt файла для всех годовых таблиц
--------------

  FORMAT OF THE SUBSETTED FILE
    
    ITEMS                      FORMAT   
     
 1 Year                          I4        
 2 Day                           I4        
 3 Hour                          I3        
 4 Minute                        I3        
 5 Scalar B, nT                  F8.2      
 6 BX, nT (GSE)                  F8.2      
 7 BY, nT (GSE)                  F8.2      
 8 BZ, nT (GSE)                  F8.2      
 9 Flow speed, km/s              F8.1      
10 Vx Velocity, km/s, GSE        F8.1      
11 Vy Velocity, km/s, GSE        F8.1      
12 Vz Velocity, km/s, GSE        F8.1      
