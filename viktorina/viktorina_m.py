class Viktorina:
    def __init__(self, q_list):
        self.savol_nomeri = 0
        self.hisob = 0
        self.savol_royxati = q_list

    def hali_ham_savollar_bor(self):
        return self.savol_nomeri < len(self.savol_royxati)

    def keyingi_savol(self):
        joriy_savol = self.savol_royxati[self.savol_nomeri]
        self.savol_nomeri += 1
        foydalanuvchi_javobi = input(f"Q.{self.savol_nomeri}: {joriy_savol.text} (True/False): ")
        self.javobni_tekshiring(foydalanuvchi_javobi, joriy_savol.javob)

    def javobni_tekshiring(self, foydalanuvchi_javobi, togri_javob):
        if foydalanuvchi_javobi.lower() == togri_javob.lower():
            self.hisob += 1
            print("Siz javobni to'g'ri topdingiz")
        else:
            print("Bu xato!")
        print(f"To'g'ri javob {togri_javob} edi")
        print(f"Sizning joriy ballingiz: {self.hisob}/{self.savol_nomeri}")
        print("\n")

