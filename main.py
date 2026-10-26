import sqlite3
import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from database import (
    create_notification,
    get_notification,
    initialize_database,
    list_notifications,
    update_notification,
)


class NotificationDialog(QDialog):
    """Formulário compartilhado pelo cadastro e pela edição."""

    def __init__(self, parent=None, notification=None):
        super().__init__(parent)

        self.setWindowTitle("Nova notificação")
        self.setMinimumWidth(500)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(20)

        form = QFormLayout()
        form.setSpacing(14)

        self.identification_input = QLineEdit()
        self.identification_input.setPlaceholderText(
            "Ex.: CES 12345 ou Maringá — 11/09/2026"
        )
        self.identification_input.setMaxLength(150)

        self.title_input = QLineEdit(
            "Relatório Fotográfico de Regularização"
        )
        self.title_input.setMaxLength(200)

        self.observation_input = QTextEdit()
        self.observation_input.setAcceptRichText(False)
        self.observation_input.setPlaceholderText("Opcional")
        self.observation_input.setFixedHeight(120)

        form.addRow("Identificação *", self.identification_input)
        form.addRow("Título do relatório *", self.title_input)
        form.addRow("Observação", self.observation_input)

        layout.addLayout(form)

        buttons = QDialogButtonBox()

        self.save_button = buttons.addButton(
            "Criar notificação",
            QDialogButtonBox.ButtonRole.AcceptRole,
        )

        buttons.addButton(
            "Cancelar",
            QDialogButtonBox.ButtonRole.RejectRole,
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        self.identification_input.textChanged.connect(
            self.validate_fields
        )
        self.title_input.textChanged.connect(self.validate_fields)

        if notification is not None:
            self.setWindowTitle("Editar notificação")
            self.save_button.setText("Salvar alterações")

            self.identification_input.setText(
                notification["identification"]
            )
            self.title_input.setText(notification["title"])
            self.observation_input.setPlainText(
                notification["observation"]
            )

        self.validate_fields()

    def validate_fields(self):
        identification = self.identification_input.text().strip()
        title = self.title_input.text().strip()

        self.save_button.setEnabled(bool(identification and title))

    def get_data(self):
        return {
            "identification": self.identification_input.text().strip(),
            "title": self.title_input.text().strip(),
            "observation": (
                self.observation_input.toPlainText().strip()
            ),
        }


class MainWindow(QMainWindow):
    """Janela principal com a lista de notificações."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gerenciador de Notificações")
        self.resize(1100, 720)
        self.setMinimumSize(800, 500)

        self.setup_ui()

        self.create_button.clicked.connect(self.open_create_dialog)
        self.notification_list.itemDoubleClicked.connect(
            self.open_notification
        )

        self.load_notifications()

    def setup_ui(self):
        container = QWidget()
        self.setCentralWidget(container)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(32, 32, 32, 32)
        layout.setSpacing(20)

        header = QHBoxLayout()

        title = QLabel("Notificações")
        title.setObjectName("pageTitle")

        self.create_button = QPushButton("+ Nova notificação")
        self.create_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        header.addWidget(title)
        header.addStretch()
        header.addWidget(self.create_button)

        layout.addLayout(header)

        subtitle = QLabel(
            "Organize os documentos e as evidências de regularização."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setWordWrap(True)

        layout.addWidget(subtitle)

        self.notification_list = QListWidget()
        layout.addWidget(self.notification_list, stretch=1)

        self.statusBar().showMessage(
            "Nenhuma notificação cadastrada"
        )

    def open_create_dialog(self):
        dialog = NotificationDialog(self)

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        try:
            create_notification(**data)
        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Erro ao salvar",
                f"Não foi possível criar a notificação.\n\n{error}",
            )
            return

        self.load_notifications()

    def open_notification(self, item):
        notification_id = item.data(Qt.ItemDataRole.UserRole)

        try:
            notification = get_notification(notification_id)
        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Erro ao abrir",
                f"Não foi possível carregar a notificação.\n\n{error}",
            )
            return

        if notification is None:
            QMessageBox.warning(
                self,
                "Notificação não encontrada",
                "Este registro não está mais disponível.",
            )
            self.load_notifications()
            return

        dialog = NotificationDialog(
            self,
            notification=notification,
        )

        if dialog.exec() != QDialog.DialogCode.Accepted:
            return

        data = dialog.get_data()

        try:
            update_notification(notification_id, **data)
        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Erro ao salvar",
                f"Não foi possível atualizar a notificação.\n\n{error}",
            )
            return

        self.load_notifications()

    def load_notifications(self):
        try:
            notifications = list_notifications()
        except sqlite3.Error as error:
            QMessageBox.critical(
                self,
                "Erro ao carregar",
                f"Não foi possível consultar as notificações.\n\n{error}",
            )
            return

        self.notification_list.clear()

        for notification in notifications:
            item = QListWidgetItem(
                f"{notification['identification']}\n"
                f"{notification['title']}"
            )

            # O ID identifica o registro mesmo após editar seu texto.
            item.setData(
                Qt.ItemDataRole.UserRole,
                notification["id"],
            )

            self.notification_list.addItem(item)

        total = len(notifications)

        self.statusBar().showMessage(
            f"{total} notificação cadastrada"
            if total == 1
            else f"{total} notificações cadastradas"
        )


STYLESHEET = """
QMainWindow, QWidget {
    background-color: #202226;
    color: #e1e3e7;
    font-family: "Segoe UI";
    font-size: 14px;
}

QLabel#pageTitle {
    font-size: 28px;
    font-weight: 600;
}

QLabel#subtitle {
    color: #a4a9b2;
}

QPushButton {
    background-color: #435b70;
    border: 1px solid #536d84;
    border-radius: 6px;
    padding: 10px 18px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #506a81;
}

QPushButton:pressed {
    background-color: #384e62;
}

QPushButton:focus {
    border: 1px solid #9bb4ca;
}

QPushButton:disabled {
    background-color: #30343a;
    color: #787e88;
    border-color: #3b4048;
}

QListWidget {
    background-color: #26292e;
    border: 1px solid #383d45;
    border-radius: 8px;
    padding: 8px;
}

QListWidget::item {
    padding: 14px;
    border-radius: 4px;
}

QListWidget::item:selected {
    background-color: #394b5d;
}

QStatusBar {
    color: #a4a9b2;
}

QLineEdit, QTextEdit {
    background-color: #26292e;
    border: 1px solid #454b55;
    border-radius: 5px;
    padding: 8px;
    selection-background-color: #435b70;
}

QLineEdit:focus, QTextEdit:focus {
    border: 1px solid #829bb1;
}
"""


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)

    try:
        initialize_database()
    except (sqlite3.Error, OSError) as error:
        QMessageBox.critical(
            None,
            "Erro de inicialização",
            f"Não foi possível preparar o banco de dados.\n\n{error}",
        )
        return

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()