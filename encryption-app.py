import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from typing import Optional

def to_binary(text: str) -> str:
    return ' '.join(format(ord(char), '08b') for char in text)

def to_decimal(text: str) -> str:
    return ' '.join(str(ord(char)) for char in text)

def from_binary(binary: str) -> str:
    binary = binary.replace(' ', '')
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def pad_key(text: str, key: str) -> str:
    return (key * (len(text) // len(key) + 1))[:len(text)]

def from_decimal(decimal: str) -> str:
    return ''.join(chr(int(num)) for num in decimal.split())

def apply_permutation(data, table) -> str:
    return ''.join(data[i - 1] for i in table)

def left_shift(bits: str, n: int) -> str:
    return bits[n:] + bits[:n]

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Encryption Tool")
        self.root.geometry("1200x800")

        # Configuration du thème sombre
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        # Création de la structure à trois colonnes
        self.create_layout()

    def create_layout(self):
        # Colonne gauche (Menu)
        self.left_frame = ctk.CTkFrame(self.root)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.menu_label = ctk.CTkLabel(self.left_frame, text="Menu", font=("Roboto", 20, "bold"))
        self.menu_label.pack(pady=10)

        algorithms = ["Substitution", "Vernam", "Vigenère", "DES"]
        self.selected_algo = tk.StringVar(value=algorithms[0])

        for algo in algorithms:
            btn = ctk.CTkButton(
                self.left_frame,
                text=algo,
                command=lambda a=algo: self.select_algorithm(a)
            )
            btn.pack(pady=5, padx=10, fill="x")

        # Colonne centrale (Zone principale)
        self.center_frame = ctk.CTkFrame(self.root)
        self.center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Zone de saisie
        self.input_label = ctk.CTkLabel(self.center_frame, text="Texte à traiter:", font=("Roboto", 14))
        self.input_label.pack(pady=5)

        self.input_text = ctk.CTkTextbox(self.center_frame, height=200)
        self.input_text.pack(fill="x", padx=10, pady=5)

        # Zone de clé
        self.key_label = ctk.CTkLabel(self.center_frame, text="Clé:", font=("Roboto", 14))
        self.key_label.pack(pady=5)

        self.key_entry = ctk.CTkEntry(self.center_frame)
        self.key_entry.pack(fill="x", padx=10, pady=5)

        # Boutons d'action
        self.button_frame = ctk.CTkFrame(self.center_frame)
        self.button_frame.pack(pady=10)

        self.encrypt_button = ctk.CTkButton(
            self.button_frame,
            text="Chiffrer",
            command=self.encrypt,
            fg_color="#FF5733"
        )
        self.encrypt_button.pack(side="left", padx=5)

        self.decrypt_button = ctk.CTkButton(
            self.button_frame,
            text="Déchiffrer",
            command=self.decrypt,
            fg_color="#FF5733"
        )
        self.decrypt_button.pack(side="left", padx=5)

        # Zone de résultat
        self.result_label = ctk.CTkLabel(self.center_frame, text="Résultat:", font=("Roboto", 14))
        self.result_label.pack(pady=5)

        self.result_text = ctk.CTkTextbox(self.center_frame, height=200)
        self.result_text.pack(fill="x", padx=10, pady=5)

        # Colonne droite (Logs)
        self.right_frame = ctk.CTkFrame(self.root)
        self.right_frame.pack(side="right", fill="y", padx=10, pady=10)

        self.log_label = ctk.CTkLabel(self.right_frame, text="Logs", font=("Roboto", 20, "bold"))
        self.log_label.pack(pady=10)

        self.log_text = ctk.CTkTextbox(self.right_frame, height=600, width=300)
        self.log_text.pack(padx=10, pady=5)

    # Algorithmes de chiffrement
    def substitution_encrypt(self, text: str, shift: int) -> str:
        result = ""
        n = 26

        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                position = ord(char) - base
                new_position = (position + shift) % n
                result += chr(base + new_position)
            else:
                result += char

        return result

    def substitution_decrypt(self, text: str, shift: int) -> str:
        return self.substitution_encrypt(text, -shift)

    def vernam_encrypt(self, plaintext: str, key: str) -> dict:
        key = pad_key(plaintext, key)
        ciphertext = ''.join(chr(ord(p) ^ ord(k)) for p, k in zip(plaintext, key))

        return {
            'binary': to_binary(ciphertext),
            'ascii': ciphertext,
            'decimal': to_decimal(ciphertext)
        }

    def vernam_decrypt(self, ciphertext: str, key: str, input_format: str = 'ascii') -> str:
        if input_format == 'binary':
            ciphertext = from_binary(ciphertext)
        elif input_format == 'decimal':
            ciphertext = from_decimal(ciphertext)

        key = pad_key(ciphertext, key)
        return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(ciphertext, key))

    def vigenere_encrypt(self, text: str, key: str) -> str:
        result = []
        key = key.upper()
        key_as_int = [ord(k) - ord('A') for k in key]

        for i, char in enumerate(text):
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                key_idx = i % len(key_as_int)
                shifted = (ord(char) - base + key_as_int[key_idx]) % 26
                result.append(chr(base + shifted))
            else:
                result.append(char)

        return ''.join(result)

    def vigenere_decrypt(self, text: str, key: str) -> str:
        result = []
        key = key.upper()
        key_as_int = [ord(k) - ord('A') for k in key]

        for i, char in enumerate(text):
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                key_idx = i % len(key_as_int)
                shifted = (ord(char) - base - key_as_int[key_idx]) % 26
                result.append(chr(base + shifted))
            else:
                result.append(char)

        return ''.join(result)

    # Méthode DES
    def des_encrypt(self, message: str, key: str) -> str:
        pc2_table = [
            14, 17, 11, 24,  1,  5,  3, 28,
            15,  6, 21, 10, 23, 19, 12,  4,
            26,  8, 16,  7, 27, 20, 13,  2,
            41, 52, 31, 37, 47, 55, 30, 40,
            51, 45, 33, 48, 44, 49, 39, 56,
            34, 53, 46, 42, 50, 36, 29, 32
        ]
        shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

        # Convertir message et clé en binaire
        message_bin = to_binary(message)
        key_bin = to_binary(key)

        # Appliquer la permutation PC2
        kp = apply_permutation(key_bin, pc2_table)

        # Diviser KP en Kleft et Kright
        k_left = kp[:len(kp)//2]
        k_right = kp[len(kp)//2:]

        self.log(f"Kleft initial: {k_left}")
        self.log(f"Kright initial: {k_right}")

        # Appliquer les décalages pour chaque round
        for round_num, shift in enumerate(shifts, start=1):
            k_left = left_shift(k_left, shift)
            k_right = left_shift(k_right, shift)
            self.log(f"Round {round_num}: Kleft={k_left}, Kright={k_right}")

        return f"Kleft final: {k_left}\nKright final: {k_right}"

    # Méthodes de l'interface
    def select_algorithm(self, algorithm: str):
        self.selected_algo.set(algorithm)
        self.log(f"Algorithme sélectionné: {algorithm}")

    def encrypt(self):
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()

        if not text or not key:
            self.log("Erreur: Texte et clé requis")
            return

        algorithm = self.selected_algo.get()
        try:
            if algorithm == "Substitution":
                result = self.substitution_encrypt(text, int(key))
            elif algorithm == "Vernam":
                result = self.vernam_encrypt(text, key)
                result = f"Binary: {result['binary']}\nASCII: {result['ascii']}\nDecimal: {result['decimal']}"
            elif algorithm == "Vigenère":
                result = self.vigenere_encrypt(text, key)
            elif algorithm == "DES":
                result = self.des_encrypt(text, key)

            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", result)
            self.log(f"Chiffrement réussi avec {algorithm}")

        except Exception as e:
            self.log(f"Erreur lors du chiffrement: {str(e)}")

    def decrypt(self):
        text = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()

        if not text or not key:
            self.log("Erreur: Texte et clé requis")
            return

        algorithm = self.selected_algo.get()
        try:
            if algorithm == "Substitution":
                result = self.substitution_decrypt(text, int(key))
            elif algorithm == "Vernam":
                input_format = "ascii"
                if text.startswith("0") or " " in text:
                    input_format = "binary" if " " in text and text.strip().replace(" ", "").isdigit() else "decimal"
                result = self.vernam_decrypt(text, key, input_format)
            elif algorithm == "Vigenère":
                result = self.vigenere_decrypt(text, key)
            elif algorithm == "DES":
                result = self.des_decrypt(text, key)

            self.result_text.delete("1.0", tk.END)
            self.result_text.insert("1.0", result)
            self.log(f"Déchiffrement réussi avec {algorithm}")

        except Exception as e:
            self.log(f"Erreur lors du déchiffrement: {str(e)}")

    def log(self, message: str):
        self.log_text.insert("1.0", f"{message}\n")

root = ctk.CTk()
app = EncryptionApp(root)
root.mainloop()


