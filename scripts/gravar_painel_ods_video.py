"""Completa capturas de painel/ODS e gera manifesto com captura principal preservada."""
import json
import re
import subprocess
import time
from pathlib import Path
import imageio_ffmpeg
from playwright.sync_api import sync_playwright
from scripts.gravar_demo_video import BASE,URL,demo_ok,new_page,save,capture_chapter

def main():
    demo_ok()
    file=BASE/"relato.webm"
    assert file.exists(),"Grave antes o fluxo principal."
    r=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),"-hide_banner","-i",str(file)],
                     capture_output=True,text=True)
    found=re.search(r"Duration: (\d\d):(\d\d):(\d\d\.\d+)",r.stderr)
    assert found,"Duracao nao detectada"
    hh,mm,ss=found.groups()
    duration=float(hh)*3600+float(mm)*60+float(ss)
    planned=[("ui_inicio",16),("ui_formulario",27),("ui_analise",22),("ui_revisao",25),("ui_recibo",13)]
    offset=duration-sum(x[1] for x in planned)
    assert 0<=offset<=20,(duration,offset)
    cur=offset
    marks=[]
    for name,d in planned:
        marks.append({"name":name,"ss":round(cur,3),"duration":d})
        cur+=d
    manifest={"relato":{"file":str(file),"bookmarks":marks}}
    print("REUSING relato",round(duration,2),"sec; offset",round(offset,2),flush=True)

    with sync_playwright() as play:
        browser=play.chromium.launch(headless=True)
        ctx,page=new_page(browser,"painel")
        page.get_by_text("Painel de relatos",exact=True).first.click()
        b=page.get_by_role("button",name=re.compile("Carregar 6 exemplos fictícios"))
        b.wait_for(timeout=20000);b.click()
        page.locator('[data-testid="stPlotlyChart"]').first.wait_for(timeout=25000)
        start=time.monotonic();bookmarks=[]

        def painel():
            page.mouse.move(990,350,steps=15)
            time.sleep(4)
            page.mouse.wheel(0,390)
            time.sleep(3)
            charts=page.locator('[data-testid="stPlotlyChart"]:visible')
            if charts.count():
                charts.first.hover(timeout=3000)
                time.sleep(3)
            tabs=page.get_by_role("tab",name=re.compile("Relatos por Categoria"))
            if tabs.count():
                tabs.first.click()
                time.sleep(5)
                visible=page.locator('[data-testid="stPlotlyChart"]:visible')
                if visible.count():
                    visible.first.hover(timeout=3000)
            page.mouse.wheel(0,-370)
            time.sleep(2)
            # Mostra aplicacao de um filtro no conjunto de exemplos ficticios.
            select=page.locator('[data-baseweb="select"]').first
            if select.count():
                select.click()
                choice=page.get_by_text("Calçadas e acessibilidade",exact=True)
                if choice.count():
                    choice.last.click()
                    time.sleep(3)
            page.mouse.move(1150,610,steps=12)
        capture_chapter(page,bookmarks,"ui_painel",34,painel)
        manifest["painel"]=save(ctx,page,"painel",bookmarks,start)

        ctx,page=new_page(browser,"ods")
        page.get_by_text("Como funciona",exact=True).first.click()
        page.get_by_text("Arquitetura, Ética e Impacto Social").first.wait_for(timeout=25000)
        start=time.monotonic();bookmarks=[]
        def ods():
            tab=page.get_by_role("tab",name=re.compile("ODS e Impacto Social"))
            tab.first.click()
            time.sleep(5)
            page.mouse.wheel(0,190)
            time.sleep(2)
            tab2=page.get_by_role("tab",name=re.compile("Ética e Limites da IA"))
            tab2.first.click()
            time.sleep(2)
        capture_chapter(page,bookmarks,"ui_ods",14,ods)
        manifest["ods"]=save(ctx,page,"ods",bookmarks,start)
        browser.close()

    dest=BASE/"manifest.json"
    dest.write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding="utf-8")
    print("MANIFEST",dest,flush=True)

if __name__=="__main__":
    main()
