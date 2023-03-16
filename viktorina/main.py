from savol_modeli import Savollar
from malumot import savol_malumoti
from viktorina_m import Viktorina

savollar_qutisi = []
for savol in savol_malumoti:
    savol_matni = savol["savol"]
    savollar_javobi = savol["togri_javob"]
    yangi_savol = Savollar(savol_matni, savollar_javobi)
    savollar_qutisi.append(yangi_savol)

viktorina = Viktorina(savollar_qutisi)
while viktorina.hali_ham_savollar_bor():
    viktorina.keyingi_savol()

print("Siz viktorinani yakunladingiz!")
print(f"Yakuniy ballingiz {viktorina.hisob}/{viktorina.savol_nomeri} bo'ldi")