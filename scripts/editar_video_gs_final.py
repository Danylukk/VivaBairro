"""Edição final ajustada ao barema de Front-end 2026.2 (4min52s).

Usa vídeo real da aplicação (modo demo), erro isolado capturado e
trechos de código lidos diretamente do repositório. Não chama OpenAI.
"""
from pathlib import Path
import json
import subprocess
from PIL import Image, ImageDraw, ImageFont
from scripts import editar_video_gs as e

TOTAL=18
ROOT=e.ROOT
BUILD=e.BUILD
OUTPUT=e.OUT


def chrome18(im,eyebrow,original_index):
    index=(-original_index if original_index < 0 else {1:1,2:2,3:3,11:12,12:16,13:17,14:18}.get(original_index,original_index))
    dr=ImageDraw.Draw(im)
    e.label(dr,eyebrow)
    dr.rounded_rectangle((100,819,1500,825),radius=4,fill=(31,107,114,130))
    dr.rounded_rectangle((100,819,100+round(1400*index/TOTAL),825),radius=4,fill=e.SEA)
    e.text(dr,(100,843),"VIVABAIRRO • GLOBAL SOLUTION 2026.2",17,e.MUTED,True)
    e.text(dr,(1500,843),f"{index:02d} / {TOTAL:02d}",17,e.MUTED,True,anchor="ra")


def overlay18(title,subtitle,num):
    im=Image.new("RGBA",(e.W,e.H),(0,0,0,0))
    dr=ImageDraw.Draw(im)
    dr.rounded_rectangle((1200,23,1545,78),radius=22,fill=(13,40,53,218))
    e.text(dr,(1372,50),"MODO DEMONSTRAÇÃO",19,e.WHITE,True,"mm")
    for y in range(723,900):
        dr.rectangle((0,y,e.W,y+1),fill=(7,29,44,245))
    dr.rectangle((0,719,17,900),fill=(*e.SEA,255))
    e.text(dr,(65,748),f"{num:02d} / {TOTAL:02d}",28,e.SEA,True)
    e.text(dr,(225,746),title,40,e.WHITE,True)
    e.text(dr,(65,820),subtitle,26,e.WHITE)
    dr.rectangle((65,891,65+round((e.W-130)*num/TOTAL),896),fill=(*e.SEA,255))
    return im


e.chrome=chrome18
e.overlay_image=overlay18

def mono(size):
    p=Path("C:/Windows/Fonts/consola.ttf")
    return ImageFont.truetype(str(p),size) if p.exists() else e.font(size)


def draw_panel(dr,box,title,path,markers,size=18):
    x0,y0,x1,y1=box
    dr.rounded_rectangle(box,radius=23,fill=(16,66,74,255),outline=(44,152,143,200),width=2)
    e.text(dr,(x0+23,y0+20),title,30,e.WHITE,True)
    e.text(dr,(x0+23,y0+64),path,19,e.SEA)
    dr.line((x0+22,y0+102,x1-22,y0+102),fill=(58,157,158,160),width=2)
    source=(ROOT/path).read_text(encoding="utf-8").splitlines()
    f=mono(size)
    y=y0+125
    for needle in markers:
        found=[(i+1,l) for i,l in enumerate(source) if needle in l]
        if not found: raise ValueError(f"Missing {path}: {needle}")
        ln,line=found[0]
        full=line.rstrip()
        # Como em um editor de código: linhas longas são cortadas visualmente.
        while dr.textbbox((0,0),line,font=f)[2]>x1-x0-120 and len(line)>16:
            line=line[:-1]
        if line!=full: line=line.rstrip()+"..."
        e.text(dr,(x0+22,y),f"{ln:>3}",size-2,(110,168,170))
        dr.text((x0+79,y),line,font=f,fill=(235,251,251))
        y+=38
        if y>y1-28:break


def code_layout(eyebrow,number,title,subtitle,left,right,bottom):
    im=e.background()
    dr=ImageDraw.Draw(im)
    chrome18(im,eyebrow,-number)
    e.text(dr,(100,142),title,58,e.WHITE,True)
    e.add_lines(dr,224,subtitle,27,e.MUTED,width=1420)
    draw_panel(dr,(100,318,785,720),*left)
    draw_panel(dr,(817,318,1500,720),*right)
    e.text(dr,(100,756),bottom,22,e.SEA)
    return im


def make_llm():
    return code_layout("CÓDIGO REAL  /  INTEGRAÇÃO LLM",13,
        "Onde a IA é chamada?",
        "Streamlit → FastAPI /api/v1/analises → LLM no back-end.",
        ("CLIENTE HTTP","frontend/providers/api.py",[
            "def enviar_relato(payload:",
            "Não usar cache para conteúdos",
            "with httpx.Client(timeout=32)",
            "response = client.post(f",
            "response.raise_for_status()",
        ]),
        ("PROVEDOR DA IA","backend/app/providers/llm.py",[
            "def analisar_openai(",
            "schema = ResultadoIA.model_json_schema()",
            '"response_format":',
            "url = f",
            "with httpx.Client(timeout=",
            "response = client.post(",
            "return ResultadoIA.model_validate_json",
        ]),
        "Pydantic valida a resposta  •  A chave nunca é enviada ao navegador")


def make_state():
    return code_layout("CÓDIGO REAL  /  ESTADO E CACHE",14,
        "Estado local. Cache seletivo.",
        "O histórico persiste no session_state; não há cache de relatos individuais.",
        ("ESTADO DA SESSÃO","frontend/state/store.py",[
            "def inicializar()",
            '"registros": [],',
            '"pendente": None,',
            '"pagina": "Fazer relato",',
            "if nome not in st.session_state:",
            "st.session_state[nome] =",
        ]),
        ("CACHE DE STATUS","frontend/providers/api.py",[
            "@st.cache_data(ttl=20, show_spinner=False)",
            "def obter_status(url: str)",
            "with httpx.Client(timeout=3)",
            "resposta = client.get",
            "Não usar cache para conteúdos",
        ]),
        "Segredos: .env fora do Git • OPENAI_API_KEY via variável de ambiente")


def make_docker():
    return code_layout("DEPLOY  /  DOCKER COMPOSE",15,
        "Aplicação reproduzível.",
        "FastAPI e Streamlit em serviços separados, com saúde e dependências.",
        ("SERVIÇO API","docker-compose.yml",[
            "services:","  api:",
            "dockerfile: backend/Dockerfile",
            "LLM_PROVIDER:",
            '"127.0.0.1:8000:8000"',
            "healthcheck:",
        ]),
        ("SERVIÇO WEB","docker-compose.yml",[
            "  web:",
            "dockerfile: frontend/Dockerfile",
            "API_BASE_URL: http://api:8000",
            "depends_on:",
            "condition: service_healthy",
            '"8501:8501"',
        ]),
        "docker compose up --build  •  Execução Docker validada anteriormente")


def error_overlay():
    im=Image.new("RGBA",(e.W,e.H),(0,0,0,0))
    dr=ImageDraw.Draw(im)
    dr.rounded_rectangle((1060,25,1545,82),radius=20,fill=(76,49,41,231))
    e.text(dr,(1302,54),"CENÁRIO CONTROLADO",20,e.WHITE,True,"mm")
    for y in range(720,900):
        dr.rectangle((0,y,e.W,y+1),fill=(7,29,44,245))
    dr.rectangle((0,718,18,900),fill=(242,167,87,255))
    e.text(dr,(64,748),"10 / 18",27,(242,177,103),True)
    e.text(dr,(225,747),"API INDISPONÍVEL",41,e.WHITE,True)
    e.text(dr,(65,822),"Mensagem de erro compreensível; sem expor detalhes técnicos.",27,e.WHITE)
    dr.rectangle((65,890,65+round((e.W-130)*10/TOTAL),896),fill=(242,177,103,255))
    return im


def error_clip(item,duration,index):
    overlay=BUILD/"overlay_erro_final.png"
    error_overlay().save(overlay)
    m=next(x for x in item["bookmarks"] if x["name"]=="ui_erro")
    out=BUILD/f"clip_{index:02d}.mp4"
    filt=(f"[0:v]fps={e.FPS},scale={e.W}:{e.H}:flags=lanczos[screen];"
          f"[screen][1:v]overlay=0:0:shortest=1,"
          f"fade=t=in:st=0:d=0.4,fade=t=out:st={duration-0.4}:d=0.4,"
          "format=yuv420p[v]")
    e.run_ffmpeg(["-ss",str(m["ss"]+3.5),"-i",item["file"],
                  "-loop","1","-i",str(overlay),
                  "-filter_complex",filt,"-map","[v]","-t",str(duration),
                  "-c:v","libx264","-preset","veryfast","-crf","24",
                  "-r",str(e.FPS),"-pix_fmt","yuv420p","-an",str(out)],"erro")
    return out


def main():
    manifest=json.loads(e.SRC.read_text(encoding="utf-8"))
    assert "erro" in manifest
    plan=[
      ("intro",10,e.make_intro),
      ("problema",15,e.make_problem),
      ("solucao",10,e.make_solution),
      ("ui_inicio",11,("relato","CIDADÃO NO CENTRO","Uma jornada guiada para qualquer morador.")),
      ("ui_formulario",24,("relato","DO RELATO À SUGESTÃO","Bairro, categoria e descrição de um problema urbano.")),
      ("ui_analise",18,("relato","SUGESTÃO ASSISTIDA","Regras locais: demonstração não é resposta do LLM real.")),
      ("ui_revisao",22,("relato","REVISÃO HUMANA","O cidadão confere e pode corrigir a sugestão.")),
      ("ui_recibo",12,("relato","COMPROVANTE TEMPORÁRIO","Código local; não é protocolo oficial da Prefeitura.")),
      ("ui_painel",26,("painel","PAINEL DE RELATOS","Filtros e gráficos Plotly com exemplos fictícios.")),
      ("ui_erro",12,None),
      ("ui_ods",12,("ods","ÉTICA E IMPACTO","ODS 11 e 16, privacidade e limites do protótipo.")),
      ("arquitetura",20,e.make_architecture),
      ("chamada_llm",18,make_llm),
      ("estado_cache",16,make_state),
      ("docker",14,make_docker),
      ("evidencias",17,e.make_evidence),
      ("feedback",20,e.make_feedback),
      ("final",15,e.make_final),
    ]
    assert sum(x[1] for x in plan)==292
    clips=[]
    for i,(name,seconds,asset) in enumerate(plan,1):
        print(f"CAPÍTULO {i:02d}/18: {name} ({seconds}s)",flush=True)
        if callable(asset):
            out=e.create_static(name,asset(),seconds,i)
        elif name=="ui_erro":
            out=error_clip(manifest["erro"],seconds,i)
        else:
            src,title,subtitle=asset
            item=manifest[src]
            mark=next(x for x in item["bookmarks"] if x["name"]==name).copy()
            mark["ss"]+= {"ui_formulario":3,"ui_painel":5,"ui_ods":1}.get(name,0)
            out=e.create_browser(name,item["file"],mark,seconds,title,subtitle,i)
        clips.append(out)
    listing=BUILD/"concat_final.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips),encoding="utf-8")
    e.run_ffmpeg(["-f","concat","-safe","0","-i",str(listing),
                  "-c","copy","-movflags","+faststart",str(e.OUT)],"video_final")
    check=subprocess.run([e.FFMPEG,"-hide_banner","-i",str(e.OUT)],
                         capture_output=True,text=True).stderr
    assert "Duration: 00:04:52." in check,check[-1200:]
    assert "1600x900" in check and "Audio:" not in check
    print("VÍDEO FINAL: ",e.OUT,"DURAÇÃO 04:52",flush=True)

if __name__=="__main__":
    main()
