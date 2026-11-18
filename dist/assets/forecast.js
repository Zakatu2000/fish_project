const waters = {
  volga: {
    fish: 'Окунь и щука',
    gear: 'Воблер 5–7 см, спиннинг с тестом 5–20 г.',
    days: [
      ['05:30–09:00', '+18 °C, облачно', '752 мм рт. ст., стабильно', 'ЮЗ, 3 м/с', 'Утром вода спокойнее, а давление держится стабильно.', [28, 43, 78, 76, 67, 54, 45, 38, 34, 42, 48, 37]],
      ['16:00–19:30', '+20 °C, переменная облачность', '750 мм рт. ст., растёт', 'З, 4 м/с', 'К вечеру ветер стихает. В этом сценарии лучше начать с прибрежной зоны.', [25, 33, 46, 52, 48, 41, 39, 52, 64, 72, 66, 44]],
      ['07:00–10:00', '+16 °C, дождь', '746 мм рт. ст., падает', 'СЗ, 5 м/с', 'Утром остаётся короткий период активности перед усилением дождя.', [21, 32, 55, 59, 41, 32, 24, 22, 25, 31, 29, 25]],
    ],
  },
  oka: {
    fish: 'Лещ и плотва',
    gear: 'Фидер, кормушка по силе течения, опарыш или червь.',
    days: [
      ['06:00–09:30', '+17 °C, малооблачно', '753 мм рт. ст., стабильно', 'Ю, 2 м/с', 'В утреннем сценарии лещ подходит ближе к береговой бровке.', [29, 51, 82, 75, 55, 49, 36, 33, 29, 31, 38, 30]],
      ['10:00–13:30', '+19 °C, облачно', '751 мм рт. ст., стабильно', 'ЮВ, 3 м/с', 'Полуденное окно подходит для ловли на глубине у границы течения.', [18, 22, 33, 48, 68, 73, 67, 48, 40, 35, 31, 22]],
      ['15:30–18:30', '+18 °C, кратковременный дождь', '749 мм рт. ст., растёт', 'З, 4 м/с', 'После дождя активность здесь постепенно растёт до вечера.', [19, 28, 35, 44, 39, 34, 37, 45, 61, 67, 60, 40]],
    ],
  },
  lake: {
    fish: 'Судак и окунь',
    gear: 'Джиг и силикон 7–10 см. Вес груза подбери под глубину и ветер.',
    days: [
      ['17:00–20:30', '+16 °C, ясно', '754 мм рт. ст., стабильно', 'С, 4 м/с', 'Лучшее окно приходится на вечер, когда вода у берега остывает.', [21, 31, 42, 51, 46, 37, 34, 44, 57, 65, 84, 75]],
      ['04:30–08:00', '+15 °C, туман', '755 мм рт. ст., растёт', 'СВ, 2 м/с', 'Самое спокойное время в этом сценарии — первые часы после рассвета.', [44, 79, 72, 60, 49, 42, 35, 34, 40, 47, 51, 42]],
      ['18:00–20:30', '+17 °C, облачно', '751 мм рт. ст., падает', 'З, 5 м/с', 'Днём ветер сильнее. Лучшее окно смещается ближе к сумеркам.', [27, 39, 44, 45, 41, 33, 30, 29, 36, 47, 61, 68]],
    ],
  },
};

const waterSelect = document.getElementById('water');
const dayOptions = document.querySelectorAll('input[name="day"]');
const chart = document.getElementById('chart');
const bars = [...chart.children];
const outputs = Object.fromEntries(
  ['window', 'score', 'forecast-note', 'weather', 'pressure', 'wind', 'moon', 'fish', 'gear']
    .map(id => [id, document.getElementById(id)]),
);

function updateForecast() {
  const { fish, gear, days } = waters[waterSelect.value];
  const day = document.querySelector('input[name="day"]:checked').value;
  const [window, weather, pressure, wind, note, levels] = days[day];
  const moon = ['Растущая', 'Растущая', 'Первая четверть'][day];
  const score = Math.max(...levels);
  const values = { window, score, 'forecast-note': note, weather, pressure, wind, moon, fish, gear };

  for (const [id, value] of Object.entries(values)) {
    outputs[id].textContent = value;
  }
  bars.forEach((bar, index) => {
    bar.style.setProperty('--level', levels[index] + '%');
    bar.classList.toggle('peak', levels[index] === score);
  });
  chart.setAttribute('aria-label', 'Активность по часам. Лучшее окно: ' + window + '. Пиковое значение: ' + score + '%.');
}

waterSelect.addEventListener('change', updateForecast);
dayOptions.forEach(option => option.addEventListener('change', updateForecast));
updateForecast();
