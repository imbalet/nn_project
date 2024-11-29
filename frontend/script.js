const params = {
    "mark": { "name": "Марка", "type": "str" },
    "model": { "name": "Модель", "type": "str" },
    "super_gen": { "name": "Поколение", "type": "str" },
    "steering_wheel": { "name": "Положение руля", "type": "str" },
    "owners": { "name": "Число владельцев", "type": "num" },
    "year": { "name": "Год выпуска", "type": "num" },
    "region": { "name": "Регион", "type": "str" },
    "mileage": { "name": "Пробег", "type": "num" },
    "doors": { "name": "Дверей", "type": "str" },
    "class": { "name": "Класс", "type": "str" },
    "body_type": { "name": "Кузов", "type": "str" },
    "gear_type": { "name": "Привод", "type": "str" },
    "engine": { "name": "Двигатель", "type": "str" },
    "transmission": { "name": "КПП", "type": "str" },
    "power": { "name": "Мощность (л. с.)", "type": "num" },
    "displacemnt": { "name": "Объем двигателя", "type": "num" },
    "color": { "name": "Цвет", "type": "str" },
}; // TODO это сделать с запросом к беку

let selectedData = Object.keys(params).reduce((acc, key) => {
    acc[key] = null; // Устанавливаем значение в null
    return acc;
}, {});

let selectedParam = null;

let variants = {};




const updateVariants = () => {
    if (selectedParam !== null && params[selectedParam]["type"] == "str") {
        //TODO тут запрос с бека GET
        /*
        какой-то такой формат ответа
        {
            "bmw": {"name": "БНВ", "pic": "images/penis.jpeg"},
        }
        */
        let variants_answ = {
            "bmw": { "name": "БНВ", "pic": "images/penis.jpeg" },
        }
        variants = variants_answ;
    }
    else {
        variants = {};
    }
};


const updateParamsList = () => {
    document.getElementById("params").innerHTML = "";

    let keys = [Object.keys(selectedData)[0]];
    for (let i = 1; i < Object.keys(selectedData).length; ++i) {
        if (selectedData[Object.keys(selectedData)[i - 1]] !== null) {
            keys.push(Object.keys(selectedData)[i]);
        } else {
            break;
        }
    }

    for (let key of keys) {
        const newDiv = document.createElement('div');
        newDiv.className = 'param';
        newDiv.innerHTML = params[key]["name"];
        newDiv.addEventListener("click", () => {
            const allParams = document.querySelectorAll('.param');
            allParams.forEach(param => param.classList.remove('pressed'));

            newDiv.classList.add('pressed');

            selectedParam = key;
            updateVariants();
        });
        if (key == keys[keys.length - 1]) { newDiv.classList.add("pressed"); }
        document.getElementById("params").append(newDiv);
    }

};



document.addEventListener('DOMContentLoaded', (e) => {
    updateParamsList();
    updateVariants();
});



