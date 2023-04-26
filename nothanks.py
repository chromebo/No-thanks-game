def main():
    import random
    import tkinter as tk
    from threading import Timer
    from os import system

    window = tk.Tk()
    window.title('No Thanks!')
    window.geometry("500x300")

    main_frame = tk.Frame(master=window)
    main_frame.pack(side="left", padx=10, pady=10)

    """Объявление переменных"""
    card_nominal = [i for i in range(3, 36)]
    for i in range(0, 10):
        card_nominal.remove(random.choice(card_nominal))

    def player_take_card():
        """Назначение команды взятия карты на верхнюю центральную кнопку"""
        player1.take_card()
        player1.label_coins['text'] = 'Монет: ' + str(player1.coins)
        player1.scoring_points()

    def pass_card():
        """Назначение команды паса на нижнюю центральную кнопку"""
        player1.passed_card()

        player2.inchoice = True
        while player2.inchoice:
            player2.check_inchoice()

        player3.inchoice = True
        while player3.inchoice:
            player3.check_inchoice()

        player1.inchoice = True

    def kill():
        system('taskkill /f /im python.exe')

    def win():
        """Объявление конца игры и финальный подсчет очков"""
        text_log.insert(tk.END, "Игра окончена!\n")
        text_log.insert(tk.END, f"Вы набрали: {player1.label_points['text']}!\n")
        if player1.res > player2.res > player3.res:
            text_log.insert(tk.END, "Вы выиграли!\n")
        else:
            text_log.insert(tk.END, "Вы проиграли!\n")
        text_log.see(tk.END)

    """Объявление функционала игрока и ботов"""
    class Player:

        def __init__(self, num: int, color: str, iniz: bool):
            self.coins = 11
            self.cards = list()
            self.points = 0
            self.inchoice = iniz
            self.name = f"Игрок {num}"

            """Объявление функциональных окон игроков"""
            self.frame = tk.Frame(master=main_frame)
            self.frame_name = tk.Frame(master=self.frame)
            self.frame_other = tk.Frame(master=self.frame, relief="groove", borderwidth=1, border=2)
            self.label_name = tk.Label(master=self.frame_name, text=self.name, relief="ridge", highlightbackground=color, highlightthickness=1)
            self.label_coins = tk.Label(master=self.frame_other, text="Монет: " + str(self.coins))
            self.entry_cards = tk.Entry(master=self.frame_other, state="readonly")
            self.label_points = tk.Label(master=self.frame_other, text="Очков: " + str(self.points))

        def take_card(self):
            """Функция снятия карты"""
            self.cards.append(nominal_label['text'])

            self.entry_cards["state"] = "normal"
            self.entry_cards.delete(0, tk.END)
            self.entry_cards.insert(tk.END, str(self.update_cards))
            self.entry_cards["state"] = "readonly"

            text_log.insert(tk.END, f"{self.name} взял карту: {nominal_label['text']}.\n")
            text_log.see(tk.END)

            """Завершение игры по исчерпанию номинала карт"""
            try:
                card_nominal.remove(nominal_label['text'])
            except ValueError or IndexError:
                take_button['command'] = ''
                pass_button['command'] = ''
                win()
                timer = Timer(5, kill)
                timer.start()

            nominal_label['text'] = random.choice(card_nominal)
            self.coins += bank_label['text']
            bank_label['text'] = 0
            self.scoring_points()

        def passed_card(self):
            """Функция пропуска карты"""
            if self.coins > 0:
                self.coins -= 1
                self.label_coins['text'] = 'Монет: ' + str(self.coins)
                bank_label['text'] += 1
                self.inchoice = False
                text_log.insert(tk.END, f"{self.name} сделал пас.\n")
                text_log.see(tk.END)
            else:
                text_log.insert(tk.END, f"{self.name} всё таки взял карту: {nominal_label['text']}.\n")
                self.take_card()

        def check_inchoice(self):
            """Только для ботов. Функция проверки хода бота и выбор из двух функций, что выше"""
            if self.inchoice:
                if random.randint(0, 5) == 0 or self.coins == 0:
                    self.take_card()
                else:
                    self.passed_card()
                self.scoring_points()

        def window(self, n: int, z: int):
            """Вывод окон из __init__ на экран"""
            self.frame.grid(row=n, column=z, sticky="nsew")

            self.frame_name.pack()
            self.label_name.pack()

            self.frame_other.pack()
            self.label_coins.pack()
            self.entry_cards.pack()
            self.label_points.pack()

        @property
        def update_cards(self):
            """Свойство + алгортим сортировки карты для далнейшего подсчёта.
            Деление чисел в списки по числам с минимальной разницей в значениях.
            Алгоритм заимствован со StackOverflow"""
            prev_element = float('-inf')
            self.sep_cards = list()
            self.cards.sort()
            for element in self.cards:
                if element - prev_element > 1:
                    self.sep_cards.append([])
                self.sep_cards[-1].append(element)
                prev_element = element
            return self.sep_cards

        def scoring_points(self):
            """Из свойства выше берутся числа, из списков и плюсуются в каунтер очков"""
            lis = self.update_cards
            self.res = 0
            for i in lis:
                self.res += min(i)
            self.res = -self.res + self.coins
            self.label_points['text'] = 'Очков: ' + str(self.res)

    """Инициализация интерфейса игрока и ботов в нужных местах
    также цвета рамки и дача инициативы (первого хода)"""
    player1 = Player(1, 'red', True)
    player1.window(2, 1)

    player2 = Player(2, 'blue', False)
    player2.window(0, 1)

    player3 = Player(3, 'green', False)
    player3.window(1, 0)

    """Отрисовка текстового лога"""
    textlog_frame = tk.Frame(master=window)
    textlog_frame.pack(side='right', expand=True, fill=tk.BOTH)

    text_log = tk.Text(master=textlog_frame, height=15, width=10)
    text_log.pack(expand=True, fill=tk.BOTH)

    """Отрисовка центральной панели"""
    center_frame = tk.Frame(master=main_frame)
    center_frame.grid(row=1, column=1)

    nominal_label = tk.Label(master=center_frame, text=random.choice(card_nominal), relief='sunken', width=3)
    nominal_label.pack(side='left', padx=10)

    bank_label = tk.Label(master=center_frame, text=0, relief='sunken', width=3)
    bank_label.pack(side='right', padx=10)

    take_button = tk.Button(master=center_frame, text="Взять", command=player_take_card)
    take_button.pack(pady=5)

    pass_button = tk.Button(master=center_frame, text="Пас", command=pass_card)
    pass_button.pack(pady=5)

    window.mainloop()


if __name__ == "__main__":
    main()
