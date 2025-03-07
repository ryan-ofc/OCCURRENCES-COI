# Empacotamento de Aplicativo PySide6 com PyArmor e PyInstaller

Este guia explica como proteger e compilar um aplicativo **PySide6** utilizando **PyArmor 8+** e **PyInstaller** .

## 📌 Requisitos

Antes de começar, certifique-se de ter os seguintes pacotes instalados:

```sh
pip install pyarmor pyinstaller
```

## 🔒 Passo 1: Proteger o Código

Para proteger seu código antes de compilar, execute o seguinte comando:

```sh
pyarmor gen -O dist-protegido main.py
```

🔹 Isso criará a pasta `dist-protegido/` contendo o código protegido.

---

## 🏗️ Passo 2: Compilar o Código

Após proteger o código, compile-o utilizando o **PyInstaller** :

```sh
pyinstaller --onefile --windowed --icon=coi.ico dist-protegido/main.py
```

🔹 Explicação dos parâmetros:

-   `--onefile` → Gera um único `.exe`
-   `--windowed` → Remove o terminal (ideal para aplicativos GUI)
-   `--icon=coi.ico` → Define o ícone do executável
-   `dist-protegido/main.py` → Usa o código protegido gerado anteriormente

---

## ✅ Conclusão

Agora seu aplicativo está protegido e empacotado corretamente! 🚀
