from flask import Flask, render_template, request, url_for

app = Flask(__name__)

dishes = [
    {
        "id": 1,
        "name": "Мексиканский вихрь в кукурузной лодке",
        "country": "Мексика",
        "description": "Маленькая, но взрывная фиеста на вашей ладони. "
                       "Тёплая, слегка шероховатая кукурузная тортилья "
                       "хранит в себе сочную, маринованную в копчёном чили свинину. Яркая зелень кинзы, резкая, хрустящая нотка белого лука, свежесть редиса и финальная капля лайма превращают каждый укус в сочный, "
                       "острый и невероятно живой карнавал красок.",
        "price": 350,
        "image": "taco.jpg"
    },
    {
        "id": 2,
        "name": "Мраморный шторм на золотой бриоши",
        "country": "США",
        "description": "Архитектура абсолютного гастрономического счастья. Хрустящая, карамелизованная корочка рубленого мраморного стейка скрывает бурный поток мясных соков. Расплавленный чеддер, словно жидкое золото, лениво стекает на сочные листья романо и хрустящий маринованный огурчик. Всё это заключено в облако воздушной, поджаристой булочки бриошь, пропитанной секретным трюфельно-горчичным соусом. Гравитация вкуса, которой невозможно сопротивляться.",
        "price": 450,
        "image": "burger.jpg"
    },
    {
        "id": 3,
        "name": "Янтарное сердце Токио",
        "country": "Япония",
        "description": "Глубокий, бархатистый бульон, который томился часами, чтобы раскрыть всю суть ума́ми. Густой пар поднимается над чашей, открывая взгляд на упругую, пружинящую лапшу, нежнейшую свинину чашу, тающую во рту, и идеальное яйцо с жидким, словно расплавленный янтарь, желтком. Это тёплые, крепкие объятия после долгого дня под светом японских фонариков.",
        "price": 500,
        "image": "ramen.jpg"
    },
    {
        "id": 4,
        "name": " Дыхание древнего огня",
        "country": "Турция",
        "description": "Сочный фарш из отборной ягнятины, приправленный восточными специями, томится на раскалённых углях, впитывая их магию. Лёгкий аромат дымка переплетается с запахом тмина, сумаха и свежего кориандра. Подаётся на тёплом, дышащем лаваше, украшенный рубиновыми зёрнами граната и каплей острого чесночного соуса. Вкус, который помнит караванные пути и древние традиции.",
        "price": 400,
        "image": "kebab.jpg"
    },
    {
        "id": 5,
        "name": "Пицца Маргарита",
        "country": "Италия",
        "description": "Тонкое, воздушное тесто с характерными поджаристыми «леопардовыми» пятнами от дровяной печи служит идеальным съедобным холстом. Ярко-алый, бархатистый соус из сладких помидоров Сан-Марцано встречается с тающими, облачными островками свежайшей моцареллы. Изумрудные листья свежего базилика добавляют пряный аромат, а финальный штрих — щедрая струйка золотистого оливкового масла первого отжима — связывает всё в единый, гармоничный вкус. Это не просто пицца, это тёплое, хрустящее объятие солнечной Италии в каждом кусочке.",
        "price": 550,
        "image": "pizza.jpg"
    },
    {
        "id": 6,
        "name": "Пад тай",
        "country": "Таиланд",
        "description": "Тонкие рисовые нити, обжаренные в раскалённом воке до лёгкого, манящего дымка, переплетаются с глянцевым соусом из тамаринда. В каждом движении палочек — звонкий хруст обжаренного арахиса, упругая сочность тигровой креветки и освежающий цитрусовый всплеск лайма. Это не просто лапша, это энергичный танец сладкого, солёного и кислого, перенесённый прямо из шумных, залитых неоновым светом ночных рынков Бангкока.",
        "price": 480,
        "image": "padthai.jpg"
    }
]

@app.route("/")
def index():
    return render_template("index.html", dishes=dishes)

@app.route("/menu")
def menu():
    country = request.args.get("country")

    if country:
        filtered_dishes = [
            dish for dish in dishes
            if dish["country"].lower() == country.lower()
        ]
    else:
        filtered_dishes = dishes

    return render_template(
        "menu.html",
        dishes=filtered_dishes,
        selected_country=country
    )

@app.route("/dish/<int:dish_id>")
def dish_detail(dish_id):
    dish = next(
        (dish for dish in dishes if dish["id"] == dish_id),
        None
    )

    if dish is None:
        return "Блюдо не найдено", 404

    return render_template("dish_detail.html", dish=dish)


@app.route("/order", methods=["GET", "POST"])
def order():
    error = None

    if request.method == "POST":
        customer_name = request.form.get("customer_name", "").strip()
        phone = request.form.get("phone", "").strip()
        dish_id = request.form.get("dish_id", "")
        quantity_text = request.form.get("quantity", "").strip()

        if len(customer_name) < 2:
            error = "Введите имя длиной не менее 2 символов."
        elif len(phone) < 5:
            error = "Введите корректный номер телефона."
        elif not any(str(dish["id"]) == dish_id for dish in dishes):
            error = "Выберите блюдо из списка."

        else:
            try:
                quantity = int(quantity_text)

                if quantity < 1 or quantity > 10:
                    error = "Количество должно быть от 1 до 10."

            except ValueError:
                error = "Количество должно быть целым числом."

        if error:
            return render_template(
                "order.html",
                dishes=dishes,
                error=error,
                customer_name=customer_name,
                phone=phone,
                selected_dish=dish_id,
                quantity=quantity_text
            )

        selected_dish = next(
            dish for dish in dishes
            if str(dish["id"]) == dish_id
        )

        total_price = selected_dish["price"] * quantity

        return render_template(
            "confirmation.html",
            customer_name=customer_name,
            phone=phone,
            dish=selected_dish,
            quantity=quantity,
            total_price=total_price
        )

    return render_template("order.html", dishes=dishes)

@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)