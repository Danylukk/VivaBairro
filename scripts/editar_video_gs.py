"""Edita video de demonstração silencioso com telas reais e legendas.

Uso: python -m scripts.editar_video_gs
Exige scripts.gravar_demo_video executado e artefatos temp presentes.
"""
from __future__ import annotations
import json
import math
import os
import subprocess
import tempfile
from pathlib import Path
import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT=Path(__file__).resolve().parents[1]
BUILD=Path(tempfile.gettempdir())/"VivaBairro_Video_GS_20261113"
SRC=BUILD/"manifest.json"
OUT=ROOT/"docs"/"video"/"VivaBairro_GS2026_2_Demo_SemAudio.mp4"
FFMPEG=imageio_ffmpeg.get_ffmpeg_exe()
W,H=1600,900
FPS=20

INK=(9,30,43)
INK2=(18,58,69)
TEAL=(17,169,147)
SEA=(34,215,178)
WHITE=(246,254,254)
MUTED=(173,204,209)

FONTDIR=Path("C:/Windows/Fonts")
def font(size,bold=False):
    options=(["seguisb.ttf","arialbd.ttf"] if bold else ["segoeui.ttf","arial.ttf"])
    for f in options:
        p=FONTDIR/f
        if p.exists():
            return ImageFont.truetype(str(p),size)
    return ImageFont.load_default()


def background():
    y=np.linspace(0,1,H,dtype=np.float32)[:,None,None]
    top=np.array(INK,dtype=np.float32)[None,None,:]
    bottom=np.array((7,48,55),dtype=np.float32)[None,None,:]
    rgb=np.uint8(np.clip(top*(1-y)+bottom*y,0,255))
    arr=np.tile(rgb,(1,W,1))
    im=Image.fromarray(arr,mode="RGB").convert("RGBA")
    deco=Image.new("RGBA",(W,H),(0,0,0,0))
    q=ImageDraw.Draw(deco)
    for i in range(5):
        radius=180+i*90
        q.ellipse((W-160-radius,40-radius,W-160+radius,40+radius),outline=(48,231,194,25),width=3)
    for yy in range(0,H,80):
        q.line([(0,yy),(W,yy)],fill=(120,219,205,8),width=1)
    for xx in range(0,W,80):
        q.line([(xx,0),(xx,H)],fill=(120,219,205,8),width=1)
    im.alpha_composite(deco)
    return im

def text(draw,xy,value,size,color=WHITE,bold=False,anchor=None):
    draw.text(xy,value,font=font(size,bold),fill=color,anchor=anchor,stroke_width=0)

def label(draw,value,x=100,y=87):
    text(draw,(x,y),value,22,SEA,True)

def pill(draw,box,value,fill=(13,77,81,235),color=SEA):
    draw.rounded_rectangle(box,radius=22,fill=fill,outline=(51,137,129,180),width=2)
    text(draw,((box[0]+box[2])/2,(box[1]+box[3])/2),value,20,color,True,"mm")

def wrap(draw,words,max_width,size,bold=False):
    result=[];line=""
    f=font(size,bold)
    for word in words.split():
        trial=(line+" "+word).strip()
        if draw.textbbox((0,0),trial,font=f)[2]>max_width and line:
            result.append(line);line=word
        else:line=trial
    if line:result.append(line)
    return result

def add_lines(draw,y,message,size=32,col=MUTED,x=100,width=1410,lineheight=None,bold=False):
    lineheight=lineheight or int(size*1.4)
    for s in wrap(draw,message,width,size,bold):
        text(draw,(x,y),s,size,col,bold)
        y+=lineheight
    return y

def chrome(im,eyebrow,chapter):
    q=ImageDraw.Draw(im)
    label(q,eyebrow)
    q.rounded_rectangle((100,819,1500,825),radius=4,fill=(31,107,114,130))
    q.rounded_rectangle((100,819,100+1400*chapter/14,825),radius=4,fill=SEA)
    text(q,(100,843),"VIVABAIRRO  •  GLOBAL SOLUTION 2026.2",17,MUTED,True)
    text(q,(1500,843),f"{chapter:02d} / 14",17,MUTED,True,anchor="ra")

def make_intro():
    im=background();q=ImageDraw.Draw(im)
    chrome(im,"FIAP   /   CITIZENTECH   /   2026.2",1)
    q.rounded_rectangle((100,188,112,594),radius=6,fill=SEA)
    text(q,(148,190),"VivaBairro",104,WHITE,True)
    text(q,(152,333),"Sua voz na cidade",50,SEA)
    add_lines(q,439,"Uma experiência mais clara para relatar e entender problemas urbanos.",35,WHITE,x=152,width=1090)
    pill(q,(150,635,565,694),"DEMONSTRAÇÃO DO PROTÓTIPO")
    return im

def make_problem():
    im=background();q=ImageDraw.Draw(im);chrome(im,"01   /   O DESAFIO",2)
    text(q,(100,157),"Problemas urbanos.",66,WHITE,True)
    text(q,(100,239),"Comunicação nem sempre simples.",47,SEA)
    labs=[("01","Calçadas danificadas"),("02","Buracos nas vias"),
          ("03","Iluminação pública"),("04","Alagamentos")]
    for i,(num,description) in enumerate(labs):
        left=100+i*355
        q.rounded_rectangle((left,385,left+325,615),radius=28,
            fill=(20,70,75,240),outline=(50,134,127,110),width=2)
        text(q,(left+23,413),num,30,SEA,True)
        for j,line in enumerate(wrap(q,description,275,30,True)):
            text(q,(left+23,480+j*40),line,30,WHITE,True)
    add_lines(q,680,"O cidadão precisa de orientação, clareza e controle sobre o relato.",31,WHITE)
    return im

def make_solution():
    im=background();q=ImageDraw.Draw(im);chrome(im,"02   /   A PROPOSTA",3)
    text(q,(100,168),"Do problema à informação útil.",66,WHITE,True)
    stages=[("01","Relatar"),("02","Analisar"),("03","Revisar"),("04","Acompanhar")]
    for i,(num,t) in enumerate(stages):
        left=100+i*355
        q.rounded_rectangle((left,390,left+316,575),radius=28,
           fill=(21,83,82,245),outline=(45,166,150,175),width=3)
        text(q,(left+24,413),num,33,SEA,True)
        text(q,(left+24,474),t,43,WHITE,True)
        if i<3: text(q,(left+328,447),"›",57,SEA,True)
    add_lines(q,661,"IA como apoio. Confirmação sempre humana.",34,SEA,True)
    return im

def make_architecture():
    im=background();q=ImageDraw.Draw(im);chrome(im,"03   /   COMO FOI CONSTRUÍDO",11)
    text(q,(100,159),"Arquitetura modular",67,WHITE,True)
    text(q,(100,260),"Do formulário à resposta validada",33,MUTED)
    layers=[
        ("STREAMLIT","Interface e estado"),
        ("FASTAPI","Processamento HTTP"),
        ("PYDANTIC","Validação rigorosa"),
        ("OPENAI","Integração validada")
    ]
    for i,(title,subtitle) in enumerate(layers):
        left=100+i*355
        q.rounded_rectangle((left,380,left+320,606),radius=26,
            fill=(20,70,75,245),outline=(42,175,157,175),width=2)
        text(q,(left+19,405),f"0{i+1}",25,SEA,True)
        text(q,(left+19,460),title,32,WHITE,True)
        text(q,(left+19,517),subtitle,24,MUTED)
    q.rounded_rectangle((100,671,1500,753),radius=18,fill=(8,48,60,230))
    add_lines(q,686,"Neste vídeo: análise por regras locais. 3 chamadas reais ao LLM já validadas separadamente.",24,WHITE,x=127,width=1350)
    return im

def make_evidence():
    im=background();q=ImageDraw.Draw(im);chrome(im,"04   /   EVIDÊNCIAS",12)
    text(q,(100,148),"Testado. Documentado. Revisado.",59,WHITE,True)
    tiles=[
        ("48 / 48","TESTES APROVADOS","Pytest; E2E validados à parte"),
        ("03","INFERÊNCIAS REAIS","OpenAI • respostas validadas"),
        ("03","PESSOAS OUVIDAS","Feedback externo documentado"),
    ]
    for i,(n,lab,sub) in enumerate(tiles):
        left=100+i*471
        q.rounded_rectangle((left,335,left+435,664),radius=27,
                           fill=(16,75,81,240),outline=(44,171,154,175),width=3)
        text(q,(left+30,359),n,75,SEA,True)
        text(q,(left+30,488),lab,25,WHITE,True)
        add_lines(q,544,sub,23,MUTED,x=left+30,width=365)
    return im

def fit_image(img,box):
    # top crop screenshots of the real UI, not fictitious mockups
    x0,y0,x1,y1=box; tw=x1-x0; th=y1-y0
    img=img.convert("RGB")
    iw,ih=img.size
    ratio=max(tw/iw,th/ih)
    nw,nh=math.ceil(iw*ratio),math.ceil(ih*ratio)
    img=img.resize((nw,nh),Image.Resampling.LANCZOS)
    # crop from upper region for visibility of analysis and revision sections
    x=max(0,(nw-tw)//2);y=max(0,min((nh-th)//5,nh-th))
    return img.crop((x,y,x+tw,y+th))

def make_feedback():
    im=background();q=ImageDraw.Draw(im);chrome(im,"05   /   MELHORIA A PARTIR DE USUÁRIA REAL",13)
    text(q,(100,132),"Menos ruído. Mais clareza.",64,WHITE,True)
    before=ROOT/"docs"/"evidencias"/"feedback_usabilidade_20261113"/"antes"/"desktop_revisao.png"
    after=ROOT/"docs"/"evidencias"/"feedback_usabilidade_20261113"/"depois"/"desktop_revisao.png"
    box_left=(100,310,773,715);box_right=(827,310,1500,715)
    for pic,box in [(before,box_left),(after,box_right)]:
        assert pic.exists(),pic
        q.rounded_rectangle((box[0]-3,box[1]-3,box[2]+3,box[3]+3),radius=19,fill=(29,130,127,210))
        img=fit_image(Image.open(pic), (0,0,box[2]-box[0],box[3]-box[1]))
        im.alpha_composite(img.convert("RGBA"),(box[0],box[1]))
    q=ImageDraw.Draw(im)
    pill(q,(111,257,345,302),"ANTES  /  MAIS TEXTO",fill=(48,63,72,245),color=WHITE)
    pill(q,(838,257,1185,302),"DEPOIS  /  FOCO NA AÇÃO",fill=(8,104,89,255),color=WHITE)
    text(q,(780,483),"→",50,SEA,True,anchor="mm")
    text(q,(105,742),"Feedback: excesso de informações → detalhes opcionais, sem perder alertas.",25,MUTED)
    return im

def make_final():
    im=background();q=ImageDraw.Draw(im);chrome(im,"VIVABAIRRO   /   SUA VOZ NA CIDADE",14)
    text(q,(100,206),"Uma cidade melhor",76,WHITE,True)
    text(q,(100,307),"começa com informação clara.",65,SEA,True)
    q.rounded_rectangle((100,485,1467,610),radius=24,fill=(16,74,77,235))
    text(q,(129,512),"github.com/Danylukk/VivaBairro",39,WHITE,True)
    add_lines(q,666,"Protótipo acadêmico • Sem protocolos oficiais • Supervisão humana",28,MUTED)
    return im

def overlay_image(title,subtitle,num):
    im=Image.new("RGBA",(W,H),(0,0,0,0))
    draw=ImageDraw.Draw(im)
    # Top right transparency, but no screen data obscuring the middle.
    draw.rounded_rectangle((1210,25,1545,79),radius=22,fill=(13,40,53,218))
    text(draw,(1378,52),"MODO DEMONSTRAÇÃO",19,WHITE,True,"mm")
    # A solid semi-transparent lower-third ensures legibility without sound.
    for row in range(723,900):
        opa=int(215+(row-723)*38/177)
        draw.rectangle((0,row,W,row+1),fill=(7,29,44,opa))
    draw.rectangle((0,719,17,900),fill=(*SEA,255))
    text(draw,(65,748),f"{num:02d} / 14",28,SEA,True)
    text(draw,(229,747),title,41,WHITE,True)
    text(draw,(65,820),subtitle,27,WHITE)
    draw.rectangle((65,890,65+int((W-130)*num/14),896),fill=(*SEA,255))
    return im

def run_ffmpeg(args,tag):
    result=subprocess.run([FFMPEG,"-hide_banner","-loglevel","error","-y",*args],
                          text=True,capture_output=True)
    if result.returncode!=0:
        print("FFMPEG ERROR",tag,result.stderr[-3500:],flush=True)
        raise RuntimeError("ffmpeg falhou em "+tag)
    print("ENCODED",tag,flush=True)

def create_static(name,img,duration,index):
    src=BUILD/f"{name}.png";out=BUILD/f"clip_{index:02d}.mp4"
    img.convert("RGB").save(src,optimize=True)
    filters=f"fade=t=in:st=0:d=0.4,fade=t=out:st={duration-0.4}:d=0.4,format=yuv420p"
    run_ffmpeg(["-loop","1","-framerate",str(FPS),"-i",str(src),
                 "-t",str(duration),"-vf",filters,"-c:v","libx264",
                 "-preset","veryfast","-crf","25","-r",str(FPS),
                 "-pix_fmt","yuv420p","-an",str(out)],name)
    return out

def create_browser(name,source,bookmark,duration,title,subtitle,index):
    overlay=BUILD/f"lower_{index:02d}.png"
    overlay_image(title,subtitle,index).save(overlay)
    ss=bookmark["ss"]
    output=BUILD/f"clip_{index:02d}.mp4"
    filt=(f"[0:v]fps={FPS},scale={W}:{H}:flags=lanczos[screen];"
          f"[screen][1:v]overlay=0:0:shortest=1,"
          f"fade=t=in:st=0:d=0.4,fade=t=out:st={duration-0.4}:d=0.4,"
          f"format=yuv420p[v]")
    run_ffmpeg(["-ss",str(ss),"-i",source,"-loop","1","-i",str(overlay),
                "-filter_complex",filt,"-map","[v]","-t",str(duration),
                "-c:v","libx264","-preset","veryfast","-crf","24",
                "-r",str(FPS),"-pix_fmt","yuv420p","-an",str(output)],name)
    return output

def main():
    assert SRC.exists(),"Execute scripts.gravar_demo_video antes da edição."
    manifest=json.loads(SRC.read_text(encoding="utf-8"))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    plan=[
      ("intro",12,make_intro),
      ("problema",17,make_problem),
      ("solucao",12,make_solution),
      ("ui_inicio",16,("relato","CIDADÃO NO CENTRO","Uma jornada guiada para qualquer morador.")),
      ("ui_formulario",27,("relato","DO RELATO À SUGESTÃO","Descreva o problema e veja a classificação preliminar.")),
      ("ui_analise",22,("relato","SUGESTÃO ASSISTIDA","No vídeo: regras de demonstração; não é resposta de IA real.")),
      ("ui_revisao",25,("relato","REVISÃO HUMANA","Você confere e pode corrigir categoria, prioridade e resumo.")),
      ("ui_recibo",13,("relato","COMPROVANTE TEMPORÁRIO","Código local. Não é protocolo oficial da Prefeitura.")),
      ("ui_painel",34,("painel","PAINEL DE RELATOS","Filtros e gráficos Plotly com exemplos fictícios identificados.")),
      ("ui_ods",14,("ods","TRANSPARÊNCIA E IMPACTO","ODS 11 e 16, privacidade e limites da inteligência artificial.")),
      ("arquitetura",22,make_architecture),
      ("evidencias",23,make_evidence),
      ("feedback",22,make_feedback),
      ("final",16,make_final)
    ]
    assert sum(item[1] for item in plan)==275
    clips=[]
    for index,(name,duration,asset) in enumerate(plan,1):
        print(f"PROCESSANDO {index}/{len(plan)}: {name} ({duration}s)",flush=True)
        if callable(asset):
            clips.append(create_static(name,asset(),duration,index))
        else:
            source_name,title,sub=asset
            item=manifest[source_name]
            mark=next(b for b in item["bookmarks"] if b["name"]==name)
            clips.append(create_browser(name,item["file"],mark,duration,title,sub,index))
    listfile=BUILD/"concat.txt"
    listfile.write_text("".join(f"file '{x.as_posix()}'\n" for x in clips),encoding="utf-8")
    run_ffmpeg(["-f","concat","-safe","0","-i",str(listfile),
                "-c","copy","-movflags","+faststart",str(OUT)],"final")
    # Validate actual duration / video dimensions / absence of audio using FFmpeg stderr.
    inspect=subprocess.run([FFMPEG,"-hide_banner","-i",str(OUT)],
                           capture_output=True,text=True)
    details=inspect.stderr
    assert "1600x900" in details,details[-2000:]
    assert "Audio:" not in details,details[-2000:]
    assert OUT.exists() and OUT.stat().st_size>1_000_000
    print("COMPLETE",str(OUT),"MB",round(OUT.stat().st_size/1e6,2),flush=True)
    print("INFO",details[-1300:],flush=True)

if __name__=="__main__":
    main()
