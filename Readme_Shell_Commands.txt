from news.models import *

1. Создать двух пользователей (с помощью метода User.objects.create_user('username')).

user1 = User.objects.create_user('Steeve')
user2 = User.objects.create_user('Jobs')

2. Создать два объекта модели Author, связанные с пользователями.

author1 = Author.objects.create(author=user1)
author2 = Author.objects.create(author=user2)

3. Добавить 4 категории в модель Category.

Category.objects.create(article_category='Наука') #1
Category.objects.create(article_category='Авто')  #2
Category.objects.create(article_category='Кино')  #3
Category.objects.create(article_category='Спорт') #4

4. Добавить 2 статьи и 1 новость.

Post.objects.create(
	post_author=author1, 
	categoryType='A', 
	title = 'К 2030 году люди будут жить на Луне, заявили в НАСА', 
	content = 'С 16 ноября космический корабль "Орион" находится на пути к Луне. Первый этап трехэтапной программы Артемида, этот разведывательный полет вокруг нашего естественного спутника предназначен главным образом для проверки работы ракеты-носителя SLS и систем космического аппарата. Если миссия пройдет гладко, экипаж может ступить на Луну уже в 2025 году. По словам Говарда Ху, возглавляющего программу "Орион", постоянное присутствие человека на Луне может быть обеспечено уже к концу десятилетия. Источник: New-Science.ru https://new-science.ru/orion-gotov-k-obletu-luny/')

Post.objects.create(
	post_author = author2, 
	categoryType = 'A', 
	title = 'В Германии представили электромобиль, частично напечатанный на 3D-принтере', 
	text = 'На выставке во Франкфурте берлинская компания представила миниатюрный электромобиль, построенный на промышленном 3D-принтере, который уже готовится к серийному производству. Печать позволяет снизить затраты и проводить некоторую кастомизацию каждой машины. Электромобиль строится на алюминиевой раме, а панели кузова, рулевое колесо и сиденья создаются на 3D-принтере. Габариты машины составляют 2,3 м в длину, 0,9 м в ширину и 1,7 м в высоту при массе всего 70 кг. Подобное транспортное средство сможет миновать дорожные заторы и с лёгкостью найти место для парковки, демонстрируя высокую манёвренность. Источник: http://newatlas.com/')


Post.objects.create(
	post_author = author1, 
	categoryType = 'N', 
	title = 'Чемпионат мира по футболу 2022.Испанцы победили Коста-Рику', 
	text = 'Сборная Испании обыграла команду Коста-Рики в матче первого тура группового этапа чемпионата мира по футболу в Катаре со счетом 7:0.')

5. Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).

Post.objects.get(id=1).post_сategory.add(Category.objects.get(id=1))
Post.objects.get(id=1).post_сategory.add(Category.objects.get(id=2))
Post.objects.get(id=3).post_сategory.add(Category.objects.get(id=4))

6. Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).

Comment.objects.create(
	comment_post=Post.objects.get(id=1), 
	comment_user=user2, 
	feedback_text='Круто. Скоро на Луну слетаем.'
)

Comment.objects.create(
	comment_post=Post.objects.get(id=1), 
	comment_user=user1, 
	feedback_text='Интерсно лоукост-полеты на Луну будут:).'
)

Comment.objects.create(
	comment_post=Post.objects.get(id=2), 
	comment_user=user1, 
	feedback_text='Мобильная техника на электротяге - это наше будущее'
)

Comment.objects.create(
	comment_post=Post.objects.get(id=3), 
	comment_user=user2, 
	feedback_text='Да! Уделалили по полной!'
)

Comment.objects.create(
	commentPost=Post.objects.get(id=3), 
	comment_user=user1, 
	feedback_text='В сухую. Не позавидуешь костариканцам'
)


7. Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.

Comment.objects.get(id=2).like()
Comment.objects.get(id=3).like()
Comment.objects.get(id=1).like()
Post.objects.get(id=1).like()
Post.objects.get(id=1).dislike()
Post.objects.get(id=2).like()
Post.objects.get(id=3).like()
Post.objects.get(id=3).like()

8. Обновить рейтинги пользователей.

user1 = Author.objects.get(id=1).update_rating()
user1.user_rate
user2 = Author.objects.get(id=2).update_rating()
user2.user_rate

9. Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).

s = Author.objects.order_by('user_rate')
	for i in s:
		i.user_rate
		i.author.username

10. Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.

bestPost = Post.objects.order_by('-post_rate')
	for i in bestPost[:1]:
		i.date_created
		i.post_author.author
		i.post_rate
		i.title
		i.preview()

11. Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.

Post.objects.all().order_by('-post_rate')[0].comment_set.values(
	'comment_date_created', 
	'comment_user', 
	'comment_rate', 
	'feedback_text'
)

