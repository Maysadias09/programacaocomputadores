from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from fastapi import Form
from typing import List
# Importação das suas classes de backend existentes
from models import Votacao, Opcao, Voto
from Operacoes import Operacoes
from OperacoesAdmin import OperacoesAdmin
from LogicaMotor import LogicaMotor
from fastapi.responses import RedirectResponse

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

@app.get("/usuario/login", response_class=HTMLResponse)
async def login_usuario(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="loginUsuario.html"
    )

@app.get("/usuario/votacoes", response_class=HTMLResponse)
async def tela_votar(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="votar.html"
    )

@app.get("/usuario/votar", response_class=HTMLResponse)
async def tela_votacao(
    request: Request
):
    return templates.TemplateResponse(
        request=request,
        name="votar.html"
    )    

@app.get("/votacao", response_class=HTMLResponse)
async def tela_votacao(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="votacao.html"
    )

@app.get("/resultados", response_class=HTMLResponse)
async def tela_resultados(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="resultados.html"
    )    



# ==========================================
# ROTAS DE API (Conexão com Regras de Negócio)
# ==========================================


@app.get("/api/resultados")
async def resultados(db: Session = Depends(get_db)):

    votacoes = db.query(Votacao).filter(
        Votacao.status == "ENCERRADA"
    ).all()

    retorno = []

    for votacao in votacoes:

        opcoes = db.query(Opcao).filter(
            Opcao.votacoes_idVotacoes == votacao.idVotacoes
        ).all()

        resultado = []

        total = 0

        for opcao in opcoes:

            qtd = db.query(Voto).filter(
                Voto.opcoes_idOpcoes == opcao.idOpcoes
            ).count()

            total += qtd

            resultado.append({
                "opcao": opcao.textoOpcao,
                "votos": qtd
            })

        retorno.append({
            "titulo": votacao.titulo,
            "resultado": resultado,
            "total_votos": total
        })

    return retorno

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
from typing import List

@app.post("/api/votacoes/criar")
async def api_criar_votacao(
    titulo: str = Form(...),
    descricao: str = Form(""),
    prazo_final: str = Form(...),
    opcoes: List[str] = Form(...),
    db: Session = Depends(get_db)
):

    operacoes = Operacoes(db)

    try:
        prazo_convertido = datetime.fromisoformat(prazo_final)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Formato de data inválido."
        )

    nova_votacao = Votacao(
        titulo=titulo,
        descricao=descricao,
        dataCriacao=datetime.now(),
        prazo_final=prazo_convertido,
        status="ATIVA"
    )

    # Adiciona as opções à votação
    for texto in opcoes:

        if texto.strip():

            nova_opcao = Opcao(
                textoOpcao=texto
            )

            nova_votacao.opcoes.append(
                nova_opcao
            )

    # Salva votação + opções
    operacoes.criarVotacao(nova_votacao)
    
    return RedirectResponse(
    url="/superusuario/criar-votacao?sucesso=1",
    status_code=303
)


@app.get("/api/votacoes")
async def listar_votacoes(
    db: Session = Depends(get_db)
):
    votacoes = db.query(Votacao).all()

    return [
        {
            "id": v.idVotacoes,
            "titulo": v.titulo,
            "descricao": v.descricao,
            "status": v.status
        }
        for v in votacoes
    ]
    

@app.get("/api/votacoes/{id}")
async def obter_votacao(
    id: int,
    db: Session = Depends(get_db)
):
    votacao = db.query(Votacao).filter(
        Votacao.idVotacoes == id
    ).first()

    if not votacao:
        raise HTTPException(
            status_code=404,
            detail="Votação não encontrada"
        )

    return {
        "id": votacao.idVotacoes,
        "titulo": votacao.titulo,
        "descricao": votacao.descricao,
        "dataCriacao": str(votacao.dataCriacao),
        "prazo_final": str(votacao.prazo_final),
        "status": votacao.status
    }

@app.get("/api/votacoes/{id}/opcoes")
async def listar_opcoes(
    id: int,
    db: Session = Depends(get_db)
):

    opcoes = db.query(Opcao).filter(
        Opcao.votacoes_idVotacoes == id
    ).all()

    return [
        {
            "id": o.idOpcoes,
            "texto": o.textoOpcao
        }
        for o in opcoes
    ]

@app.get("/api/votacoes/{id}/resultado")
async def resultado(
    id: int,
    db: Session = Depends(get_db)
):

    opcoes = db.query(Opcao).filter(
        Opcao.votacoes_idVotacoes == id
    ).all()

    retorno = []

    total = 0

    for opcao in opcoes:

        qtd = db.query(Voto).filter(
            Voto.opcoes_idOpcoes == opcao.idOpcoes
        ).count()

        total += qtd

        retorno.append({
            "texto": opcao.textoOpcao,
            "votos": qtd
        })

    for item in retorno:

        item["percentual"] = (
            item["votos"] * 100 / total
        ) if total > 0 else 0

    return retorno

@app.post("/api/votar")
async def votar(
    id_opcao: int,
    db: Session = Depends(get_db)
):

    opcao = db.query(Opcao).filter(
        Opcao.idOpcoes == id_opcao
    ).first()

    if not opcao:
        raise HTTPException(
            status_code=404,
            detail="Opção não encontrada"
        )

    voto = Voto(
       matriculaUsuario=f"TESTE_{datetime.now().timestamp()}",
        votacoes_idVotacoes=opcao.votacoes_idVotacoes,
        opcoes_idOpcoes=id_opcao
    )

    db.add(voto)
    db.commit()

    return {"ok": True}


@app.post("/api/votacoes/{id}/encerrar")
async def encerrar_votacao(
    id: int,
    db: Session = Depends(get_db)
):

    votacao = db.query(Votacao).filter(
        Votacao.idVotacoes == id
    ).first()

    if not votacao:
        raise HTTPException(404)

    votacao.status = "ENCERRADA"

    db.commit()

    return {
        "mensagem": "Votação encerrada com sucesso"
    }    

@app.get("/api/dashboard")
async def dashboard(
    db: Session = Depends(get_db)
):

    return {
        "ativas":
            db.query(Votacao)
            .filter(Votacao.status=="ATIVA")
            .count(),

        "encerradas":
            db.query(Votacao)
            .filter(Votacao.status=="ENCERRADA")
            .count(),

        "votos":
            db.query(Voto).count()
    }

