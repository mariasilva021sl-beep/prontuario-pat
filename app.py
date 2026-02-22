import os
import sys
from flask import Flask
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from config import Config
from extensions import db, login_manager, bcrypt
from models.usuario import Usuario
from models.paciente import Paciente
from models.profissional import Profissional
from models.agenda import Agenda
from models.triagem import Triagem
from models.fila import FilaEspera
from models.atendimento import Atendimento
from models.soap import Soap
from models.prescricao import Prescricao
from models.injetavel import Injetavel, InjetavelEstoque, InjetavelLote
from models.relatorio import Relatorio
from models.medicacao import MedicacaoClinica
from models.documento import DocumentoClinico
from models.especialidade import Especialidade
from models.anamnese import AnamneseClinica
from models.procedimento import Procedimento
from models.pagamento import Pagamento
from models.financeiro import FinanceiroLancamento
from models.medicamento_catalogo import MedicamentoCatalogo
from routes.auth import auth_bp
from routes.dashboard import dashboard_bp
from routes.pacientes import pacientes_bp
from routes.agenda import agenda_bp
from routes.fila import fila_bp
from routes.atendimento import atendimento_bp
from routes.triagem import triagem_bp
from routes.prontuario import prontuario_bp
from routes.prescricao import prescricao_bp
from routes.injetaveis import injetaveis_bp
from routes.admin import admin_bp
from routes.relatorios import relatorios_bp
from routes.api import api_bp
from routes.medicacao import medicacao_bp
from routes.pagamentos import pagamentos_bp
from routes.financeiro import financeiro_bp


login_manager.login_view = "auth.login"
login_manager.login_message_category = "warning"


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(pacientes_bp)
    app.register_blueprint(agenda_bp)
    app.register_blueprint(fila_bp)
    app.register_blueprint(atendimento_bp)
    app.register_blueprint(triagem_bp)
    app.register_blueprint(prontuario_bp)
    app.register_blueprint(prescricao_bp)
    app.register_blueprint(injetaveis_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(relatorios_bp)
    app.register_blueprint(medicacao_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(pagamentos_bp)
    app.register_blueprint(financeiro_bp)

    with app.app_context():
        db.create_all()
        _seed_admin()
        _seed_injetaveis()
        _seed_especialidades()
        _seed_medicamentos_catalogo()

    return app


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


def _seed_admin():
    if Usuario.query.first():
        return
    admin_user = os.getenv("ADMIN_USER", "admin")
    admin_pass = os.getenv("ADMIN_PASS", "admin123")
    Usuario.create_admin(admin_user, admin_pass)


def _seed_injetaveis():
    nomes_estoque = {
        "Dipirona injetavel",
        "Diclofenaco injetavel",
        "Dexametasona injetavel",
        "Ceftriaxona injetavel",
        "Benzetacil",
        "Hidrocortisona",
    }
    for nome, _categoria in _medicamentos_padrao():
        nomes_estoque.add(nome)

    for nome in sorted(nomes_estoque):
        existente = InjetavelEstoque.query.filter(InjetavelEstoque.nome.ilike(nome)).first()
        if not existente:
            existente = InjetavelEstoque(nome=nome, unidade="unidade")
            db.session.add(existente)
            db.session.flush()

        lote_disponivel = (
            InjetavelLote.query
            .filter_by(estoque_id=existente.id, lote="INI-001")
            .first()
        )
        if not lote_disponivel:
            db.session.add(
                InjetavelLote(
                    estoque_id=existente.id,
                    lote="INI-001",
                    validade=None,
                    quantidade=20,
                )
            )
    db.session.commit()


def _seed_especialidades():
    if Especialidade.query.first():
        return
    nomes = [
        "Clinico",
        "Dermatologia",
        "Psiquiatria",
        "Injetaveis",
        "Outros",
    ]
    for nome in nomes:
        db.session.add(Especialidade(nome=nome))
    db.session.commit()


def _seed_medicamentos_catalogo():
    medicamentos = _medicamentos_padrao()
    for nome, categoria in medicamentos:
        if not MedicamentoCatalogo.query.filter_by(nome=nome).first():
            db.session.add(MedicamentoCatalogo(nome=nome, categoria=categoria))
    db.session.commit()


def _medicamentos_padrao():
    return [
        ("Dipirona sódica", "Analgésicos / Antitérmicos"),
        ("Paracetamol", "Analgésicos / Antitérmicos"),
        ("Ibuprofeno", "Analgésicos / Antitérmicos"),
        ("Ácido acetilsalicílico (AAS)", "Analgésicos / Antitérmicos"),
        ("Cetoprofeno", "Analgésicos / Antitérmicos"),
        ("Tramadol", "Analgésicos / Antitérmicos"),
        ("Codeína + Paracetamol", "Analgésicos / Antitérmicos"),
        ("Diclofenaco sódico", "Anti-inflamatórios (AINEs)"),
        ("Diclofenaco potássico", "Anti-inflamatórios (AINEs)"),
        ("Nimesulida", "Anti-inflamatórios (AINEs)"),
        ("Meloxicam", "Anti-inflamatórios (AINEs)"),
        ("Piroxicam", "Anti-inflamatórios (AINEs)"),
        ("Naproxeno", "Anti-inflamatórios (AINEs)"),
        ("Indometacina", "Anti-inflamatórios (AINEs)"),
        ("Amoxicilina", "Antibióticos"),
        ("Amoxicilina + Clavulanato", "Antibióticos"),
        ("Benzilpenicilina benzatina", "Antibióticos"),
        ("Cefalexina", "Antibióticos"),
        ("Ceftriaxona", "Antibióticos"),
        ("Cefuroxima", "Antibióticos"),
        ("Azitromicina", "Antibióticos"),
        ("Claritromicina", "Antibióticos"),
        ("Ciprofloxacino", "Antibióticos"),
        ("Levofloxacino", "Antibióticos"),
        ("Metronidazol", "Antibióticos"),
        ("Sulfametoxazol + Trimetoprima", "Antibióticos"),
        ("Loratadina", "Anti-alérgicos / Respiratórios"),
        ("Desloratadina", "Anti-alérgicos / Respiratórios"),
        ("Cetirizina", "Anti-alérgicos / Respiratórios"),
        ("Fexofenadina", "Anti-alérgicos / Respiratórios"),
        ("Dexclorfeniramina", "Anti-alérgicos / Respiratórios"),
        ("Prednisolona", "Anti-alérgicos / Respiratórios"),
        ("Budesonida inalatório", "Anti-alérgicos / Respiratórios"),
        ("Salbutamol", "Anti-alérgicos / Respiratórios"),
        ("Losartana", "Cardiovasculares"),
        ("Enalapril", "Cardiovasculares"),
        ("Captopril", "Cardiovasculares"),
        ("Amlodipina", "Cardiovasculares"),
        ("Hidroclorotiazida", "Cardiovasculares"),
        ("Atenolol", "Cardiovasculares"),
        ("Sinvastatina", "Cardiovasculares"),
        ("Atorvastatina", "Cardiovasculares"),
        ("Espironolactona", "Cardiovasculares"),
        ("Furosemida", "Cardiovasculares"),
        ("Metformina", "Diabetes"),
        ("Glibenclamida", "Diabetes"),
        ("Gliclazida", "Diabetes"),
        ("Insulina NPH", "Diabetes"),
        ("Insulina Regular", "Diabetes"),
        ("Sertralina", "Sistema Nervoso Central"),
        ("Fluoxetina", "Sistema Nervoso Central"),
        ("Escitalopram", "Sistema Nervoso Central"),
        ("Amitriptilina", "Sistema Nervoso Central"),
        ("Clonazepam", "Sistema Nervoso Central"),
        ("Diazepam", "Sistema Nervoso Central"),
        ("Carbamazepina", "Sistema Nervoso Central"),
        ("Fenitoína", "Sistema Nervoso Central"),
        ("Valproato de sódio", "Sistema Nervoso Central"),
        ("Omeprazol", "Gastrointestinais"),
        ("Pantoprazol", "Gastrointestinais"),
        ("Ranitidina", "Gastrointestinais"),
        ("Ondansetrona", "Gastrointestinais"),
        ("Metoclopramida", "Gastrointestinais"),
        ("Dimeticona", "Gastrointestinais"),
        ("Hidrocortisona", "Dermatológicos"),
        ("Betametasona", "Dermatológicos"),
        ("Miconazol", "Dermatológicos"),
        ("Nistatina", "Dermatológicos"),
        ("Neomicina + Bacitracina", "Dermatológicos"),
        ("Permetrina", "Dermatológicos"),
        ("Sulfato ferroso", "Hematológicos / Suplementos"),
        ("Ácido fólico", "Hematológicos / Suplementos"),
        ("Vitamina B12", "Hematológicos / Suplementos"),
        ("Vitamina D", "Hematológicos / Suplementos"),
        ("Cálcio + Vitamina D", "Hematológicos / Suplementos"),
    ]


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
