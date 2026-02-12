from tkinter import *
from tkinter import messagebox
import os
import random
import string
import tkinter.font as font


def lancer_action(nom_action):
    print(f"Action lancée : {nom_action}")


def action_desinstaller_logiciels():
    lancer_action("Désinstaller les logiciels inutiles")
    os.system("control appwiz.cpl")


def action_parefeu_profils():
    lancer_action("Activé Pare-feu sur tous les profils")
    os.system("control firewall.cpl")


def action_bitlocker_c():
    lancer_action("Activer BitLocker sur le disque C:")
    os.system("control /name Microsoft.BitLockerDriveEncryption")


def action_desactiver_smbv1():
    lancer_action("Désactiver le protocole SMBv1")
    cmd = (
        r'powershell -Command '
        r'"Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart; '
        r'Set-SmbServerConfiguration -EnableSMB1Protocol $false -Force"'
    )
    code_retour = os.system(cmd)

    if code_retour == 0:
        messagebox.showinfo(
            "SMBv1 désactivé",
            "Le protocole SMBv1 a été désactivé avec succès.\n"
            "Un redémarrage de l’ordinateur peut être nécessaire pour appliquer complètement les changements.",
        )
    else:
        messagebox.showerror(
            "Erreur SMBv1",
            "Une erreur est survenue lors de la tentative de désactivation de SMBv1.\n"
            "Vérifie que l’application est lancée avec les droits administrateur.",
        )


def action_protections_defender():
    lancer_action("Activer toutes les protections Windows Defender")
    os.system(r'start "" "windowsdefender://threat"')


def action_mises_a_jour_auto():
    lancer_action("Activer les mises à jour automatiques de Windows")
    os.system(r'start "" "ms-settings:windowsupdate-options"')


def action_renommer_admin_invite():
    lancer_action("Renommer compte administrateur et désactiver compte invité")
    os.system("lusrmgr.msc")


def action_regler_uac_max():
    lancer_action("Régler l'UAC au maximum")
    os.system("UserAccountControlSettings.exe")


def generer_mot_de_passe(longueur: int = 16) -> str:
    """Génère un mot de passe complexe (majuscules, minuscules, chiffres, caractères spéciaux)."""
    lettres_majuscules = string.ascii_uppercase
    lettres_minuscules = string.ascii_lowercase
    chiffres = string.digits
    speciaux = "!@#$%^&*()-_=+[]{};:,.?/"


    mot_de_passe = [
        random.choice(lettres_majuscules),
        random.choice(lettres_minuscules),
        random.choice(chiffres),
        random.choice(speciaux),
    ]

    tous_les_caracteres = lettres_majuscules + lettres_minuscules + chiffres + speciaux
    mot_de_passe += [random.choice(tous_les_caracteres) for _ in range(longueur - 4)]
    random.shuffle(mot_de_passe)

    return "".join(mot_de_passe)


main = Tk()
main.title("Raccourcis durcissement de poste Windows 11")
main.geometry("600x550")
main.resizable(False, False)
main.configure(bg="#5b5b5b")
main.iconbitmap('icon.ico')



f = font.Font(family="Open Sans", size=12, weight="bold")
j = font.Font(family="Open Sans", size=10, weight="bold")
b = font.Font(family="Open Sans", size=14, weight="bold")


elements = [
    ("Désinstaller les logiciels inutiles", action_desinstaller_logiciels),
    ("Activé Pare-feu sur tous les profils", action_parefeu_profils),
    ("Activer BitLocker sur le disque C: (⚠️ Windows Pro)", action_bitlocker_c),
    ("Activer toutes les protections Windows Defender", action_protections_defender),
    ("Activer les mises à jour autmatique de Windows", action_mises_a_jour_auto),
]

tlong = [
    ("Renommer compte administrateur et désativé compte invité", action_renommer_admin_invite),
    ("Régler l'UAC au maximum (Demande de permission admin)", action_regler_uac_max),
    ("Désactiver le protocole SMBv1(⚠️Nécessite mode administrateur)", action_desactiver_smbv1),
]

for texte, action in elements:
    ligne = Frame(main, bg="white")
    ligne.pack(fill="x", padx=10, pady=5)
    

    label = Label(ligne, text=f"• {texte}", bg="white", anchor="w", font=f)
    label.pack(side="left", fill="x", expand=True)


    bouton = Button(ligne, text="M'y emmener !", font=b, command=action)
    bouton.configure(bg="#003791")
    bouton.pack(side="right")
    
for texte, action in tlong:
    ligne = Frame(main, bg="white")
    ligne.pack(fill="x", padx=10, pady=5)
    

    label = Label(ligne, text=f"• {texte}", bg="white", anchor="w", font=j)
    label.pack(side="left", fill="x", expand=True)


    bouton = Button(ligne, text="M'y emmener !", font=b, command=action)
    bouton.configure(bg="#003791")
    bouton.pack(side="right")
    


pwd_frame = Frame(main, bg="#5b5b5b")
pwd_frame.pack(side="bottom", fill="x", padx=10, pady=15)

pwd_titre = Label(
    pwd_frame,
    text="🔒Générateur de mot de passe fort",
    bg="#5b5b5b",
    fg="black",
    font=b,
    anchor="w",
)
pwd_titre.pack(fill="x")

pwd_var = StringVar()
pwd_entry = Entry(pwd_frame, textvariable=pwd_var, font=f, width=40)
pwd_entry.pack(side="left", padx=(0, 10), pady=5, fill="x", expand=True)


def on_generer_pwd():
    pwd_var.set(generer_mot_de_passe())


pwd_button = Button(
    pwd_frame,
    text="Générer",
    font=b,
    command=on_generer_pwd,
    bg="#003791",
    fg="black",
)
pwd_button.pack(side="right")


main.mainloop()