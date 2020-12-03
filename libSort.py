null = None
#основний алгоритм
def LibrarySort(arr, rebalance_local=True):
	#Локальне (True) чи повне (False) перебалансування
		
	global arr_new#допоміжний масив
		
	e = 3#у скільки разів допоміжний масив більший основного
	#print(e, rebalance_local, 'modified')
	#Локальне (True) чи повне (False) перебалансування
	#створюємо допоміжний масив
	newSize = e * (len(arr) + 1) - 1
	arr_new = [null for i in range(newSize)]
		
	#Перший елемент переносимо в середину доп. мас.
	arr_new[LibrarySort_Pos(1, 1, newSize)] = arr[0]
		
	#Починаючи з другого ел. шукаємо місце вставки 
	#та переносимо в доп. мас.
	start = 0
	finish = newSize - 1
	i = 1
	#Перебираємо по порядку ел. осн. мас.
	while(i < len(arr)) :
		#бінарним пошуком шукаємо місце вставки в доп. мас.
		pos = LibrarySort_BinarySearch(arr[i], start, finish, newSize)
		if(pos == False) :#не знайшли точку вставки
			#повне перебалансування
			LibrarySort_Rebalance_Total_Modified(i, newSize)#####################################################################################################################
			#LibrarySort_Rebalance_Total(i, newSize)#####################################################################################################################
		else :#перевіряємо, чи вільна точка вставкиа
			if(arr_new[pos] != null) :#Точка вставки зайнята
				if(rebalance_local) :#Локальне перебалансування (+ вставка)
					LibrarySort_Rebalance_Local(arr[i], pos, newSize)
					i += 1
				else :#Повне перебалансування
					LibrarySort_Rebalance_Total_Modified(i, newSize)#####################################################################################################################
					#LibrarySort_Rebalance_Total(i, newSize)#####################################################################################################################
				
			else :#точка вставки вільна, просто вставляємо
				arr_new[pos] = arr[i]
				i += 1
			
	#переносимо з доп.мас. в основний
	pos = 0
	for i in range(0, newSize):
		if(arr_new[i] != null):
			arr[pos] = arr_new[i]
			pos += 1
		
	return arr


#############################################################
# Позиція number-го елемента з наявних count
# у допоміжному масиві після перебалансування
#number - який за рахунком в масиві (з початку) елемент
#count - скільки на даний момент перенесено елементів
#newSize - повний розмір допоміжного масиву
#number <= count <= count (arr) <= newSize)
def LibrarySort_Pos(number, count, newSize):
	return number * (newSize + 1) // (count + 1) - 1

#############################################################
#бінарний пошук місця вставки в допоміжному масиві
#search - значення елемента з основного масиву, який потрібно перенести в допоміжний
# (Start, finish) - крайні індекси діапазону, в якому відбувається пошук
#newSize - повний розмір допоміжного масиву
def LibrarySort_BinarySearch(search, start, finish, newSize) :
	
	global arr_new#доп. мас.

    #пошук у лівій частині

    # На лівій межі діапазону повинен знаходитися елемент, а не порожня клітинка
    # Звужуємо зліва діапазон, якщо на лівому краю порожні елементи
	while(arr_new[start] == null and start < newSize - 1) :
		start += 1

    # Якщо на кордоні такого ж значення елемент що і шуканий, то потрібно вставити відразу за ним або перед ним
	if(search == arr_new[start]) :
		return LibrarySort_PosNearby(start, newSize)
    # Може зустрітися випадок, коли шуканий елемент менше ніж ліва межа
	elif(search < arr_new[start]) :
        # Тоді шуканому елементу місце між лівою межею і початком додаткового масиву
		if(start > 0) :#Перед start є вільне місце
			finish = start
			start = 0
			return (start + finish) // 2
		else :#start == 0, перед ним нічого не вставити
			return start# Якщо не знайшли вільну клітинку, повертаємо тоді непорожню

     # На правій межі діапазону повинен знаходитися елемент, а не порожня клітинка
     # Звужуємо справа діапазон, якщо на лівому краю порожні елементи
	while(arr_new[finish] == null and finish > 0) :
		finish -= 1

    # Якщо на межі такого ж значення елемент що і шуканий, то потрібно вставити відразу за ним або перед
	if(search == arr_new[finish]) :
		return LibrarySort_PosNearby(finish, newSize)
    #Може зустрітися випадок, коли шуканий елемент більше ніж права межа
	elif(search > arr_new[finish]) :
        #Тоді шуканого елементу місце між правою кордоном і кінцем додаткового масиву
		if(finish < newSize - 1) :#Після finish є вільне місце
			start = finish
			finish = newSize - 1
			return (start + finish + 1) // 2
		else :#finish == newSize - 1, після нього нічого не вставити
			return finish#Якщо не знайшли вільну клітинку, повертаємо тоді непорожню

	# Шуканий елемент не збігається з краями,
	# Значить, його потрібно вставити десь всередині діапазону
	# При цьому потрібно перевірити, чи є всередині діапазону ще елементи
	if(finish - start > 1) :#Ділити діапазон має сенс, якщо там мінімум 3 елементи
		middle = (start + finish + 1) // 2 #індекс середини діапазона
		middle_Pos = 0 #Непустую "середину" диапазона пока не нашли
		offset = 0 #Будемо рухатися від точної середини в пошуках непорожньої елемента

		#Отже, рухаємося від середини вліво / вправо, доки не знайдемо непорожній елемент
		while(middle - offset > start and middle_Pos == 0):
			if(arr_new[middle - offset] != null) :
				middle_Pos = middle - offset
			elif(middle + offset < finish and arr_new[middle + offset] != null) :
				middle_Pos = middle + offset

			offset+=1
	
        # Якщо всередині знайшли непорожній елемент, то, в залежності від його значення,
		# Або шукаємо місце біля нього або рекурсивно застосовуємо до лівої чи правої частини діапазону
		if(middle_Pos) :
			if(arr_new[middle_Pos] == search) :
				return LibrarySort_PosNearby(middle_Pos, newSize)
			else :
				if(arr_new[middle_Pos] > search) :
					finish = middle_Pos
				else :#arr_new[middle_Pos] < search
					start = middle_Pos
				
				return LibrarySort_BinarySearch(search, start, finish, newSize)
		else :#middle_Pos == 0 - всередині діапазону (не рахуючи його кордонів) не знайдені непусті елементи
				return middle#Середина такого діапазону - місце, куди можна вставити елемент


	else :#Знайшли мінімальний відрізок, але вільного місця в ньому немає
		return (start + finish) // 2
	
	
	return False#Якщо сюди дісталися, значить бінарний пошук нічого не дав


#############################################################
#якщо при пошуку елемент рівний одному з кінців відрізка
# Якщо елемент дорівнює кінцю відрізка, то ставимо його поруч зліва чи справа
#start - позиція, на якій вже стоїть елемент рівний шуканого
#newSize - повний розмір допоміжного масиву
def LibrarySort_PosNearby(start, newSize) :
	global arr_new#доп. мас.
    #Спочатку спробуємо знайти вільне місце перед елементом
	for left in range(start-1, -1, -1):
		if(arr_new[left] == null) :#порожня клітинка
			return left#вставляємо сюди
		elif(arr_new[left] != arr_new[start]) :#наткнулися на елемент із іншим значенням
			break #зліва вставити не вийде, припиняємо пошук

	#Если не нашли свободного места слева, попробуем поискать справа
	for right in range(start+1, newSize):
		if(arr_new[right] == null) :#порожня клітинка
			return right #вставляємо сюди
		elif(arr_new[right] != arr_new[start]) :#наткнулися на елемент із іншим значенням
			break #Справа вставити не вийде, припиняємо пошук
	return start #Ні зліва, ні справа від кінця відрізка не знайшли місця вставки. Але ми повертаємо хоча б точку, з якої почали пошук

#############################################################
#локальне перебалансування додаткового масиву
#insert - значення, яке треба вставити
#pos - починаючи з якого елементу потрібно зрушити кілька штук вліво або вправо
#newSize - повний розмір допоміжного масиву
def LibrarySort_Rebalance_Local(insert, pos, newSize) :
	global arr_new#доп. мас.
	#Уточнюємо pos для insert, іноді треба трохи лівіше або правіше
	while(pos - 1 >= 0 and arr_new[pos - 1] != null and arr_new[pos - 1] > insert) :
		pos -= 1
	while(pos + 1 <= newSize - 1 and arr_new[pos + 1] != null and arr_new[pos + 1] < insert) :
		pos += 1
	middle = newSize // 2#середина масиву
	if(pos <= middle) :#точка вставки в лівій частині масиву
		if(arr_new[pos] != null and arr_new[pos] < insert):
		   pos += 1
		#здвигаємо праворуч
		right = pos
		right += 1
		while(arr_new[right] != null) :
			right += 1
		for i in range(right, pos, -1):
			arr_new[i] = arr_new[i - 1]
		
	else :#Точка вставки в правій частині масиву
		if(arr_new[pos] != null and insert < arr_new[pos]):
		   pos -= 1
		#здвигаємо ліворуч
		left = pos
		left -= 1
		while(arr_new[left] != null) :
			left -= 1
		for i in range(left, pos):
			arr_new[i] = arr_new[i + 1]
				
	arr_new[pos] = insert

#############################################################
#повне перебалансування допоміжного масиву
#count - скільки елементів на даний момент в масиві
#newSize - повний розмір допоміжного масиву
def LibrarySort_Rebalance_Total(count, newSize) :
	global arr_new#доп. мас.
	global library_Number#Який за рахунком елемент переносимо
	global library_LeftPos#Найлівіша позиція при якій вліво переносили елементи
	
	library_Number = count #Починаємо переносити останні з кінця за рахунком елементи
	library_LeftPos = newSize - 1#Поки невідома, тому максимально праве значення

    #Проходимо елементи в доп. мас. від останнього до початку
	i = newSize - 1
	while(i >= 0) :
		if(arr_new[i] != null) :#непорожній елемент
			pos = LibrarySort_Pos(library_Number, count, newSize)#перенести треба сюди
			if(i == pos) :#ел. уже на своєму місці
				i -= 1#рухаємося до наступного
			elif(i < pos) :#ел. треба перенести праворуч
				arr_new[pos] = arr_new[i]
				arr_new[i] = null
				i -= 1#рухаємося далі
			else :#i > pos - ел. треба перенести вліво
                #Рекурсивна процедура для перенесення елемента вліво
				LibrarySort_RemoveLeft(i, pos, count, newSize)
				if (i > library_LeftPos):
					i = library_LeftPos - 1
				else:
					i -= 1
			
			library_Number -= 1#перенести на один ел. треба менше
		else :#порожня клітинка, переносити не треба
			i -= 1#рухаємося далі

#############################################################################################################################################################################################
#повне перебалансування додаткового масиву
#count - скільки елементів на даний момент в масиві
#newSize - повний розмір допоміжного масиву
def LibrarySort_Rebalance_Total_Modified(count, newSize) :
    
	global arr_new#доп. мас.
	global library_Number#Який за рахунком елемент переносимо
	global library_LeftPos#Найлівіша позиція при якій вліво переносили елементи
	arr_buf = [null for i in range(newSize)]#створюємо буферний масив

	arr_new = list(filter((null).__ne__, arr_new))#видаляємо порожні елементи
	for i in range(len(arr_new)):#кожен ел. із доп. мас. треба перенести в буф. мас.
		pos = LibrarySort_Pos(i+1, count, newSize)#перенести треба сюди
		arr_buf[pos] = arr_new[i]#переносимо
	arr_new = arr_buf#зливаємо масиви

#############################################################
#перенос елемента лівіше при повному перебалансуванні
# Цьому можуть заважати інші елементи, що знаходяться зліва
#i - в якій комірці знаходиться елемент, який потрібно перенести
#pos - в яку комірку потрібно перенести елемент
#count - скільки всього зараз елементів у допоміжному масиві
#newSize - повний розмір допоміжного масиву
def LibrarySort_RemoveLeft(i, pos, count, newSize) :

	global arr_new#доп. мас.
	global library_Number#Який за рахунком елемент переносимо
	global library_LeftPos#Найлівіша позиція при якій вліво переносили елементи
	
	left = False
	left_Pos = False#Поки найближчий сусід зліва не знайдено
	j = i#Починаємо перебирати відразу від елемента, який переноситься
    #Потрібно знайти найближчого сусіда зліва
	while(j > 0 and left == False) :#Поки в межах допоміжного масиву і поки не знайдений найближчий сусід зліва
		j -= 1 #Продовжуємо вліво пошук найближчого сусіда
		if(arr_new[j] != null):
			left = j#Найближчий сусід зліва знайдений
	if(left == False or left < pos) :#Найближчий сусід зліва (якщо він знайдений) не заважає переносу
        #Нічого додатково робити не потрібно
		pass
	else : #left >= pos, сусід зліва заважає переносу
		library_Number -= 1#Значить, лівіше потрібно перенести сусіда зліва, який заважає 
		left_Pos = LibrarySort_Pos(library_Number, count, newSize)#Сусіда зліва треба перенести сюди
        #Рекурсивно переносимо сусіда зліва на його правильну позицію
		LibrarySort_RemoveLeft(left, left_Pos, count, newSize)
        #Сусід зліва відсунутий, тепер можна перенести елемент

	#З сусідом зліва все нормально, переносимо елемент
	arr_new[pos] = arr_new[i]
	arr_new[i] = null
    #Уточнюємо, чи був це самий вліво перенесений з сусідів
	if(pos < library_LeftPos):
	   library_LeftPos = pos



###############################################
if (__name__ == '__main__'):
	mas = [4,7,2,5,1,0,4,234,9]
	print(LibrarySort(mas))