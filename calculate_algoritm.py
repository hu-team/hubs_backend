
class Situation:
    def __init__(self, aanwezige_uren, totale_uren, leerjaar, cijfers):
        self.aanwezige_uren = aanwezige_uren
        self.totale_uren = totale_uren
        self.leerjaar = leerjaar
        self.cijfers = cijfers

        self.s = 0
        self.a = 0
        self.c = 0
        self.m = 0

    @property
    def gemiddeld_cijfer(self):
        return sum(self.cijfers) / len(self.cijfers)

    @property
    def jaren_te_gaan(self):
        jaren_te_gaan = 4 - self.leerjaar
        if jaren_te_gaan < 0:
            jaren_te_gaan = 0
        return jaren_te_gaan

    def calculate(self):
        self.s = 1 + (self.jaren_te_gaan / 100 * 5)
        self.a = (100 - (self.aanwezige_uren / self.totale_uren * 100)) * 0.4
        self.c = (10 - self.gemiddeld_cijfer) * 8
        self.m = 100 - (self.a + self.c) * self.s
        return self.m

    def __str__(self):
        self.calculate()
        return 'Aanwezigheid: {} van de {} uur. Gemiddeld cijfer: {}. Leerjaar: {} ({} te gaan).\n{}'.format(
            self.aanwezige_uren,
            self.totale_uren,
            self.gemiddeld_cijfer,
            self.leerjaar,
            self.jaren_te_gaan,
            'S={}, A={}, C={}, M={}'.format(self.s, self.a, self.c, self.m)
        )

def main():
    situations = [
        Situation(
            aanwezige_uren=15,
            totale_uren=20,
            leerjaar=2,
            cijfers=[6]
        ),
        Situation(
            aanwezige_uren=5,
            totale_uren=20,
            leerjaar=3,
            cijfers=[8]
        ),
        Situation(
            aanwezige_uren=5,
            totale_uren=20,
            leerjaar=3,
            cijfers=[6]
        ),
        Situation(
            aanwezige_uren=20,
            totale_uren=20,
            leerjaar=3,
            cijfers=[0]
        ),
        Situation(
            aanwezige_uren=20,
            totale_uren=20,
            leerjaar=1,
            cijfers=[10]
        ),
        Situation(
            aanwezige_uren=0,
            totale_uren=20,
            leerjaar=1,
            cijfers=[0]
        ),
    ]

    for situation in situations:
        print('{}'.format(situation))


if __name__ == '__main__':
    main()
