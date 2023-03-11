from flask import Flask, render_template

app = Flask(__name__)

# define a rota / e a funcao que sera executada nessa rota (no caso, home)


@app.route('/')
def home():
    # define uma lista de itens e usa a funcao render_template pra renderizar o html e enviar o array items pro html. la, esse array podera ser iterado
    items = ['item 1', 'item 2', 'item 3']
    return render_template('home.html', items=items)


# Executa o programa
if __name__ == '__main__':
    app.run(debug=True)
