from flask import render_template, url_for, request, redirect, session
from app import app


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")

# block user-----------------------------------


@app.route('/registry', methods=['POST', 'GET'])
def registry():
    if request.method == 'POST':
        alias = request.form['login']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']
        # проверить данные
        if password1 != password2:
            res = "Пароль и его подтверждение не совпадают..."
            return render_template('/registry.html', mess=res)


        from app.models.users import add_user
        res = add_user(alias=alias, email=email, password=password1)
        if type(res) == int:
            # если новый пользователь зарегистрирован - страница подтверждения регистрации
            confirmref = "http://127.0.0.1:5000/confirmreg"
            # отправить email
            return render_template('/entry.html', mess='Для завершения регистрации перейдите по ссылке, отправленной Вам на указанный email')
        else:
            # если нет - на страницу регистрации
            return render_template('/registry.html', mess=res)
    else:
        return render_template('/registry.html')


@app.route('/entry', methods=['POST', 'GET'])
def entry():
    if request.method == 'POST':
        alias = request.form['login']
        password = request.form['password']
        # проверить данные
        from app.models import login_user
        res = login_user(alias=alias, password=password)
        if type(res) == int:
            # если такой пользователь есть - переходим на предыдушую страницу
            session['ss_userid'] = res
            session['ss_username'] = alias
            return render_template('/index.html', mess='Вход выполнен')
        else:
            # если нет - на страницу регистрации
            return render_template('/entry.html', mess=res)
    else:
        return render_template('/entry.html')


@app.route('/userpage/<string:name>')
def userpage(name):
    return "Станица пользоватея: " + name


@app.route('/logout')
def logout():
    session.pop('ss_userid', None)
    session.pop('ss_username', None)
    return  redirect(url_for('index'))











@app.route('/addbook', methods=['POST', 'GET'])
def addbook():
    if request.method == 'POST':
        try:
            code = request.form['code']
            title = request.form['title']
            description = request.form['description']
            file = request.form['file']
            strsql = "INSERT INTO books VALUES (NULL, '" + code + "', '" + title + "', '" \
                     + description + "', NULL, '" + file + "')"
            engine.execute(strsql)
            return redirect('/')

        except:
            return 'Ошибка добавления записи'
    else:
        return render_template("addbook.html")


@app.route('/booklist')
def booklist():
    from app.models.books import get_booklist
    #strsql = "SELECT * FROM books ORDER BY title"
    booklist = get_booklist()
    return render_template("booklist.html", booklist=booklist)
