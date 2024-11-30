const data = {
    owners: 2.0,
    year: "2011",
    region: "Санкт-Петербург и Ленинградская область",
    mileage: 253000.0,
    doors: 5.0,
    class: "D",
    body_type: "ALLROAD_5_DOORS",
    mark: "Nissan",
    model: "X-Trail",
    super_gen: "II Рестайлинг",
    steering_wheel: "LEFT",
    gear_type: "ALL_WHEEL_DRIVE",
    engine: "GASOLINE",
    transmission: "VARIATOR",
    power: 141.0,
    displacemnt: 1997.0,
    color: "200204"
};

fetch('http://0.0.0.0:1488/predict', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
    .then(response => {
        if (!response.ok) {
            throw new Error('Сеть ответила статусом ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        console.log('Ответ сервера:', data);
    })
    .catch(error => {
        console.error('Произошла ошибка при отправке запроса:', error);
    });
