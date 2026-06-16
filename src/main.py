from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

# Importação das suas classes de backend existentes
from models import Votacao, Opcao, Voto
from Operacoes import Operacoes
from OperacoesAdmin import OperacoesAdmin
from LogicaMotor import LogicaMotor

# 1. Configuração do Banco de Dados
DATABASE_URL = "mysql+mysqlconnector://root:123456@localhost:3306/sistema_decisoes"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 2. Inicialização do FastAPI e Configuração de Frontend
app = FastAPI(title="Sistema Inteligente de Votação")

# Monta a pasta estática para o navegador carregar o CSS
app.mount("/css", StaticFiles(directory="static/css"), name="css")

# Configura o motor de templates HTML
templates = Jinja2Templates(directory="templates")

# Dependência para injetar a sessão do banco em cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# ROTAS DO FRONTEND (Telas HTML)
# ==========================================

@app.get("/", response_class=RedirectResponse)
async def raiz():
    """Redireciona a raiz do site para a tela de login."""
    return RedirectResponse(url="/superusuario/login", status_code=303)

@app.get("/superusuario/login", response_class=HTMLResponse)
async def tela_login_admin(request: Request):
    """Renderiza a tela de login do Superusuário."""
    return templates.TemplateResponse(request=request, name="loginSU.html")

@app.get("/superusuario/painel", response_class=HTMLResponse)
async def tela_painel_admin(request: Request, db: Session = Depends(get_db)):
    """Renderiza o painel do Superusuário com os dados do banco."""
    # Exemplo: Buscando votações ativas para mostrar no painel
    votacoes = db.query(Votacao).order_by(Votacao.prazo_final.desc()).all()
    return templates.TemplateResponse(request=request, name="painelSU.html", context={"votacoes": votacoes})

@app.get("/superusuario/criar-votacao", response_class=HTMLResponse)
async def tela_criar_votacao(request: Request):
    """Renderiza a tela de criação de formulários."""
    return templates.TemplateResponse(request=request, name="criarVotacao.html")

@app.get("/superusuario/encerrar-votacao", response_class=HTMLResponse)
async def tela_encerrar_votacao(request: Request, db: Session = Depends(get_db)):
    """Renderiza a tela para encerramento manual de votações antes do prazo."""
    # Busca apenas as votações ativas para enviar ao HTML
    votacoes_ativas = db.query(Votacao).filter(Votacao.status == "ATIVA").all()
    return templates.TemplateResponse(
        request=request, 
        name="encerrarVotacao.html", 
        context={"votacoes_ativas": votacoes_ativas}
    )

@app.get("/superusuario/pesquisar-votacao", response_class=HTMLResponse)
async def tela_pesquisar_votacao(request: Request):
    """Renderiza a tela de pesquisa geral de votações."""
    return templates.TemplateResponse(
        request=request, 
        name="pesquisarVotacao.html"
    )


# ==========================================
# ROTAS DE API (Conexão com Regras de Negócio)
# ==========================================

@app.post("/api/admin/login")
async def api_admin_login(senha: str = Form(...)):
    print("Senha recebida:", senha)

    if senha == "admin123":
        print("LOGIN OK")
        return RedirectResponse(
            url="/superusuario/painel",
            status_code=303
        )

    print("LOGIN FALHOU")
    raise HTTPException(
        status_code=401,
        detail="Senha incorreta. Acesso negado."
    )

@app.post("/api/votacoes/criar")
async def api_criar_votacao(
    titulo: str = Form(...),
    descricao: str = Form(""),
    prazo_final: str = Form(...), # Esperando formato YYYY-MM-DDTHH:MM
    db: Session = Depends(get_db)
):
    """Aciona a classe Operacoes para salvar no banco."""
    operacoes = Operacoes(db)
    
    try:
        prazo_convertido = datetime.fromisoformat(prazo_final)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de data inválido.")

    nova_votacao = Votacao(
        titulo=titulo,
        descricao=descricao,
        dataCriacao=datetime.now(),
        prazo_final=prazo_convertido,
        status="ATIVA"
    )
    
    # Obs: A lógica de receber múltiplas opções do HTML (dinamicamente) exige
    # processar uma lista de campos no frontend e enviar para cá.
    operacoes.criarVotacao(nova_votacao)
    
    return {"mensagem": "Votação criada com sucesso!"}

@app.get("/api/votacoes/{id_votacao}/consenso")
async def api_ver_consenso(id_votacao: int, db: Session = Depends(get_db)):
    """Aciona o LogicaMotor (Pandas) e retorna os resultados para o painel[cite: 32]."""
    motor = LogicaMotor(db)
    
    # Chama o método que analisa os dados via DataFrame Pandas
    resultado = motor.analisarConsenso(id_votacao)
    return {"consenso": resultado}

