from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QTextEdit, QHBoxLayout, QMessageBox, QDialog, QScrollArea
)
from PyQt6.QtGui import QFont
import sys


# ---------------------------
# Funções de conversão
# ---------------------------

def texto_para_binario(texto):
    return ' '.join(format(ord(char), '08b') for char in texto)


def binario_para_texto(binario):
    grupos = [g for g in binario.split() if g.strip()]

    for g in grupos:
        if len(g) != 8 or any(c not in '01' for c in g):
            raise ValueError("Código binário inválido.")

    return ''.join(chr(int(b, 2)) for b in grupos)


# ---------------------------
# Janela de regras (QDialog)
# ---------------------------

class RegrasConversao(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Regras de Conversão")
        self.setGeometry(300, 200, 500, 350)

        layout = QVBoxLayout()
        self.setLayout(layout)

        texto_regras = (
            "📘 Regras de Conversão\n\n"
            "🔹 Conversão de Texto para Binário:\n"
            "1. Cada caractere é transformado no código ASCII.\n"
            "2. O código ASCII é convertido em binário de 8 bits.\n"
            "3. Cada byte é separado por espaços.\n\n"
            "🔹 Conversão de Binário para Texto:\n"
            "1. O binário deve estar em grupos de 8 bits.\n"
            "2. Cada conjunto de 8 bits vira um número decimal.\n"
            "3. O decimal é convertido para o caractere ASCII.\n"
        )

        label = QLabel(texto_regras)
        label.setFont(QFont("Arial", 12))
        label.setWordWrap(True)

        scroll = QScrollArea()
        scroll.setWidget(label)
        scroll.setWidgetResizable(True)

        layout.addWidget(scroll)


# ---------------------------
# Interface principal
# ---------------------------

class ConversorBinario(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Conversor Binário - PyQt6 (Profissional)")
        self.setGeometry(200, 100, 650, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        # Título
        titulo = QLabel("Conversor de Texto ⇄ Binário")
        titulo.setFont(QFont("Arial", 16, 600))
        titulo.setStyleSheet("margin-bottom: 10px;")
        layout.addWidget(titulo)

        # Entrada
        self.entrada = QTextEdit()
        self.entrada.setFont(QFont("Arial", 12))
        self.entrada.setPlaceholderText("Digite texto ou código binário aqui...")
        layout.addWidget(self.entrada)

        # Botões
        botoes = QHBoxLayout()

        btn_binario = QPushButton("Converter p/ Binário")
        btn_binario.clicked.connect(self.converter_para_binario)
        botoes.addWidget(btn_binario)

        btn_texto = QPushButton("Converter p/ Texto")
        btn_texto.clicked.connect(self.converter_para_texto)
        botoes.addWidget(btn_texto)

        btn_copiar = QPushButton("Copiar Resultado")
        btn_copiar.clicked.connect(self.copiar_resultado)
        botoes.addWidget(btn_copiar)

        btn_limpar = QPushButton("Limpar Tudo")
        btn_limpar.clicked.connect(self.limpar_tudo)
        botoes.addWidget(btn_limpar)

        btn_regras = QPushButton("Regras de Conversão")
        btn_regras.clicked.connect(self.abrir_regras)
        botoes.addWidget(btn_regras)

        layout.addLayout(botoes)

        # Saída
        label_saida = QLabel("Resultado:")
        label_saida.setFont(QFont("Arial", 12))
        label_saida.setStyleSheet("margin-top: 10px;")
        layout.addWidget(label_saida)

        self.saida = QTextEdit()
        self.saida.setReadOnly(True)
        self.saida.setFont(QFont("Arial", 12))
        layout.addWidget(self.saida)

        # Estilo moderno
        self.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 13px;
                background-color: #e0e0e0;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
            QTextEdit {
                border: 1px solid #888;
                border-radius: 6px;
            }
        """)

    # ---------------------------
    # Funções dos botões
    # ---------------------------

    def converter_para_binario(self):
        texto = self.entrada.toPlainText().strip()

        if not texto:
            QMessageBox.warning(self, "Erro", "Digite algum texto.")
            return

        resultado = texto_para_binario(texto)
        self.saida.setPlainText(resultado)

    def converter_para_texto(self):
        binario = self.entrada.toPlainText().strip()

        if not binario:
            QMessageBox.warning(self, "Erro", "Digite algum código binário.")
            return

        try:
            resultado = binario_para_texto(binario)
            self.saida.setPlainText(resultado)
        except ValueError:
            QMessageBox.critical(self, "Erro", "Código binário inválido. Use apenas grupos de 8 bits.")

    def copiar_resultado(self):
        texto = self.saida.toPlainText().strip()

        if not texto:
            QMessageBox.warning(self, "Erro", "Nada para copiar.")
            return

        QApplication.clipboard().setText(texto)
        QMessageBox.information(self, "Copiado", "Resultado copiado para a área de transferência!")

    def limpar_tudo(self):
        self.entrada.clear()
        self.saida.clear()

    def abrir_regras(self):
        janela_regras = RegrasConversao()
        janela_regras.exec()


# ---------------------------
# EXECUÇÃO DO APP
# ---------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConversorBinario()
    window.show()
    sys.exit(app.exec())
