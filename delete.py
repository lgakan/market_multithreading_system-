import matplotlib.pyplot as plt

visual = []
step = []
dispers = []
iteracja = []

if __name__ == "__main__":
    x = [1, 4, 7, 10, 13, 16, 19, 22, 25, 27]
    values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    min_value_index = values.index(min(values))  # znajduje indeks najmniejszej wartości w tablicy values

    plt.plot(x, values, marker='o')  # tworzy wykres, marker='o' oznacza punkty danych jako kółka
    plt.scatter(x[min_value_index], values[min_value_index],
                color='red')  # dodaje czerwoną kropkę na najmniejszej wartości
    plt.xlabel('x')  # etykieta osi x
    plt.ylabel('values')  # etykieta osi y
    plt.title('Wykres wartości w zależności od x')  # tytuł wykresu
    plt.xticks(x)  # ustawia niestandardowe etykiety osi x na wartości z tablicy x
    plt.grid(True)  # włącza siatkę na wykresie
    plt.show()  # wyświetla wykres

